# -*- coding: utf-8 -*-
"""
hunyuan_img_no_logo - 去水印版混元生图客户端（YZZX-cover 专用）

基于 WorkBuddy 内置 buddy-cloud.py 逻辑复刻，唯一关键差异：
  - 图片生成分支 _build_image_body 默认带 "LogoAdd": 0（不带「AI生成」角标）
  - 默认分辨率 1152:1536（3:4 竖版，不拉长）

保留内置脚本的：
  - TC3-HMAC-SHA256 签名逻辑（_sign_request）
  - endpoint 解析（BUDDY_CLOUD_ENDPOINT / ACC_PRODUCT_CONFIG_V3 / fallback）
  - token 优先级（stdin > file > env BUDDY_CLOUD_TOKEN > CLI）
  - 提交 + 轮询（SubmitTextToImageJob -> QueryTextToImageJob）

为什么不直接改 App bundle 的 buddy-cloud.py：
  那会影响平台上所有生图且会在更新时被覆盖。本脚本只服务于本 skill，
  需要用户运行前提供有效 token（见下文）。

运行方式（需 WorkBuddy 运行态可用的 BUDDY_CLOUD_TOKEN）：
  BUDDY_CLOUD_TOKEN=<token> python3 hunyuan_img_no_logo.py image "提示词" \
      --resolution 1152:1536 --revise 0 --output /path/out.png

注：内置 image 分支为 SubmitTextToImageJob（文生图）。若需图生图（带参考角色图），
当前混元 image 3.0 接口走文生图，参考图需以 prompt 描述或后续平台支持。
"""

import argparse
import base64 as _b64
import datetime
import hashlib
import hmac
import io
import json
import os
import subprocess
import sys
import time
from urllib.parse import urlparse

if sys.stdout.encoding and sys.stdout.encoding.lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower().replace('-', '') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def _d(s: str) -> str:
    return _b64.b64decode(s).decode()


_PROVIDER_MAP = {
    "image": {
        "provider": _d("aHktYWlhcnQ="),
        "service": _d("YWlhcnQ="),
        "version": "2022-12-29",
        "submit_action": _d("U3VibWl0VGV4dFRvSW1hZ2VKb2I="),
        "query_action": _d("UXVlcnlUZXh0VG9JbWFnZUpvYg=="),
    },
}

_REGION = "ap-guangzhou"
_TCPROXY_PATH = "/agenttool/v1/tcproxy"
_FALLBACK_ENDPOINT = "https://copilot.tencent.com" + _TCPROXY_PATH


def _resolve_default_endpoint() -> str:
    explicit = os.environ.get("BUDDY_CLOUD_ENDPOINT")
    if explicit:
        return explicit
    product_config_raw = os.environ.get("ACC_PRODUCT_CONFIG_V3")
    if product_config_raw:
        try:
            config = json.loads(product_config_raw)
            ep = config.get("endpoint")
            if ep:
                return ep.rstrip("/") + _TCPROXY_PATH
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
    return _FALLBACK_ENDPOINT


_DEFAULT_ENDPOINT = _resolve_default_endpoint()
_SIGNING_KEY = "codebuddy"


def _ensure_requests():
    try:
        import requests as _r  # noqa: F401
        return _r
    except ImportError:
        print("[INFO] Installing required dependency...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "requests", "-q"],
            stdout=sys.stderr, stderr=sys.stderr, timeout=60,
        )
        import requests as _r
        return _r


requests = _ensure_requests()


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hmac_sha256(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


def _sign_request(secret_id, secret_key, service, action, version, region, host, payload, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    content_type = "application/json; charset=utf-8"
    signed_headers = "content-type;host;x-tc-action"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{host}\n"
        f"x-tc-action:{action.lower()}\n"
    )
    hashed_payload = _sha256_hex(payload.encode("utf-8"))
    canonical_request = (
        f"{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n"
        f"{canonical_headers}\n{signed_headers}\n{hashed_payload}"
    )
    algorithm = "TC3-HMAC-SHA256"
    credential_scope = f"{date}/{service}/tc3_request"
    hashed_canonical = _sha256_hex(canonical_request.encode("utf-8"))
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_canonical}"
    secret_date = _hmac_sha256((_d("VEMz") + secret_key).encode("utf-8"), date.encode("utf-8"))
    secret_service = _hmac_sha256(secret_date, service.encode("utf-8"))
    secret_signing = _hmac_sha256(secret_service, b"tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"{algorithm} Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return {
        "Authorization": authorization,
        "Content-Type": content_type,
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Version": version,
        "X-TC-Region": region,
        "X-TC-Timestamp": str(timestamp),
    }


def _call_api(endpoint, provider, service, version, action, body, token):
    secret_id = f"{provider}.{token}"
    secret_key = _SIGNING_KEY
    parsed = urlparse(endpoint)
    host = parsed.hostname
    payload = json.dumps(body, ensure_ascii=False)
    headers = _sign_request(secret_id, secret_key, service, action, version, _REGION, host, payload)
    print("[INFO] Submitting generation request...", file=sys.stderr)
    resp = requests.post(endpoint, headers=headers, data=payload.encode("utf-8"), timeout=120)
    try:
        result = resp.json()
    except Exception:
        _error_out({"error": "INVALID_RESPONSE", "message": f"Unexpected response (HTTP {resp.status_code})."})
        return {}
    if resp.status_code >= 400:
        _error_out({"error": "HTTP_ERROR", "message": str(result.get("message", result.get("error", ""))), "http_status": resp.status_code})
    if "Response" in result:
        inner = result["Response"]
        if "Error" in inner:
            _error_out({"error": "GENERATION_FAILED", "message": inner["Error"].get("Message", "Request failed."), "request_id": inner.get("RequestId", "")})
        return inner
    if "error" in result:
        _error_out({"error": "API_ERROR", "message": str(result.get("message", result.get("error", "")))})
    return result


_ACTIVE_TOKEN = ""


def _redact_token(text):
    if not _ACTIVE_TOKEN or len(_ACTIVE_TOKEN) < 8:
        return text
    return text.replace(_ACTIVE_TOKEN, "[REDACTED]")


def _error_out(obj):
    raw = json.dumps(obj, ensure_ascii=False, indent=2)
    print(_redact_token(raw))
    sys.exit(1)


def _safe_print_json(obj):
    raw = json.dumps(obj, ensure_ascii=False, indent=2)
    print(_redact_token(raw))


def _format_output(result, job_id=None):
    output = {}
    if job_id:
        output["job_id"] = job_id
    elif "JobId" in result:
        output["job_id"] = result["JobId"]
    if "Status" in result:
        output["status"] = result["Status"]
    elif "JobStatusCode" in result:
        code_map = {"1": "QUEUED", "2": "PROCESSING", "4": "FAIL", "5": "DONE", 1: "QUEUED", 2: "PROCESSING", 4: "FAIL", 5: "DONE"}
        output["status"] = code_map.get(result["JobStatusCode"], str(result["JobStatusCode"]))
    for url_field in ("ResultUrl", "ResultVideoUrl", "ResultImage", "ResultImageUrl", "ModelUrl", "ResultModelUrl"):
        if url_field in result and result[url_field]:
            val = result[url_field]
            output["result_url"] = val if not isinstance(val, list) else val
            break
    if "result_url" not in output:
        output["raw_result"] = result
    if "RequestId" in result:
        output["request_id"] = result["RequestId"]
    return output


def _build_parser():
    parser = argparse.ArgumentParser(description="Hunyuan image generation client (LogoAdd=0 by default).")
    sub = parser.add_subparsers(dest="command", help="Generation command")
    p_image = sub.add_parser("image", help="Generate an image from text prompt (no watermark)")
    p_image.add_argument("prompt", help="Text description of the image to generate")
    p_image.add_argument("--resolution", default="1152:1536",
                         help="Image resolution 'width:height' (default 1152:1536 = 3:4)")
    p_image.add_argument("--revise", type=int, default=0, choices=[0, 1],
                         help="Prompt rewriting: 1=yes, 0=no (default 0 to keep text stable)")
    p_image.add_argument("--seed", type=int, default=None)
    p_image.add_argument("--logo-add", type=int, default=0, choices=[0, 1],
                         help="0=no watermark (default), 1=with watermark")
    p_image.add_argument("--output", default="",
                         help="If ResultImage is base64, decode and write to this path")
    _add_common_args(p_image)
    return parser


def _add_common_args(parser, include_poll=True):
    parser.add_argument("--token", default="")
    parser.add_argument("--token-stdin", action="store_true")
    parser.add_argument("--token-file", default="")
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    if include_poll:
        parser.add_argument("--no-poll", action="store_true")
        parser.add_argument("--poll-interval", type=int, default=5)
        parser.add_argument("--max-poll-time", type=int, default=600)


def _build_image_body(prompt, resolution=None, revise=None, seed=None, logo_add=0):
    """图片生成请求体（混元 image 3.0）。关键修复：带上 LogoAdd。

    内置脚本原 _build_image_body 未传 LogoAdd，混元服务端默认 LogoAdd=1 -> 带水印。
    此处默认 logo_add=0，关闭「AI生成」角标。
    """
    body = {"Prompt": prompt, "LogoAdd": logo_add}
    if resolution is not None:
        body["Resolution"] = resolution
    if revise is not None:
        body["Revise"] = revise
    if seed is not None:
        body["Seed"] = seed
    return body


def _poll_job(endpoint, provider, service, version, query_action, job_id, token, poll_interval, max_poll_time):
    print(f"[INFO] Waiting for job {job_id}...", file=sys.stderr)
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > max_poll_time:
            _error_out({"error": "POLL_TIMEOUT", "message": f"Job not complete within {max_poll_time}s.", "job_id": job_id})
        result = _call_api(endpoint, provider, service, version, query_action, {"JobId": job_id}, token)
        status = result.get("Status", "")
        raw_code = result.get("JobStatusCode")
        status_code = int(raw_code) if raw_code is not None else None
        if status == "DONE" or status_code == 5:
            return result
        elif status == "FAIL" or status_code == 4:
            _error_out({"error": "GENERATION_FAILED", "message": result.get("ErrorMessage", "Generation failed."), "job_id": job_id})
        print(f"[INFO] status={status or status_code}, elapsed={int(elapsed)}s, next in {poll_interval}s", file=sys.stderr)
        time.sleep(poll_interval)


def main():
    parser = _build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    token = ""
    if getattr(args, "token_stdin", False):
        token = sys.stdin.readline().strip()
    elif getattr(args, "token_file", "") and args.token_file:
        try:
            with open(args.token_file, "r") as f:
                token = f.read().strip()
        except (IOError, OSError) as e:
            _error_out({"error": "TOKEN_FILE_ERROR", "message": f"Cannot read token file: {e}"})
    elif os.getenv("BUDDY_CLOUD_TOKEN", ""):
        token = os.getenv("BUDDY_CLOUD_TOKEN", "")
    elif args.token:
        token = args.token

    if not token:
        _error_out({
            "error": "TOKEN_NOT_CONFIGURED",
            "message": (
                "需要 BUDDY_CLOUD_TOKEN。运行方式：\n"
                "  BUDDY_CLOUD_TOKEN=<token> python3 hunyuan_img_no_logo.py image \"提示词\" "
                "--resolution 1152:1536 --output out.png\n"
                "token 由 WorkBuddy 运行态注入，请在有 token 的环境运行本脚本。"
            ),
        })

    global _ACTIVE_TOKEN
    _ACTIVE_TOKEN = token
    endpoint = args.endpoint

    if args.command == "image":
        body = _build_image_body(args.prompt, resolution=args.resolution,
                                 revise=args.revise, seed=args.seed, logo_add=args.logo_add)
        cfg = _PROVIDER_MAP["image"]
        submit = _call_api(endpoint, cfg["provider"], cfg["service"], cfg["version"],
                           cfg["submit_action"], body, token)
        job_id = submit.get("JobId")
        if not job_id:
            _error_out({"error": "NO_JOB_ID", "message": "Service did not return a job ID.", "raw_response": submit})
        print(f"[INFO] Job submitted: {job_id}", file=sys.stderr)
        if not getattr(args, "no_poll", False):
            result = _poll_job(endpoint, cfg["provider"], cfg["service"], cfg["version"],
                               cfg["query_action"], job_id, token, args.poll_interval, args.max_poll_time)
            output = _format_output(result, job_id=job_id)
            # 若返回 base64 图片且指定了 --output，解码写出
            if args.output and "ResultImage" in result and result["ResultImage"]:
                try:
                    data = result["ResultImage"]
                    if isinstance(data, str) and (data.startswith("http://") or data.startswith("https://")):
                        output["result_url"] = data
                    else:
                        img_bytes = _b64.b64decode(data)
                        with open(args.output, "wb") as f:
                            f.write(img_bytes)
                        output["saved_to"] = args.output
                except Exception as e:
                    output["decode_error"] = str(e)
            _safe_print_json(output)
        else:
            _safe_print_json({"job_id": job_id, "status": "SUBMITTED"})
    else:
        _error_out({"error": "UNKNOWN_COMMAND", "message": args.command})


if __name__ == "__main__":
    main()

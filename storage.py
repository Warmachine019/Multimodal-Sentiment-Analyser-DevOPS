# storage.py - optional batched logging of analysis scores to S3 (enabled when S3_BUCKET is set)
import json
import os
import threading
import time
import uuid

BUCKET = os.environ.get("S3_BUCKET")
PREFIX = os.environ.get("S3_PREFIX", "results")
BATCH = int(os.environ.get("S3_BATCH_SIZE", "30"))

_buf = []
_lock = threading.Lock()
_s3 = None


def _client():
    global _s3
    if _s3 is None:
        import boto3  # credentials come from the EC2 instance role
        _s3 = boto3.client("s3")
    return _s3


def _flush(records):
    try:
        key = f"{PREFIX}/{time.strftime('%Y/%m/%d')}/{int(time.time())}-{uuid.uuid4().hex[:8]}.jsonl"
        body = "\n".join(json.dumps(r) for r in records).encode()
        _client().put_object(Bucket=BUCKET, Key=key, Body=body, ContentType="application/json")
    except Exception as e:
        print("S3 upload failed:", e)


def record_result(record):
    if not BUCKET:
        return
    with _lock:
        _buf.append({"ts": time.time(), **record})
        if len(_buf) < BATCH:
            return
        batch = _buf[:]
        _buf.clear()
    threading.Thread(target=_flush, args=(batch,), daemon=True).start()

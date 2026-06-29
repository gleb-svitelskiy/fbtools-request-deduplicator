import hashlib
import logging

from mitmproxy import http

logger = logging.getLogger(__name__)
seen = set()


def request(flow: http.HTTPFlow):
    # logger.info(flow.request.method)
    # logger.info(flow.request.pretty_url)
    # logger.info(flow.request.get_content())
    if flow.request.method == "PUT":
        body = flow.request.get_content() or b""
        body_hash = hashlib.sha256(body).hexdigest()

        key = (flow.request.method, flow.request.pretty_url, body_hash)

        if key in seen:
            flow.response = http.Response.make(
                200,
                b"{}",
                {"Content-Type": "application/json"}
            )

            logger.info(f"[DUPLICATE] {flow.request.pretty_url} {body}")
            return

        seen.add(key)
        logger.info(f"[PROXY_REQUEST] {flow.request.pretty_url} {body}")

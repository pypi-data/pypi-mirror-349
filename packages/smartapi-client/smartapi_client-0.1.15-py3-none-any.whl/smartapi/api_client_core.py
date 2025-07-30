import logging
import os
import requests


def _setup_logging(self, log_level):
    if not self.logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(log_level.value)


def _configure_session(self, default_params, default_headers, retry_options):
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter

    if default_params:
        self.session.params.update(default_params)

    headers = default_headers.copy() if default_headers else {}
    if self.api_key:
        headers['Authorization'] = f'Bearer {self.api_key}'
    if self.tracking_id:
        headers['X-Tracking-ID'] = self.tracking_id
    self.session.headers.update(headers)

    retry_strategy = Retry(
        total=retry_options.get("retries", 3),
        connect=retry_options.get("connect", 3),
        read=retry_options.get("read", 3),
        status=retry_options.get("status", 3),
        backoff_factor=retry_options.get("backoff_factor", 0.5),
        status_forcelist=retry_options.get(
            "status_forcelist", [500, 502, 503, 504, 429]),
        allowed_methods=frozenset(retry_options.get(
            "allowed_methods", ["GET", "POST", "PUT", "DELETE", "PATCH"])),
        raise_on_status=retry_options.get("raise_on_status", False),
        respect_retry_after_header=retry_options.get(
            "respect_retry_after_header", True)
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    self.session.mount("http://", adapter)
    self.session.mount("https://", adapter)

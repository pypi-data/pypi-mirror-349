from datetime import datetime
from typing import Any

import requests


def get_api_output_in_standard_format(
    data: Any = None,
    message: str = None,
    log: Any = None,
):
    return {"data": data, "message": message, "log": log}


def make_request_json_output(
    method,
    base_url,
    endpoint,
    data=None,
    json=None,
    params=None,
    headers=None,
    files=None,
    auth=None,
):

    try:
        url = f"{base_url}/{endpoint}"
        if headers:
            headers = {key.replace("_", "-"): value for key, value in headers.items()}
        response = requests.request(
            method,
            url,
            json=json,
            data=data,
            params=params,
            headers=headers,
            files=files,
            auth=auth,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        raise


def create_cookie(
    key: str,
    value: str,
    domain: str = None,
    expires: datetime = None,
    path: str = "/",
    same_site: str = "Strict",  # "Strict", "Lax", or "None"
    secure: bool = False,
    http_only: bool = True,
) -> dict:
    if not key or not value:
        raise ValueError("Cookie key and value are required.")

    cookie_options = {
        "httponly": http_only,
        "path": path,
        "secure": secure,
        "samesite": same_site,
        "value": value,
        "key": key,
    }

    if expires:
        if not isinstance(expires, datetime):
            raise ValueError("Expires must be a datetime object.")
        cookie_options["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    if domain:
        cookie_options["domain"] = domain
    return cookie_options

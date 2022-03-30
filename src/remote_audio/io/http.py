#!/usr/bin/env python3

from typing import Any, Dict, Union


import requests

from remote_audio.exceptions import HTTPIOError
from remote_audio.io.file import get_wav_header_size

def get_http_size(
    url:str,
    params:Dict[str, Any]={},
    **kwargs,
)->int:
    _response = requests.head(
        url=url,
        params=params,
        allow_redirects=True,
        **kwargs,
    )

    _size = _response.headers.get("content-length", None)

    if (_size):
        return int(_size)
    else:
        return HTTPIOError("Returned header does not contain content-length.")


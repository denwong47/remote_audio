#!/usr/bin/env python3

from typing import Any, Callable, Dict, Union

from http import HTTPStatus
import requests

from remote_audio.exceptions import HTTPIOError

DEFAULT_HTTP_TIMEOUT = 3
DEFAULT_HTTP_CHUNK_SIZE = 2**20

def build_exception(
    response:requests.Response,
):
    """
    Construct an exception describing the response error
    """

    _code = response.status_code
    _error = HTTPStatus(_code)
    _phrase = _error.phrase
    _description = _error.description
    return HTTPIOError(f"Error occured during HTTP operation: {_code} {_phrase}: {_description}.")


def get_http_size(
    url:str,
    params:Dict[str, Any]={},
    **kwargs,
)->int:
    """
    Send header request to query file size
    """

    _response = requests.head(
        url=url,
        params=params,
        allow_redirects=True,
        **kwargs,
    )

    _size = _response.headers.get("content-length", None)

    if (_response.status_code == HTTPStatus.OK):
        if (_size):
            return int(_size)
        else:
            return HTTPIOError("Returned header does not contain content-length.")
    else:
        return build_exception(_response)


def iter_http_data(
    url:str,
    timeout:float = DEFAULT_HTTP_TIMEOUT,
    chunk_size:int = DEFAULT_HTTP_CHUNK_SIZE,
    params:Dict[str, Any]={},
    **kwargs,
):
    """
    Returns a generator to iterate through the content of a HTTP file.
    """

    _response = requests.get(
        url = url,
        timeout = timeout,
        params=params,
        allow_redirects=True,
        stream = True,
    )

    if (_response.status_code == HTTPStatus.OK):
        return _response.iter_content(
            chunk_size = chunk_size,
            decode_unicode = False,
        )
    else:
        return build_exception(_response)


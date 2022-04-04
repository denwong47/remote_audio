from unittest import result
import requests
import time as timer

from typing import Callable

from remote_audio.device import AudioDevice
from remote_audio.io import WaveStreamIO
from remote_audio.io.http import get_http_size

_url = ""

from concurrent.futures import ThreadPoolExecutor

def delay_print(text):
    timer.sleep(2)
    print (text)
    

def get_url(
    url:str,
    timeout:int = 3,
    chunk_size:int = None,
    callback:callable = None,
):
    _file_size = get_http_size(
        url
    )

    _req = requests.get(
        url = url,
        timeout = timeout,
        stream = True,
    )

    _last = timer.perf_counter()
    
    _result = []
    _count = 0
    with ThreadPoolExecutor() as _executor:
        for _data in _req.iter_content(
            chunk_size = min(_file_size/2, 2**20),
            decode_unicode = False,
        ):
            _count += 1
            print (f"Main Loop Start: {_count}")
            _lapsed = timer.perf_counter() - _last
            _last = timer.perf_counter()

            _result.append(_executor.submit(callback, _count))
            print (f"Main Loop End: {_count}")

    
    return result

get_url(_url, callback = lambda data: delay_print(f"Callback: {data}"))
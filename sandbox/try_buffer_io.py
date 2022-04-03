
import threading
import io

"""
This is the development version of StreamIO in remote_audio.classes.
Probably not up to date.
"""
class StreamIO(io.BytesIO):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.lock = threading.Lock()
        
        pass

    def read(
        self,
        *args,
        **kwargs,
    ):
        with self.lock:
            return super().read(*args, **kwargs)

    def write(
        self,
        *args,
        **kwargs,
    ):
        with self.lock:
            _pos = self.tell()
            self.seek(0, io.SEEK_END)
            _return = super().write(*args, **kwargs)
            self.seek(_pos, io.SEEK_SET)

        return _return

_f = StreamIO()

_tasks = []
_tasks.append(lambda :print(_f.read()))
_tasks.append(lambda :_f.write(b"Start"))
_tasks.append(lambda :_f.write(b"Append"))
_tasks.append(lambda :print(_f.read()))
_tasks.append(lambda :print(_f.read()))
_tasks.append(lambda :_f.write(b"End"))
_tasks.append(lambda :_f.write(b"Postscript"))
_tasks.append(lambda :print(_f.read()))


from concurrent.futures import ThreadPoolExecutor
from execute_timer import execute_timer


with execute_timer(echo=True) as _timer_threads:
    with ThreadPoolExecutor(max_workers=4) as _executor:
        _results = [ _executor.submit(_task) for _task in _tasks ]

    list(_results)

with execute_timer(echo=True) as _timer_sequential:
    for _task in _tasks:
        _task()

print (f'Threaded took {abs(_timer_threads.lapsed() - _timer_sequential.lapsed()):.6f}s {"shorter" if _timer_threads.lapsed()<_timer_sequential.lapsed() else "longer"} than Sequential execution.')

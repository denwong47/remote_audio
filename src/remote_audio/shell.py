import shell
from typing import Any, List, Union

def check_command_exists(
    command: Union[
        List[str],
        str
    ],
):
    """
    Check if a command returns a specific error code of 127,
    which is command not found.
    """

    _return = shell.run(
        command,
        safe_mode = True,
    )

    if (isinstance(_return, shell.ShellReturnedFailure)):
        if (_return.exit_code == 127):
            return False

    return True



class ShellCommandExists():
    """
    A psuedo-Singleton class that create only one instance of each unique 'command' value.
    This avoids spending time running subprocesses more than once.
    """

    _instances={}   # this dict is shared by all instances, do not create a new one

    exists = None

    def __new__(
        cls,
        command:Union[
            List[str],
            str
        ],
        *args,
        **kwargs,
    ):
        """
        Create new instance if cls(command) was not called before;
            otherwise return the instance that already exists.
        Put the instance back into the library.
        """

        _instance = cls._instances.get(
            command,
            super().__new__(cls, *args, **kwargs)
        )

        cls._instances[command] = _instance

        return _instance
    
    def __init__(
        self,
        command:Union[
            List[str],
            str
        ],
        *args,
        **kwargs,
    ):
        """
        Check if command exists, then store it in self.exists.
        """

        # Avoids running this twice if __new__() returned an existing instance
        if (self.exists is None):
            self.exists = check_command_exists(command)

    def __bool__(
        self,
    ):
        return self.exists

    __nonzero__ = __bool__
    
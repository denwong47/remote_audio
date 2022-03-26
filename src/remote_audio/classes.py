#!/usr/bin/env python3

import os, sys
import re
from enum import Enum
from typing import Any, Dict, Iterable, List, Tuple, Union
from unicodedata import name

import pyaudio

from remote_audio import exceptions
from remote_audio import api


class DeviceSignature(dict):
    """
    Simple class proxying a dict, that defines where the device is located in terms of
    - host_api, and
    - device_index
    """

    def __init__(
        self,
        host_api_index:int=0,
        host_api_device_index:int=0,
    )->None:
        super().__init__({
                "host_api_index":host_api_index,
                "host_api_device_index":host_api_device_index,
            })
        

class AudioDevice():
    """
    Proxy for a selected Audio Device
    """

    def __init__(
        self,
        signature:DeviceSignature,
        **kwargs,
    ):
        _p = api.pya

        _device_info = _p.get_device_info_by_host_api_device_index(
            **signature
        )
        
        self.properties =   {
            **_device_info,
            **kwargs,
        }
        self.signature  =   signature

    def __repr__(
        self,
    ):
        return f"{type(self).__name__}(signature={repr(self.signature)}, name={repr(self.name)})"

    def __getattr__(
        self,
        attr:str,
    ):
        """
        If an unknown attribute is requested, look for it in self.properties.
        If found, return it (e.g. self.name);
        otherwise return None.
        """
        return self.properties.get(attr, None)

    @property
    def canInput(self):
        return bool(self.maxInputChannels)
    
    @property
    def canOutput(self):
        return  bool(self.maxOutputChannels)
    
    @classmethod
    def get(
        cls,
        signature:Union[
            DeviceSignature,
            Tuple[int, int],
            int
        ]=None,
        host_api_index:int=0,
        host_api_device_index:int=0,
    )->"AudioDevice":
        """
        Retrieve a device by signature
        """

        if (not(signature) and \
            isinstance(host_api_index, int) and \
            isinstance(host_api_device_index, int)
        ):
            # Using raw index mode
            return cls.get(
                signature = DeviceSignature(
                    host_api_index          = host_api_index,
                    host_api_device_index   = host_api_device_index
                )
            )
        else:

            if ((len(signature)>=2) if isinstance(signature, tuple) else False):
                # Using tuple mode
                signature = DeviceSignature(
                    host_api_index          = signature[0],
                    host_api_device_index   = signature[1],
                )
            elif (isinstance(signature, int)):
                signature = DeviceSignature(
                    host_api_index          = 0,
                    host_api_device_index   = signature,
                )

            # Lets see if the signature is now ready to be processed by __init__()
            if (isinstance(signature, DeviceSignature)):
                # Using DeviceSignature mode, simply build it using __init__()
                try:
                    return cls(
                        signature
                    )
                except OSError as e:
                    # [Errno -9978] Invalid host API
                    # [Errno -9996] Invalid device
                    return exceptions.DeviceNotFound(
                        str(e)
                    )
                except TypeError as e:
                    return exceptions.InvalidInputParameters(
                        f"Device Signature has an error in type: {str(e)}"
                    )
            else:
                return

    @classmethod
    def default(
        cls,
        input:bool=False,
        output:bool=True,
    ):
        """
        Getting the default input or output device
        """

        _p = api.pya

        output = not input
        
        if (input):
            _device_info = _p.get_default_input_device_info()
        elif (output):
            _device_info = _p.get_default_output_device_info()

        return cls.get(
            host_api_index=_device_info.get("hostApi"),
            host_api_device_index=_device_info.get("index"),
        )

    @classmethod
    def list(
        cls
    )->Iterable[
        "AudioDevice"
    ]:
        """
        Return a list of all devices available
        """
        _p = api.pya

        for _api_id in range(_p.get_host_api_count()):
            for _device_id in range(_p.get_device_count()):
                # check all combinations of _api_id and _device_id
                _device_signature = DeviceSignature(
                    host_api_index          =   _api_id,
                    host_api_device_index   =   _device_id,
                )

                _device = cls.get(
                    signature = _device_signature
                )

                if (_device):
                    yield _device


    @classmethod
    def find(
        cls,
        input:bool=False,
        output:bool=True,
        name:str=Union[
            re.Pattern,
            str,
        ],
    )->Iterable[
        "AudioDevice"
    ]:
        """
        Look for devices fitting certain criteria.

        Returns a list of "signature" dictionaries.
        """
        
        for _device in cls.list():
            if (input and not _device.canInput): continue
            if (output and not _device.canOutput): continue

            if (isinstance(name, str)):
                # If its an empty string, this will return everything
                if (not name.lower() in _device.name.lower()): continue
            elif (isinstance(name, re.Pattern)):
                if (not name.match(_device.name)): continue
            
            yield _device

    @classmethod
    def find_first(
        cls,
        *args,
        **kwargs,
    )-> "AudioDevice":
        """
        Return the first device that fit the supplied criteria
        """

        for _device in cls.find(
            *args,
            **kwargs,
        ):
            return _device
            # Forget about the restm, we only want one
        
        # The generator is empty, we have nothing
        return None



def main():
    from dict_tree import DictionaryTree

    DictionaryTree(
        list(AudioDevice.find(
            output=True,
        ))
    )


if (__name__=="__main__"):
    main()
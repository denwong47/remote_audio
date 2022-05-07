#!/usr/bin/env python3

import os, sys
import re

from typing import Any, BinaryIO, Dict, Iterable, List, Tuple, Union

from remote_audio import audio
from remote_audio import exceptions
from remote_audio import api

from remote_audio.stream import AudioStream
import remote_audio.classes


class DeviceHostAPISignature(dict):
    """
    Simple class proxying a dict, that defines where the device is located in terms of
    - device_index
    - host_api, and
    - host_api_device_index
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

    @classmethod
    def from_device_index(
        cls,
        device_index:int = 0,
    )->"DeviceHostAPISignature":

        _self_info = api.pya.get_device_info_by_index(device_index=device_index)
        
        host_api_device_index = 0
        while (_self_info is not None):
            try:
                _device_info = api.pya.get_device_info_by_host_api_device_index(
                    host_api_index=_self_info.get("hostApi", None),
                    host_api_device_index=host_api_device_index,
                )

                if (_self_info == _device_info):
                    return cls(
                        host_api_index=_self_info.get("hostApi", None),
                        host_api_device_index=host_api_device_index,
                    )

                host_api_device_index += 1
            except OSError as e:
                break
                
        return None



class AudioDevice():
    """
    Proxy for a selected Audio Device

    Usage:
    # by Device Index, NON-error handled:
    AudioDevice(device_index)
    
    - or - 

    # by Device Index, error handled:
    AudioDevice.by_device_index(device_index)

    - or - 

    # by Host API Index, error handled:
    AudioDevice.by_host_api_device_index(signature)
    """

    properties = {
        # 'index': 0,
        # 'structVersion': 2,
        # 'name': 'DELL U2520D',
        # 'hostApi': 0,
        # 'maxInputChannels': 0,
        # 'maxOutputChannels': 2,
        # 'defaultLowInputLatency': 0.01,
        # 'defaultLowOutputLatency': 0.0024375,
        # 'defaultHighInputLatency': 0.1,
        # 'defaultHighOutputLatency': 0.011770833333333333,
        # 'defaultSampleRate': 48000.0
    }

    def __init__(
        self,
        device_index:int,
        **kwargs,
    ):
        _p = api.pya

        _device_info = _p.get_device_info_by_index(
            device_index=device_index
        )
        
        self.properties =   {
            **_device_info,
            **kwargs,
        }

        self.device_index = device_index
        self.signature = DeviceHostAPISignature.from_device_index(self.device_index)

    def __repr__(
        self,
    ):
        return f"{type(self).__name__}(device_index={repr(self.device_index)}, signature={repr(self.signature)}, name={repr(self.name)})"

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
    def by_device_index(
        cls,
        device_index:int=0,
        **kwargs,
    )->"AudioDevice":

        try:
            _device = cls(device_index=device_index, **kwargs)
            return _device
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

    @classmethod
    def by_host_api_device_index(
        cls,
        signature:Union[
            DeviceHostAPISignature,
            Tuple[int, int],
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
            return cls.by_host_api_device_index(
                signature = DeviceHostAPISignature(
                    host_api_index          = host_api_index,
                    host_api_device_index   = host_api_device_index
                )
            )
        else:

            if ((len(signature)>=2) if isinstance(signature, tuple) else False):
                # Using tuple mode
                signature = DeviceHostAPISignature(
                    host_api_index          = signature[0],
                    host_api_device_index   = signature[1],
                )

            # Lets see if the signature is now ready to be processed by __init__()
            if (isinstance(signature, DeviceHostAPISignature)):
                # Using DeviceSignature mode, simply build it using __init__()
                try:
                    _p = api.pya
                    _device_info = _p.get_device_info_by_host_api_device_index(
                        **signature
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
                
                return cls(
                    _device_info.get("index", 0)
                )
            else:
                return exceptions.InvalidInputParameters(
                    f"Unknown Device Signature of type {type(signature).__name__}."
                )

    @classmethod
    def default(
        cls,
        input:bool=False,
        output:bool=True,
    )->"AudioDevice":
        """
        Getting the default input or output device
        """

        _p = api.pya

        output = not input
        
        if (input):
            _device_info = _p.get_default_input_device_info()
        elif (output):
            _device_info = _p.get_default_output_device_info()


        return cls.by_device_index(
            device_index=_device_info.get("index")
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

        for _device in map(
            cls.by_device_index,
            range(_p.get_device_count())
        ):
            if (_device):
                yield _device

    @classmethod
    def find(
        cls,
        input:bool=False,
        output:bool=True,
        name:Union[
            re.Pattern,
            str,
        ]=None,
    )->Iterable[
        "AudioDevice"
    ]:
        """
        Look for devices fitting certain criteria.

        Returns a generator for AudioDevices.

        Note that all criteria are AND operated - meaning if input=True and ouput=True, nothing will be produced.
        """
        output = not input  # default output is True, so if input=True, its deliberate. We assume that if that's the case, then output should be False.
        
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


    def start_wav_stream(
        self,
        io:BinaryIO,
        chunk_size:int=1024,
        start:bool=True,
        bytes_total:int=None,
        timeout:float=None,
        exit_interrupt:bool=False,
        **kwargs,
    )->AudioStream:
        """
        Play an audio
        """
        return audio.start_wav_stream(
            io=io,
            device_index=self.device_index,
            chunk_size=chunk_size,
            start=start,
            bytes_total=bytes_total,
            timeout=timeout,
            exit_interrupt=exit_interrupt,
            **kwargs,
        )


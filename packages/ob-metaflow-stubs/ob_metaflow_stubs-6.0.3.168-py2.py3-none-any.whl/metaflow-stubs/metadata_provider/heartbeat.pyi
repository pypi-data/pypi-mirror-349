######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.13.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-20T18:21:15.666543                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ..exception import MetaflowException as MetaflowException

SERVICE_HEADERS: dict

HB_URL_KEY: str

class HeartBeatException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class MetadataHeartBeat(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    @classmethod
    def get_worker(cls):
        ...
    ...


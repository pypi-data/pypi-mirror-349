######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.2+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-19T23:34:02.830963                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger


class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...


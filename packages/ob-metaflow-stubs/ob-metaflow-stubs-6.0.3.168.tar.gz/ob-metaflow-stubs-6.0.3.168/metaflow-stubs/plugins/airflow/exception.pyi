######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.13.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-20T18:21:15.704242                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...


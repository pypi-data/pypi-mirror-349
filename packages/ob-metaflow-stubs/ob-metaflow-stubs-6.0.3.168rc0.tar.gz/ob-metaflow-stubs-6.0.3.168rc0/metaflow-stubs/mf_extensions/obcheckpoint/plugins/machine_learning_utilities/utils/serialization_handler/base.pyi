######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.2+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-19T23:34:02.912147                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


class SerializationHandler(object, metaclass=type):
    def serialze(self, *args, **kwargs) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, *args, **kwargs) -> typing.Any:
        ...
    ...


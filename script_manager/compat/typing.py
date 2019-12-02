try:
    from typing import _GenericAlias
    from typing import *
except ImportError:
    from script_manager.compat import add_metaclass

    class _GenericAlias(object):
        __origin__ = type(None)  # type: type

    class TypingPlaceHolderMeta(type):
        def __getitem__(self, item):
            return self

    @add_metaclass(TypingPlaceHolderMeta)
    class TypingPlaceHolder(object):
        pass

    Optional = Union = Tuple = List = Dict = Mapping = TypingPlaceHolder

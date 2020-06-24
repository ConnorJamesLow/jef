from typing import Any, AnyStr, Callable
import json


class Observer:
    """
    Convert a `dict` to an observable object.
    """

    def __init__(
        self,
        subject: dict,
        callback:  Callable[[object, AnyStr, Any], bool],
        name: str = ''
    ):
        """
        `subject` - the dictionary to convert into an observable  

        `callback` - a function hook to run when setattr happens  

        `name` - optionally specify the name for this object. Child Observers will be given a name from their key.
        """
        self.__hook = callback
        self.__attribute_name = name
        self.__subject = {}
        for key in subject.keys():
            value = subject[key]
            setattr(self, key, value)

    def __setattr__(self, name, value):
        # Skip our private members
        if name.startswith('_Observer__'):
            return super().__setattr__(name, value)

        # If this is a dictionary, create a child Observer that bubbles events to parent's callback.
        if isinstance(value, dict):
            def call_parent(_, ca_name, ca_value):
                return self.__hook(self, ca_name, ca_value)

            # Child Observer instance
            value = Observer(value, call_parent, name)

        # set value
        self.__subject[name] = value
        res = super().__setattr__(name, value)

        # Execute hook
        self.__hook(self, name, value)
        return res

    def to_dict(self) -> dict:
        """
        Recursively transforms nested `Observer`s into `dict`s
        """
        res = self.__subject
        for key in res:
            if isinstance(res[key], Observer):
                res[key] = res[key].to_dict()
        return res

    def get_name(self) -> str:
        """
        Returns the attribute name of this `Observer`.
        """
        return self.__attribute_name

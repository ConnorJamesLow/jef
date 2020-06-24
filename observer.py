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
        self.__wait = True
        self.__hook = callback
        self.__attribute_name = name
        self.__subject = {}
        for key in subject.keys():
            value = self.__might_transform_to_observer(key, subject[key])
            self.__subject[key] = value
            setattr(self, key, value)
        self.__wait = False

    def __might_transform_to_observer(self, name: str, value: Any) -> Any:
        # If this is a dict, convert to observer
        if isinstance(value, dict):
            def bubble(_, ca_name: str, ca_value: str) -> Any:
                return self.__hook(self, ca_name, ca_value)
            return Observer(value, bubble, name)
        return value

    def __setattr__(self, name, value: Any):
        # Skip our private members
        if name.startswith('_Observer__') or self.__wait:
            return super().__setattr__(name, value)

        # If this is a dictionary, create a child Observer that bubbles events to parent's callback.
        value = self.__might_transform_to_observer(name, value)

        # set value
        self.__subject[name] = value
        super().__setattr__(name, value)

        # Execute hook
        self.__hook(self, name, value)

    def to_dict(self) -> dict:
        """
        Recursively transforms nested `Observer`s into `dict`s
        """
        subject = self.__subject
        res = {}
        for key in subject.keys():
            if isinstance(subject[key], Observer):
                res[key] = subject[key].to_dict()
            else:
                res[key] = subject[key]
        return res

    def get_name(self) -> str:
        """
        Returns the attribute name of this `Observer`.
        """
        return self.__attribute_name

from __future__ import annotations

import functools
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

Disposables = TypeVar("Disposables", bound="DisposableBase")


class DisposableBase(metaclass=ABCMeta):
    """
    Base class to whitch class need to dispose

    if you want to override __del__ method,
    you must call sub_class's dispose method
    or super_class's __del__ method
    """

    __disposed: bool = False

    @property
    def is_disposed(self) -> bool:
        """
        Get whether it has already been disposed or not

        Returns:
            bool: disposed yet or not
        """
        return self.__disposed

    def __del__(self: Disposables) -> None:
        self.dispose()

    @abstractmethod
    def dispose(self):
        self.__disposed = True


def disposed_checker(func: Callable) -> Any:
    """
    Decorator to check if it's already disposed

    Only attach to the super class of DisposableBase

    Parameters
    ----------
    func : Callable
        function whose first argumet is an instance of DisposableBase

    Returns
    -------
    Any
        wrapper of function
    """

    @functools.wraps(func)
    def wrapper(self: Disposables, *args: Any, **kwargs: Any) -> None:
        if self.is_disposed:
            return

        return func(self, *args, **kwargs)

    return wrapper

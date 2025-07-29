"""
Use case tracking system class implementation.

This module provides an abstract base class `BasicUseCase` that integrates
transactional tracing into a use case execution flow.
"""

from abc import ABC
from typing import Optional, Generic, Callable

from bisslog.transactional.transaction_traceable import TransactionTraceable

from .use_case_base import UseCaseBase
from .use_case_decorator import use_case
from ..typing_compat import ParamSpec, P, R


if ParamSpec is not None:

    class BasicUseCase(UseCaseBase, TransactionTraceable, ABC, Generic[P, R]):
        """Base class for use cases with optional transactional tracing.

        Automatically looks for a method decorated with @use_case. If none is found,
        falls back to a method named `use`, which will be decorated dynamically.

        On call, the selected method is executed as the entrypoint.
        """

        def __init__(self, keyname: Optional[str] = None, *, do_trace: bool = True) -> None:
            UseCaseBase.__init__(self, keyname)
            self._do_trace = do_trace
            self._entrypoint = self._resolve_entrypoint()

        def _resolve_entrypoint(self) -> Callable[P, R]:
            """Resolves the method to be used as the use case entrypoint.

            Priority:
            1. Method explicitly decorated with @use_case.
            2. Method named `use`, decorated dynamically if needed.

            Returns
            -------
            Callable[P, R]
                The resolved entrypoint function.

            Raises
            ------
            AttributeError
                If no suitable method is found.
            """
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if callable(attr) and getattr(attr, "__is_use_case__", False):
                    return attr

            use_fn = getattr(self, "use", None) or getattr(self, "run", None)
            if use_fn is None or not callable(use_fn):
                raise AttributeError(
                    f"No method decorated with @use_case or named 'use' "
                    f"found in {self.__class__.__name__}"
                )

            if not getattr(use_fn, "__is_use_case__", False):
                use_fn = use_case(keyname=self.keyname, do_trace=self._do_trace)(use_fn)
                setattr(self, "use", use_fn)

            return use_fn

        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
            """
            Invokes the resolved use case entrypoint method.

            Parameters
            ----------
            *args :
                Positional arguments.
            **kwargs :
                Keyword arguments.

            Returns
            -------
            R
                The result of the use case.
            """
            return self._entrypoint(*args, **kwargs)

else:
    class BasicUseCase(UseCaseBase, TransactionTraceable, ABC):
        """Fallback for use cases without signature preservation (ParamSpec unavailable).

        This version is used on Python versions < 3.10 without typing_extensions installed.
        """

        def __init__(self, keyname: Optional[str] = None, *, do_trace: bool = True) -> None:
            UseCaseBase.__init__(self, keyname)
            self._do_trace = do_trace
            self._entrypoint = self._resolve_entrypoint()

        def _resolve_entrypoint(self) -> Callable[..., R]:
            """Resolves the method to be used as the use case entrypoint.

            Priority:
            1. Method explicitly decorated with @use_case.
            2. Method named `use`, decorated dynamically if needed.

            Returns
            -------
            Callable[..., R]
                The resolved entrypoint function.

            Raises
            ------
            AttributeError
                If no suitable method is found.
            """
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if callable(attr) and getattr(attr, "__is_use_case__", False):
                    return attr

            use_fn = getattr(self, "use", None) or getattr(self, "run", None)
            if use_fn is None or not callable(use_fn):
                raise AttributeError(
                    f"No method decorated with @use_case or named "
                    f"'use' found in {self.__class__.__name__}"
                )

            if not getattr(use_fn, "__is_use_case__", False):
                use_fn = use_case(keyname=self.keyname, do_trace=self._do_trace)(use_fn)
                setattr(self, "use", use_fn)

            return use_fn

        def __call__(self, *args, **kwargs):
            """
            Invokes the resolved use case entrypoint method.

            Parameters
            ----------
            *args :
                Positional arguments.
            **kwargs :
                Keyword arguments.

            Returns
            -------
            Any
                The result of the use case.
            """
            return self._entrypoint(*args, **kwargs)

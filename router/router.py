# this is normal router file
import typing
from abc import abstractmethod


class _AbstractRoute(typing.Protocol):
    @abstractmethod
    def get(self, **handle_func):
        raise NotImplementedError

    @abstractmethod
    def post(self):
        raise NotImplementedError

    @abstractmethod
    def head(self):
        raise NotImplementedError

    @abstractmethod
    def put(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def any(self):
        raise NotImplementedError

    @abstractmethod
    def options(self):
        raise NotImplementedError

    @abstractmethod
    def add_route(self, path, cb, method):
        raise NotImplementedError

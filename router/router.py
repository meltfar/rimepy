# this is normal router file

class _AbstractRoute:
    def get(self, **handle_func):
        pass

    def post(self):
        pass

    def head(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def any(self):
        pass

    def options(self):
        pass


class RouterInfo:
    def __init__(self):
        self._is_root = True
        self._base_path = "/"
        pass

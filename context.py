# this is context in every request and response
from __future__ import annotations

import typing

from werkzeug.wrappers import Request, Response
import json
from io import StringIO


class Context:
    def __init__(self, req: Request, resp: Response):
        self._request = req
        self._response = resp

    @property
    def request(self) -> Request:
        return self._request

    @property
    def response(self) -> Response:
        return self._response

    # set response as json
    def json(self, obj: object) -> None:
        self._response.content_type = "application/json"

        jout = StringIO()
        json.dump(obj, jout)
        jout.flush()
        self._response.set_data(value=jout.getvalue())

    def text(self, txt: str) -> None:
        self._response.content_type = "text/html"
        self._response.set_data(value=txt)

    def get_parameter_list(self, k: str) -> list[str]:
        args = self.request.args
        if len(args) > 0:
            v = args.getlist(k)
            if len(v) > 0:
                return v

        form = self.request.form
        if len(form) > 0:
            v = form.getlist(k)
            if len(v) > 0:
                return v
        return []

    def get_parameter(self, k: str) -> str | None:
        v = self.get_parameter_list(k)
        if len(v) > 0:
            return v[0]
        return None

    def get_json(self) -> typing.Any:
        return self.request.get_json()

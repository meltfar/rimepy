# this is context in every request and response
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

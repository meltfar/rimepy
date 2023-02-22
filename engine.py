import typing

import context
from werkzeug.urls import url_parse
from werkzeug.wrappers import Request, Response

test_func = lambda c: c.json({"name": "wochao", "age": 18, "gender": 1})


class Engine:
    def __init__(self):
        self._method_trees = []  # router

    def dispatch_request(self, c: context.Context):
        print(c.request.path)
        for pat in self._method_trees:
            print(pat)
        # TODO: router part, select registered handler by router path
        # c.response.set_data(value=c.request.path)
        d = dict()
        d["name"] = "wocao"
        d["age"] = 18
        d["gender"] = 1
        c.json(d)
        print(c.response.status)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        resp = Response()
        c = context.Context(request, resp)  # should put into pool later to reduce memory/cpu consumption
        try:
            test_func(c)
            # self.dispatch_request(c)
        except Exception as e:
            print("error: ", e)
        return c.response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def add_route(self, path: str, cb: typing.Callable[[context.Context], None], method: str = "GET"):
        pass
        return self

    def add_route_callback(self, path: str, cb: typing.Callable[[context.Context], None], method: str = "GET"):
        pass
        return self

    def run_server(self, addr: str = "0.0.0.0", port: int = 8080):
        from werkzeug.serving import run_simple
        print("server starting...")

        run_simple(addr, port, self, use_debugger=True, use_reloader=False)


if __name__ == "__main__":
    r = Engine()
    r.add_route("/ping", lambda c: print(c), "GET")  # add a get route
    r.run_server()

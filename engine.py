import typing

import context
from werkzeug.wrappers import Request, Response
from router import trie


class Engine:
    def __init__(self):
        self._router = trie.TrieRouterImpl()  # using a trie router

    def dispatch_request(self, c: context.Context):
        # c.response.set_data(value=c.request.path)
        cb = self._router.match_request(c.request)
        if cb is not None:
            try:
                cb(c)
            except Exception as e:
                print(e)
                c.response.status_code = 500
                c.response.set_data(str(e))
        else:
            # TODO: custom error handler for user
            c.response.status_code = 404
            c.response.set_data("sorry, destination not found")

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        resp = Response()
        c = context.Context(request, resp)  # should put into pool later to reduce memory/cpu consumption
        try:
            self.dispatch_request(c)
        except Exception as e:
            print("error: ", e)
        return c.response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def add_route(self, path: str, cb: typing.Callable[[context.Context], None], method: str = "GET"):
        self._router.add_route(path, cb, method)
        return self

    def run_server(self, addr: str = "0.0.0.0", port: int = 8080):
        from werkzeug.serving import run_simple
        print("server starting...")

        run_simple(addr, port, self, use_debugger=True, use_reloader=False)


def test_post(c: context.Context):
    c.text("wocao")


def test_par(c: context.Context):
    n = c.get_parameter("name")
    if n is not None:
        print("we got a", n)
        print(n)
    c.text("okok")


if __name__ == "__main__":
    r = Engine()
    r.add_route("/ping/del", lambda c: print(c), "GET") \
        .add_route("/ping/get", test_post, "GET") \
        .add_route("/user/name", test_par, "GET")

    r.run_server()

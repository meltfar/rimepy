from __future__ import annotations

import re
import typing

allowed_methods = ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"]


class TrieRouterImpl:
    def __init__(self):
        self.__root_map = dict()
        for m in allowed_methods:
            self.__root_map[m] = Tree()

    def any(self):
        pass

    def get(self, path: str, cb: typing.Callable):
        self.__root_map["GET"].add_router(path, cb)

    def post(self):
        pass

    def head(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def options(self):
        pass

    def add_route(self, path, cb, method: str):
        if method not in allowed_methods:
            raise Exception("unsupported http method")
        self.__root_map[method.upper()].add_router(path, cb)

    def match_request(self, req) -> typing.Callable or None:
        return self.__root_map[req.method.upper()].get_handler(req.path)


reg = re.compile("/+")


class Tree:
    def __init__(self):
        self.__tree = TreeNode()

    def get_handler(self, uri: str) -> typing.Callable or None:
        mn = self.__tree.find_by_path(uri)
        if mn is None:
            return None
        return mn.get_handler()

    def add_router(self, uri: str, cb: typing.Callable):
        r = self.__tree
        if r.find_by_path(uri) is not None:
            raise Exception("GET -> uri: " + uri + " exists")

        segments = reg.sub(uri, "/").split("/")
        for i in range(0, len(segments)):
            s = segments[i]
            if is_wildcard(s) is not True:
                s = s.upper()
            is_last = i == len(segments) - 1

            node = None
            children_nodes = r.find_children(s)
            if len(children_nodes) > 0:
                # found
                for cn in children_nodes:
                    if cn.get_path() == s:
                        node = cn
                        break

            # not matched with any node, so we just need to create a new one
            if node is None:
                cn = TreeNode()
                cn.set_path(s)
                if is_last:
                    cn.is_last = True
                    cn.handler = cb
                r.children.append(cn)
                node = cn
            r = node


def is_wildcard(s: str) -> bool:
    return s.startswith(":")


class TreeNode:
    def __init__(self):
        self.__is_last = False
        self.__segment = ""
        self.__handler = None
        self.__children = []

    def get_handler(self):
        return self.__handler

    # def is_last(self) -> bool:
    #     return self.__is_last

    def get_path(self) -> str:
        return self.__segment

    def set_path(self, s: str):
        self.__segment = s

    @property
    def is_last(self):
        return self.__is_last

    @property
    def children(self):
        return self.__children

    @property
    def handler(self):
        return self.__handler

    @handler.setter
    def handler(self, v):
        self.__handler = v

    # match
    def find_by_path(self, path: str) -> TreeNode or None:
        # max-split means how many times should we cut ths string
        # in this situation, should be 1
        segments = path.split("/", maxsplit=1)
        print("segments are: ", segments)

        if len(segments) <= 0:
            raise Exception("invalid route path: " + path)
        seg = segments[0]
        if not is_wildcard(seg):
            seg = seg.upper()

        children = self.find_children(seg)
        if len(children) <= 0:
            return None

        if len(segments) == 1:
            for c in children:
                if c.is_last:
                    return c
            return None
        for c in children:
            c_matched = c.find_by_path(segments[1])
            if c_matched is not None:
                return c_matched

            # TODO: test for not using recursion ?
            # while len(c.children) > 0:
            #     desired_child = None
            #     for cc in c.children:
            #         cc.get_path() == ""
            #     if desired_child is not None:
            #         c = desired_child
        return None

    # filterChildNodes
    def find_children(self, segment: str) -> list[TreeNode]:
        if len(self.__children) <= 0:
            return []
        if is_wildcard(segment):
            return self.__children
        ret = []
        for n in self.__children:
            if is_wildcard(n.__segment):
                ret.append(n)
            elif n.__segment == segment:
                ret.append(n)
        return ret

    @is_last.setter
    def is_last(self, value):
        self.__is_last = value

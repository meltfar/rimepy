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
        pass

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


reg = re.compile("/+")

'''
the last add router function likes below
// 增加路由节点
/*
/book/list
/book/:id (冲突)
/book/:id/name
/book/:student/age
/:user/name
/:user/name/:age(冲突)
*/
func (tree *Tree) AddRouter(uri string, handler ControllerHandler) error {
  n := tree.root
  if n.matchNode(uri) != nil {
    return errors.New("route exist: " + uri)
  }

  segments := strings.Split(uri, "/")
  // 对每个segment
  for index, segment := range segments {

    // 最终进入Node segment的字段
    if !isWildSegment(segment) {
      segment = strings.ToUpper(segment)
    }
    isLast := index == len(segments)-1

    var objNode *node // 标记是否有合适的子节点

    childNodes := n.filterChildNodes(segment)
    // 如果有匹配的子节点
    if len(childNodes) > 0 {
      // 如果有segment相同的子节点，则选择这个子节点
      for _, cnode := range childNodes {
        if cnode.segment == segment {
          objNode = cnode
          break
        }
      }
    }

    if objNode == nil {
      // 创建一个当前node的节点
      cnode := newNode()
      cnode.segment = segment
      if isLast {
        cnode.isLast = true
        cnode.handler = handler
      }
      n.childs = append(n.childs, cnode)
      objNode = cnode
    }

    n = objNode
  }

  return nil
}'''


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
        pass


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

    def is_last(self) -> bool:
        return self.__is_last

    # match
    def find_by_path(self, path: str) -> TreeNode or None:
        segments = path.split("/", maxsplit=2)
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
                if c.is_last():
                    return c
            return None
        for c in children:
            c_matched = c.find_by_path(segments[1])
            if c_matched is not None:
                return c_matched
        return None

    # filterChildNodes
    def find_children(self, segment: str) -> list[TreeNode]:
        if len(self.__children):
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

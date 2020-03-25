from util import stack_size4b


class Node(object):
    path = []

    def __init__(self, data, parent=None, debug: bool = False):
        self.children = {}
        self.data = [data]
        self.parent = parent
        self.debug = debug

    def __str__(self):
        if self.debug:
            print(stack_size4b() - 2, self.data, sorted([x for x in self.children.keys() if x != 'overflow']))

        if len(self.data) == 1:
            return str(f"{self.children['left']}," if "left" in self.children else '') + str(self.data[0]) + str(
                f",{self.children['right']}" if "right" in self.children else '')
        elif len(self.data) == 2:
            return str(f"{self.children['left']}," if "left" in self.children else '') + str(min(self.data)) + str(
                f",{self.children['mid']}," if "mid" in self.children else ',') + str(max(self.data)) + str(
                f",{self.children['right']}" if "right" in self.children else '')

    def insert(self, value: object):
        """
        Adds the value to the tree
        :param value: the value to add to the tree
        :return: None
        """
        Node.path = []
        insert_node = self._search(value)
        insert_node._add(value)

    def _split(self):
        if self.parent is None and self.children:
            branch = Node.path.pop()
            new_node_left = Node(self.data.pop(0), self, self.debug)
            new_node_right = Node(self.data.pop(1), self, self.debug)
            if branch == "left":
                new_node_left.children["left"] = self.children["left"]
                new_node_left.children["right"] = self.children["overflow"]
                new_node_right.children["left"] = self.children["mid"]
                new_node_right.children["right"] = self.children["right"]
            elif branch == "mid":
                new_node_left.children["left"] = self.children["left"]
                new_node_left.children["right"] = self.children["mid"]
                new_node_right.children["left"] = self.children["overflow"]
                new_node_right.children["right"] = self.children["right"]
            elif branch == "right":
                new_node_left.children["left"] = self.children["left"]
                new_node_left.children["right"] = self.children["mid"]
                new_node_right.children["left"] = self.children["right"]
                new_node_right.children["right"] = self.children["overflow"]
            new_node_left.children["left"].parent = new_node_left
            new_node_left.children["right"].parent = new_node_left
            new_node_right.children["left"].parent = new_node_right
            new_node_right.children["right"].parent = new_node_right
            self.children["left"] = new_node_left
            self.children["right"] = new_node_right
            del self.children["mid"]

        elif self.parent is not None and self.children:
            branch = Node.path.pop()
            new_node = Node(self.data.pop(), self.parent, self.debug)
            self.parent.children["overflow"] = new_node
            if branch == "left":
                new_node.children["left"] = self.children["mid"]
                new_node.children["right"] = self.children["right"]
                self.children["right"] = self.children["overflow"]
            elif branch == "mid":
                new_node.children["left"] = self.children["overflow"]
                new_node.children["right"] = self.children["right"]
                self.children["right"] = self.children["mid"]
            elif branch == "right":
                new_node.children["left"] = self.children["right"]
                new_node.children["right"] = self.children["overflow"]
                self.children["right"] = self.children["mid"]
            new_node.children["left"].parent = new_node
            new_node.children["right"].parent = new_node
            del self.children["mid"]

        elif self.parent is None and not self.children:
            self.children["left"] = Node(self.data.pop(0), self, self.debug)
            self.children["right"] = Node(self.data.pop(1), self, self.debug)

        elif self.parent is not None and not self.children:
            self.parent.children["overflow"] = Node(self.data.pop(), self.parent, self.debug)

    def _add(self, value):
        # if value not in self.data:
        self.data.append(value)
        self.data.sort()
        if len(self.data) == 3:
            self._split()
            if self.parent is not None:
                self.parent._add(self.data.pop())
        else:
            if "overflow" in self.children:
                branch = Node.path.pop()
                if branch == "left":
                    self.children["mid"] = self.children["overflow"]
                elif branch == "right":
                    self.children["mid"] = self.children["right"]
                    self.children["right"] = self.children["overflow"]
                del self.children["overflow"]

    def _search(self, value):
        if self.children:
            bound_left = min(self.data)
            bound_right = max(self.data)
            if bound_left == bound_right:
                if value < bound_left:
                    Node.path.append("left")
                    return self.children["left"]._search(value)
                else:
                    Node.path.append("right")
                    return self.children["right"]._search(value)
            else:
                if value < bound_left:
                    Node.path.append("left")
                    return self.children["left"]._search(value)
                elif value > bound_right:
                    Node.path.append("right")
                    return self.children["right"]._search(value)
                else:
                    Node.path.append("mid")
                    return self.children["mid"]._search(value)
        else:
            return self

    def element(self, value: object) -> bool:
        """
        Checks if a value is in the tree
        :param value: the value to search for
        :return: True if the value is in the tree or False otherwise
        """
        if value in self.data:
            return True
        elif self.children:
            bound_left = min(self.data)
            bound_right = max(self.data)
            if value < bound_left:
                return self.children["left"].element(value)
            elif value > bound_right:
                return self.children["right"].element(value)
            else:
                return self.children["mid"].element(value)
        else:
            return False


if __name__ == '__main__':
    import random

    choices = list(range(100))
    random.shuffle(choices)
    print(choices)

    tree = Node(choices[0], debug=True)
    for i in choices[1:]:
        tree.insert(i)
    content = str(tree)
    print(content)
    print(len(content.split(',')))
    print('----------')
class Node:
    def __init__(self, value, below):
        self.value = value
        self.below = below

class Stack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.top = None 
        self.size = 0

    def push(self, value):
        if self.is_full():
            raise("Stack дүүрсэн байна")
        self.top = Node(value, self.top)
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise("Stack хоосон байна")
        value = self.top.value
        self.top = self.top.below
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise("Stack хоосон байна")
        return self.top.value

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size >= self.capacity

    def items(self):
        result = []
        node = self.top
        while node:
            result.insert(0, node.value)
            node = node.below
        return result

    def __str__(self):
        return " ".join(self.items()) + " <- top"
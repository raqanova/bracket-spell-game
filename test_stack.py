# Ажиллуулах: python test_stack.py
from stack import Stack

s = Stack(3)
assert s.is_empty()

s.push("(")
s.push("[")
assert s.peek() == "["
assert s.items() == ["(", "["]

assert s.pop() == "["  
assert s.pop() == "("
assert s.is_empty()

s.push("(")
s.push("(")
s.push("(")
assert s.is_full()

print("Бүх шалгалт амжилттай ✓")

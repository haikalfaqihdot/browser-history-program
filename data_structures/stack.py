class Stack:
    def __init__(self):
        self.data = []

    def push_unique(self, item):
        if item in self.data:
            self.data.remove(item)
        self.data.insert(0, item)

    def peek(self):
        if self.data:
            return self.data[0]
        return None

    def get_all(self):
        return self.data

    def is_empty(self):
        return len(self.data) == 0
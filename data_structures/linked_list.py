class Node:
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, url, title):
        new_node = Node(url, title)
        new_node.next = self.head
        self.head = new_node

    def get_all(self):
        data = []
        temp = self.head

        while temp:
            data.append((temp.url, temp.title))
            temp = temp.next

        return data
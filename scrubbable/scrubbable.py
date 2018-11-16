class Node:
    __slots__ = ['data', 'timestamp', 'next', 'prev']

    def __init__(self, timestamp, data):
        self.data = data
        self.timestamp = timestamp
        self.next = None
        self.prev = None

class Scrubbable :
    def __init__(self):
        self.timestamps = {}
        self.head = None
        self.current = None

    def get(self, timestamp):
        return self.timestamps[timestamp].data

    def read(self):
        tmp = self.current
        self.current = self.current.next
        return tmp

    def readback(self):
        tmp = self.current.prev
        self.current = self.current.prev
        return tmp

    def append(self, timestamp, data):
        if self.head is None:
            new_node = Node(timestamp, data)
            new_node.prev = None
            self.head = new_node
            self.current = new_node
            self.timestamps[timestamp] = new_node

        else:
            new_node = Node(timestamp, data)
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
            self.timestamps[timestamp] = new_node
            new_node.prev = cur
            new_node.next = None

    def prepend(self, data):
        if self.head is None:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node

        else:
            new_node = Node(data)
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def add_after_node(self, key, data):
        cur = self.head
        while cur:
            if cur.next is None and cur.data == key:
                self.append(data)
            elif cur.data == key:
                new_node = Node(data)
                nxt = cur.next
                cur.next = new_node
                new_node.next = nxt
                nxt.prev = new_node
            cur = cur.next

    def add_before_node(self, key, data):
        cur = self.head
        while cur:
            if cur.prev is None and cur.data == key:
                self.prepend(data)
            elif cur.data == key:
                new_node = Node(data)
                prev = cur.prev
                prev.next = new_node
                cur.prev = new_node
                new_node.next = cur
            cur = cur.next

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur = cur.next

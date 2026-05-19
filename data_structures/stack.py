class Stack:
    """
    Stack berbasis list dengan fitur push_unique.
    Urutan: index 0 = halaman TERBARU (top of stack).
    """

    def __init__(self):
        self.data = []

    def push(self, item):
        """Push item tanpa cek duplikat."""
        self.data.insert(0, item)

    def push_unique(self, item):
        """
        Push item ke atas stack.
        Tidak menghapus duplikat URL — setiap kunjungan dicatat apa adanya,
        karena timestamp berbeda = kunjungan yang berbeda.
        Alias push() agar kompatibel dengan pemanggilan lama.
        """
        self.data.insert(0, item)

    def pop(self):
        """Hapus dan kembalikan item teratas."""
        if self.data:
            return self.data.pop(0)
        return None

    def peek(self):
        """Lihat item teratas tanpa menghapus."""
        return self.data[0] if self.data else None

    def get_all(self):
        """Kembalikan semua item (index 0 = terbaru)."""
        return list(self.data)

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def clear(self):
        self.data.clear()


# ─────────────────────────────────────────────────────────────────────────────


class Node:
    def __init__(self, url, title):
        self.url   = url
        self.title = title
        self.next  = None


class LinkedList:
    """
    Singly-linked list untuk menyimpan bookmarks.
    Head = bookmark terbaru.
    """

    def __init__(self):
        self.head = None

    def add(self, url, title):
        """Tambah bookmark baru di depan; skip jika URL sudah ada."""
        # cek duplikat
        temp = self.head
        while temp:
            if temp.url == url:
                return False   # sudah ada
            temp = temp.next

        new_node       = Node(url, title)
        new_node.next  = self.head
        self.head      = new_node
        return True

    def remove(self, url):
        """Hapus bookmark berdasarkan URL."""
        prev, curr = None, self.head
        while curr:
            if curr.url == url:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev, curr = curr, curr.next
        return False

    def get_all(self):
        data, temp = [], self.head
        while temp:
            data.append((temp.url, temp.title))
            temp = temp.next
        return data

    def is_empty(self):
        return self.head is None
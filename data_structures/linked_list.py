class Node:
    # Node digunakan untuk menyimpan 1 data bookmark
    # Setiap node memiliki:
    # url   → alamat website
    # title → judul website
    # next  → pointer ke node berikutnya
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.next = None


class LinkedList:
    # LinkedList digunakan untuk menyimpan kumpulan bookmark
    # head menunjuk ke node pertama pada list
    def __init__(self):
        self.head = None

    def add(self, url, title):
        new_node = Node(url, title)
        new_node.next = self.head
        self.head = new_node

    #   1. Membuat node baru berisi url dan title
    #   2. Node baru diarahkan ke head lama
    #    3. Head dipindahkan ke node baru
    # Bookmark terbaru akan berada di paling depan.
    def get_all(self):
        data = []
        
         # Pointer sementara untuk traversal
        temp = self.head

         # Traversal Linked List
        while temp:
            data.append((temp.url, temp.title))
            # Pindah ke node berikutnya
            temp = temp.next

        return data
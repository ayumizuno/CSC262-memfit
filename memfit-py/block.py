class Block:

    def __init__(self, name, size, offset):
        self.name = name
        self.size = size
        self.offset = offset

    def is_adjacent(self, block):
        if block.offset == self.offset + self.size or \
                self.offset == block.offset + self.size:
            return True
        return False



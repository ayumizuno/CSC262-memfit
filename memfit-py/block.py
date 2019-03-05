class Block:
    """
    This class creates a block, which represents
    a unit of space in the pool.
    """
    def __init__(self, name, size, offset):
        """
        This creates a block object with its
        name, size, and offset.
        :param name: name of block
        :param size: size of block
        :param offset: location of block in pool
        """
        self.name = name
        self.size = size
        self.offset = offset

    def is_adjacent(self, block):
        """
        Checks if the block is next to another given block by
        using their offsets and size.
        :param block: block to check whether it's adjacent to
        :return:
            True if the two are adjacent
            False if the two are not adjacent
        """
        if block.offset == self.offset + self.size or \
                self.offset == block.offset + self.size:
            return True
        return False



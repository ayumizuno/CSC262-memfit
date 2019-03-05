import sys, random
import block as blk


class Simulation(object):
    """
    This class creates a pool simulation object
    that keeps track of its free list and used list
    """
    def __init__(self, algorithm, size):
        """
        This creates a simulation of a pool based
        on a given algorithm and pool size
        :param algorithm: algorithm to run the simulation with
        :param size: size of the pool
        """
        self.algorithm = algorithm
        self.size = size
        self.free_list = []
        self.used_list = []
        self.last_offset = 0
        self.failed = 0

    def print_lists(self):
        """
        prints both free and used lists in offset order
        """
        print("Free List")
        self.free_list.sort(key=lambda block: block.offset)
        for block in self.free_list:
            print("\t",
                  "offset:", block.offset, "\t",
                  "size:", block.size)

        print("Used List")
        self.used_list.sort(key=lambda block: block.offset)
        for block in self.used_list:
            print("\t",
                  "offset:", block.offset, "\t",
                  "size:", block.size, "\t",
                  "name:", block.name)

    def get_stats(self):
        """
        Calculates percent of free and used space
        in the pool and returns those values
        :return:
            pct_free: percent of free space in pool
            pct_used: percent of used space in pool
        """
        free = 0
        used = 0
        for block in self.free_list:
            free += block.size
        for block in self.used_list:
            used += block.size
        pct_free = round((free/self.size) * 100, 2)
        pct_used = round((used/self.size) * 100, 2)
        return pct_free, pct_used

    def alloc(self, name, size):
        """
        Gets a block from the algorithm being run and
        splits the block based on the input size given.
        If there is no available block of desired size,
        count the allocation as a failure.
        :param name: name of block to allocate
        :param size: size of block desired
        """
        if self.algorithm == "first":
            block = self.alloc_first(size)
        elif self.algorithm == "best":
            block = self.alloc_best(size)
        elif self.algorithm == "worst":
            block  = self.alloc_worst(size)
        elif self.algorithm == "next":
            block = self.alloc_next(size)
        elif self.algorithm == "random":
            block = self.alloc_random(size)
        else:
            raise ValueError("Invalid algorithm specified in input file.")

        if block is not None:
            self.block_split(block, name, size)
        else:
            self.failed += 1
            print("Failed allocation of", name)

    def find(self, size):
        """
        Search for a block in the free_list with size
        greater than or equal to the specified size.
        :param size: min size of block wanted
        :return:
            block: next available block from free list
            None: if there is no such block
        """
        for block in self.free_list:
            if block.size >= size:
                return block
        return None

    def find_with_index(self, size, start, stop):
        """
        Search for the next available block in free list in range(start, stop)
        :param size: size of space needed
        :param start: index at which to start search
        :param stop: index at which to stop search
        :return:
            block: next available block from free list
            None: if there is no such block
        """
        for block in self.free_list:
            if block.offset >= start and block.offset <= stop:
                if block.size >= size:
                    self.last_offset = block.offset
                    return block
        return None

    def alloc_first(self, size):
        """
        Returns the next available space based on the first-fit algorithm
        :param size: size of block wanted
        :return: appropriate block based on this algorithm
        """
        self.free_list.sort(key=lambda block: block.offset)
        return self.find(size)

    def alloc_best(self, size):
        """
        Returns the next available space based on the best-fit algorithm
        :param size: size of block wanted
        :return: appropriate block based on this algorithm
        """
        self.free_list.sort(key=lambda block: block.size)
        return self.find(size)

    def alloc_worst(self, size):
        """
        Returns the next available space based on the worst-fit algorithm
        :param size: size of block wanted
        :return: appropriate block based on this algorithm
        """
        self.free_list.sort(key=lambda block: block.size, reverse=True)
        return self.find(size)

    def alloc_next(self, size):
        """
        Returns next available space based on the next-fit algorithm.
        Uses the last_offset property to keep track of the last position
        on the pool.
        :param size: size of block wanted
        :return:
            block: appropriate block based on this algorithm
        """
        print(self.last_offset)
        self.free_list.sort(key=lambda block: block.offset)
        block = self.find_with_index(size, self.last_offset, sim.size)
        if block is not None:
            return block
        else:
            # look in section before index if no available block after
            block = self.find_with_index(size, 0, self.last_offset)
            return block

    def alloc_random(self, size):
        """
        Randomly shuffles the free_list and finds returns the first
        available block.
        :param size: size of block wanted
        :return: appropriate block based on this algorithm
        """
        random.shuffle(self.free_list)
        return self.find(size)

    def free(self, name):
        """
        Free block in used_list and add it back to free_list.
        :param name: name of block to free from used_list
        """
        for block in self.used_list:
            if block.name == name:
                self.used_list.remove(block)
                self.free_list.append(block)
                return

    def compact_free(self):
        """
        Go through the free list and compact adjacent blocks
        so that they become one free space.
        """
        self.free_list.sort(key=lambda block: block.offset)
        copy_list = []
        copy_block = blk.Block("free",0,0)
        i = 0
        while i < len(self.free_list):
            if copy_block.is_adjacent(self.free_list[i]):
                copy_block.size += self.free_list[i].size
            else:
                if copy_block.size > 0:
                    copy_list.append(copy_block)
                copy_block = self.free_list[i]
            i += 1
        if copy_block.size > 0:
            copy_list.append(copy_block)
        self.free_list = copy_list

    def block_split(self, block, new_name, size):
        """
        Construct one or two new blocks given a block and a
        specific size to allocate.
        :param block: block to split
        :param new_name: name of new block
        :param size: size to allocate from the given block
        """
        if size > block.size:
            raise ValueError("Shouldn't be splitting this block with size requested.")
        if size == block.size:
            block.name = new_name
            self.used_list.append(block)
            self.free_list.remove(block)
        else:
            new_block = blk.Block(new_name, size, block.offset)
            block.offset += size
            block.size -= size
            self.used_list.append(new_block)


def start(f):
    """
    Sets up the program by creating a simulation object
    with a block of the size given in the input file in the
    free_list
    :param f: input file
    :return:
        sim: the Simulation object
    """
    pool_line = f.readline().strip("\n").split(" ")
    sim = Simulation(pool_line[1], int(pool_line[2]))
    sim.free_list = [blk.Block("pool", int(pool_line[2]), 0)]
    return sim


def print_stats(pct_free, pct_used, failed):
    """
    Prints how much of the space is used and free, as
    well as the number of failed allocations.
    :param pct_free: Percent of space free
    :param pct_used: Percent of space used
    :param failed: number of failed allocations
    """
    print("Percent of used memory: ", pct_used, "%", sep="")
    print("Percent of free memory: ", pct_free, "%", sep="")
    print("Number of failed allocations:", failed)


if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    sim = start(f)

    for line in f:
        line = line.strip("\n")
        if len(line) > 1:
            print(line)
            line = line.split(" ")
            if "alloc" in line:
                sim.alloc(line[1], int(line[2]))
            elif "free" in line:
                sim.free(line[1])
                sim.compact_free()
            else:
                raise ValueError("Invalid line in input file.")
            sim.print_lists()
            print()
        print()

    pct_free, pct_used = sim.get_stats()
    print_stats(pct_free, pct_used, sim.failed)

    f.close()

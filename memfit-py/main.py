import sys, random
import block as blk


class Simulation(object):
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size
        self.free_list = []
        self.used_list = []
        self.next_index = 0

    def print_lists(self):
        print("Free List")
        for block in self.free_list:
            print("\t",
                  "offset:", block.offset, "\t",
                  "size:", block.size)

        print("Used List")
        for block in self.used_list:
            print("\t",
                  "name:", block.name, "\t",
                  "offset:", block.offset, "\t",
                  "size:", block.size)

    def alloc(self, name, size):
        if self.algorithm == "first":
            block = self.alloc_first(size)
        elif self.algorithm == "best":
            block = self.alloc_best(size)
        elif self.algorithm == "worst":
            block  = self.alloc_worst(size)
        elif self.algortihm == "next":
            block = self.alloc_next(size)
        elif self.algortihm == "random":
            block = self.alloc_random(size)
        else:
            #error
            print("invalid algorithm")

        self.block_split(block, name, size)

    def find(self, size):
        for block in self.free_list:
            if block.size >= size:
                return block
        # can't find block error

    def alloc_first(self, size):
        self.free_list.sort(key=lambda block: block.offset)
        return self.find(size)

    def alloc_best(self, size):
        self.free_list.sort(key=lambda block: block.size)
        return self.find(size)

    def alloc_worst(self, size):
        self.free_list.sort(key=lambda block: block.size, reverse=True)
        return self.find(size)

    def alloc_next(self, size):
        # returns next available block after last used block
        i = self.next_index
        while i < len(self.free_list):
            if self.free_list[i].size >= size:
                self.next_index = i + 1
                return self.free_list[i]
            i += 1
        #return Can't find block error

    def alloc_random(self, size):
        random.shuffle(self.free_list)
        return self.find(size)


    def free(self, name):
        #free block in used_list and add it back to free_list
        for block in self.used_list:
            if block.name == name:
                self.used_list.remove(block)
                self.free_list.append(block)
                return

    def compact_free(self):
        self.free_list.sort(key=lambda block: block.offset)
        copy_list = []
        copy_block = blk.Block()
        i = 0
        while i < len(self.free()):
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
        if size > block.size:
            #can't be allocated ERROR
            return None
        if size == block.size:
            self.used_list.append(block)
            self.free_list.remove(block)
        else:
            new_block = blk.Block(new_name, size, block.offset)
            block.offset += size
            block.size -= size
            self.used_list.append(new_block)


def start(f):
    # create Simulation with pool block in free_list
    pool_line = f.readline().strip("\n").split(" ")
    sim = Simulation(pool_line[1], int(pool_line[2]))
    sim.free_list = [blk.Block("pool", int(pool_line[2]), 0)]
    return sim


if __name__ == '__main__':
    print("Hello World!")
    #get input file
    f = open(sys.argv[1], "r")

    sim = start(f)

    for line in f:
        print(line)
        line = line.strip("\n").split(" ")
        if "alloc" in line:
            sim.alloc(line[1], int(line[2]))
        elif "free" in line:
            sim.free(line[1])
        sim.print_lists()


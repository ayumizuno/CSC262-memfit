import sys, random
import block as blk
import block_graphics as blk_graphics

from graphics import *


class Simulation(object):
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size
        self.free_list = []
        self.used_list = []
        self.last_offset = 0
        self.failed = 0

    def print_lists(self):
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

    def find(self, size):
        for block in self.free_list:
            if block.size >= size:
                return block
        return None

    def find_with_index(self, size, start, stop):
        """
        search for the next available block in free list in range(start, stop)
        :param size: size of space needed
        :param start: index at which to start search
        :param stop: index at which to stop search
        :return: next available block from free list
        """
        for block in self.free_list:
            if block.offset >= start and block.offset <= stop:
                if block.size >= size:
                    self.last_offset = block.offset
                    return block
        return None

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
        self.free_list.sort(key=lambda block: block.offset)
        block = self.find_with_index(size, self.last_offset, sim.size)
        if block is not None:
            return block
        else:
            # look in section before index if no available block after
            block = self.find_with_index(size, 0, self.last_offset)
            return block

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
    # create Simulation with pool block in free_list
    pool_line = f.readline().strip("\n").split(" ")
    sim = Simulation(pool_line[1], int(pool_line[2]))
    sim.free_list = [blk.Block("pool", int(pool_line[2]), 0)]
    return sim


def clear_text(win):
    for item in win.items:
        if type(item) == Text:
            item.undraw()
    win.update()


def redraw(free, used, win):

    for block in used:
        used_block = blk_graphics.BlockGraphics(block.name, block.size, block.offset)
        used_block.unit.setFill("pink")
        used_block.display(win)

    for free_block in free:
        used_block = blk_graphics.BlockGraphics(free_block.name, free_block.size, free_block.offset)
        used_block.unit.setFill("white")
        used_block.display_free(win)


def set_graphics():
    """
    set up GUI window with pool rectangle bar
    """
    win = GraphWin('GUI', 1100, 500)
    pool = Rectangle(Point(50, 100), Point(1050, 200))
    pool.draw(win)
    return win


def print_stats(pct_free, pct_used, failed):
    print("Percent of used memory: ", pct_used, "%", sep="")
    print("Percent of free memory: ", pct_free, "%", sep="")
    print("Number of failed allocations:", failed)


if __name__ == '__main__':
    #win = set_graphics()
    f = open(sys.argv[1], "r")
    sim = start(f)

    for line in f:
        #current processing line
        line = line.strip("\n")
        if len(line) > 1:
            print(line)
            line = line.split(" ")
            #line_text = Text(Point(500, 300), line)
            #line_text.draw(win)

            if "alloc" in line:
                sim.alloc(line[1], int(line[2]))
            elif "free" in line:
                sim.free(line[1])
            else:
                raise ValueError("Invalid line in input file.")
            sim.print_lists()
            print()

            #redraw(sim.free_list, sim.used_list, win)
            #time.sleep(2)
            #clear_text(win)

    pct_free, pct_used = sim.get_stats()
    print_stats(pct_free, pct_used, sim.failed)



    f.close()

   #win.getMouse()
   #win.close()

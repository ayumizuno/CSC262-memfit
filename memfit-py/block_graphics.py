from graphics import *


class BlockGraphics:

    def __init__(self, name, size, offset):
        # pool rectangle x offset is 50
        self.name = name
        self.unit = Rectangle(Point(offset + 50, 100), Point(offset + 50 + size, 200))
        self.label_offset = Text(Point(offset + 50, 80), offset)
        self.label_name = Text(Point(offset + 65, 130), name)
        self.label_size = Text(Point(offset + 65, 150), size)

    def display(self, win):
        self.unit.draw(win)
        self.label_name.draw(win)
        self.label_offset.draw(win)
        self.label_size.draw(win)

    def display_free(self, win):
        self.unit.draw(win)
        self.label_offset.undraw()

    def clear_labels(self):
        """clear labels when freeing a block"""
        self.label_name.undraw()
        self.label_offset.undraw()


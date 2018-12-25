from GameMechanic.BaseBlock import *


class WallBlock(BaseBlock):
    def __init__(self):
        super(WallBlock, self).__init__()
        self.drawable = EDrawable.Wall

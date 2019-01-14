from GameMechanic.BaseBlock import *
from random import randrange


class DeusBlock(BaseBlock):
    def __init__(self):
        super(DeusBlock, self).__init__()
        self.gift = randrange(10) % 2 == 0
        self.turn = 0
        self.drawable = EDrawable.DeusActivating

    def prepare_turn(self, levelController):
        self.turn += 1
        if self.turn >= 2:
            self.drawable = EDrawable.DeusActivated
        if self.turn >= 4:
            levelController.deus = None
            levelController.gridContainer.remove_block(self)

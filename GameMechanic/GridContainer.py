class GridContainer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blockMatrix = []
        for i in range(0, width):
            self.blockMatrix.append([])
            for j in range(0, height):
                self.blockMatrix[i].append(set())

    def move_block(self, baseBlock, x, y):
        x = x % self.width
        y = y % self.height
        if baseBlock.x >= 0 and baseBlock.y >= 0:
            self.blockMatrix[baseBlock.y][baseBlock.x].remove(baseBlock)
        baseBlock.x = x
        baseBlock.y = y
        self.blockMatrix[y][x].add(baseBlock)

    def debug_grid_print(self):
        for x in self.blockMatrix:
            for y in x:
                print(len(y), end=' ')
            print()
        print("\n\n")

    def remove_block(self, baseBlock):
        if baseBlock.x >= 0 and baseBlock.y >= 0:
            self.blockMatrix[baseBlock.y][baseBlock.x].remove(baseBlock)

    def has_blocks(self, x, y):
        x = x % self.width
        y = y % self.height
        return len(self.blockMatrix[x][y]) > 0

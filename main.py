from GameMechanic.Snake import *

from GameMechanic.LevelController import *

if __name__=="__main__":
    print("Zdravo")
    """
    b = BaseBlock()
    grid = GridContainer(15, 15)
    grid.move_block(b, 2, 2)
    grid.debug_grid_print()
    grid.move_block(b, 2, 3)
    grid.debug_grid_print()
    snake = Snake(grid, 4, 4, 5,3,EMoveDirection.right)
    grid.debug_grid_print()
    """
    lc = LevelController()
    lc.gridContainer.debug_grid_print()

    step = True
    while step:
        step = lc.make_turn_step()
        lc.gridContainer.debug_grid_print()


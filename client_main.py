from Network.Client import Client
from Network.NetworkCommand import *
from Network.MovingPlans import *

if __name__ == "__main__":
    c = Client("127.0.0.1", 12355)
    c.connect()
    snakes = []
    while True:
        comm = c.get_command()
        print("Primljena komanda: ", comm.comm)
        if comm.comm == ENetworkCommand.container_update:
            comm.data.gridContainer.debug_grid_print()
            snakes = comm.data.snakes
            for s in comm.data.snakes:
                print("Snake head x=", s.get_head().x, ", y=", s.get_head().y)
            print("\n\n")
        if comm.comm == ENetworkCommand.call_for_plans:
            plans = MovingPlans()
            for s in snakes:
                moves = []
                for _ in range(s.steps):
                    moves.append(s.lastStepDirection)
                plans.set_plan(s, moves)
            c.send_plans(plans)

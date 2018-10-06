from helper import *

from random import randint

class Bot:

    def __init__(self):
        movement = self.hardcode_turn()
        self.moves = [Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)]
        self.mode = (1, 0, 0, 0)  # onehot: first is collect resource, second is find shoppe, third is ATTACK RECKLESSLY, fourth is go home even if pack not full

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def hardcode_turn(self):
        updown = 11
        up = -1
        rightleft = 3
        right = 1
        moves = []
        for i in range(updown):
            moves.append(Point(0, up))
        for i in range(rightleft):
            moves.append(Point(right, 0))
        return moves

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        print(self.mode)
        try:
            action= self.do_decision(gameMap)
        # Write your bot here. Use functions from aiHelper to instantiate your actions.
            return action
        except Exception as e:
            print(e)

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    def do_decision(self, gamemap):
        if self.PlayerInfo.Position == self.PlayerInfo.HouseLocation:
            self.mode = (1,0,0,0)
            #if self.TotalResources >= 10000: #or other upgrade goal:
             #   return self.buy_upgrade()
        if self.mode[3] == 1 or self.PlayerInfo.CarriedResources>=self.PlayerInfo.CarryingCapacity:
            return self.go_home(gamemap)
        elif self.mode[0] == 1 :
            return self.mine_nearest_resource(gamemap)
        else:
            return None

    def mine_nearest_resource(self, gamemap):
        res, dist = find_nearest_resource(gamemap, self.PlayerInfo)
        if res:
            if dist == 1:
                print("MINING")
                print(str(self.PlayerInfo.CarriedResources))
                return create_collect_action(res.Position - self.PlayerInfo.Position)
            else:
                #Call find empty spot here
                emptyres, emptydist = find_empty_spot(gamemap, self.PlayerInfo, res.Position)
                print("Trying to find empty spot to mine")
                if emptyres:
                    return self.move_to(gamemap, emptyres)
                else:
                    return self.go_home(gamemap)
        else:
            return self.go_home(gamemap)

    def go_home(self, gamemap):
        print("GOING HOME")
        self.mode=(0,0,0,1)
        return (self.move_to(gamemap, self.PlayerInfo.HouseLocation))

    def move_to(self, gamemap, target):
        path = a_star(gamemap, self.PlayerInfo, target)
        if path:
            next_tile = path.pop().position
            direction = next_tile - self.PlayerInfo.Position
            return create_move_action(direction)
        else:
            return self.go_home(gamemap)

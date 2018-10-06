from helper import *

from random import randint

class Bot:

    def __init__(self):
        self.upgradeOrder = [ UpgradeType.CarryingCapacity, UpgradeType.CollectingSpeed, UpgradeType.AttackPower, UpgradeType.Defence, UpgradeType.MaximumHealth]
        self.upgradePrices = [10000, 15000,	25000, 50000, 100000]
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
            if not action:
                action = create_move_action(self.moves[randint(0, 3)])
            return action
        except Exception as e:
            print(e)
        try:
            if self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
                tile = gameMap.getTileAt(self.PlayerInfo.Position + self.moves[0])
                if tile == TileContent.Wall:
                    return create_attack_action(self.moves[0])
                if tile == TileContent.Resource:
                    return create_collect_action(self.moves[0])
                if tile == TileContent.House:
                    return create_steal_action(self.moves[0])
                if tile == TileContent.Player:
                    return create_attack_action(self.moves[0])
                return create_move_action(self.moves[0])
            else:
                tile = gameMap.getTileAt(self.PlayerInfo.Position + self.moves[2])
                if tile == TileContent.Resource:
                    return create_collect_action(self.moves[2])
                if tile == TileContent.Player:
                    return create_attack_action(self.moves[2])
                return create_move_action(self.moves[2])                
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
            if self.PlayerInfo.TotalResources > 0:
                for i in range(len(self.upgradeOrder)):
                    level = self.PlayerInfo.getUpgradeLevel(self.upgradeOrder[i])
                    if self.PlayerInfo.TotalResources >= self.upgradePrices[level]:
                        return create_upgrade_action(self.upgradeOrder[i])
        if self.mode[3] == 1 or self.PlayerInfo.CarriedResources>=self.PlayerInfo.CarryingCapacity:
            return self.go_home(gamemap)
        elif self.mode[0] == 1 :
            return self.mine_nearest_resource(gamemap, 0)
        else:
            return None

    def mine_nearest_resource(self, gamemap, index):
        if index >= len(gamemap.resourceTiles):
            return self.go_home(gamemap)
        res, dist = find_nearest_resource(gamemap, self.PlayerInfo, index)
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
                    return None
        else:
            return self.go_home(gamemap)

    def go_home(self, gamemap):
        print("GOING HOME")
        self.mode=(0,0,0,1)
        return self.move_to(gamemap, self.PlayerInfo.HouseLocation)

    def move_to(self, gamemap, target):
        path = a_star(gamemap, self.PlayerInfo, target)
        if path:
            next_tile = path.pop().position
            direction = next_tile - self.PlayerInfo.Position
            return create_move_action(direction)
        else:
            return None

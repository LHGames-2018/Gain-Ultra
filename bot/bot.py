from helper import *
import traceback
from random import randint

from helper.combat import evaluate_target


class Bot:

    def __init__(self):
        self.upgradeOrder = [ UpgradeType.CarryingCapacity, UpgradeType.CollectingSpeed, UpgradeType.AttackPower, UpgradeType.Defence, UpgradeType.MaximumHealth]
        self.upgradePrices = [10000, 15000,	25000, 50000, 100000]
        self.moves = [Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)]

        self.mode = (1, 0, 0, 0)  # onehot: first is collect resource, second is find shoppe, third is ATTACK RECKLESSLY, fourth is go home even if pack not full
        self.default = (0,1,0,0)

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo


    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        print(self.mode)
        try:
            action= self.do_decision(gameMap, visiblePlayers)

        # Write your bot here. Use functions from aiHelper to instantiate your actions.
            if not action:
                action = create_move_action(self.moves[randint(0, 3)])
            return action
        except Exception as e:
            traceback.print_exc()

        try:
            if self.PlayerInfo.Position == self.PlayerInfo.HouseLocation:
                if self.PlayerInfo.TotalResources > 0:
                    for i in range(len(self.upgradeOrder)):
                        level = self.PlayerInfo.getUpgradeLevel(self.upgradeOrder[i])
                        if self.PlayerInfo.TotalResources >= self.upgradePrices[level]:
                            return create_upgrade_action(self.upgradeOrder[i])
            if self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
                for i in range(len(self.moves)):
                    tile = gameMap.getTileAt(self.PlayerInfo.Position + self.moves[i])
                    if tile == TileContent.Player:
                        return create_attack_action(self.moves[i])
                    if tile == TileContent.Wall:
                        return create_attack_action(self.moves[i])
                    if tile == TileContent.Resource:
                        return create_collect_action(self.moves[i])
                    if tile == TileContent.House and (self.PlayerInfo.Position + self.moves[i]) != self.PlayerInfo.HouseLocation:
                        return create_steal_action(self.moves[i])
                return create_move_action(self.moves[1])
            else:
                for i in range(len(self.moves)):
                    tile = gameMap.getTileAt(self.PlayerInfo.Position + self.moves[i])
                    if tile == TileContent.Player:
                        return create_attack_action(self.moves[i])
                    if tile == TileContent.Wall:
                        return create_attack_action(self.moves[i])
                return self.go_home(gameMap)              
        except Exception as e:
            traceback.print_exc()



    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    def do_decision(self, gamemap, visible):

        if self.breakableNear(gamemap):
            return self.breakit(gamemap)
        if self.PlayerInfo.Position == self.PlayerInfo.HouseLocation:
            self.mode = self.default

            if self.PlayerInfo.TotalResources > 0:
                for i in range(len(self.upgradeOrder)):
                    level = self.PlayerInfo.getUpgradeLevel(self.upgradeOrder[i])
                    if self.PlayerInfo.TotalResources >= self.upgradePrices[level]:
                        return create_upgrade_action(self.upgradeOrder[i])
        if self.mode[3] == 1 or self.PlayerInfo.CarriedResources>=self.PlayerInfo.CarryingCapacity:
            return self.go_home(gamemap)
        elif self.mode[0] == 1 :

            random = randint(0,6)
            if random == 0:
                self.mode=(0,1,0,0)
            else:
                return self.mine_nearest_resource(gamemap)
        if self.mode[1] == 1:
            target = evaluate_target(self.PlayerInfo, visible)
            if target:
                pos = find_empty_spot(gamemap,self.PlayerInfo, target.Position)
                if pos:
                    return self.move_to(gamemap, pos[0])
                else:
                    return None
            else:
                mode = (1,0,0,0)
                return self.mine_nearest_resource(gamemap)
        elif self.mode[2] == 1:
            return self.destructTree(gamemap)
        else:
            return None


    def destructTree(self, gamemap):
        return create_move_action(Point(0, 1))


    def breakableNear(self, gamemap):
        for i in range(len(self.moves)):
            tile = gamemap.getTileAt(self.PlayerInfo.Position + self.moves[i])
            if tile == TileContent.Wall or tile == TileContent.Player:
                return True
        else: return False


    def breakit(self, gamemap):
        for i in range(len(self.moves)):
            tile = gamemap.getTileAt(self.PlayerInfo.Position + self.moves[i])
            if tile == TileContent.Wall or tile == TileContent.Player:
                self.mode = (1,0,0,0)
                return create_attack_action(self.moves[i])
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
        return self.move_to(gamemap, self.PlayerInfo.HouseLocation)

    def move_to(self, gamemap, target):
        path = a_star(gamemap, self.PlayerInfo, target)
        if path:
            next_tile = path.pop().position
            direction = next_tile - self.PlayerInfo.Position
            return create_move_action(direction)
        else:
            return None



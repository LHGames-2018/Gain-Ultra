from helper import *
from random import randint

class Bot:

    def __init__(self):
        self.upgradeOrder = [ UpgradeType.CarryingCapacity, UpgradeType.CollectingSpeed, UpgradeType.AttackPower, UpgradeType.Defence, UpgradeType.MaximumHealth]
        self.upgradePrices = [10000, 15000,	25000, 50000, 100000]
        movement = self.hardcode_turn()
        self.moves = [Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)]

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
        try:
            if self.PlayerInfo.TotalResources > 0 and self.PlayerInfo.Position == self.PlayerInfo.HouseLocation:
                for i in range(len(self.upgradeOrder)):
                    level = self.PlayerInfo.getUpgradeLevel(self.upgradeOrder[i])
                    if self.PlayerInfo.TotalResources >= self.upgradePrices[level]:
                        return create_upgrade_action(self.upgradeOrder[i])
            action = self.PlayerInfo.mine_nearest_resource(gameMap)
        # Write your bot here. Use functions from aiHelper to instantiate your actions.
            return action
        except Exception as e:
            print(e)

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass


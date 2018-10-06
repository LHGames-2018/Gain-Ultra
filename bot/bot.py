from helper import *


class Bot:

    def __init__(self):
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

        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        for i in range(len(self.moves)):
            tile = gameMap.getTileAt(self.PlayerInfo.position + self.moves[i])
            if tile.TileContent == TileContent.Resource:
                return create_collect_action(self.moves[i])
        return create_move_action(self.moves[randint(0, 3)])

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass


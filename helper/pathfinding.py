from helper.structs import *
from helper.tile import TileContent


class Node:
    def __init__(self, position):
        self.parent = None
        self.position = position
        self.H = 0
        self.G = 0


def enfants(current, gamemap):
    liens = [Point(current.position.x - 1, current.position.y), Point(current.position.x, current.position.y - 1), Point(current.position.x, current.position.y + 1), Point(current.position.x + 1, current.position.y)]
    return [Node(lien) for lien in liens if (gamemap.getTileAt(lien) == TileContent.Empty or gamemap.getTileAt(lien) == TileContent.House)]


def manhattan(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def a_star(gamemap, player, target):
    while abs(target.x - player.Position.x) > 8 or abs(target.y - player.Position.y) > 8:
        target.x = (target.x - player.Position.x) / 2 + player.Position.x
        target.y = (target.y - player.Position.y) / 2 + player.Position.y
    current = Node(player.Position)
    closedset = set()
    openset = set()
    openset.add(current)

    while openset:
        if len(openset) > 400:
            break
        current = min(openset, key=lambda o: o.G + o.H)
        if current.position.x == target.x and current.position.y == target.y:  # Quand le but est trouve, on depile les cases trouvees
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            return path
        openset.remove(current)
        closedset.add(current)
        for node in enfants(current, gamemap):
            if node in closedset:
                continue
            if node in openset:
                if node.G > current.G + 1:
                    node.G = current.G + 1
                    node.parent = current
            else:
                node.G = current.G + 1
                node.H = manhattan(current.position, target)
                node.parent = current
                openset.add(node)
    return []

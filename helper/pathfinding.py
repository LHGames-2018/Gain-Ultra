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
    while abs(target.x - player.Position.x) > 16 or abs(target.y - player.Position.y) > 16:
        target.x = (target.x - player.Position.x) / 2 + player.Position.x
        target.y = (target.y - player.Position.y) / 2 + player.Position.y
    current = Node(player.Position)
    closedset = set()
    openset = set()
    openset.add(current)

    while openset:
        if len(openset) > 1000:
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


def find_nearest_resource(gamemap, player):
    dist = 1000000
    nearest_resource = None
    man = 0
    for tile in gamemap.resourceTiles:
        man = manhattan(player.Position, tile.Position)
        if abs(player.Position.x - tile.Position.x) <= 16 and abs(player.Position.y - tile.Position.y) <= 16 and man < dist:
            dist = man
            nearest_resource = tile

    return (nearest_resource, dist)

def find_empty_spot(gamemap, player, target):
    dist = 1000000
    ret = None
    for i in range(target.x - 1, target.x + 1):
        for j in range(target.y - 1, target.y + 1):
            point = Point(i, j)
            man = manhattan(player.Position, point)
            if gamemap.getTileAt(point) == TileContent.Empty:
                dist = man
                ret = point
    return (ret, dist)


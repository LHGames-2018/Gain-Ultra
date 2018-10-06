from helper.structs import *
from helper.tile import TileContent
import heapq


class Node:
    def __init__(self, position):
        self.parent = None
        self.position = position
        self.H = 0
        self.G = 0

    def __lt__(self, other):
        return self.H + self.G < other.H + other.G

def enfants(current, gamemap):
    liens = [Point(current.position.x - 1, current.position.y), Point(current.position.x, current.position.y - 1), Point(current.position.x, current.position.y + 1), Point(current.position.x + 1, current.position.y)]
    return [Node(lien) for lien in liens if (gamemap.getTileAt(lien) == TileContent.Empty or gamemap.getTileAt(lien) == TileContent.House)]


def manhattan(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def a_star(gamemap, player, target):
    #while abs(target.x - player.Position.x) > 10 or abs(target.y - player.Position.y) > 10:
    #    target.x = (target.x - player.Position.x) / 2 + player.Position.x
    #    target.y = (target.y - player.Position.y) / 2 + player.Position.y
    current = Node(player.Position)
    visited = set()
    pqueue = []
    heapq.heappush(pqueue, current)

    while pqueue:
        if len(pqueue) > 5000:
            break
        current = heapq.heappop(pqueue)
        if current.position.x == target.x and current.position.y == target.y:  # Quand le but est trouve, on depile les cases trouvees
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            return path
        visited.add(current)
        for node in enfants(current, gamemap):
            if node in visited:
                continue
            if node in pqueue:
                if node.G > current.G + 1:
                    node.G = current.G + 1
                    node.parent = current
            else:
                node.G = current.G + 1
                node.H = manhattan(current.position, target)
                node.parent = current
                heapq.heappush(pqueue, node)
    return []


def find_nearest_resource(gamemap, player, index):
    dist = 1000000
    nearest_resource = None
    man = 0
    for tile in gamemap.resourceTiles[index:]:
        man = manhattan(player.Position, tile.Position)
        if man < dist:
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

def find_nearest_tree(gamemap, player):
    dist = 1000000
    nearest_resource = None
    man = 0
    for tile in gamemap.resourceTiles:
        man = manhattan(player.Position, tile.Position)
        if abs(player.Position.x - tile.Position.x) <= 8 and abs(player.Position.y - tile.Position.y) <= 8 and man < dist:
            dist = man
            nearest_resource = tile

    return (nearest_resource, dist)
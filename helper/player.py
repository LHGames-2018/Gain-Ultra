from helper.pathfinding import *
from helper.aiHelper import *
from helper.structs import *
from helper.tile import *

class Player:
    def __init__(self, health, maxHealth, carriedResources, carryingCapacity,
                 collectingSpeed, totalResources, attackPower, defence, position, houseLocation,
                 carriedItems, score, name, upgradeLevels):
        self.Health = health
        self.MaxHealth = maxHealth
        self.CarriedResources = carriedResources
        self.CarryingCapacity = carryingCapacity
        self.CollectingSpeed = collectingSpeed
        self.TotalResources = totalResources
        self.AttackPower = attackPower
        self.Defence = defence
        self.Position = position
        self.HouseLocation = houseLocation
        self.CarriedItems = carriedItems
        self.Score = score
        self.Name = name
        self.UpgradeLevels = upgradeLevels

    def getUpgradeLevel(self, type):
        return self.UpgradeLevels[type]

    def move_to(self, gamemap, target):
        path = a_star(gamemap, self, target)
        if path:
            next_tile = path.pop().position
            direction = next_tile - self.Position
            return create_move_action(direction)
        else:
            return create_move_action(Point(0, 0))

    def go_home(self, gamemap):
        print("GOING HOME")
        return self.move_to(gamemap, self.HouseLocation)

    def mine_nearest_resource(self, gamemap):
        if self.CarriedResources < self.CarryingCapacity:
            res, dist = find_nearest_resource(gamemap, self)
            if res:
                if dist == 1:
                    print("MINING")
                    print(str(self.CarriedResources))
                    return create_collect_action(res.Position - self.Position)
                else:
                    #Call find empty spot here
                    emptyres, emptydist = find_empty_spot(gamemap, self, res.Position)
                    print("Trying to find empty spot to mine")
                    if emptyres:
                        return self.move_to(gamemap, emptyres)
                    else:
                        return self.go_home(gamemap)
            else:
                return self.go_home(gamemap)
        else:
            return self.go_home(gamemap)





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
        self.mode = (1,0,0,0) #onehot: first is collect resource, second is find shoppe, third is ATTACK RECKLESSLY, fourth is go home even if pack not full

    def getUpgradeLevel(self, type):
        return self.UpgradeLevels[type]

    def move_to(self, gamemap, target):
        path = a_star(gamemap, self, target)
        if path:
            next_tile = path.pop().position
            direction = next_tile - self.Position
            return create_move_action(direction)
        else:
            return self.go_home(gamemap)

    def go_home(self, gamemap):
        print("GOING HOME")
        self.mode = (0,0,0,1)
        return self.move_to(gamemap, self.HouseLocation)

    def buy_upgrade(self):#TODO
        return create_upgrade_action(UpgradeType.CarryingCapacity)

    def mine_nearest_resource(self, gamemap):
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


    def do_decision(self, gamemap):
        print("doing decisioin, mode =")
        print(self.mode)
        if self.Position == self.HouseLocation:
            self.mode = (1,0,0,0)
            if self.TotalResources >= 10000: #or other upgrade goal:
                return self.buy_upgrade()
        if self.mode[3]==1 or self.CarriedResources>=self.CarryingCapacity:
            return self.go_home(gamemap)
        elif self.mode[0]==1 :
            return self.mine_nearest_resource(gamemap)
        else:
            return None








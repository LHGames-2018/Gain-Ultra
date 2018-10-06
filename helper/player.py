from helper.pathfinding import a_star
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


from helper.structs import *
from helper.pathfinding import *
import heapq

class Enemy:
    def __init__(self, player, h):
        self.player = player
        self.h = h

    def __lt__(self, other):
        return self.h < other.h

def evaluate_target(player, visiblePlayers):
    possibilities = []
    results = []
    for enemy in visiblePlayers:
        turns_to_kill = estimate_outcome(player, enemy)
        turns_to_get_killed = estimate_outcome(enemy, player)
        if turns_to_kill <= turns_to_get_killed:
            distance = manhattan(player.Position, enemy.Position)
            score_diff = enemy.Score - player.Score
            if score_diff > 0:
                h = (turns_to_kill/turns_to_get_killed) * (1000/score_diff) * distance
            else:
                h = (turns_to_kill/turns_to_get_killed) * -score_diff * distance
            heapq.heappush(possibilities, Enemy(enemy, h))

    if possibilities:
        target = heapq.heappop(possibilities)
    else:
        return None
    if not target or target.h > 50000:
        return None
    return target.player


def estimate_outcome(player, other):
    #loor(3 + attacker's power + offensive items - 2 * (defender's defence + defensive items) ^ 0.6 )
    attack_power = math.floor((3 + player.AttackPower) - (2 * (other.Defence**0.6)))
    if attack_power ==0:
        return 1000
    return math.ceil(other.Health / attack_power)

"""
Baseball Lineup Optimizer - Naive/Exhaustive Approach
Constraint: Strict alternation of batter handedness (L-R-L-R or R-L-R-L)
            Same-hand consecutive batters only when a pool is exhausted.
"""
class BaseballNaive:
    def __init__(self, players, lineupLen=9):
        self.players = sorted(players, key=lambda x: x[0])
        self.lineup = []
        self.lineupLen = lineupLen
        self.totalAvg = 0.0
        self.pathsExplored = 0
    
    def calcScore(self, lineup):
        # weight earlier positions more heavily
        return sum(player[0] * (self.lineupLen - i) for i, player in enumerate(lineup))
    
    def explore(self, currentLineup, remainingL, remainingR, bestLineup, bestScore):
        # base case: lineup is complete
        if len(currentLineup) == self.lineupLen:
            self.pathsExplored += 1
            score = self.calcScore(currentLineup)
            if score > bestScore[0]:
                bestScore[0] = score
                bestLineup.clear()
                bestLineup.extend(currentLineup)
            return
        
        # alternating hand
        if len(currentLineup) == 0:
            # first position: try both L & R as starting points
            for i, lefty in enumerate(remainingL):
                newRemainingL = remainingL[:i] + remainingL[i+1:]
                self.explore(currentLineup + [lefty], newRemainingL, remainingR, bestLineup, bestScore)
            for i, righty in enumerate(remainingR):
                newRemainingR = remainingR[:i] + remainingR[i+1:]
                self.explore(currentLineup + [righty], remainingL, newRemainingR, bestLineup, bestScore)
        else:
            lastHand = currentLineup[-1][1]
            # try to alternate
            if lastHand == 'L' and remainingR:
                for i, righty in enumerate(remainingR):
                    newRemainingR = remainingR[:i] + remainingR[i+1:]
                    self.explore(currentLineup + [righty], remainingL, newRemainingR, bestLineup, bestScore)
            elif lastHand =='R' and remainingL:
                for i, lefty in enumerate(remainingL):
                    newRemainingL = remainingL[:i] + remainingL[i+1:]
                    self.explore(currentLineup + [lefty], newRemainingL, remainingR, bestLineup, bestScore)
            # if can't alternate, use what's left
            elif remainingL:
                for i, lefty in enumerate(remainingL):
                    newRemainingL = remainingL[:i] + remainingL[i+1:]
                    self.explore(currentLineup + [lefty], newRemainingL, remainingR, bestLineup, bestScore)
            elif remainingR:
                for i, righty in enumerate(remainingR):
                    newRemainingR = remainingR[:i] + remainingR[i+1:]
                    self.explore(currentLineup + [righty], remainingL, newRemainingR, bestLineup, bestScore)

    def naiveBaseballLineup(self):
        l = [p for p in self.players if p[1] == 'L']
        r = [p for p in self.players if p[1] == 'R']

        bestLineup = []
        bestScore = [float('-inf')]

        self.explore([], l, r, bestLineup, bestScore)

        self.lineup = bestLineup
        if self.lineup:
            self.totalAvg = sum(player[0] for player in self.lineup) / len(self.lineup)
        

# Test - Realistic MLB scenario: 20 players, 9-batter lineup
players = [
    # 10 Right-handed batters
    (0.340, "R"),  # Mike Trout
    (0.315, "R"),  # Aaron Judge
    (0.305, "R"),  # Mookie Betts
    (0.295, "R"),  # José Ramírez
    (0.285, "R"),  # Nolan Arenado
    (0.275, "R"),  # Pete Alonso
    (0.265, "R"),  # Vladimir Guerrero Jr.
    (0.255, "R"),  # Rafael Devers
    (0.245, "R"),  # Bo Bichette
    (0.235, "R"),  # Dansby Swanson
    # 10 Left-handed batters
    (0.335, "L"),  # Freddie Freeman
    (0.325, "L"),  # Juan Soto
    (0.310, "L"),  # Yordan Alvarez
    (0.300, "L"),  # Kyle Tucker
    (0.290, "L"),  # Randy Arozarena
    (0.280, "L"),  # Christian Yelich
    (0.270, "L"),  # Corey Seager
    (0.260, "L"),  # Max Muncy
    (0.250, "L"),  # Brandon Lowe
    (0.240, "L"),  # Anthony Rizzo
]

import time

def calcExpectedPaths(nL, nR, lineupLen):
    """Calculate expected paths given alternating hand constraint"""
    total = 0
    
    # Starting with L: L-R-L-R-L-R...
    paths_L = 1
    l_remaining, r_remaining = nL, nR
    for i in range(lineupLen):
        if i % 2 == 0:  # L positions
            if l_remaining > 0:
                paths_L *= l_remaining
                l_remaining -= 1
            else:
                break
        else:  # R positions
            if r_remaining > 0:
                paths_L *= r_remaining
                r_remaining -= 1
            else:
                break
    total += paths_L
    
    # Starting with R: R-L-R-L-R-L...
    paths_R = 1
    l_remaining, r_remaining = nL, nR
    for i in range(lineupLen):
        if i % 2 == 0:  # R positions
            if r_remaining > 0:
                paths_R *= r_remaining
                r_remaining -= 1
            else:
                break
        else:  # L positions
            if l_remaining > 0:
                paths_R *= l_remaining
                l_remaining -= 1
            else:
                break
    total += paths_R
    
    return total

lineupLen = 9
nL = sum(1 for p in players if p[1] == 'L')
nR = sum(1 for p in players if p[1] == 'R')
expectedPaths = calcExpectedPaths(nL, nR, lineupLen)

baseball = BaseballNaive(players, lineupLen)
print(f"Starting naive search with {len(players)} players ({nL}L, {nR}R), {lineupLen}-batter lineup...")
print(f"Expected paths: {expectedPaths:,}\n")

start = time.time()
baseball.naiveBaseballLineup()
elapsed = time.time() - start

print("Lineup:", baseball.lineup)
print("Batting Average =", round(baseball.totalAvg, 3))
print("Paths Explored =", f"{baseball.pathsExplored:,}")
print(f"Time: {elapsed:.2f} seconds")


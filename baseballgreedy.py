class Baseball:
    def __init__(self, players, lineupLen=9):
        self.players = sorted(players, key = lambda x: x[0])
        self.lineup = []
        self.lineupLen = lineupLen
        self.totalAvg = 0.0
    def greedyBaseballLinup(self):
        l = ([p for p in self.players if p[1] == "L"])
        r = ([p for p in self.players if p[1] == "R"])

        self.lineup.append(self.players.pop())
        if self.lineup[0][1] == "L":
            l.remove(self.lineup[0])
        else:
            r.remove(self.lineup[0])
        
        while self.lineupLen > len(self.lineup):
            lastHandiness = self.lineup[-1][1]
            if lastHandiness == "L" and r:
                self.lineup.append(r.pop())
            elif lastHandiness == "R" and l:
                self.lineup.append(l.pop())
            elif l:
                self.lineup.append(l.pop())
            elif r:
                self.lineup.append(r.pop())
                
        if self.lineup:
            self.totalAvg = sum(player[0] for player in self.lineup) / len(self.lineup)



# players =  [(.333,"L"), (.275,"L"), (.300,"L"), (.290,"L"), (.310,"L"), (0.280,"R"), (0.265,"R"), (0.310,"R"), (0.295,"R"), (0.305,"R")]

# baseball = Baseball(players)
# lineup = baseball.greedyBaseballLinup()
# print("lineup: ",baseball.lineup)

players = [(0.340,"R"), (0.315,"R"), (0.305,"R"), (0.295,"R"), (0.285,"R"),(0.335,"L"), (0.325,"L"), (0.310,"L"), (0.300,"L"), (0.290,"L")]
baseball = Baseball(players, 5)
lineup = baseball.greedyBaseballLinup()
print(baseball.lineup)
print("Batting Average = ", baseball.totalAvg)

# Example with one left-handed player
# players = [(0.340,"R"), (0.315,"R"), (0.305,"R"), (0.295,"R"), (0.285,"R"),(0.335,"L")]
# baseball = Baseball(players, 5)
# lineup = baseball.greedyBaseballLinup()
# print("Lineup with one leftie: ", baseball.lineup)
# print("Batting Average = ", baseball.totalAvg)

# Example with one right-handed player
# players = [(0.340,"R"), (0.335,"L"), (0.325,"L"), (0.310,"L"), (0.300,"L"), (0.290,"L")]
# baseball = Baseball(players, 5)
# lineup = baseball.greedyBaseballLinup()
# print("Lineup with one rightie: ", baseball.lineup)
# print("Batting Average = ", baseball.totalAvg)




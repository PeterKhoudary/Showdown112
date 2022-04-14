import math
from moveClass import *

class Monster():
    level = 100
    IVs = {'HP': 31, 'ATK': 31, 'DEF': 31, 'SPATK': 31, 'SPDEF': 31, 'SPE': 31}

    def __init__(self, name, base):
        self.name = name
        self.types = base["types"]
        self.type = "-".join(self.types)
        self.baseStats = base["baseStats"]
        self.movepool = base["movepool"]
        self.moveset = list(self.movepool) #edit this later
        self.EVs = dict()
        self.finalStats = dict()
        for stat in self.baseStats:
            self.EVs[stat] = 0
            self.finalStats[stat] = self.finalStat(stat)
        self.fainted = False

    def finalStat(self, stat):
        if stat == "HP":
            newStat = math.floor(.01 * (2 * self.baseStats["HP"] + self.IVs["HP"] + math.floor(.25 * self.EVs["HP"])) * self.level) + self.level + 10
            self.currentHP = newStat
        else:
            newStat = math.floor(.01 * (2 * self.baseStats[stat] + self.IVs[stat] + math.floor(.25 * self.EVs[stat])) * self.level) + 5
        return newStat
    
    def __str__(self):
        return self.name
    
    def setEVs(self):
        self.EVtotal = 0
        for stat in self.EVs:
            print(f'Current EV total = {self.EVtotal}, {508 - self.EVtotal} remaining')
            EVamount = int(input(f'How many {stat} EVs? (0 - 252): '))
            while (EVamount < 0 or EVamount > 255 or self.EVtotal + EVamount > 508):
                if EVamount < 0:
                    EVamount = int(input("Can't have negative EVs, try again (0 - 252): "))
                elif EVamount > 255:
                    EVamount = int(input("One stat can't have more than 252 EVs, try again (0 - 252): "))
                else:
                    EVamount = int(input(f"A single monster can only have 508 EVs, you can only pick a number between 0 and {508 - self.EVtotal}: "))
            self.EVtotal += EVamount
            self.EVs[stat] = EVamount
        for stat in self.finalStats:
            self.finalStats[stat] = self.finalStat(stat)
        return f'EVs = {self.EVs}'
    
    def setMoves(self):
        print(f"Potential moves for {self.name}:")
        for name in self.movepool:
            print(name, end = "    ")
        print()
        for moveSlot in range(4):
            moveChoice = input(f'Pick move {moveSlot + 1} for {self.name}: ')
            while moveChoice not in self.movepool or moveChoice in self.moveset:
                if moveChoice not in self.movepool:
                    moveChoice = input(f"{self.name} can't learn {moveChoice}, try again: ")
                else:
                    moveChoice = input(f"{self.name} already knows {moveChoice}, try again: ")
            self.moveset.append(moveChoice)
        print(self.moveset)

#List of pokemon bases
dragoniteBase = {"baseStats" : {'HP': 91, 'ATK': 134, 'DEF': 95, 'SPATK': 100, 'SPDEF': 100, 'SPE': 80},
                 "types": {"dragon", "flying"},
                 "movepool": {"Dragon Claw", "Ice Beam", "Extreme Speed", "Earthquake"}}
volcBase = {"baseStats": {'HP': 85, 'ATK': 60, 'DEF': 65, 'SPATK': 135, 'SPDEF': 105, 'SPE': 100},
            "types": {"bug", "fire"},
            "movepool" : {"Fire Blast", "Bug Buzz", "Quick Attack", "Hurricane"}}

lance = Monster("Dragonite", dragoniteBase)
alder = Monster("Volcarona", volcBase)
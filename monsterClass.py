import math
from moveClass import *

class Monster():
    level = 100
    IVs = {'HP': 31, 'ATK': 31, 'DEF': 31, 'SPATK': 31, 'SPDEF': 31, 'SPE': 31}

    def __init__(self, base):
        self.name = base["name"]
        self.types = base["types"]
        self.type = "-".join(self.types)
        self.baseStats = base["baseStats"]
        self.movepool = base["movepool"]
        self.moveset = [] 
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
dragoniteBase = {"name": "Dragonite",
                 "baseStats" : {'HP': 91, 'ATK': 134, 'DEF': 95, 'SPATK': 100, 'SPDEF': 100, 'SPE': 80},
                 "types": {"dragon", "flying"},
                 "movepool": {"Dragon Claw", "Ice Beam", "Extreme Speed", "Earthquake", "Iron Head", "Body Slam"}}
volcBase = {"name": "Volcarona",
            "baseStats": {'HP': 85, 'ATK': 60, 'DEF': 65, 'SPATK': 135, 'SPDEF': 105, 'SPE': 100},
            "types": {"bug", "fire"},
            "movepool" : {"Fire Blast", "Bug Buzz", "Psychic", "Hurricane"}}
keldBase = {"name": "Keldeo",
            "baseStats": {'HP': 91, 'ATK': 72, 'DEF': 90, 'SPATK': 129, 'SPDEF': 90, 'SPE': 108},
            "types": {"water", "fighting"},
            "movepool" : {"Secret Sword", "Scald", "Hydro Pump", "Icy Wind"}}
tyrantBase = {"name": "Tyranitar",
              "baseStats": {'HP': 100, 'ATK': 134, 'DEF': 110, 'SPATK': 95, 'SPDEF': 100, 'SPE': 61},
              "types": {"dark", "rock"},
              "movepool" : {"Stone Edge", "Crunch", "Earthquake", "Iron Head", "Dragon Claw", "Ice Beam", "Body Slam"}}

#Monster names

monNames = {"Dragonite": dragoniteBase, "Tyranitar": tyrantBase, 
            "Volcarona": volcBase, "Keldeo": keldBase}

thugger = Monster(tyrantBase)
alder = Monster(volcBase)
lance = Monster(dragoniteBase)
blunder = Monster(keldBase)

assignMoves = [["Stone Edge", "Dragon Claw", "Iron Head", "Body Slam"], 
               ["Bug Buzz", "Fire Blast" , "Hurricane", "Psychic"], 
               ["Ice Beam", "Dragon Claw", "Iron Head", "Body Slam"], 
               ["Scald", "Hydro Pump", "Secret Sword", "Icy Wind"]]
monList = [thugger, alder, lance, blunder]
for bruh in range(len(assignMoves)):
    monList[bruh].moveset = monList[bruh].moveset + assignMoves[bruh]


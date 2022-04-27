import math

class Monster():
    level = 100
    IVs = {'HP': 31, 'ATK': 31, 'DEF': 31, 'SPATK': 31, 'SPDEF': 31, 'SPE': 31}

    def __init__(self, base, EVs = dict(), moveset = []):
        self.name = base["name"]
        self.types = base["types"]
        self.type = "-".join(self.types)
        self.baseStats = base["baseStats"]
        self.movepool = base["movepool"]
        if moveset != []:
            self.moveset = moveset
        self.finalStats = dict() 
        if EVs != dict():
            self.EVs = EVs
            for stat in self.baseStats:
                self.finalStats[stat] = self.finalStat(stat)
        else:
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

#Test Monsters
thugger = Monster(tyrantBase, 
                  {'HP': 252, 'ATK': 252, 'DEF': 0, 'SPATK': 4, 'SPDEF': 0, 'SPE': 0}, 
                  [['Crunch', 24], ['Stone Edge', 8], ['Dragon Claw', 24], ['Ice Beam', 16]])
alder = Monster(volcBase, 
                {'HP': 0, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 4, 'SPE': 252}, 
                [['Psychic', 16], ['Bug Buzz', 16], ['Fire Blast', 8], ['Hurricane', 16]])
lance = Monster(dragoniteBase, 
                {'HP': 4, 'ATK': 252, 'DEF': 0, 'SPATK': 0, 'SPDEF': 0, 'SPE': 252}, 
                [['Dragon Claw', 24], ['Extreme Speed', 8], ['Iron Head', 24], ['Earthquake', 16]])
blunder = Monster(keldBase, 
                  {'HP': 4, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 0, 'SPE': 252}, 
                  [['Secret Sword', 16], ['Hydro Pump', 8], ['Icy Wind', 24], ['Scald', 24]])

globalUserTeam = [blunder, alder, 2]
globalFoeTeam = [lance, thugger, 2]

# def teamRefresh(userTeam, foeTeam):
#     for team in [userTeam, foeTeam]:
#         for monSlot in range(len(userTeam) - 1):
#             team[monSlot].currentHP = team[monSlot].finalStats["HP"]
#             team[monSlot].fainted = False
#             for moveSlot in team[monSlot].moveset:
#                 moveSlot[1] = moveNames[moveSlot[0]].PP
#         team[-1] = len(team) - 1
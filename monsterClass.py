#This contains the monster class, which does 90% of the heavy lifting in terms of state analysis, plus all the data for all pokemon

import math
from moveClass import *
class Monster(): #class for all pokemon
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
        monNames[self.name] = base #adds base to dictionary

    def finalStat(self, stat): #sets acutal stats given level IVs EVs
        if stat == "HP":
            newStat = math.floor(.01 * (2 * self.baseStats["HP"] + self.IVs["HP"] + math.floor(.25 * self.EVs["HP"])) * self.level) + self.level + 10
            self.currentHP = newStat
        else:
            newStat = math.floor(.01 * (2 * self.baseStats[stat] + self.IVs[stat] + math.floor(.25 * self.EVs[stat])) * self.level) + 5
        return newStat
    
    def __str__(self):
        return self.name

monNames = {} #initialize dictionary

#List of pokemon bases, listing name, base stats, type, and moves they can learn
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
chompBase = {"name": "Garchomp",
            "baseStats": {'HP': 108, 'ATK': 130, 'DEF': 95, 'SPATK': 80, 'SPDEF': 85, 'SPE': 102},
            "types": {"ground", "dragon"},
            "movepool" : {"Earthquake", "Dragon Claw", "Fire Blast", "Iron Head", "Aqua Tail", "Stone Edge"}}
garBase = {"name": "Gengar",
            "baseStats": {'HP': 60, 'ATK': 65, 'DEF': 60, 'SPATK': 130, 'SPDEF': 70, 'SPE': 110},
            "types": {"ghost", "poison"},
            "movepool" : {"Shadow Ball", "Focus Blast", "Energy Ball", "Thunderbolt", "Sludge Bomb", "Psychic"}}
scizBase = {"name": "Scizor",
            "baseStats": {'HP': 70, 'ATK': 130, 'DEF': 100, 'SPATK': 55, 'SPDEF': 80, 'SPE': 65},
            "types": {"ghost", "poison"},
            "movepool" : {"Bullet Punch", "X-Scissor", "Brick Break", "Iron Head", "Acrobatics", "Night Slash"}}
kissBase = {"name": "Togekiss",
            "baseStats": {'HP': 85, 'ATK': 50, 'DEF': 95, 'SPATK': 120, 'SPDEF': 115, 'SPE': 80},
            "types": {"normal", "flying"},
            "movepool" : {"Tri Attack", "Air Slash", "Fire Blast", "Flamethrower", "Psychic", "Shadow Ball"}}  
sceptBase = {"name": "Sceptile",
            "baseStats": {'HP': 70, 'ATK': 85, 'DEF': 65, 'SPATK': 105, 'SPDEF': 85, 'SPE': 120},
            "types": {"grass"},
            "movepool" : {"Acrobatics", "Brick Break", "Energy Ball", "Dragon Pulse", "Rock Slide", "Thunder Punch", "X-Scissor"}}      
weavBase = {"name": "Weavile",
            "baseStats": {'HP': 70, 'ATK': 120, 'DEF': 65, 'SPATK': 45, 'SPDEF': 85, 'SPE': 125},
            "types": {"dark", "ice"},
            "movepool" : {"Night Slash", "Ice Shard", "Ice Punch", "Brick Break", "X-Scissor"}}
miloBase = {"name": "Milotic",
            "baseStats": {'HP': 95, 'ATK': 60, 'DEF': 79, 'SPATK': 100, 'SPDEF': 125, 'SPE': 81},
            "types": {"water"},
            "movepool" : {"Dragon Pulse", "Scald", "Hydro Pump", "Ice Beam"}}
apeBase = {"name": "Infernape",
            "baseStats": {'HP': 76, 'ATK': 104, 'DEF': 71, 'SPATK': 104, 'SPDEF': 71, 'SPE': 108},
            "types": {"fire", "fighting"},
            "movepool" : {"Acrobatics", "Brick Break", "Focus Blast", "Rock Slide", "Earthquake", "Flamethrow", "Fire Blast", "Thunder Punch", "Stone Edge"}}
laxBase = {"name": "Snorlax",
            "baseStats": {'HP': 160, 'ATK': 110, 'DEF': 65, 'SPATK': 65, 'SPDEF': 110, 'SPE': 30},
            "types": {"normal"},
            "movepool" : {"Body Slam", "Brick Break", "Crunch", "Iron Head", "Rock Slide", "Thunder Punch"}}
magBase = {"name": "Magnezone",
            "baseStats": {'HP': 70, 'ATK': 70, 'DEF': 115, 'SPATK': 130, 'SPDEF': 90, 'SPE': 60},
            "types": {"electric", "steel"},
            "movepool" : {"Thunderbolt", "Flash Cannon", "Tri Attack", "Body Press"}}
gardBase = {"name": "Gardevoir",
            "baseStats": {'HP': 68, 'ATK': 65, 'DEF': 65, 'SPATK': 125, 'SPDEF': 115, 'SPE': 80},
            "types": {"psychic"},
            "movepool" : {"Psychic", "Shadow Ball", "Energy Ball", "Focus Blast", "Thunderbolt"}}

#Monsters to be put in teams
tar = Monster(tyrantBase, 
                  {'HP': 252, 'ATK': 252, 'DEF': 0, 'SPATK': 4, 'SPDEF': 0, 'SPE': 0}, 
                  [['Crunch', 24], ['Stone Edge', 8], ['Dragon Claw', 24], ['Ice Beam', 16]])
volc = Monster(volcBase, 
                {'HP': 0, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 4, 'SPE': 252}, 
                [['Psychic', 16], ['Bug Buzz', 16], ['Fire Blast', 8], ['Hurricane', 16]])
drag = Monster(dragoniteBase, 
                {'HP': 4, 'ATK': 252, 'DEF': 0, 'SPATK': 0, 'SPDEF': 0, 'SPE': 252}, 
                [['Dragon Claw', 24], ['Extreme Speed', 8], ['Iron Head', 24], ['Earthquake', 16]])
keld = Monster(keldBase, 
                  {'HP': 4, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 0, 'SPE': 252}, 
                  [['Secret Sword', 16], ['Hydro Pump', 8], ['Icy Wind', 24], ['Scald', 24]])
chomp = Monster(chompBase, 
                  {'HP': 4, 'ATK': 252, 'DEF': 0, 'SPATK': 0, 'SPDEF': 0, 'SPE': 252}, 
                  [['Dragon Claw', 24], ['Earthquake', 16], ['Fire Blast', 8], ['Stone Edge', 8]])
gar = Monster(garBase, 
                {'HP': 0, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 4, 'SPE': 252}, 
                [['Focus Blast', 8], ['Shadow Ball', 24], ['Energy Ball', 16], ['Sludge Bomb', 16]])
sciz = Monster(scizBase, 
                  {'HP': 252, 'ATK': 252, 'DEF': 4, 'SPATK': 0, 'SPDEF': 0, 'SPE': 0}, 
                  [['Bullet Punch', 48], ['X-Scissor', 24], ['Acrobatics', 24], ['Night Slash', 24]])
kiss = Monster(kissBase, 
                  {'HP': 125, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 125, 'SPE': 6}, 
                  [['Air Slash', 32], ['Tri Attack', 16], ['Shadow Ball', 24], ['Flamethrower', 24]])
scept = Monster(sceptBase, 
                {'HP': 0, 'ATK': 125, 'DEF': 0, 'SPATK': 131, 'SPDEF': 0, 'SPE': 252}, 
                [['Rock Slide', 16], ['Dragon Pulse', 16], ['Energy Ball', 16], ['Earthquake', 16]])
weav = Monster(weavBase, 
                {'HP': 0, 'ATK': 252, 'DEF': 125, 'SPATK': 252, 'SPDEF': 125, 'SPE': 6}, 
                [['Night Slash', 24], ['Brick Break', 24], ['Ice Shard', 48], ['Ice Punch', 24]])
milo = Monster(miloBase, 
                  {'HP': 6, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 0, 'SPE': 0}, 
                  [['Ice Beam', 16], ['Hydro Pump', 8], ['Dragon Pulse', 16], ['Scald', 24]])
ape = Monster(apeBase, 
                {'HP': 0, 'ATK': 125, 'DEF': 0, 'SPATK': 131, 'SPDEF': 0, 'SPE': 252}, 
                [['Rock Slide', 16], ['Focus Blast', 8], ['Acrobatics', 24], ['Flamethrower', 24]])
lax = Monster(laxBase, 
                  {'HP': 125, 'ATK': 252, 'DEF': 6, 'SPATK': 0, 'SPDEF': 125, 'SPE': 0}, 
                  [['Crunch', 24], ['Body Slam', 24], ['Earthquake', 16], ['Iron Head', 24]])
mag = Monster(magBase, 
                {'HP': 6, 'ATK': 0, 'DEF': 252, 'SPATK': 252, 'SPDEF': 0, 'SPE': 0}, 
                [['Flash Cannon', 16], ['Thunderbolt', 24], ['Body Press', 16], ['Tri Attack', 16]])
gard = Monster(gardBase, 
                {'HP': 0, 'ATK': 0, 'DEF': 0, 'SPATK': 252, 'SPDEF': 4, 'SPE': 252}, 
                [['Psychic', 16], ['Focus Blast', 8], ['Shadow Ball', 24], ['Energy Ball', 16]])


#Teams to be battled with, last element represents number of pokemon alive
cynthia = [milo, kiss, chomp, 3]
wunner = [drag, gar, lax, 3]
fwg = [scept, ape, keld, 3]
circle = [mag, tar, gard, 3]
binary = [weav, volc, sciz, 3]

#list of all teams and a string to print them with
teamTuples = [("Cynthia Redux" , cynthia), ("Kanto Purist", wunner), ("FWG", fwg), ("Circle of Life", circle), ("Binary", binary)]
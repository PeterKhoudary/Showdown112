class Move():
    def __init__(self, name, type, BP, accuracy, startPP, attacking, defending, priority):
        self.name = name
        self.type = type
        self.power = BP
        self.accuracy = accuracy
        self.PP = startPP
        self.uses = attacking
        self.hits = defending
        self.priority = priority
    
    def __str__(self):
        return self.name

#List of available moves-
dragonClaw = Move("Dragon Claw", "dragon", 80, 1, 24, "ATK", "DEF", 0)
extremeSpeed = Move("Extreme Speed", "normal", 80, 1, 8, "ATK", "DEF", 2)
earthquake = Move("Earthquake", "ground", 100, 1, 16, "ATK", "DEF", 0)
iceBeam = Move("Ice Beam", "ice", 95, 1, 16, "SPATK", "SPDEF", 0)
fireBlast = Move("Fire Blast", "fire", 120, .85, 8, "SPATK", "SPDEF", 0)
bugBuzz = Move("Bug Buzz", "bug", 90, 1, 16, "SPATK", "SPDEF", 0)
hurricane = Move("Hurricane", "flying", 120, .7, 16, "SPATK", "SPDEF", 0)
psychic = Move("Psychic", "psychic", 90, 1, 16, "SPATK", "SPDEF", 1)
scald = Move("Scald", "water", 80, 1, 24, "SPATK", "SPDEF", 0)
secretSword = Move("Secret Sword", "fighting", 85, 1, 16, "SPATK", "DEF", 0)
hydroPump = Move("Hydro Pump", "water", 120, .8, 8, "SPATK", "SPDEF", 0)
icyWind = Move("Icy Wind", "ice", 55, .95, 24, "SPATK", "SPDEF", 0)
crunch = Move("Crunch", "dark", 80, 1, 24, "ATK", "DEF", 0)
stoneEdge = Move("Stone Edge", "rock",  100, .8, 8, "ATK", "DEF", 0)
bodySlam = Move("Body Slam", "normal", 85, .100, 24, "ATK", "DEF", 0)
ironHead = Move("Iron Head", "steel", 80, 1, 24, "ATK", "DEF", 0)

moveNames = {"Dragon Claw": dragonClaw, "Extreme Speed": extremeSpeed,
             "Earthquake": earthquake, "Ice Beam": iceBeam,
             "Fire Blast": fireBlast, "Bug Buzz": bugBuzz,
             "Hurricane": hurricane, "Psychic": psychic,
             "Scald": scald, "Secret Sword": secretSword,
             "Hydro Pump": hydroPump, "Icy Wind": icyWind,
             "Crunch": crunch, "Stone Edge": stoneEdge,
             "Body Slam": bodySlam, "Iron Head": ironHead}

#Type chart
resists = {"fire" : {"fire", "grass", "ice", "bug", "steel"},
           "bug": {"grass", "fighting", "ground"},
           "dragon": {"fire", "water", "grass", "electric"},
           "flying": {"grass", "fighting", "bug"},
           "normal": {},
           "water": {"water", "fire", "ice", "steel"},
           "grass": {"grass", "water", "electric"},
           "electric": {"electric", "steel"},
           "ice": {"ice"},
           "fighting": {"rock", "bug", "dark"},
           "poison": {"grass", "fighting", "poison", "bug"},
           "ground": {"poison", "rock"},
           "psychic": {"fighting", "psychic"},
           "rock": {"normal", "fire", "poison", "flying"},
           "ghost": {"poison", "bug"},
           "dark": {"ghost", "dark"},
           "steel": {"normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel"}}

weaknesses = {"fire" : {"water", "ground", "rock"},
           "bug": {"fire", "flying", "rock"},
           "dragon": {"dragon", "ice"},
           "flying": {"electric", "ice", "rock"},
           "normal": {"fighting"},
           "water": {"electric", "grass"},
           "grass": {"fire", "bug", "flying", "ice", "poison"},
           "electric": {"ground"},
           "ice": {"fire", "fighting", "rock", "steel"},
           "fighting": {"psychic", "flying"},
           "poison": {"psychic", "ground"},
           "ground": {"water", "grass", "ice"},
           "psychic": {"dark", "ghost", "bug"},
           "rock": {"water", "grass", "steel", "fighting", "ground"},
           "ghost": {"dark", "ghost"},
           "dark": {"bug", "fighting"},
           "steel": {"fighting", "ground", "fire"}}

immunities = {"fire" : {},
           "bug": {},
           "dragon": {},
           "flying": {"ground"},
           "normal": {"ghost"},
           "water": {},
           "grass": {},
           "electric": {},
           "ice": {},
           "fighting": {},
           "poison": {},
           "ground": {"electric"},
           "psychic": {},
           "rock": {},
           "ghost": {"normal", "fighting"},
           "dark": {"psychic"},
           "steel": {"poison"}}

moveColors = {"fire" : "red",
           "bug": "green yellow",
           "dragon": "medium slate blue",
           "flying": "deep sky blue",
           "normal": "papaya whip",
           "water": "royal blue",
           "grass": "green",
           "electric": "gold",
           "ice": "light cyan",
           "fighting": "indian red",
           "poison": "dark magenta",
           "ground": "tan",
           "psychic": "Fuchsia",
           "rock": "saddle brown",
           "ghost": "indigo",
           "dark": "black",
           "steel": "dark grey"}
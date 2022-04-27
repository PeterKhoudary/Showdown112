Pokemon Showdown112!

Description: Pokemon Showdown112! is a Pokemon battling simulator based off the highly popular fanmade simulator https://play.pokemonshowdown.com/
Players can choose a team of three and fight an AI that employs minmaxing to play optimally.

How to run: The program uses local sprites in order to display the pokemon, so the app
will not run without downloading those. Simply go to https://drive.google.com/drive/folders/1t1X491t9ZCCIysRQ-u5M7NTeLGLBCfnl?usp=sharing
and download the folder. Put the contents of that folder in the same exact folder that all the other code is in.
Do not put it them a subfolder, drop them directly in the folder.
Once that is complete, and you have your modules installed, run animation.py and begin the game!

Modules: This program uses CMU_112_graphics, which is a .py responsible for graphics using pillow.
CMU_112_graphics comes with the code, but you will need to install pillow and requests should you not already have them.
Instructions on how to do so are provided from the 112 course website: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#installingModules

Shortcuts: There are no shortcut commands.

Sources for all images:
All sprites are from version 19.1 of Pokemon essentials, a fanmade utility to help other fans make their own pokemon games.
Link: https://reliccastle.com/essentials/

End screen pngs
"You Win": https://toppng.com/photo/184796
"You Lose": http://pixelartmaker.com/art/8d3202a41dfe82e

The mode backgrounds come from Pokemon Showdown's website, but here are specific links:
"harmonica.jpg"/help background: https://play.pokemonshowdown.com/fx/client-bg-horizon.jpg
"shaymins.jpg"/team select background: https://play.pokemonshowdown.com/fx/client-bg-shaymin.jpg
"ocean.png"/mode select background: https://www.deviantart.com/quanyails/art/Sunrise-Ocean-402667154

The starry background for the actual battle comes from pokemon Rejuvenation/Reborn, two highly popular fangames that also employ
pokemon essentials material. I ripped this image from the wiki
"starlight.png" : https://static.wikia.nocookie.net/pokemon-reborn/images/6/60/Starlight_Arena_.jpg/revision/latest?cb=20200921184011

Title screen
pokemon logo : https://pngset.com/download-free-png-meqdo
The artwork is the official box art for Pokemon Mystery Dungeon: Explorers of Sky, which is a real pokemon game. I got this image
from a reddit post
"pmd.png" : https://www.reddit.com/r/MysteryDungeon/comments/g3e65s/pokemon_mystery_dungeon_explorers_of_sky_was/

Pokemon proprietary formulas: Both the formula for calculating damage and calculating final stats are pokemon unique things, so they must be directly taken.
Damage formula: https://bulbapedia.bulbagarden.net/wiki/Damage
Stat calculation formula: https://bulbapedia.bulbagarden.net/wiki/Stat

Other than roundHalfUp and almostEqual, which are both properly linked in the code itself, no code was directly taken for this
project, but a lot of pseudo code and just generally brainstorming was involved, so I am going to link anything that I looked at related
to this project.

https://www.cs.cmu.edu/~112/notes/student-tp-guides/GameAI.pdf
https://www.w3schools.com/colors/colors_names.asp
https://becominghuman.ai/minimax-or-maximin-8772fbd6d0c2
https://stackoverflow.com/questions/19431674/rounding-floats-to-nearest-10th
https://niklasriewald.com/2019/10/27/the-math-behind-competitive-pokemon-part-5-game-tree-pruning/
https://gamedev.stackexchange.com/questions/54703/minimax-where-bots-make-simultaneous-moves
https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Expectiminimax
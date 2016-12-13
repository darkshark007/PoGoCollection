import moves

class Species:
    def __init__(self, name):
        species_data = get_species_data_from_species(name)
        self.Name = species_data[SPECIES_KEYS.Name]
        self.Family = species_data[SPECIES_KEYS.Family]
        self.Id = species_data[SPECIES_KEYS.Id]
        self.HP = species_data[SPECIES_KEYS.HP]
        self.Attack = species_data[SPECIES_KEYS.Attack]
        self.Defense = species_data[SPECIES_KEYS.Defense]
        self.Min_CP = species_data[SPECIES_KEYS.Min_CP]
        self.Max_CP = species_data[SPECIES_KEYS.Max_CP]
        self.Type1 = species_data[SPECIES_KEYS.Type1]
        self.Type2 = species_data[SPECIES_KEYS.Type2]
        self.Evolves_Into = species_data[SPECIES_KEYS.Evolves_Into]
        self.Evolves_From = species_data[SPECIES_KEYS.Evolves_From]
        self.Quick_Moves = species_data[SPECIES_KEYS.Quick_Moves]
        self.Charge_Moves = species_data[SPECIES_KEYS.Charge_Moves]


    @staticmethod
    def _get_species_from_species_name(name):
        spc = Species()


class SPECIES_KEYS:
    Name = 0
    Family = 1
    Id = 2
    HP = 3
    Attack = 4
    Defense = 5
    Min_CP = 6 # Values are Outdated
    Max_CP = 7
    Type1 = 8
    Type2 = 9
    Evolves_Into = 10
    Evolves_From = 11
    Quick_Moves = 12
    Charge_Moves = 13


# Adapted from the spreadsheet
RAW_SPECIES_DATA = [
    # Assumed to be sorted by PKID
    ["Bulbasaur",1,1,90,118,118,838,981,"Grass","Poison",["Ivysaur"],"",["Vine Whip", "Tackle"],["Sludge Bomb", "Power Whip", "Seed Bomb"]],
    ["Ivysaur",1,2,120,151,151,1342,1552,"Grass","Poison",["Venusaur"],"Bulbasaur",["Vine Whip", "Razor Leaf"],["Solar Beam", "Sludge Bomb", "Power Whip"]],
    ["Venusaur",1,3,160,198,198,2212,2568,"Grass","Poison",[""],"Ivysaur",["Vine Whip", "Razor Leaf"],["Solar Beam", "Petal Blizzard", "Sludge Bomb"]],
    ["Charmander",4,4,78,116,96,734,831,"Fire","",["Charmeleon"],"",["Scratch", "Ember"],["Flamethrower", "Flame Burst", "Flame Charge"]],
    ["Charmeleon",4,5,116,158,129,1273,1484,"Fire","",["Charizard"],"Charmander",["Scratch", "Ember"],["Flamethrower", "Fire Punch", "Flame Burst"]],
    ["Charizard",4,6,156,223,176,2231,2686,"Fire","Flying",[""],"Charmeleon",["Wing Attack", "Ember"],["Fire Blast", "Flamethrower", "Dragon Claw"]],
    ["Squirtle",7,7,88,94,122,782,808,"Water","",["Wartortle"],"",["Bubble", "Tackle"],["Aqua Tail", "Aqua Jet", "Water Pulse"]],
    ["Wartortle",7,8,118,126,155,1296,1324,"Water","",["Blastoise"],"Squirtle",["Water Gun", "Bite"],["Hydro Pump", "Ice Beam", "Aqua Jet"]],
    ["Blastoise",7,9,158,171,210,2176,2291,"Water","",[""],"Wartortle",["Water Gun", "Bite"],["Hydro Pump", "Ice Beam", "Flash Cannon"]],
    ["Caterpie",10,10,90,55,62,298,393,"Bug","",["Metapod"],"",["Bug Bite", "Tackle"],["Struggle"]],
    ["Metapod",10,11,100,45,94,324,419,"Bug","",["Butterfree"],"Caterpie",["Bug Bite", "Tackle"],["Struggle"]],
    ["Butterfree",10,12,120,167,151,1182,1701,"Bug","Flying",[""],"Metapod",["Bug Bite", "Confusion"],["Bug Buzz", "Psychic", "Signal Beam"]],
    ["Weedle",13,13,80,63,55,304,397,"Bug","Poison",["Kakuna"],"",["Bug Bite", "Poison Sting"],["Struggle"]],
    ["Kakuna",13,14,90,46,86,333,392,"Bug","Poison",["Beedrill"],"Weedle",["Bug Bite", "Poison Sting"],["Struggle"]],
    ["Beedrill",13,15,130,169,150,1169,1777,"Bug","Poison",[""],"Kakuna",["Bug Bite", "Poison Jab"],["Sludge Bomb", "X-Scissor", "Aerial Ace"]],
    ["Pidgey",16,16,80,85,76,498,580,"Normal","Flying",["Pidgeotto"],"",["Tackle", "Quick Attack"],["Twister", "Aerial Ace", "Air Cutter"]],
    ["Pidgeotto",16,17,126,117,108,976,1085,"Normal","Flying",["Pidgeot"],"Pidgey",["Wing Attack", "Steel Wing"],["Twister", "Aerial Ace", "Air Cutter"]],
    ["Pidgeot",16,18,166,166,157,1763,1994,"Normal","Flying",[""],"Nidorino",["Wing Attack", "Steel Wing"],["Hurricane", "Aerial Ace", "Air Cutter"]],
    ["Rattata",19,19,60,103,70,413,588,"Normal","",["Raticate"],"",["Tackle", "Quick Attack"],["Body Slam", "Hyper Fang", "Dig"]],
    ["Raticate",19,20,110,161,144,1171,1549,"Normal","",[""],"Rattata",["Bite", "Quick Attack"],["Hyper Beam", "Hyper Fang", "Dig"]],
    ["Spearow",21,21,80,112,61,503,673,"Normal","Flying",["Fearow"],"",["Peck", "Quick Attack"],["Drill Peck", "Aerial Ace", "Twister"]],
    ["Fearow",21,22,130,182,135,1446,1814,"Normal","Flying",[""],"Spearow",["Steel Wing", "Peck"],["Drill Run", "Aerial Ace", "Twister"]],
    ["Ekans",23,23,70,110,102,619,778,"Poison","",["Arbok"],"",["Poison Sting", "Acid"],["Sludge Bomb", "Gunk Shot", "Wrap"]],
    ["Arbok",23,24,120,167,158,1463,1737,"Poison","",[""],"Ekans",["Bite", "Acid"],["Gunk Shot", "Sludge Wave", "Dark Pulse"]],
    ["Pikachu",25,25,70,112,101,673,787,"Electric","",["Raichu"],"",["Thunder Shock", "Quick Attack"],["Thunder", "Thunderbolt", "Discharge"]],
    ["Raichu",25,26,120,193,165,1698,2025,"Electric","",[""],"Pikachu",["Spark", "Thunder Shock"],["Thunder", "Thunder Punch", "Brick Break"]],
    ["Sandshrew",27,27,100,126,145,600,1194,"Ground","",["Sandslash"],"",["Mud Shot", "Scratch"],["Dig", "Rock Slide", "Rock Tomb"]],
    ["Sandslash",27,28,150,182,202,1505,2328,"Ground","",[""],"Sandshrew",["Mud Shot", "Metal Claw"],["Earthquake", "Rock Tomb", "Bulldoze"]],
    ["Nidoran F",29,29,110,86,94,668,736,"Poison","",["Nidorina"],"",["Poison Sting", "Bite"],["Sludge Bomb", "Body Slam", "Poison Fang"]],
    ["Nidorina",29,30,140,117,126,1138,1218,"Poison","",["Nidoqueen"],"Nidoran F",["Poison Sting", "Bite"],["Sludge Bomb", "Poison Fang", "Dig"]],
    ["Nidoqueen",29,31,180,180,174,2125,2338,"Poison","Ground",[""],"Nidorina",["Poison Jab", "Bite"],["Earthquake", "Stone Edge", "Sludge Wave"]],
    ["Nidoran M",32,32,92,105,76,639,739,"Poison","",["Nidorino"],"",["Poison Sting", "Peck"],["Sludge Bomb", "Body Slam", "Horn Attack"]],
    ["Nidorino",32,33,122,137,112,1108,1252,"Poison","",["Nidoking"],"Nidoran M",["Poison Sting", "Poison Jab"],["Sludge Bomb", "Horn Attack", "Dig"]],
    ["Nidoking",32,34,162,204,157,2114,2386,"Poison","Ground",[""],"Nidorino",["Poison Jab", "Fury Cutter"],["Earthquake", "Megahorn", "Sludge Wave"]],
    ["Clefairy",35,35,140,107,116,955,1085,"Normal","",["Clefable"],"",["Pound", "Zen Headbutt"],["Moonblast", "Body Slam", "Disarming Voice"]],
    ["Clefable",35,36,190,178,171,2045,2353,"Normal","",[""],"Clefairy",["Pound", "Zen Headbutt"],["Moonblast", "Psychic", "Dazzling Gleam"]],
    ["Vulpix",37,37,76,96,122,627,774,"Fire","",["Ninetales"],"",["Ember", "Quick Attack"],["Flamethrower", "Body Slam", "Flame Charge"]],
    ["Ninetales",37,38,146,169,204,1850,2157,"Fire","",[""],"Vulpix",["Ember", "Feint Attack"],["Fire Blast", "Flamethrower", "Heat Wave"]],
    ["Jigglypuff",39,39,230,80,44,682,713,"Normal","",["Wigglytuff"],"",["Pound", "Feint Attack"],["Body Slam", "Play Rough", "Disarming Voice", "Dazzling Gleam"]],
    ["Wigglytuff",39,40,280,156,93,1825,1906,"Normal","",[""],"Jigglypuff",["Pound", "Feint Attack"],["Hyper Beam", "Play Rough", "Dazzling Gleam"]],
    ["Zubat",41,41,80,83,76,466,569,"Poison","Flying",["Golbat"],"",["Bite", "Quick Attack"],["Sludge Bomb", "Poison Fang", "Air Cutter"]],
    ["Golbat",41,42,150,161,153,1607,1830,"Poison","Flying",[""],"Zubat",["Wing Attack", "Bite"],["Poison Fang", "Air Cutter", "Ominous Wind"]],
    ["Oddish",43,43,90,131,116,905,1069,"Grass","Poison",["Gloom"],"",["Razor Leaf", "Acid"],["Sludge Bomb", "Seed Bomb", "Moonblast"]],
    ["Gloom",43,44,120,153,139,1393,1512,"Grass","Poison",["Vileplume"],"Oddish",["Razor Leaf", "Acid"],["Petal Blizzard", "Sludge Bomb", "Moonblast"]],
    ["Vileplume",43,45,150,202,170,2130,2367,"Grass","Poison",[""],"Gloom",["Acid", "Razor Leaf"],["Solar Beam", "Petal Blizzard", "Moonblast"]],
    ["Paras",46,46,70,121,99,698,836,"Bug","Grass",["Parasect"],"Paras",["Bug Bite", "Scratch"],["Seed Bomb", "X-Scissor", "Cross Poison"]],
    ["Parasect",46,47,120,165,146,1445,1657,"Bug","Grass",[""],"Paras",["Bug Bite", "Fury Cutter"],["Solar Beam", "X-Scissor", "Cross Poison"]],
    ["Venonat",48,48,120,100,102,803,902,"Bug","Poison",["Venomoth"],"",["Bug Bite", "Confusion"],["Signal Beam", "Poison Fang", "Psybeam"]],
    ["Venomoth",48,49,140,179,150,1577,1937,"Bug","Poison",[""],"Venonat",["Bug Bite", "Confusion"],["Bug Buzz", "Psychic", "Poison Fang"]],
    ["Diglett",50,50,20,109,88,280,465,"Ground","",["Dugtrio"],"",["Mud Slap", "Mud Shot", "Scratch"],["Dig", "Mud Bomb", "Rock Tomb"]],
    ["Dugtrio",50,51,70,167,147,915,1333,"Ground","",[""],"Diglett",["Mud Shot", "Mud Slap", "Sucker Punch"],["Earthquake", "Stone Edge", "Mud Bomb"]],
    ["Meowth",52,52,80,92,81,563,638,"Normal","",["Persian"],"",["Scratch", "Bite"],["Body Slam", "Night Slash", "Dark Pulse"]],
    ["Persian",52,53,130,150,139,1342,1539,"Normal","",[""],"Meowth",["Scratch", "Feint Attack"],["Play Rough", "Night Slash", "Power Gem"]],
    ["Psyduck",54,54,100,122,96,873,966,"Water","",["Golduck"],"",["Water Gun", "Zen Headbutt"],["Cross Chop", "Aqua Tail", "Psybeam"]],
    ["Golduck",54,55,160,191,163,2033,2270,"Water","",[""],"Psyduck",["Water Gun", "Confusion"],["Hydro Pump", "Psychic", "Ice Beam"]],
    ["Mankey",56,56,80,148,87,668,1002,"Fighting","",["Primeape"],"",["Scratch", "Karate Chop"],["Cross Chop", "Brick Break", "Low Sweep"]],
    ["Primeape",56,57,130,207,144,1552,2105,"Fighting","",[""],"Mankey",["Low Kick", "Karate Chop"],["Cross Chop", "Low Sweep", "Night Slash"]],
    ["Growlithe",58,58,110,136,96,1072,1110,"Fire","",["Arcanine"],"",["Bite", "Ember"],["Flamethrower", "Body Slam", "Flame Wheel"]],
    ["Arcanine",58,59,180,227,166,2586,2839,"Fire","",[""],"Growlithe",["Fire Fang", "Bite"],["Fire Blast", "Flamethrower", "Bulldoze"]],
    ["Poliwag",60,60,80,101,82,597,695,"Water","",["Poliwhirl"],"",["Bubble", "Mud Shot"],["Body Slam", "Bubble Beam", "Mud Bomb"]],
    ["Poliwhirl",60,61,130,130,130,1080,1313,"Water","",["Poliwrath"],"Poliwag",["Bubble", "Mud Shot"],["Scald", "Mud Bomb", "Bubble Beam"]],
    ["Poliwrath",60,62,180,182,187,2144,2441,"Water","Fighting",[""],"Poliwhirl",["Bubble", "Mud Shot"],["Hydro Pump", "Submission", "Ice Punch"]],
    ["Abra",63,63,50,195,103,424,1148,"Psychic","",["Kadabra"],"Abra",["Zen Headbutt"],["Psyshock", "Signal Beam", "Shadow Ball"]],
    ["Kadabra",63,64,80,232,138,887,1859,"Psychic","",["Alakazam"],"Abra",["Psycho Cut", "Confusion"],["Psybeam", "Dazzling Gleam", "Shadow Ball"]],
    ["Alakazam",63,65,110,271,194,1502,2887,"Psychic","",[""],"Kadabra",["Psycho Cut", "Confusion"],["Psychic", "Dazzling Gleam", "Shadow Ball"]],
    ["Machop",66,66,140,137,88,854,1199,"Fighting","",["Machoke"],"",["Low Kick", "Karate Chop"],["Cross Chop", "Brick Break", "Low Sweep"]],
    ["Machoke",66,67,160,177,130,1460,1910,"Fighting","",["Machamp"],"Machop",["Low Kick", "Karate Chop"],["Cross Chop", "Brick Break", "Submission"]],
    ["Machamp",66,68,180,234,162,2226,2889,"Fighting","",[""],"Machoke",["Karate Chop", "Bullet Punch"],["Cross Chop", "Stone Edge", "Submission"]],
    ["Bellsprout",69,69,100,139,64,872,916,"Grass","Poison",["Weepinbell"],"",["Vine Whip", "Acid"],["Sludge Bomb", "Power Whip", "Wrap"]],
    ["Weepinbell",69,70,130,172,95,1419,1475,"Grass","Poison",["Victreebel"],"Bellsprout",["Razor Leaf", "Acid"],["Sludge Bomb", "Power Whip", "Seed Bomb"]],
    ["Victreebel",69,71,160,207,138,2162,2268,"Grass","Poison",[""],"Weepinbell",["Acid", "Razor Leaf"],["Solar Beam", "Sludge Bomb", "Leaf Blade"]],
    ["Tentacool",72,72,80,97,182,691,956,"Water","Poison",["Tentacruel"],"",["Bubble", "Poison Sting"],["Bubble Beam", "Water Pulse", "Wrap"]],
    ["Tentacruel",72,73,160,166,237,1880,2374,"Water","Poison",[""],"Tentacool",["Poison Jab", "Acid"],["Hydro Pump", "Blizzard", "Sludge Wave"]],
    ["Geodude",74,74,80,132,163,643,1193,"Rock","Ground",["Graveler"],"",["Rock Throw", "Tackle"],["Rock Slide", "Dig", "Rock Tomb"]],
    ["Graveler",74,75,110,164,196,1162,1815,"Rock","Ground",["Golem"],"Geodude",["Mud Shot", "Mud Slap", "Rock Throw"],["Stone Edge", "Rock Slide", "Dig"]],
    ["Golem",74,76,160,211,229,1957,2916,"Rock","Ground",[""],"Graveler",["Mud Shot", "Mud Slap", "Rock Throw"],["Earthquake", "Stone Edge", "Ancient Power"]],
    ["Ponyta",77,77,100,170,132,1233,1502,"Fire","",["Rapidash"],"",["Ember", "Tackle"],["Fire Blast", "Flame Charge", "Flame Wheel"]],
    ["Rapidash",77,78,130,207,167,1857,2252,"Fire","",[""],"Ponyta",["Ember", "Low Kick"],["Fire Blast", "Heat Wave", "Drill Run"]],
    ["Slowpoke",79,79,180,109,109,967,1204,"Water","Psychic",["Slowbro"],"",["Water Gun", "Confusion"],["Psychic", "Psyshock", "Water Pulse"]],
    ["Slowbro",79,80,190,177,194,2229,2482,"Water","Psychic",[""],"Slowpoke",["Water Gun", "Confusion"],["Psychic", "Ice Beam", "Water Pulse"]],
    ["Magnemite",81,81,50,165,128,664,1083,"Electric","Steel",["Magneton"],"",["Spark", "Thunder Shock"],["Thunderbolt", "Discharge", "Magnet Bomb"]],
    ["Magneton",81,82,100,223,182,1559,2237,"Electric","Steel",[""],"Magnemite",["Spark", "Thunder Shock"],["Flash Cannon", "Discharge", "Magnet Bomb"]],
    ["Farfetch'd",83,83,104,124,118,1010,1092,"Normal","Flying",[""],"",["Cut", "Fury Cutter"],["Leaf Blade", "Aerial Ace", "Air Cutter"]],
    ["Doduo",84,84,70,158,88,645,1011,"Normal","Flying",["Dodrio"],"",["Peck", "Quick Attack"],["Drill Peck", "Aerial Ace", "Swift"]],
    ["Dodrio",84,85,120,218,145,1525,2138,"Normal","Flying",[""],"Doduo",["Feint Attack", "Steel Wing"],["Drill Peck", "Aerial Ace", "Air Cutter"]],
    ["Seel",86,86,130,85,128,870,899,"Water","",["Dewgong"],"",["Water Gun", "Lick", "Ice Shard"],["Aqua Tail", "Aqua Jet", "Icy Wind"]],
    ["Dewgong",86,87,180,139,184,1811,1894,"Water","Ice",[""],"Seel",["Frost Breath", "Ice Shard"],["Blizzard", "Icy Wind", "Aqua Jet"]],
    ["Grimer",88,88,160,135,90,1027,1269,"Poison","",["Muk"],"",["Poison Jab", "Acid", "Mud Slap"],["Sludge Bomb", "Mud Bomb"]],
    ["Muk",88,89,210,190,184,2234,2709,"Poison","",[""],"Grimer",["Poison Jab", "Acid", "Lick"],["Gunk Shot", "Sludge Wave", "Dark Pulse"]],
    ["Shellder",90,90,60,116,168,614,958,"Water","",["Cloyster"],"",["Tackle", "Ice Shard"],["Water Pulse", "Bubble Beam", "Icy Wind"]],
    ["Cloyster",90,91,100,186,323,1714,2475,"Water","Ice",[""],"Shellder",["Frost Breath", "Ice Shard"],["Blizzard", "Hydro Pump", "Icy Wind"]],
    ["Gastly",92,92,60,186,70,596,1002,"Ghost","Poison",["Haunter"],"",["Lick", "Sucker Punch"],["Sludge Bomb", "Ominous Wind", "Dark Pulse"]],
    ["Haunter",92,93,90,223,112,1107,1716,"Ghost","Poison",["Gengar"],"Gastly",["Shadow Claw", "Lick"],["Sludge Bomb", "Shadow Ball", "Dark Pulse"]],
    ["Gengar",92,94,120,261,156,1743,2619,"Ghost","Poison",[""],"Haunter",["Shadow Claw", "Sucker Punch"],["Sludge Bomb", "Sludge Wave", "Shadow Ball", "Dark Pulse"]],
    ["Onix",95,95,70,85,288,641,1002,"Rock","Ground",[""],"",["Rock Throw", "Tackle"],["Stone Edge", "Rock Slide", "Iron Head"]],
    ["Drowzee",96,96,120,89,158,842,992,"Psychic","",["Hypno"],"",["Pound", "Confusion"],["Psychic", "Psyshock", "Psybeam"]],
    ["Hypno",96,97,170,144,215,1847,2048,"Psychic","",[""],"Drowzee",["Zen Headbutt", "Confusion"],["Psychic", "Psyshock", "Shadow Ball"]],
    ["Krabby",98,98,60,181,156,589,1386,"Water","",["Kingler"],"",["Bubble", "Mud Shot"],["Vice Grip", "Bubble Beam", "Water Pulse"]],
    ["Kingler",98,99,110,240,214,1511,2694,"Water","",[""],"Krabby",["Metal Claw", "Mud Shot"],["X-Scissor", "Vice Grip", "Water Pulse"]],
    ["Voltorb",100,100,80,109,114,635,857,"Electric","",["Electrode"],"",["Spark", "Tackle"],["Thunderbolt", "Discharge", "Signal Beam"]],
    ["Electrode",100,101,120,173,179,1354,1900,"Electric","",[""],"Voltorb",["Spark", "Tackle"],["Thunderbolt", "Hyper Beam", "Discharge"]],
    ["Exeggcute",102,102,120,107,140,865,1102,"Grass","Psychic",["Exeggutor"],"",["Confusion"],["Psychic", "Seed Bomb", "Ancient Power"]],
    ["Exeggutor",102,103,190,233,158,2558,2916,"Grass","Psychic",[""],"Exeggcute",["Zen Headbutt", "Confusion"],["Solar Beam", "Psychic", "Seed Bomb"]],
    ["Cubone",104,104,100,90,165,780,943,"Ground","",["Marowak"],"",["Mud Slap", "Rock Smash"],["Bone Club", "Dig", "Bulldoze"]],
    ["Marowak",104,105,120,144,200,1361,1691,"Ground","",[""],"Cubone",["Mud Slap", "Rock Smash"],["Earthquake", "Bone Club", "Dig"]],
    ["Hitmonlee",106,106,100,224,211,1212,2406,"Fighting","",[""],"",["Rock Smash", "Low Kick"],["Stone Edge", "Brick Break", "Low Sweep", "Stomp"]],
    ["Hitmonchan",107,107,100,193,212,1231,2098,"Fighting","",[""],"",["Rock Smash", "Bullet Punch"],["Brick Break", "Thunder Punch", "Fire Punch", "Ice Punch"]],
    ["Lickitung",108,108,180,108,137,1336,1322,"Normal","",[""],"",["Lick", "Zen Headbutt"],["Hyper Beam", "Power Whip", "Stomp"]],
    ["Koffing",109,109,80,119,164,905,1091,"Poison","",["Weezing"],"",["Acid", "Tackle"],["Sludge Bomb", "Dark Pulse"]],
    ["Weezing",109,110,130,174,221,1904,2183,"Poison","",[""],"Koffing",["Acid", "Tackle"],["Sludge Bomb", "Shadow Ball", "Dark Pulse"]],
    ["Rhyhorn",111,111,160,140,157,936,1679,"Ground","Rock",["Rhydon"],"",["Mud Slap", "Rock Smash"],["Bulldoze", "Horn Attack", "Stomp"]],
    ["Rhydon",111,112,210,222,206,1900,3300,"Ground","Rock",[""],"Rhyhorn",["Mud Slap", "Rock Smash"],["Stone Edge", "Earthquake", "Megahorn"]],
    ["Chansey",113,113,500,60,176,433,1469,"Normal","",[""],"",["Pound", "Zen Headbutt"],["Hyper Beam", "Psychic", "Psybeam", "Dazzling Gleam"]],
    ["Tangela",114,114,130,183,205,1440,2208,"Grass","",[""],"",["Vine Whip"],["Solar Beam", "Power Whip", "Sludge Bomb"]],
    ["Kangaskhan",115,115,210,181,165,1715,2463,"Normal","",[""],"",["Mud Slap", "Low Kick"],["Earthquake", "Stomp", "Brick Break"]],
    ["Horsea",116,116,60,129,125,590,921,"Water","",["Seadra"],"",["Water Gun", "Bubble"],["Dragon Pulse", "Bubble Beam", "Flash Cannon"]],
    ["Seadra",116,117,110,187,182,1412,1979,"Water","",[""],"Horsea",["Water Gun", "Dragon Breath"],["Hydro Pump", "Blizzard", "Dragon Pulse"]],
    ["Goldeen",118,118,90,123,115,745,1006,"Water","",["Seaking"],"",["Mud Shot", "Peck"],["Aqua Tail", "Water Pulse", "Horn Attack"]],
    ["Seaking",118,119,160,175,154,1719,2040,"Water","",[""],"Goldeen",["Poison Jab", "Peck"],["Megahorn", "Drill Run", "Icy Wind"]],
    ["Staryu",120,120,60,137,112,712,926,"Water","",["Starmie"],"",["Water Gun", "Tackle", "Quick Attack"],["Swift", "Bubble Beam", "Power Gem"]],
    ["Starmie",120,121,120,210,184,1839,2303,"Water","Psychic",[""],"Staryu",["Water Gun", "Tackle", "Quick Attack"],["Hydro Pump", "Psychic", "Power Gem", "Psybeam"]],
    ["Mr. Mime",122,122,80,192,233,1204,1984,"Psychic","",[""],"",["Zen Headbutt", "Confusion"],["Psychic", "Psybeam", "Shadow Ball"]],
    ["Scyther",123,123,140,218,170,1745,2464,"Bug","Flying",[""],"",["Fury Cutter", "Steel Wing"],["Bug Buzz", "X-Scissor", "Night Slash"]],
    ["Jynx",124,124,130,223,182,1418,2512,"Ice","Psychic",[""],"",["Frost Breath", "Pound"],["Psyshock", "Ice Punch", "Draining Kiss"]],
    ["Electabuzz",125,125,130,198,173,1784,2196,"Electric","",[""],"",["Thunder Shock", "Low Kick"],["Thunder", "Thunderbolt", "Thunder Punch"]],
    ["Magmar",126,126,130,206,169,1916,2254,"Fire","",[""],"",["Ember", "Karate Chop"],["Fire Blast", "Flamethrower", "Fire Punch"]],
    ["Pinsir",127,127,130,238,197,1787,2770,"Bug","",[""],"",["Fury Cutter", "Rock Smash"],["X-Scissor", "Submission", "Vice Grip"]],
    ["Tauros",128,128,150,198,197,1536,2488,"Normal","",[""],"",["Tackle", "Zen Headbutt"],["Earthquake", "Horn Attack", "Iron Head"]],
    ["Magikarp",129,129,40,29,102,152,220,"Water","",["Gyarados"],"",["Splash"],["Struggle"]],
    ["Gyarados",129,130,190,237,197,2314,3281,"Water","Flying",[""],"Magikarp",["Dragon Breath", "Bite"],["Hydro Pump", "Dragon Pulse", "Twister"]],
    ["Lapras",131,131,260,186,190,2582,2980,"Water","Ice",[""],"",["Frost Breath", "Ice Shard"],["Blizzard", "Ice Beam", "Dragon Pulse"]],
    ["Ditto",132,132,96,91,91,706,718,"Normal","",[""],"",["Transform"],["Struggle"]],
    ["Eevee",133,133,110,104,121,845,969,"Normal","",["Vaporeon", "Jolteon", "Flareon"],"",["Tackle", "Quick Attack"],["Body Slam", "Dig", "Swift"]],
    ["Vaporeon",133,134,260,205,177,2428,3157,"Water","",[""],"Eevee",["Water Gun"],["Hydro Pump", "Aqua Tail", "Water Pulse"]],
    ["Jolteon",133,135,130,232,201,1804,2730,"Electric","",[""],"Eevee",["Thunder Shock"],["Thunder", "Thunderbolt", "Discharge"]],
    ["Flareon",133,136,130,246,204,2261,2904,"Fire","",[""],"Eevee",["Ember"],["Fire Blast", "Flamethrower", "Heat Wave"]],
    ["Porygon",137,137,130,153,139,1396,1567,"Normal","",[""],"",["Tackle", "Zen Headbutt", "Quick Attack"],["Psybeam", "Signal Beam", "Discharge"]],
    ["Omanyte",138,138,70,155,174,873,1345,"Rock","Water",["Omastar"],"",["Water Gun", "Mud Shot"],["Ancient Power", "Brine", "Rock Tomb"]],
    ["Omastar",138,139,140,207,227,1891,2685,"Rock","Water",[""],"Omanyte",["Water Gun", "Rock Throw", "Mud Shot"],["Hydro Pump", "Rock Slide", "Ancient Power"]],
    ["Kabuto",140,140,60,148,162,853,1172,"Rock","Water",["Kabutops"],"Kabuto",["Scratch", "Mud Shot"],["Ancient Power", "Aqua Jet", "Rock Tomb"]],
    ["Kabutops",140,141,120,220,203,1792,2517,"Rock","Water",[""],"Kabuto",["Mud Shot", "Fury Cutter"],["Stone Edge", "Water Pulse", "Ancient Power"]],
    ["Aerodactyl",142,142,160,221,164,1830,2608,"Rock","Flying",[""],"",["Bite", "Steel Wing"],["Hyper Beam", "Ancient Power", "Iron Head"]],
    ["Snorlax",143,143,320,190,190,2698,3355,"Normal","",[""],"",["Lick", "Zen Headbutt"],["Hyper Beam", "Body Slam", "Earthquake"]],
    ["Articuno",144,144,180,192,249,2581,2933,"Ice","Flying",[""],"",["Frost Breath"],["Blizzard", "Ice Beam", "Icy Wind"]],
    ["Zapdos",145,145,180,253,188,2708,3330,"Electric","Flying",[""],"",["Thunder Shock"],["Thunder", "Thunderbolt", "Discharge"]],
    ["Moltres",146,146,180,251,184,2824,3272,"Fire","Flying",[""],"",["Ember"],["Fire Blast", "Flamethrower", "Heat Wave"]],
    ["Dratini",147,147,82,119,94,759,860,"Dragon","",["Dragonair"],"",["Dragon Breath"],["Aqua Tail", "Wrap", "Twister"]],
    ["Dragonair",147,148,122,163,138,1446,1609,"Dragon","",["Dragonite"],"Dratini",["Dragon Breath"],["Dragon Pulse", "Aqua Tail", "Wrap"]],
    ["Dragonite",147,149,182,263,201,3067,3581,"Dragon","Flying",[""],"Dragonair",["Dragon Breath", "Steel Wing"],["Hyper Beam", "Dragon Pulse", "Dragon Claw"]],
    ["Mewtwo",150,150,212,330,200,3671,4760,"Psychic","",[""],"",["Psycho Cut", "Confusion"],["Hyper Beam", "Psychic", "Shadow Ball"]],
    ["Mew",151,151,200,210,210,2882,3090,"Psychic","",[""],"",["Pound"],["Solar Beam", "Blizzard", "Hyper Beam", "Psychic", "Fire Blast", "Earthquake", "Thunder", "Hurricane", "Moonblast", "Dragon Pulse"]],
]


def __VALIDATE_POKEMON_MOVES():
    #print("Validating pokemon moves...")
    for species in RAW_SPECIES_DATA:
        for qm in species[SPECIES_KEYS.Quick_Moves]:
            if moves._get_basic_move_by_name(qm) is None:
                print("Invalid move "+qm+" for PKMN "+species[SPECIES_KEYS.Name])
        for cm in species[SPECIES_KEYS.Charge_Moves]:
            if moves._get_charge_move_by_name(cm) is None:
                print("Invalid move "+cm+" for PKMN "+species[SPECIES_KEYS.Name])
__VALIDATE_POKEMON_MOVES()


def get_id_from_species(name):
    for species in RAW_SPECIES_DATA:
            if name.lower() == species[SPECIES_KEYS.Name].lower():
                return int(species[SPECIES_KEYS.Id])
    return -1


def get_species_data_from_species(name):
    return RAW_SPECIES_DATA[get_id_from_species(name)-1]


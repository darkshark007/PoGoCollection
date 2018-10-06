import pokemon as PK

# Read in Pokemon file
def read_pokemon_from_file(filename):
    pkList = []
    try:
        file_in = open(filename, 'r')
    except IOError:
        # File not found
        return

    for line in file_in:
        if line == "\n":
            continue

        # ---------- Output format ----------
        # Name, Species, CP, HP, Dust, Mv1, Mv2, Appraisal, BestStat, StatLevel, IVOpts, Strengths, Weaknesses
        split = line.strip().split(",")
        pkmn = PK.Pokemon()
        pkmn.name = split[0]
        pkmn.species = split[1]
        pkmn.cp = int(split[2])
        pkmn.hp = int(split[3])
        pkmn.dust = int(split[4])
        pkmn.move_one = split[5]
        pkmn.move_two = split[6]        
        pkmn.appraisal = int(split[7])
        pkmn.bestStat = int(split[8])
        pkmn.statLevel = int(split[9])
        if split[10] == "":
            pkmn.IVOptions = []
        else:
            pkmn.IVOptions = split[10].split(":")
        pkmn.minIV = int(split[11])
        pkmn.maxIV = int(split[12])
        pkmn.skin = split[13]

        # pkmn.calculate_iv_options() # Re-calculate IVs on read
        pkList.append(pkmn)
    file_in.close()
    return pkList


def write_pokemon_to_file(pkList, filename):
    try:
        file_out = open(filename, 'w')
    except IOError:
        # File not found
        return

    for pkmn in pkList:
        serial = ""
        serial += pkmn.name + ","
        serial += pkmn.species + ","
        serial += str(pkmn.cp) + ","
        serial += str(pkmn.hp) + ","
        serial += str(pkmn.dust) + ","
        serial += pkmn.move_one + ","
        serial += pkmn.move_two + ","
        serial += str(pkmn.appraisal) + ","
        serial += str(pkmn.bestStat) + ","
        serial += str(pkmn.statLevel) + ","
        serial += (":".join(pkmn.IVOptions)).strip() + ","
        serial += str(pkmn.minIV) + ","
        serial += str(pkmn.maxIV) + ","
        serial += pkmn.skin
        serial = serial.strip()
        file_out.write(serial+"\n")
    file_out.close()




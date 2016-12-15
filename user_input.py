import Data.species as Species
import Data.moves as Moves

consumable_input = []
def get_input(displayString):
    # Get input
    if len(consumable_input) == 0:
        inp = raw_input(displayString)
    else:
        inp = consumable_input.pop(0).strip()
        if inp == "pause":
            raw_input("Input paused.  Press Enter to continue\n>  ")
            return get_input(displayString)
        else:
            print(displayString+inp)

    # Convert to UTF-8
    # try:
    #     inp = unicodedata.normalize('NFKD', inp).encode('ascii','ignore')
    # except:
    #     pass

    return inp


def input_number(message, minVal=None, maxVal=None):
    """
    General input method for requesting an integer.  Validates input, rejects
    non-numeric values and optionally asserts minimum and maximum values.

    :param string message: The message displayed when prompting for input
    :param int minVal: The minimum accepted value for expected input
    :param int maxVal: The maximum accepted value for expected input
    """
    inp = get_input(message)
    try:
        val = int(inp)
        # TODO Check for floats?!  Input floats will be truncated unexpectedly
        if minVal != None and val < minVal:
            print("Value \'"+inp+"\' is too low")
            return input_number(message, minVal, maxVal)
        if maxVal != None and val > maxVal:
            print("Value \'"+inp+"\' is too high")
            return input_number(message, minVal, maxVal)
        return val
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_number(message, minVal, maxVal)


def input_float(message, minVal=None, maxVal=None):
    """
    General input method for requesting a float.  Validates input, rejects
    non-numeric values and optionally asserts minimum and maximum values.

    :param string message: The message displayed when prompting for input
    :param int minVal: The minimum accepted value for expected input
    :param int maxVal: The maximum accepted value for expected input
    """
    inp = get_input(message)
    try:
        val = float(inp)
        if minVal != None and val < minVal:
            print("Number \'"+inp+"\' is too low")
            return input_float(message, minVal, maxVal)
        if maxVal != None and val > maxVal:
            print("Number \'"+inp+"\' is too high")
            return input_float(message, minVal, maxVal)
        return val
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_float(message, minVal, maxVal)


def input_tf(message):
    """
    General input method for requesting a boolean, or yes/no, value.  Validates
    input, rejects non-truthy values.

    :param string message: The message displayed when prompting for input
    """
    inp = get_input(message).lower()
    if inp == "y" or inp == "yes" or inp == "t" or inp == "true":
        return True
    elif inp == "n" or inp == "no" or inp == "f" or inp == "false":
        return False
    else:
        print("Invalid value \'"+inp+"\'")
        return input_tf(message)


def input_species():
    """ Specialized input method for requesting a Pokemon Species.  Validates input, rejects
    non-numeric values and optionally asserts minimum and maximum values.
    """
    inp = get_input("Species? (Name or ID)\n>  ")
    try:
        # Maybe they entered a number?
        inp_num = int(inp)
        if inp_num < 1 or inp_num > len(Species.RAW_SPECIES_DATA):
            print("Invalid Species ID #"+str(inp_num))
            return input_species()
        else:
            return Species.RAW_SPECIES_DATA[inp_num-1][Species.SPECIES_KEYS.Name]
    except ValueError:
        # Maybe they entered a name?
        inp_num = Species.get_id_from_species(inp)
        if inp_num == -1:
            print("Could not find Species Name or ID # for \'"+inp+"\'")
            print("Did you mean...")
            for species in Species.RAW_SPECIES_DATA:
                if fuzzy_string_search(inp.lower(), species[Species.SPECIES_KEYS.Name].lower()):
                    print("? ["+str(species[Species.SPECIES_KEYS.Id])+"] "+species[Species.SPECIES_KEYS.Name])
            print("\n")
            return input_species()
        else:
            return Species.RAW_SPECIES_DATA[inp_num-1][Species.SPECIES_KEYS.Name]


def input_cp():
    inp = input_number("CP?\n>  ")
    if inp < 10:
        print("CP value \'"+str(inp)+"\' is too low!")
        return input_cp()
    else:
        return inp


def input_hp():
    inp = get_input("HP?\n>  ")
    try:
        inp = int(inp)
        if inp < 10:
            print("HP value \'"+str(inp)+"\' is too low!")
            return input_hp()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_hp()


VALID_DUST_VALUES = [200,400,600,800,1000,1300,1600,1900,2200,2500,3000,3500,4000,4500,5000,6000,7000,8000,9000,10000]
LEVELS_FOR_DUST_VALUES = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39]
def input_dust():
    inp = get_input("Stardust cost?\n>  ")
    try:
        inp = int(inp)
        if inp not in VALID_DUST_VALUES:
            print("Stardust cost value \'"+str(inp)+"\' is not valid!")
            return input_dust()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_dust()


def input_quick_move():
    inp = get_input("Quick Move?\n>  ")
    for mv in Moves.BASIC_MOVE_DATA:
        if inp.lower() == mv[Moves.BASIC_MOVE.Name].lower():
            return mv[Moves.BASIC_MOVE.Name]
    # Couldn't find it
    print("Could not identify quick move \'"+inp+"\'")
    print("Did you mean...")
    for mv in Moves.BASIC_MOVE_DATA:
        if fuzzy_string_search(inp.lower(), mv[Moves.BASIC_MOVE.Name].lower()):
            print("? "+mv[Moves.BASIC_MOVE.Name])
    print("\n")
    return input_quick_move()


def input_charge_move():
    inp = get_input("Charge Move?\n>  ")
    for mv in Moves.CHARGE_MOVE_DATA:
        if inp.lower() == mv[Moves.CHARGE_MOVE.Name].lower():
            return mv[Moves.CHARGE_MOVE.Name]
    # Couldn't find it
    print("Could not identify charge move \'"+inp+"\'")
    print("Did you mean...")
    for mv in Moves.CHARGE_MOVE_DATA:
        if fuzzy_string_search(inp.lower(), mv[Moves.CHARGE_MOVE.Name].lower()):
            print("? "+mv[Moves.CHARGE_MOVE.Name])
    print("\n")
    return input_charge_move()

def input_appraisal():
    inp = get_input(\
"""
Appraisal?
  [0]  0% -  49% ( 0 - 22 pts)
  [1] 50% -  65% (23 - 29 pts)
  [2] 66% -  80% (30 - 36 pts)
  [3] 81% - 100% (37 - 45 pts)
> """)
    try:
        inp = int(inp)
        if inp < 0 or inp > 3:
            print("Appraisal value \'"+str(inp)+"\' is not valid! (Should be between 0-3)")
            return input_appraisal()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_appraisal()    


def input_bestStat():
    inp = get_input(\
"""
Highest Stat?
  [0] Attack
  [1] Defence
  [2] HP
  [3] Attack + Defence
  [4] HP + Defence
  [5] HP + Attack
  [6] HP + Attack + Defence
> """)
    try:
        inp = int(inp)
        if inp < 0 or inp > 6:
            print("Highest Stat value \'"+str(inp)+"\' is not valid! (Should be between 0-6)")
            return input_bestStat()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_bestStat()    

def input_stat_level():
    inp = get_input(\
"""
Best-Stat Level?
  [0]  0 -  7
  [1]  8 - 12
  [2] 13 - 14
  [3] 15
> """)
    try:
        inp = int(inp)
        if inp < 0 or inp > 3:
            print("Best-Stat level value \'"+str(inp)+"\' is not valid! (Should be between 0-3)")
            return input_stat_level()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_stat_level()    


def input_type():
    inp = get_input("Type?\n>  ").lower()
    if inp in TYPE_ADVANTAGE_KEYS:
        return inp
    else:
        print("Invalid Pokemon Type \'"+inp+"\'")
        return input_type()


def input_pkmn_list_index(max_value):
    inp = get_input("Idx? \n>  ")
    try:
        inp = int(inp)
        if inp >= max_value or inp < -1:
            print("Index value \'"+str(inp)+"\' is not valid! (Should be between 0-"+str(max_value-1)+", or -1 to cancel)")
            return input_pkmn_list_index(max_value)
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_pkmn_list_index(max_value)


def input_pkmn_list_index_list(max_value):
    inp = get_input("Comma-separated Idx List?\n>  ")
    inp = inp.split(",")
    try:
        for i in range(len(inp)):
            inp[i] = int(inp[i].strip())
            if inp[i] >= max_value or inp[i] < -1:
                print("Index value \'"+str(inp[i])+"\' is not valid! (Should be between 0-"+str(max_value-1)+", or -1 to cancel)")
                return input_pkmn_list_index_list(max_value)
        return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_pkmn_list_index_list(max_value)    


def input_remember_setting():
    inp = get_input("Remember this value? (y/n)\n>  ").lower()
    if inp != "y" and inp != "n":
        print("Invalid value \'"+inp+"\'")
        return input_remember_setting()
    else:
        return inp


def input_ascending_descending():
    inp = get_input("ascending/descending order? (a/d)\n>  ").lower()
    if inp != "a" and inp != "d":
        print("Invalid value \'"+inp+"\'")
        return input_ascending_descending()
    else:
        return inp



def fuzzy_string_search(inp, within, fuzz=5):
    if inp in within:
        return True
    for i in range(len(inp)-(fuzz-1)):
        if inp[i:i+fuzz] in within:
            return True
    return False

from ctypes import Structure, py_object, c_bool
import math
from multiprocessing import Process, Queue
import os
import platform
import sys
import thread
import time
import unicodedata

import user_input as UInp
import file_io as fio
import Data.species as Species
import Data.moves as Moves
import pokemon as PK


filter_interface = """
Select Filter or Sort:
  [x] CLEAR ACTIVE FILTERS

  Filter by:
    [fs]  Species Name
    [ff]  Species Family
    [f-]  Min CP
    [f+]  Max CP
    [f>]  Strong against #Imp
    [f<]  Weak against #Imp
    [fm+] Filter out Non-Marked
    [fm-] Filter out Marked

  Sort by:
    [sn]  Name
    [ss]  Species #Imp
    [sc]  CP
    [si+] Max IVs #Imp
    [si-] Min IVs #Imp
> """
gym_builder_interface = """
Gym Builder:
  [a]  Add Pokemon to Gym
  [e]  Edit Pokemon in Gym
  [r]  Remove Pokemon from Gym

  [t]  Find counters for specific Pokemon
  [b]  Build counter teams

  [x]  Exit
> """

pkmnList = []
filteredList = pkmnList
currentFilter = ""
savedViews = []

should_show = {
    'Idx':         [True,  4],
    'Nickname':    [True, 12],
    'Species':     [True, 16],
    'CP':          [True,  4],
    'IVs':         [True,  5, 5, 6],
    'Move1':       [True, 22],
    'Move2':       [True, 22],
    'Mark':        [True,  35],
    'Skin':        [True, 20],
    'Move_Score':  [False, 5],
}
def list_pokemon():

    def pad_left(inp, length):
        ret = inp
        if len(ret) < length:
            ret = " "*(length-len(ret))+ret
        return ret

    def pad_right(inp, length):
        ret = inp
        if len(ret) < length:
            ret = ret+" "*(length-len(ret))
        return ret

    def pad_center(inp, length):
        ret = inp
        while length - len(ret) >= 2:
            ret = " "+ret+" "
        while length - len(ret) >= 1:
            ret = ret+" "
        return ret

    apply_active_filters()
    title_string = ""
    divider_string = ""
    if should_show['Idx'][0]:
        title_string += pad_center('Idx', should_show['Idx'][1])+" | "
        divider_string += "-"*should_show['Idx'][1]+"-:-"
    if should_show['Nickname'][0]:
        title_string += pad_center('Nickname', should_show['Nickname'][1])+" | "
        divider_string += "-"*should_show['Nickname'][1]+"-:-"
    if should_show['Species'][0]:
        title_string += pad_center('Species', should_show['Species'][1])+" | "
        divider_string += "-"*should_show['Species'][1]+"-:-"
    if should_show['CP'][0]:
        title_string += pad_center('CP', should_show['CP'][1])+" | "
        divider_string += "-"*should_show['CP'][1]+"-:-"
    if should_show['IVs'][0]:
        title_string += pad_center('IVs', should_show['IVs'][1]+should_show['IVs'][2]+should_show['IVs'][3]+4)+" | "
        divider_string += "-"*(should_show['IVs'][1]+should_show['IVs'][2]+should_show['IVs'][3]+4)+"-:-"
    if should_show['Move1'][0]:
        title_string += pad_center('Basic Move', should_show['Move1'][1])+" | "
        divider_string += "-"*should_show['Move1'][1]+"-:-"
    if should_show['Move2'][0]:
        title_string += pad_center('Charge Move', should_show['Move2'][1])+" | "
        divider_string += "-"*should_show['Move2'][1]+"-:-"
    if should_show['Mark'][0]:
        title_string += pad_center('Marks', should_show['Mark'][1])+" | "
        divider_string += "-"*should_show['Mark'][1]+"-:-"
    if should_show['Skin'][0]:
        title_string += pad_center('Skin', should_show['Skin'][1])+" | "
        divider_string += "-"*should_show['Skin'][1]+"-:-"
    if should_show['Move_Score'][0]:
        title_string += pad_center('Score', should_show['Move_Score'][1])+" | "
        divider_string += "-"*should_show['Move_Score'][1]+"-:-"
    print(title_string)
    print(divider_string)
    # TODO List IVs?
    for idx, pkmn in enumerate(filteredList):
        species = Species.Species(pkmn.species)
        # Idx  | Nickname     | Species      | CP
        printString = ""

        # Print Index
        if should_show['Idx'][0]:
            printString += pad_left(str(idx), should_show['Idx'][1])+" | "

        # Print Nickname
        if should_show['Nickname'][0]:
            printString += pad_right(pkmn.name, should_show['Nickname'][1])+" | "

        # Print Species
        if should_show['Species'][0]:
            tempString = pad_right(pkmn.species, should_show['Species'][1])
            if pkmn.skin is not "":
                tempString = bcolors.Cyan+tempString+bcolors.Clear
            printString += tempString+" | "

        # Print CP
        if should_show['CP'][0]:
            printString += pad_left(str(pkmn.cp), should_show['CP'][1])+" | "

        # Print IVs
        if should_show['IVs'][0]:
            item1 = pad_left(str(int(pkmn.minIV/0.045)/10.0), should_show['IVs'][1])
            item2 = "   "+pad_left("", should_show['IVs'][2])
            item3 = " "+pad_left("", should_show['IVs'][3])
            if len(pkmn.IVOptions) != 1:
                item2 = " - "+pad_left(str(int(pkmn.maxIV/0.045)/10.0), should_show['IVs'][2])
                item3 = " "+pad_left("("+str(len(pkmn.IVOptions))+")", should_show['IVs'][3])
            printString += item1+item2+item3+" | "

        # Print Basic Move
        if should_show['Move1'][0]:
            moveString = pad_left(pkmn.move_one, should_show['Move1'][1])
            if (not (pkmn.move_one in species.Quick_Moves)):
                moveString = bcolors.Orange+moveString+bcolors.Clear
            printString += moveString+" | "

        # Print Charge Move
        if should_show['Move2'][0]:
            moveString = pad_left(pkmn.move_two, should_show['Move1'][1])
            if (not (pkmn.move_two in species.Charge_Moves)):
                moveString = bcolors.Orange+moveString+bcolors.Clear
            printString += moveString+" | "

        # Print Mark
        if should_show['Mark'][0]:
            printString += pad_left(str(pkmn.marks), should_show['Mark'][1])+" | "

        # Print Skin
        if should_show['Skin'][0]:
            printString += pad_right(str(pkmn.skin), should_show['Skin'][1])+" | "

        # Print Move_Score
        if should_show['Move_Score'][0]:
            payload = pkmn.calculate_type_advantages()
            printString += pad_right(str(round(1000*payload['max_score'])/1000), should_show['Move_Score'][1])+" | "

        print(printString)    


def run():
    interface = """
Select Command:
  Pokemon Management functions:
    [a] Add Pokemon
    [e] Edit Pokemon
    [d] Delete Pokemon
    [l] List Pokemon

  Analysis functions
    [m] Mark Pokemon
    [f] Filter list
    [b] Build Gym

  Other
    [i] Input Command String
    [x] Exit
> """
    global pkmnList
    global filteredList
    global currentFilter
    while True:
        cmd = UInp.get_input(interface).lower()

        clear_screen()

        # Add Pokemon
        if cmd == "a":
            print("Adding new pokemon to the Collection")
            pkmn = PK.Pokemon()
            pkmn.name = UInp.get_input("Pokemon Nickname?\n>  ")
            pkmn.species = UInp.input_species()
            if pkmn.name[0] == "$":
                pkmn.name = pkmn.name[1:10000]
                pkmn.skin = UInp.get_input("Skin?\n>  ")
            pkmn.cp = UInp.input_cp()
            pkmn.hp = UInp.input_hp()
            pkmn.dust = UInp.input_dust()
            pkmn.move_one = UInp.input_quick_move()
            pkmn.move_two = UInp.input_charge_move()
            pkmn.appraisal = UInp.input_appraisal()
            pkmn.bestStat = UInp.input_bestStat()
            pkmn.statLevel = UInp.input_stat_level()
            print("\n")
            pkmn.calculate_iv_options()
            pkmnList.append(pkmn)
            write_pokemon_collection()
            apply_active_filters()
            try:
                idx = filteredList.index(pkmn)
            except ValueError:
                idx = -1
            print("Created new "+pkmn.species+" (Idx #"+str(idx)+")")

        # Edit Pokemon
        elif cmd == "e":
            print("Select a Pokemon to Edit:")
            list_pokemon()
            filteredIdxList = UInp.input_pkmn_list_index(len(filteredList))            
            pkmn = filteredList[filteredIdxList]
            clear_screen()
            run_edit_pokemon(pkmn)
            print("\n")
            pkmn.calculate_iv_options(False)
            write_pokemon_collection()
            print("Updated "+pkmn.species)

        # Mark Pokemon
        elif cmd == "m":
            run_mark_pokemon()

        # Delete Pokemon
        elif cmd == "d":
            list_pokemon()
            filteredIdxList = UInp.input_pkmn_list_index_list(len(filteredList))
            filteredIdxList.sort(reverse=True)
            for i in range(len(filteredIdxList)):
                filteredIdx = filteredIdxList[i]
                if filteredIdx == -1:
                    clear_screen()                
                    break;
                else:
                    pkmn = filteredList[filteredIdx]
                    listIdx = pkmnList.index(pkmn)
                    del pkmnList[listIdx]
                    if pkmnList is not filteredList:
                        del filteredList[filteredIdx]
                    print("Deleted pokemon #"+str(filteredIdx)+" "+pkmn.name+" ("+pkmn.species+")")
            write_pokemon_collection()

        # Build Gym
        elif cmd == "b":
            clear_screen()
            isFriendlyGym = UInp.input_tf("Friendly Gym?\n> ")
            gymList = []
            while True:
                count = 0
                print("\n\nGym Pokemon:")
                for pk in gymList:
                    print("  ["+str(count)+"] "+pk.species+", "+str(pk.cp)+" cp   ("+pk.move_one+"/"+pk.move_two+")")
                    count += 1
                print("")
                cmd = UInp.get_input(gym_builder_interface).lower()
                if cmd == "a":
                    pkmn = PK.Pokemon()
                    pkmn.species = UInp.input_species()
                    pkmn.cp = UInp.input_cp()
                    pkmn.IVOptions = []
                    pkmn.calculate_iv_options(False)
                    gymList.append(pkmn)
                    gymList.sort(key=lambda pk: (pk.cp))                    


                elif cmd == "e":
                    if len(gymList) == 0:
                        print("No pokemon to edit!")
                        continue
                    idx = UInp.input_number("Idx? \n>  ",0,(len(gymList)-1))
                    pkmn = gymList[idx]
                    run_edit_pokemon(pkmn)
                    pkmn.IVOptions = []
                    print("\n")
                    pkmn.calculate_iv_options(False)
                    print("Updated "+pkmn.species)

                elif cmd == "r":
                    print("")

                elif cmd == "t":
                    if len(gymList) == 0:
                        print("No pokemon to find!")
                        continue
                    idx = UInp.input_number("Idx? (-1 for all)\n>  ",-1,(len(gymList)-1))
                    min_value = UInp.input_float("Minimum attacker score?\n> ", 0, None)
                    if isFriendlyGym:
                        max_CP = UInp.input_number("Maximum CP?\n> ",10)
                    print('\n\n')
                    if idx == -1:
                        pkList = gymList
                    else:
                        pkList = [gymList[idx]]
                    for pkmn in pkList:
                        print("Gym Pokemon:  "+pkmn.species+", "+str(pkmn.cp)+" cp   ("+pkmn.move_one+"/"+pkmn.move_two+")")
                        print("Effective Counters:")
                        counters = []
                        for pk in pkmnList:
                            result = PK.Pokemon.calculate_gym_attack_score_for_combatants(pk,pkmn)
                            score = result['gym_score']
                            shouldAdd = False
                            if score >= min_value:
                                if isFriendlyGym and pk.cp > max_CP:
                                    continue
                                score = round(score * 1000)/1000
                                entry = {
                                    'pk': pk,
                                    'result': result,
                                    'score': score,
                                }
                                counters.append(entry)

                        counters.sort(key=lambda ct: (ct['score']), reverse=True)
                        min_cp = 10000
                        print_count = 0
                        for ct in counters:
                            pk = ct['pk']
                            score = ct['score']
                            color = bcolors.Lime+bcolors.Bold

                            # Pruning
                            if isFriendlyGym:
                                if print_count > 10:
                                    break

                                if pk.cp > int(pkmn.cp*0.5):
                                    if (pk.cp*0.9) > min_cp:
                                        continue
                                    else:
                                        min_cp = pk.cp
                                else:
                                    min_cp = pk.cp
                                    print_count += 1
                            else:
                                if print_count > 10:
                                    break
                                else:
                                    print_count += 1

                            if isFriendlyGym:
                                if pk.cp > int(pkmn.cp*1.5):
                                    continue
                                elif pk.cp > int(pkmn.cp*1.0):
                                    color = bcolors.Red
                                elif pk.cp > int(pkmn.cp*0.75):
                                    color = bcolors.Orange
                                elif pk.cp > int(pkmn.cp*0.5):
                                    color = bcolors.Gold
                            weave = "Weave"
                            if ct['result']['atk_noweave_dmg'] > ct['result']['atk_weave_dmg']:
                                weave = "No-Weave"

                            print(color+"  "+str(score)+" -- "+pk.name+" ("+pk.species+")  "+str(pk.cp)+"cp  "+str(pk.hp)+"hp  "+pk.move_one+"/"+pk.move_two+" ("+weave+")"+bcolors.Clear)
                        print("\n\n")


                elif cmd == "b":
                    print("")

                elif cmd == "x":
                    break
    
                else:
                    print("Gym Builder Command \'"+cmd+"\' not recognized")


        # List Pokemon
        elif cmd == "l":
            list_pokemon()

        # Filter list
        elif cmd == "f":
            cmd = UInp.get_input(filter_interface).lower()
            if cmd == "x": # CLEAR FILTERS
                print("List Filters Cleared")
                currentFilter = ""

            # Filters
            elif cmd == "fs": # Filter by Species
                currentFilter += "species"
            elif cmd == "ff": # Filter by Species
                currentFilter += "family"
            elif cmd == "f-": # Filter by Min CP
                currentFilter += "minCP"
            elif cmd == "f+": # Filter by Max CP
                currentFilter += "maxCP"
            elif cmd == "f>": # Filter by Species
                currentFilter += "strong" # TODO Implement
            elif cmd == "f<": # Filter by Species
                currentFilter += "weak" # TODO Implement
            elif cmd == "fm+": # Filter by Species
                currentFilter += "marked"
            elif cmd == "fm-": # Filter by Species
                currentFilter += "nonmarked"

            # Sorts
            elif cmd == "sn": # Sort by Name
                currentFilter += "sortName"
            elif cmd == "sc": # Sort by CP
                currentFilter += "sortCP"
            elif cmd == "si-": # Sort by Min IVs
                currentFilter += "sortMinIV"
            elif cmd == "si+": # Sort by Max IVs
                currentFilter += "sortMaxIV"

            else:
                print("Filter Command \'"+cmd+"\' not recognized")
            
            apply_active_filters()
            # print("CFilt: "+currentFilter)


        # Input commands
        elif cmd == "i":
            inp = UInp.get_input("Semi-colon separated user inputs\n> ")
            append_input = inp.split(";")
            # TODO Make this an API method instead of a direct mutation after the refactor
            UInp.consumable_input.extend(append_input)

        # Exit
        elif cmd == "x":
            sys.exit(0)

        # Command not found
        else:
            print("Command \'"+cmd+"\' not found.\n")

def run_mark_pokemon():
    mark_pokemon_interface = """
Mark:
  [i]    List of Pokemon from filtered list by Index
  [k]    Pokemon with Skins
  [l]    Pokemon at a specific level
  [n]    Pokemon with given name
  [s]    Pokemon of a particular species
  [cp]   N Highest CP Pokemon
  [in]   N Highest IV's per Species and/or Moveset
  [iv]   Pokemon at or above a specific IV, in points [0-45]
  [em]   Max Evolved Pokemon
  [gc]   Top-Scoring Gym Combatants
  [leg]  Pokemon with legacy movesets
  [mvt]  Moves of the same type + type advantage
  [lgdy] Legendary Pokemon

Modifiers:
  [!]  Negate Mark criteria
  [^]  Flip Mark result
  [%]  Use filtered list instead of full list to apply Marks

  [x]  Clear Markers
> """
    cmd = UInp.get_input(mark_pokemon_interface).lower()

    # Allow all mark commands to be negatable
    negate = False
    flip = False
    mark_list = pkmnList
    if '!' in cmd:
        negate = True
        cmd = cmd.replace('!', '')
    if '^' in cmd:
        flip = True
        cmd = cmd.replace('^', '')
    if '%' in cmd:
        mark_list = filteredList
        cmd = cmd.replace('%', '')

    pkList = []
    for pkmn in mark_list:
        pkList.append(pkmn)


    def mark_pokemon(pkmn, result):
        # print("Marking "+pkmn.name+" ("+pkmn.species+") "+str(pkmn.cp)+"cp == "+str(result))
        if flip:
            if result is True and negate is False:
                if mark_name in pkmn.marks:
                    pkmn.marks.remove(mark_name)
            if result is True and negate is True:
                return # Dont mark false
            if result is False and negate is True:
                if mark_name in pkmn.marks:
                    pkmn.marks.remove(mark_name)
            if result is False and negate is False:
                return # Dont mark false
        else:
            if result is True and negate is False:
                pkmn.marks.append(mark_name)
            if result is True and negate is True:
                return # Dont mark false
            if result is False and negate is True:
                pkmn.marks.append(mark_name)
            if result is False and negate is False:
                return # Dont mark false

    if cmd == "x":
        mark_name = UInp.get_input("Mark Name? (Or blank for all marks)\n> ")
        if mark_name is "":
            for pkmn in pkList:
                pkmn.marks = []
        else:
            for pkmn in pkList:
                while mark_name in pkmn.marks:
                    pkmn.marks.remove(mark_name)
        return

    mark_name = UInp.get_input("Mark Name?\n> ")

    if cmd == "i":
        list_pokemon()
        filteredIdxList = UInp.input_pkmn_list_index_list(len(filteredList))
        for idx in filteredIdxList:
            mark_pokemon(filteredList[idx],True)

    elif cmd == "l":
        lvlMin = UInp.input_float("Min Level?\n>  ",1, 40.5)
        lvlMax = UInp.input_float("Max Level?  (0 for non-range)\n>  ",0, 40.5)
        for pkmn in pkList:
            min_level = pkmn.get_min_level()
            max_level = pkmn.get_max_level()
            if lvlMax == 0 and lvlMin >= min_level and lvlMin <= max_level:
                mark_pokemon(pkmn,True)
            elif lvlMax != 0 and ((lvlMin >= min_level and lvlMin <= max_level) or (lvlMax >= min_level and lvlMax <= max_level)):
                mark_pokemon(pkmn,True)
            else:
                mark_pokemon(pkmn,False)

    elif cmd == "k":
        for pkmn in pkList:
            if pkmn.skin != "":
                mark_pokemon(pkmn,True)
            else:
                mark_pokemon(pkmn,False)

    elif cmd == "n":
        inp_name = UInp.get_input("Name?\n>  ")
        for pkmn in pkList:
            if pkmn.name == inp_name:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "s":
        inp_species = UInp.input_species()
        for pkmn in pkList:
            if pkmn.species == inp_species:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "in":
        inp_N = UInp.input_number("N?\n> ")
        inp_family = UInp.input_tf("Per family?\n>  ")
        inp_moveset = UInp.input_tf("Per moveset?\n>  ")
        inp_skin = UInp.input_tf("Per skin?\n>  ")
        # Construct the IV list
        pk_sets = {}

        # Loop and break the list into sets
        for pkmn in pkList:
            species = Species.Species(pkmn.species)
            if inp_family:
                key = str(species.Family)
            else:
                key = str(species.Id)
            if inp_moveset:
                key += "-"+pkmn.move_one+"-"+pkmn.move_two
            if inp_skin:
                if pkmn.skin is not "":
                    key += "-"+pkmn.skin
            try:
                pk_sets[key].append(pkmn)
            except KeyError:
                pk_sets[key] = [pkmn]

        # Iterate over the sets and mark the N highest IV ones
        for key in pk_sets:
            pk_set = pk_sets[key]
            pk_set.sort(key=lambda pk: (pk.minIV), reverse=True)
            if len(pk_set) >= inp_N:
                score = pk_set[inp_N-1].minIV
            else:
                score = pk_set[-1].minIV

            for pkmn in pk_set:
                if pkmn.maxIV >= score:
                    mark_pokemon(pkmn, True)
                else:
                    mark_pokemon(pkmn, False)

    elif cmd == "iv":
        inp_minIV = UInp.input_number("IV level, in points? [0-45]\n>  ", 0, 45)
        for pkmn in pkList:
            if pkmn.minIV >= inp_minIV:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "cp":
        # OLD
        # inp_N = UInp.input_number("N?\n>  ",1)
        # # TODO: Refactor to be per species/per moveset
        # # inp_species = UInp.input_tf("Per species?\n>  ")
        # pkList.sort(key=lambda pk: (pk.cp), reverse=True)
        # count = 0
        # for pkmn in pkList:
        #     if count < inp_N:
        #         mark_pokemon(pkmn, True)
        #     else:
        #         mark_pokemon(pkmn, False)
        #     count += 1
        # List is assumed to be always sorted by CP, which it should be.
        inp_N = UInp.input_number("N?\n>  ",1)
        inp_species = UInp.input_tf("Per species?\n>  ")
        inp_moveset = False
        if inp_species:
            inp_moveset = UInp.input_tf("Per moveset?\n>  ")
        pkList.sort(key=lambda pk: (pk.cp), reverse=True)
        if inp_species:
            pkList.sort(key=lambda pk: (Species.get_id_from_species(pk.species)))
        if inp_moveset:
            pkList.sort(key=lambda pk: (pk.move_one))
            pkList.sort(key=lambda pk: (pk.move_two))

        key = "NONE"
        count = 0
        for pkmn in pkList:
            curr_key = "K"
            if inp_species:
                curr_key += "-"+pkmn.species
            if inp_moveset:
                curr_key += "-"+pkmn.move_one+"/"+pkmn.move_two
            if curr_key != key:
                count = 0
                key = curr_key
            if count < inp_N:
                mark_pokemon(pkmn, True)
                count += 1
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "em":
        for pkmn in pkList:
            species = Species.Species(pkmn.species)
            if species.Evolves_Into[0] == "":
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "leg":
        inp_effective = UInp.input_tf("Type-Effective Moves?\n>  ")
        # inp_effective = False
        # f;x;m;x;;m;leg;leg;n;f;fm+;leg;n;m;leg;test;y;l
        for pkmn in pkList:
            # print("Checking "+pkmn.name+"/"+pkmn.species+"/"+str(pkmn.cp)+"/"+str(pkmn.hp))
            species = Species.Species(pkmn.species)
            mv1_legacy = not (pkmn.move_one in species.Quick_Moves)
            mv1Data = Moves._get_basic_move_by_name(pkmn.move_one)
            if mv1_legacy and inp_effective:
                # print("  Move 1 is legacy ")
                mv1_legacy = False
                mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
                mv1STAB = 1.25 if mv1Type == species.Type1 or mv1Type == species.Type2 else 1.0
                for def_type1 in PK.TYPE_ADVANTAGE_KEYS:
                    for def_type2 in PK.TYPE_ADVANTAGE_KEYS:
                        if def_type1 == def_type2:
                            continue

                        # print("  Checking Types "+def_type1+"/"+def_type2)
                        ratio = mv1STAB

                        # Offensive Bonus
                        ratio = ratio * PK.get_ratio_from_types(mv1Type,def_type1)
                        ratio = ratio * PK.get_ratio_from_types(mv1Type,def_type2)

                        # Defensive Bonus
                        defense_ratio = 1.0
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type1)
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type2)
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type2, species.Type1)
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type2, species.Type2)

                        if ratio > 1.26 and defense_ratio <= 1.0:
                            # print("True!  >> "+str(ratio)+"/"+str(defense_ratio))
                            mv1_legacy = True

                        if mv1_legacy:
                            break

                    ratio = mv1STAB

                    # Offensive Bonus
                    ratio = ratio * PK.get_ratio_from_types(mv1Type,def_type1)

                    # Defensive Bonus
                    defense_ratio = 1.0
                    defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type1)
                    defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type2)

                    if ratio > 1.26 and defense_ratio <= 1.0:
                        mv1_legacy = True


                    if mv1_legacy:
                        break

            mv2_legacy = not (pkmn.move_two in species.Charge_Moves)
            mv2Data = Moves._get_charge_move_by_name(pkmn.move_two)
            if mv2_legacy and inp_effective:
                # print("  Move 2 is legacy ")
                mv2_legacy = False
                mv2Type = mv2Data[Moves.BASIC_MOVE.Type]
                mv2STAB = 1.25 if mv2Type == species.Type1 or mv2Type == species.Type2 else 1.0
                for def_type1 in PK.TYPE_ADVANTAGE_KEYS:
                    for def_type2 in PK.TYPE_ADVANTAGE_KEYS:
                        if def_type1 == def_type2:
                            continue

                        # print("  Checking Types "+def_type1+"/"+def_type2)
                        ratio = mv2STAB

                        # Offensive Bonus
                        ratio = ratio * PK.get_ratio_from_types(mv2Type,def_type1)
                        ratio = ratio * PK.get_ratio_from_types(mv2Type,def_type2)

                        # Defensive Bonus
                        defense_ratio = 1.0
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type1)
                        # print('>> '+str(defense_ratio))
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type2)
                        # print('>> '+str(defense_ratio))
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type2, species.Type1)
                        # print('>> '+str(defense_ratio))
                        defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type2, species.Type2)
                        # print('>> '+str(defense_ratio))

                        if ratio > 1.26 and defense_ratio <= 1.0:
                            # print("True!  >> "+str(ratio)+"/"+str(defense_ratio))
                            mv2_legacy = True

                        if mv2_legacy:
                            break

                    ratio = mv2STAB

                    # Offensive Bonus
                    ratio = ratio * PK.get_ratio_from_types(mv2Type,def_type1)

                    # Defensive Bonus
                    defense_ratio = 1.0
                    defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type1)
                    defense_ratio = defense_ratio * PK.get_ratio_from_types(def_type1, species.Type2)

                    if ratio > 1.26 and defense_ratio <= 1.0:
                        mv2_legacy = True

                    if mv2_legacy:
                        break


            if (mv1_legacy) or (mv2_legacy):
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "lgdy":
        for pkmn in pkList:
            species = Species.Species(pkmn.species)
            if (species.Id in Species.LEGENDARY_SPECIES_IDS):
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "mvt":
        for pkmn in pkList:
            species = Species.Species(pkmn.species)
            shouldMark = False
            mv1Data = Moves._get_basic_move_by_name(pkmn.move_one)
            mv1Type = mv1Data[Moves.BASIC_MOVE.Type].lower()
            mv2Data = Moves._get_charge_move_by_name(pkmn.move_two)
            mv2Type = mv2Data[Moves.CHARGE_MOVE.Type].lower()
            types_equal = mv1Type == mv2Type
            payload = pkmn.calculate_type_advantages()
            type_advantage = types_equal and payload["max_score"] > 1
            print(pkmn.name+"/"+pkmn.species+"/"+str(pkmn.cp)+"  "+str(types_equal)+"/"+str(type_advantage))
            if type_advantage:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "gc":

        class Battle_Worker(Process):
            def __init__(self):
                super(Battle_Worker, self).__init__()
                self.defender = None
                self.attackers = Queue(1)
                self.scores = Queue(1)
                self.ready = Queue(1)

            def run(self):
                defender = self.defender
                bestAttackers = [[],[],[],[]]
                bestScore = [-1, -1, -1, -1]
                for idx in range(len(pkList)):
                    attacker = pkList[idx]
                    score = PK.Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)['gym_score']
                    # Tier 0 - Half CP or less
                    if attacker.cp <= int(defender.cp*0.5):
                        if score > bestScore[0]:
                            bestAttackers[0] = []
                            bestAttackers[0].append(idx)
                            bestScore[0] = score
                        elif score == bestScore[0]:
                            bestAttackers[0].append(idx)
                            bestScore[0] = score
                    # Tier 1 - Three-quarters CP or less
                    if attacker.cp <= int(defender.cp*0.75):
                        if score > bestScore[1]:
                            bestAttackers[1] = []
                            bestAttackers[1].append(idx)
                            bestScore[1] = score
                        elif score == bestScore[1]:
                            bestAttackers[1].append(idx)
                            bestScore[1] = score
                    # Tier 2 - Same CP or less
                    if attacker.cp <= defender.cp:
                        if score > bestScore[2]:
                            bestAttackers[2] = []
                            bestAttackers[2].append(idx)
                            bestScore[2] = score
                        elif score == bestScore[2]:
                            bestAttackers[2].append(idx)
                            bestScore[2] = score
                    # Tier 3 - Any CP
                    if score > bestScore[3]:
                        bestAttackers[3] = []
                        bestAttackers[3].append(idx)
                        bestScore[3] = score
                    elif score == bestScore[3]:
                        bestAttackers[3].append(idx)
                        bestScore[3] = score

                self.attackers.put(bestAttackers)
                self.scores.put(bestScore)
                self.ready.put(True)


        fullList = fio.read_pokemon_from_file(GENERATED_POKEMON_FILE_FULL_CP_RANGE)
        results = []
        for i in range(len(fullList)+1):
            results.append(None)

        threads_available = 2
        thread_index = 0
        print_index = 0
        start_time = time.time()
        while True:

            # Print results so far
            printString = ""
            # print('Waiting')
            while results[print_index] != None and results[print_index].ready.full() == True:
                # print('Processing')
                res = results[print_index]
                defender = res.defender
                printString += "["+str(print_index)+"] Battling "+defender.species+" "+str(defender.cp)+"cp ("+defender.move_one+"/"+defender.move_two+")\n"
                if not res.attackers.full():
                    # Skip
                    results[print_index] = None
                    print_index += 1
                    continue
                ls = res.attackers.get()
                scores = res.scores.get()
                for tier in range(4):
                    for pkIdx in ls[tier]:
                        # TODO: Can I refactor this so it supports negation?  Combine all the tiers into one list and iterate over pkmnList, comparing to the built list?
                        pkmn = pkList[pkIdx]
                        pkmn.marks.append(mark_name)
                        printString += "  ["+str(tier)+"] "+pkmn.name+" ("+pkmn.species+") "+str(pkmn.cp)+"cp with a score of "+str(scores[tier])+"\n"

                # Discard
                res.join()
                results[print_index] = None
                print_index += 1
                threads_available += 1
            if printString != "":
                print(printString.strip())


            # Launch new Threads
            while threads_available > 0 and thread_index < len(fullList):
                # thread.start_new_thread(process_battle, (fullList[thread_index], thread_index, results))
                # Process(target=process_battle, args=(fullList[thread_index],thread_index, results[thread_index])).start()
                worker = Battle_Worker()
                worker.defender = fullList[thread_index]
                worker.index = thread_index
                results[thread_index] = worker
                thread_index += 1
                if worker.defender.cp < 1000:
                    # print('Skipping')
                    worker.ready.put(True)
                else:
                    # print('Starting')
                    threads_available -= 1
                    worker.start()
                # print("Loop F:"+str(results[thread_index]))
            # print(results[print_index].results['ready'])

            # If we've completed, then break
            if print_index == len(fullList):
                break

            # Sleep
            time.sleep(0.01)

        end_time = time.time()
        tDelta = end_time-start_time
        tMin = int(tDelta/60)
        tSec = int(tDelta-(60*tMin))
        print("Total Time: "+str(tMin)+"m"+str(tSec)+"s")


def run_edit_pokemon(pkmn):
    edit_pokemon_interface = """
  Edit Pokemon:
    [n]  Edit Nickname
    [s]  Edit Species
    [c]  Edit CP
    [h]  Edit HP
    [d]  Edit Dust cost
    [m1] Edit Quick Move
    [m2] Edit Charge Move
    [a]  Edit Appraisal
    [k]  Change Skin

    [ia] Calculate IVs
    [ic] Clear IVs

    [e]  Evolve Pokemon
    [ep] Predict evolved Pokemon #IMP

    [x]  Exit
> """
    while True:
        title_string = pkmn.name+" ("+pkmn.species+")"
        if pkmn.skin != "":
            title_string += " ["+pkmn.skin+" skin]"
        print(title_string)
        print "CP: "+str(pkmn.cp)
        print "HP: "+str(pkmn.hp)
        print "Stardust: "+str(pkmn.dust)
        print "IVs: "+str(int(pkmn.minIV/0.045)/10.0)+"-"+str(int(pkmn.maxIV/0.045)/10.0)+" ("+str(len(pkmn.IVOptions))+")"
        for iv in pkmn.IVOptions:
            sp = iv.split("_")
            if len(sp) != 2:
                continue
            pointSum = PK._hex_to_int(sp[1][0])+PK._hex_to_int(sp[1][1])+PK._hex_to_int(sp[1][2])
            print "L "+sp[0]+"  "+str(PK._hex_to_int(sp[1][0]))+" / "+str(PK._hex_to_int(sp[1][1]))+" / "+str(PK._hex_to_int(sp[1][2]))+" ("+str(int(pointSum/0.045)/10.0)+")"
        print
        print "Moves: "+pkmn.move_one+"/"+pkmn.move_two
        print "Appraisal: "+str(pkmn.appraisal)+" / "+str(pkmn.bestStat)+" / "+str(pkmn.statLevel)
        cmd = UInp.get_input(edit_pokemon_interface).lower()
        if cmd == "n":
            pkmn.name = UInp.get_input("Pokemon Nickname?\n>  ")
        elif cmd == "s":
            pkmn.species = UInp.input_species()
        elif cmd == "c":
            pkmn.cp = UInp.input_cp()
        elif cmd == "h":
            pkmn.hp = UInp.input_hp()
        elif cmd == "d":
            pkmn.dust = UInp.input_dust()
        elif cmd == "m1":
            pkmn.move_one = UInp.input_quick_move()
        elif cmd == "m2":
            pkmn.move_two = UInp.input_charge_move()
        elif cmd == "k":
            pkmn.skin = UInp.get_input("Pokemon Skin?\n>  ")
        elif cmd == "ia":
            print("\n")
            pkmn.calculate_iv_options()
            print("\n")
        elif cmd == "ic":
            pkmn.IVOptions = []
        elif cmd == "a":
            pkmn.appraisal = UInp.input_appraisal()
            pkmn.bestStat = UInp.input_bestStat()
            pkmn.statLevel = UInp.input_stat_level()
        elif cmd == "e":
            pkmn.name = UInp.get_input("Pokemon Nickname?\n>  ")
            pkmn.species = UInp.input_species()
            pkmn.cp = UInp.input_cp()
            pkmn.hp = UInp.input_hp()
            pkmn.move_one = UInp.input_quick_move()
            pkmn.move_two = UInp.input_charge_move()
            print("")
            pkmn.calculate_iv_options()
            print("\n")
        elif cmd == "x":
            break
        # Command not found
        else:
            print("Command \'"+cmd+"\' not found.\n")    

def clear_screen():
    # "Clear" the screen
    if os.name == 'posix' and platform.system() == 'Darwin' and platform.machine() == 'x86_64':
        # os.system('cls')
        os.system('clear')
    else:
        # print(chr(27) + "[2J")
        # print(chr(8)*10000)
        print("\n"*120)


def apply_active_filters():
    global pkmnList
    global filteredList
    global currentFilter

    # Reset the list
    filteredList = [pk for pk in pkmnList if True ]

    # print("Starting Filters: "+currentFilter)
    active_filters = currentFilter.split(":")
    currentFilter = ""
    for flt in active_filters:
        params = flt.split(" ")

        if params[0] == "": # Pokemon Family Filter
            continue
        elif params[0] == "family": # Pokemon Family Filter
            species = apply_yn_filter(params,UInp.input_species)
            family = Species.Species(species).Family
            filteredList = [pk for pk in filteredList if Species.Species(pk.species).Family == family]
        elif params[0] == "species": # Pokemon Species Filter
            species = apply_yn_filter(params,UInp.input_species)
            filteredList = [pk for pk in filteredList if pk.species == species]
        elif params[0] == "minCP": # Minimum CP Filter
            cp = int(apply_yn_filter(params,UInp.input_cp))
            filteredList = [pk for pk in filteredList if pk.cp >= cp ]        
        elif params[0] == "maxCP": # Minimum CP Filter
            cp = int(apply_yn_filter(params,UInp.input_cp))
            filteredList = [pk for pk in filteredList if pk.cp <= cp ]
        elif params[0] == "marked": # Marked
            mark_name = apply_yn_filter(params, lambda: UInp.get_input("Mark Name?\n> "))
            if mark_name is "":
                filteredList = [pk for pk in filteredList if len(pk.marks) is not 0 ]
            else:
                filteredList = [pk for pk in filteredList if mark_name in pk.marks ]
        elif params[0] == "nonmarked": # Non-marked
            mark_name = apply_yn_filter(params, lambda: UInp.get_input("Mark Name?\n> "))
            if mark_name is "":
                filteredList = [pk for pk in filteredList if len(pk.marks) is 0 ]                
            else:
                filteredList = [pk for pk in filteredList if mark_name not in pk.marks ]
        elif params[0] == "sortName": # Name Sort
            apply_ad_sort(params, sortFunc=lambda pk: pk.name)
        elif params[0] == "sortCP": # CP Sort
            apply_ad_sort(params, sortFunc=lambda pk: pk.cp)
        elif params[0] == "sortMinIV": # Min IV Sort
            apply_ad_sort(params, sortFunc=lambda pk: pk.minIV)
        elif params[0] == "sortMaxIV": # Max IV Sort
            apply_ad_sort(params, sortFunc=lambda pk: pk.maxIV)
        else:
            print("Invalid filter configuration for \'"+flt+"\'")
            return

        currentFilter += ":"
    # print("Ending Filters: "+currentFilter)


def apply_yn_filter(params, inputFunc=lambda: ""):
    global currentFilter
    if len(params) == 3:
        inp = params[2]
        remember = params[1]
    elif len(params) == 2:
        inp = inputFunc()
        remember = params[1]
    elif len(params) == 1:
        inp = inputFunc()
        remember = UInp.input_remember_setting()
    else:
        print("Invalid filter configuration for \'"+" ".join(params)+"\'")
        return
    currentFilter += params[0]+" "+remember+" "+str(inp)
    return inp


def apply_ad_sort(params, sortFunc):
    global currentFilter
    if len(params) == 2:
        ad = params[1]
    elif len(params) == 1:
        ad = UInp.input_ascending_descending()
    else:
        print("Invalid sort configuration for \'"+" ".join(params)+"\'")
        return
    if ad == "a":
        filteredList.sort(key=sortFunc)
    else:
        filteredList.sort(key=sortFunc, reverse=True)
    currentFilter += params[0]+" "+ad


def generate_all_pokemon_with_wide_range_of_CPs():
    pokeList = []
    for sp in Species.RAW_SPECIES_DATA:
        species = Species.Species(sp[Species.SPECIES_KEYS.Name])
        count = int(species.Max_CP/100)
        for cpLevel in range(count):
            cp = (cpLevel+1)*100
            # print("Creating "+species.Name+" "+str(cp))

            pkmn = PK.Pokemon()
            pkmn.species = species.Name
            pkmn.IVOptions = []
            pkmn.appraisal = 2
            # pkmn.bestStat = UInp.input_bestStat()
            pkmn.statLevel = 1
            delta = [0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8,9,-9,10,-10,11,-11,12,-12,13,-13,14,-14,15,-15,16,-16,17,-17,18,-18,19,-19,20,-20]
            for d in delta:
                pkmn.cp = cp+d
                pkmn.calculate_iv_options(False)
                if len(pkmn.IVOptions) > 0:
                    break
            if len(pkmn.IVOptions) == 0:
                continue

            lvl = pkmn.get_level()
            atk = 10
            dfn = 10
            stm = 10
            pkmn.hp = max(int(math.sqrt(PK.Pokemon._fLvl(lvl)) * (species.HP + stm)), 10)
            pkmn.cp = max(int((species.Attack+atk) * math.sqrt(species.Defense+dfn) * math.sqrt(species.HP+stm) * PK.Pokemon._fLvl(lvl) / 10.0), 10)
            pkmn.IVOptions = [str(lvl)+"_AAA"]
            for mv1 in species.Quick_Moves:
                for mv2 in species.Charge_Moves:
                    pkmn2 = PK.Pokemon()
                    pkmn2.species = species.Name
                    pkmn2.IVOptions = pkmn.IVOptions
                    pkmn2.appraisal = 2
                    pkmn2.statLevel = 1
                    pkmn2.cp = pkmn.cp
                    pkmn2.hp = pkmn.hp
                    pkmn2.move_one = mv1
                    pkmn2.move_two = mv2
                    pokeList.append(pkmn2)
                    print("["+str(len(pokeList))+"] Created "+species.Name+" "+str(pkmn.cp)+" with ("+mv1+"/"+mv2+")")
    fio.write_pokemon_to_file(pokeList, GENERATED_POKEMON_FILE_FULL_CP_RANGE)



def generate_all_max_level_pokemon():
    # TODO IMP
    pokeList = []
    for sp in Species.RAW_SPECIES_DATA:
        species = Species.Species(sp[Species.SPECIES_KEYS.Name])
        pkmn = PK.Pokemon()
        pkmn.species = species.Name
        pkmn.IVOptions = ["40.5_AAA"]
        pkmn.appraisal = 3
        pkmn.bestStat = 6
        pkmn.statLevel = 3
        pkmn.hp = max(int(math.sqrt(PK.Pokemon._fLvl(40.5)) * (species.HP + 15)), 10)
        pkmn.cp = max(int((species.Attack+15) * math.sqrt(species.Defense+15) * math.sqrt(species.HP+15) * PK.Pokemon._fLvl(40.5) / 10.0), 10)
        for mv1 in species.Quick_Moves:
            for mv2 in species.Charge_Moves:
                pkmn2 = pkmn.clone()
                pkmn2.move_one = mv1
                pkmn2.move_two = mv2
                pokeList.append(pkmn2)
                print("["+str(len(pokeList))+"] Created "+species.Name+" "+str(pkmn.cp)+" with ("+mv1+"/"+mv2+")")

    fio.write_pokemon_to_file(pokeList, GENERATED_POKEMON_FILE_MAX_CP)    

def generate_all_cps_for_pokemon(pkmn):
    # TODO IMP
    species = Species.Species(pkmn)
    pokeList = []
    for lvl in range(1,81):
        lvl_actual = ((lvl/2.0)+0.5)
        for atk in range(0,16):
            for defn in range(0,16):
                for stam in range(0,16):
                    pkmn = PK.Pokemon()
                    pkmn.species = species.Name
                    iv_string = str(lvl_actual)+"_"+str(PK._int_to_hex(atk))+str(PK._int_to_hex(defn))+str(PK._int_to_hex(stam))
                    pkmn.name = iv_string
                    pkmn.IVOptions = [iv_string]
                    pkmn.hp = max(int(math.sqrt(PK.Pokemon._fLvl(lvl_actual)) * (species.HP + stam)), 10)
                    pkmn.cp = max(int((species.Attack+atk) * math.sqrt(species.Defense+defn) * math.sqrt(species.HP+stam) * PK.Pokemon._fLvl(lvl_actual) / 10.0), 10)
                    pokeList.append(pkmn)
                    print("["+str(len(pokeList))+"] Created "+species.Name+" "+str(pkmn.cp)+", "+str(pkmn.hp)+", "+str(pkmn.IVOptions))

    fio.write_pokemon_to_file(pokeList, GENERATED_POKEMON_FILE_ALL_CPS)

def generate_target_top_pokemon_list():
    max_lvl_pokemon = fio.read_pokemon_from_file(GENERATED_POKEMON_FILE_MAX_CP)

    legendaries = ["Articuno","Zapdos","Moltres","Mewtwo","Mew"]

    # .-----------------------.
    # |   Top Gym Attackers   |
    # '-----------------------'

    # Build results lists
    print("Building Results List")
    for defender in max_lvl_pokemon:
        # Dont allow defenders to be non-max evolved
        defender.results = []
        defender.beats = []
        defender.beaten_by = []
        if Species.Species(defender.species).Evolves_Into[0] != "":
            continue
        print("  Evaluating Defender >> "+defender.species+" w/ "+defender.move_one+"/"+defender.move_two)
        for attacker in max_lvl_pokemon:
            # Dont allow attackers to be legendaries
            if attacker.species in legendaries:
                continue
            result = PK.Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)
            defender.results.append(result)

    # Find the top result(s)
    print("Processing Results")
    for defender in max_lvl_pokemon:
        if len(defender.results) == 0:
            continue
        defender.results.sort(key=lambda res: (res['gym_score']), reverse=True)
        best_result = defender.results[0]

        # Only use Top attacker
        attacker = best_result['attacker']
        attacker.beats.append(defender)
        defender.beaten_by.append(attacker)
        print("  "+defender.species+" w/ "+defender.move_one+"/"+defender.move_two+"  is beaten by  "+attacker.species+" w/ "+attacker.move_one+"/"+attacker.move_two)


        # # Use all qualifying attackers
        # for result in defender.results:
        #     if result['gym_score'] >= 1.5 or best_result['gym_score']-result['gym_score'] <= 0.2:
        #         attacker = result['attacker']
        #         attacker.beats.append(defender)
        #         defender.beaten_by.append(attacker)
        #         print("  "+defender.species+" w/ "+defender.move_one+"/"+defender.move_two+"  is beaten by  "+attacker.species+" w/ "+attacker.move_one+"/"+attacker.move_two)
        #     else:
        #         break


    # Find the best core of attackers, using a minimum-vertex-cover algorithm
    print("Generating Core Attackers")
    defenders_remaining = []
    core_attackers = []
    for defender in max_lvl_pokemon:
        if len(defender.beaten_by) == 0:
            continue
        defenders_remaining.append(defender)
    while len(defenders_remaining) > 0:
        # Find the defender with the lowest number of successful attackers
        best_defender = defenders_remaining[0]
        for defender in defenders_remaining:
            if len(defender.beaten_by) < len(best_defender.beaten_by):
                best_defender = defender
        print("  Found Defender >> "+best_defender.species+" w/ "+best_defender.move_one+"/"+best_defender.move_two)

        # Find the attacker with the highest number successful attacks
        best_attacker = best_defender.beaten_by[0]
        for attacker in best_defender.beaten_by:
            if len(attacker.beats) > len(best_attacker.beats):
                best_attacker = attacker

        # Add the attacker to the list
        core_attackers.append(best_attacker)
        print("  Adding Attacker >> "+best_attacker.species+" w/ "+best_attacker.move_one+"/"+best_attacker.move_two)
        iter_list = [p for p in best_attacker.beats]
        for defender in iter_list:
            print("    Removing defender >> "+defender.species+" w/ "+defender.move_one+"/"+defender.move_two)
            for attacker in defender.beaten_by:
                attacker.beats.remove(defender)
            defender.beaten_by.remove(best_attacker)
            defenders_remaining.remove(defender)



###########################################
##    Pokemon Go Collection Management   ##
###########################################

PKMN_FILE = "Lists/PoGoCollection.txt"
GENERATED_POKEMON_FILE_FULL_CP_RANGE = "Lists/generated_pokemon_full.txt"
GENERATED_POKEMON_FILE_MAX_CP = "Lists/generated_pokemon_max.txt"
GENERATED_POKEMON_FILE_ALL_CPS = "Lists/generated_pokemon_all_cp.txt"

def sort_pokemon():
    pkmnList.sort(key=lambda pk: (pk.id()*5000)+(5000-int(pk.cp)))

def read_pokemon_collection():
    global pkmnList
    pkmnList = fio.read_pokemon_from_file(PKMN_FILE)

    # __VALIDATE_POKEMON_MOVES() # Validate Pokemon move sets.  Run this when 
    # PK.Pokemon.calculate_gym_attack_score_for_combatants(pkmnList[342],pkmnList[356])['gym_score']

    # pkmn = PK.Pokemon()
    # # ----- SNORLAX -----
    # # pkmn.species = "Snorlax"
    # # pkmn.cp = 2048
    # # pkmn.IVOptions = []
    # # # pkmn.move_one = "Lick"
    # # # pkmn.move_two = "Body Slam"
    # # # pkmn.hp = 209
    # # # pkmn.dust = 3000
    # # ----- VAPOREON -----
    # pkmn.species = "Vaporeon"
    # pkmn.cp = 2564
    # pkmn.IVOptions = []
    # pkmn.move_one = "Water Gun"
    # pkmn.move_two = "Hydro Pump"
    # # pkmn.hp = 196
    # # pkmn.dust = 4500
    # pkmn.calculate_iv_options() # Re-calculate IVs on read
    # print(pkmn.hp)
    # print(pkmn.get_level())
    # print(pkmn.get_IVs())
    # # Squirt == 587
    # # Snorlax == 611
    # run_edit_pokemon(pkmn)
    # for pk in pkmnList:
    #     print(pk.name+" ("+pk.species+")\t"+str(PK.Pokemon.calculate_gym_attack_score_for_combatants(pk,pkmn)['gym_score']))
    # generate_all_pokemon()

def write_pokemon_collection():
    global pkmnList
    sort_pokemon()
    fio.write_pokemon_to_file(pkmnList, PKMN_FILE)





##################################
##    Text Formatting Utility   ##
##################################
# Heavily modified from original at:
#   http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

class bcolors:
    # Colors
    Red = '\033[31m'
    Orange = '\033[91m'
    Yellow = '\033[93m'
    Gold = '\033[33m'
    Green = '\033[32m'
    Lime = '\033[92m'
    Aqua = '\033[96m'
    Cyan = '\033[36m'
    Blue = '\033[34m'
    Indigo = '\033[94m'
    Violet = '\033[95m'
    Magenta = '\033[35m'
    Black = '\033[30m'
    Gray = '\033[90m'
    LightGray = '\033[37m'
    White = '\033[97m'

    # Highlight Colors
    BgRed = '\033[41m'
    BgOrange = '\033[101m'
    BgYellow = '\033[103m'
    BgGold = '\033[43m'
    BgGreen = '\033[42m'
    BgLime = '\033[102m'
    BgAqua = '\033[106m'
    BgCyan = '\033[46m'
    BgBlue = '\033[44m'
    BgIndigo = '\033[104m'
    BgViolet = '\033[105m'
    BgMagenta = '\033[45m'
    BgBlack = '\033[40m'
    BgGray = '\033[100m'
    BgLightGray = '\033[107m'
    BgWhite = '\033[47m'

    # Controls/Formatting
    Clear = '\033[0m'
    Dim = '\033[2m'
    Bold = '\033[1m'
    Underline = '\033[4m'
    Italic = '\033[3m'
    Blink = '\033[5m'

    # Test
    Highlight = '\033[7m' # Highlight?!





#######################
##    Main Program   ##
#######################

# Read in from collection file
read_pokemon_collection()
# Write back to collection file, Useful for output refactors/migrations
# TODO: Implement a write-to-temp-file/rename system, and/or a collection backup system
write_pokemon_collection()

# for pkm in pkmnList:
#     payload = pkm.calculate_type_advantages()
#     print("  max_score: "+str(payload["max_score"]))
# exit()

# generate_target_top_pokemon_list()

# generate_all_cps_for_pokemon('Magikarp')

# Run the main input loop
run()

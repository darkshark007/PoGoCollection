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
  [s] Save Active Filters #Imp
  [l] Load Saved Filter #Imp

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
    [si+] Min IVs #Imp
    [si+] Max IVs #Imp
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


def list_pokemon():
    apply_active_filters()
    print("Idx  | Nickname     | Species      | CP   | IV Score Range       | Basic Move             | Charge Move            | Mark  |")
    print("-----:--------------:--------------:------:----------------------:------------------------:------------------------:-------:")
    # TODO List IVs?
    for idx, pkmn in enumerate(filteredList):
        # Idx  | Nickname     | Species      | CP
        printString = ""

        # Print Index
        item = str(idx)
        if len(item) < 4:
            item = " "*(4-len(item))+item
        printString += item+" | "

        # Print Nickname
        item = str(pkmn.name)
        if len(item) < 12:
            item = item+" "*(12-len(item))
        printString += item+" | "

        # Print Species
        item = str(pkmn.species)
        if len(item) < 12:
            item = item+" "*(12-len(item))
        printString += item+" | "

        # Print CP
        item = str(pkmn.cp)
        if len(item) < 4:
            item = " "*(4-len(item))+item
        printString += item+" | "


        # Print IVs
        item = str(int(pkmn.minIV/0.045)/10.0)
        if len(item) < 5:
            item = " "*(5-len(item))+item
        printString += item

        if len(pkmn.IVOptions) != 1:
            item = str(int(pkmn.maxIV/0.045)/10.0)
            if len(item) < 5:
                item = " "*(5-len(item))+item
            printString += " - "+item

            item = "("+str(len(pkmn.IVOptions))+")"            
            if len(item) < 6:
                item = " "*(6-len(item))+item
            printString += " "+item
        else:
            printString += (" "*15)
        printString += " | "

        # Print Basic Move
        item = str(pkmn.move_one)
        if len(item) < 22:
            item = " "*(22-len(item))+item
        printString += item+" | "

        # Print Charge Move
        item = str(pkmn.move_two)
        if len(item) < 22:
            item = " "*(22-len(item))+item
        printString += item+" | "

        # Print Mark
        item = str(pkmn.marked)
        if len(item) < 5:
            item = " "*(5-len(item))+item
        printString += item+" | "

        # Calculate Duel Score(s)
        # minScore = 100
        # keep = False
        # item = str(int(pkmn.calculate_duel_score_for_types("","")))
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # # #1
        # score = int(pkmn.calculate_duel_score_for_types("Water",""))
        # if score > minScore:
        #     keep = True
        # item = str(score)
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # # #2
        # score = int(pkmn.calculate_duel_score_for_types("Ground","Rock"))
        # if score > minScore:
        #     keep = True
        # item = str(score)
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # # #3
        # score = int(pkmn.calculate_duel_score_for_types("Water","Ice"))
        # if score > minScore:
        #     keep = True
        # item = str(score)
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # # #4
        # score = int(pkmn.calculate_duel_score_for_types("Dragon","Flying"))
        # if score > minScore:
        #     keep = True
        # item = str(score)
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # # #5
        # score = int(pkmn.calculate_duel_score_for_types("Fire",""))
        # if score > minScore:
        #     keep = True
        # item = str(score)
        # if len(item) < 4:
        #     item = " "*(4-len(item))+item
        # printString += item+" | "
        # if not keep:
        #     continue


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
            pkmn.calculate_iv_options()
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
                                if pk.cp > int(pkmn.cp*0.5) and pk.cp > min_cp:
                                    continue
                                else:
                                    min_cp = pk.cp
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
            elif cmd == "s": # Save 
                print("Saving Active Filters...")
                # TODO Implement
            elif cmd == "l": # Save 
                print("Loading Saved Filter...")
                # TODO Implement
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
Mark Pokemon:
  [t]  Highest CP per Species
  [n]  Pokemon with given name
  [s]  Pokemon of a particular species
  [in] N Highest IV's per Species
  [em] Max Evolved Pokemon
  [gc] Top-Scoring Gym Combatants

  [x]  Clear Markers
> """

    cmd = UInp.get_input(mark_pokemon_interface).lower()

    # Allow all mark commands to be negatable
    negate = False
    if cmd[0] == "!":
        negate = True
        cmd = cmd[1:]

    def mark_pokemon(pkmn, result):
        if result is True and negate is False:
            pkmn.marked = True
        if result is True and negate is True:
            return # Dont mark false
        if result is False and negate is True:
            pkmn.marked = True
        if result is False and negate is False:
            return # Dont mark false

    if cmd == "t":
        loop_species = "NONE"
        # pkmnList is assumed to be always sorted by CP, which it should be.
        for pkmn in pkmnList:
            if pkmn.species != loop_species:
                mark_pokemon(pkmn,True)
                loop_species = pkmn.species
            else:
                mark_pokemon(pkmn,False)

    elif cmd == "n":
        inp_name = UInp.get_input("Name?\n>  ")
        for pkmn in pkmnList:
            if pkmn.name == inp_name:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "s":
        inp_species = UInp.input_species()
        for pkmn in pkmnList:
            if pkmn.species == inp_species:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "in":
        inp_N = UInp.input_number("N?\n> ")
        inp_skip = UInp.input_tf("Skip currently marked pokemon?\n>  ")
        # Construct the IV list
        iv_list = []
        iv_list.append([]) # Skip 0
        for species in Species.RAW_SPECIES_DATA:
            iv_list.append([])

        # Loop and collect the N highest IV values
        for pkmn in pkmnList:
            if inp_skip and pkmn.marked:
                continue
            pkid = Species.get_id_from_species(pkmn.species)
            score = pkmn.minIV
            if len(iv_list[pkid]) < inp_N:
                iv_list[pkid].append(score)
            else:
                # Find the lowest index
                lowest_index = -1
                lowest_val = 110
                for i in range(inp_N):
                    if iv_list[pkid][i] < lowest_val:
                        lowest_index = i
                        lowest_val = iv_list[pkid][i]
                if score > lowest_val:
                    iv_list[pkid][lowest_index] = score

        # Loop over the IV values and pull out the lowest one
        for pkid in range(len(iv_list)):
            # Find the lowest index
            lowest_index = -1
            lowest_val = 110
            for i in range(len(iv_list[pkid])):
                if iv_list[pkid][i] < lowest_val:
                    lowest_index = i
                    lowest_val = iv_list[pkid][i]
            iv_list[pkid] = lowest_val

        # Loop and mark pkmn with highest IVs
        for pkmn in pkmnList:
            if pkmn.maxIV >= iv_list[Species.get_id_from_species(pkmn.species)]:
                mark_pokemon(pkmn, True)
            else:
                mark_pokemon(pkmn, False)

    elif cmd == "em":
        for pkmn in pkmnList:
            species = Species.Species(pkmn.species)
            if species.Evolves_Into[0] == "":
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
                # global pkmnList
                defender = self.defender
                bestAttackers = [[],[],[],[]]
                bestScore = [-1, -1, -1, -1]
                for idx in range(len(pkmnList)):
                    attacker = pkmnList[idx]
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

        threads_available = 32
        thread_index = 0
        print_index = 0
        start_time = time.time()
        while True:

            # Print results so far
            printString = ""
            while results[print_index] != None and results[print_index].ready.full() == True:
                res = results[print_index]
                defender = res.defender
                printString += "["+str(print_index)+"] Battling "+defender.species+" "+str(defender.cp)+"cp ("+defender.move_one+"/"+defender.move_two+")\n"
                ls = res.attackers.get()
                scores = res.scores.get()
                for tier in range(4):
                    for pkIdx in ls[tier]:
                        # TODO: Can I refactor this so it supports negation?  Combine all the tiers into one list and iterate over pkmnList, comparing to the built list?
                        pkmn = pkmnList[pkIdx]
                        pkmn.marked = True
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
                worker.start()
                # print("Loop F:"+str(results[thread_index]))
                threads_available -= 1
                thread_index += 1
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



    elif cmd == "x":
        for pkmn in pkmnList:
            pkmn.marked = False

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
    [x]  Exit
> """
    while True:
        print(pkmn.name+" ("+pkmn.species+")")
        print "CP: "+str(pkmn.cp)
        print "HP: "+str(pkmn.hp)
        print "Stardust: "+str(pkmn.dust)
        print "IVs: "+str(int(pkmn.minIV/0.045)/10.0)+"-"+str(int(pkmn.maxIV/0.045)/10.0)+" ("+str(len(pkmn.IVOptions))+")"
        for iv in pkmn.IVOptions:
            sp = iv.split("_")
            if len(sp) != 2:
                continue
            print "L "+sp[0]+"  "+str(PK._hex_to_int(sp[1][0]))+" / "+str(PK._hex_to_int(sp[1][1]))+" / "+str(PK._hex_to_int(sp[1][2]))
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
        elif cmd == "a":
            pkmn.appraisal = UInp.input_appraisal()
            pkmn.bestStat = UInp.input_bestStat()
            pkmn.statLevel = UInp.input_stat_level()
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
            apply_yn_filter(params)
            filteredList = [pk for pk in filteredList if pk.marked == True ]
        elif params[0] == "nonmarked": # Non-marked
            apply_yn_filter(params)
            filteredList = [pk for pk in filteredList if pk.marked == False ]
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


def generate_all_pokemon():
    pokeList = []
    for species in species.RAW_SPECIES_DATA:
        count = int(species[SPECIES.Max_CP]/100)
        for cpLevel in range(count):
            cp = (cpLevel+1)*100
            # print("Creating "+species[SPECIES.Name]+" "+str(cp))

            pkmn = PK.Pokemon()
            pkmn.species = species[SPECIES.Name]
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
            pkmn.hp = max(int(math.sqrt(PK.Pokemon._fLvl(lvl)) * (species[SPECIES.HP] + stm)), 10)
            pkmn.cp = max(int((species[SPECIES.Attack]+atk) * math.sqrt(species[SPECIES.Defense]+dfn) * math.sqrt(species[SPECIES.HP]+stm) * PK.Pokemon._fLvl(lvl) / 10.0), 10)
            pkmn.IVOptions = [str(lvl)+"_AAA"]
            for mv1 in species[SPECIES.Quick_Moves]:
                for mv2 in species[SPECIES.Charge_Moves]:
                    pkmn2 = PK.Pokemon()
                    pkmn2.species = species[SPECIES.Name]
                    pkmn2.IVOptions = pkmn.IVOptions
                    pkmn2.appraisal = 2
                    pkmn2.statLevel = 1
                    pkmn2.cp = pkmn.cp
                    pkmn2.hp = pkmn.hp
                    pkmn2.move_one = mv1
                    pkmn2.move_two = mv2
                    pokeList.append(pkmn2)
                    print("["+str(len(pokeList))+"] Created "+species[SPECIES.Name]+" "+str(pkmn.cp)+" with ("+mv1+"/"+mv2+")")
    fio.write_pokemon_to_file(pokeList, GENERATED_POKEMON_FILE_FULL_CP_RANGE)





###########################################
##    Pokemon Go Collection Management   ##
###########################################

PKMN_FILE = "Lists/PoGoCollection.txt"
GENERATED_POKEMON_FILE_FULL_CP_RANGE = "Lists/generated_pokemon_full.txt"

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

# Run the main input loop
run()

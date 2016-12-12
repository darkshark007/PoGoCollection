import math
import os
import platform
import sys
import thread
from multiprocessing import Process, Value, Array, Manager, Queue
import time
import unicodedata
from ctypes import Structure, py_object, c_bool

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
filter_interface = """
Select Filter or Sort:
  [x] CLEAR ACTIVE FILTERS
  [s] Save Active Filters #Imp
  [l] Load Saved Filter #Imp

  Filter by:
    [fs] Species Name
    [ff] Species Family
    [f-] Min CP
    [f+] Max CP
    [f>] Strong against #Imp
    [f<] Weak against #Imp

  Sort by:
    [sn] Name
    [ss] Species #Imp
    [sc] CP
    [s?] Min IVs #Imp
    [s?] Max IVs #Imp
> """
mark_pokemon_interface = """
Mark Pokemon:
  [t]  Highest CP per Species
  [n]  Pokemon with given name
  [s]  Pokemon of a particular species
  [in] N Highest IV's per Species
  [em] Max Evolved Pokemon  
  [en] Non-Max Evolved Pokemon
  [gc] Top-Scoring Gym Combatants

  [x]  Clear Markers
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


# From http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
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
    Bold = '\033[1m'
    Underline = '\033[4m'
    Italic = '\033[3m'
    Blink = '\033[5m'

    # Test
    Dim = '\033[2m' # Dim??
    Highlight = '\033[7m' # Highlight?!


class Pokemon:
    def __init__(self):
        self.name = ""
        self.species = ""
        self.cp = -1
        self.hp = -1
        self.dust = -1
        self.move_one = ""
        self.move_two = ""
        self.appraisal = -1
        self.bestStat = -1
        self.statLevel = -1

        # Calculated Properties
        self.IVOptions = []
        self.minIV = 0
        self.maxIV = 45
        self.strengths = []
        self.weaknesses = []
        self.marked = False


    def calculate_iv_options(self, shouldPrint=True):
        options = []
        speciesData = SPECIES_DATA[get_id_from_species(self.species)-1]
        baseAtk = int(speciesData[SPECIES.Attack])
        baseDef = int(speciesData[SPECIES.Defense])
        baseStm = int(speciesData[SPECIES.HP])
        if self.dust != -1: 
            baseLvl = LEVELS_FOR_DUST_VALUES[VALID_DUST_VALUES.index(self.dust)]
            levelRange = [baseLvl, baseLvl+0.5, baseLvl+1.0, baseLvl+1.5]
        else:
            levelRange = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27,27.5,28,28.5,29,29.5,30,30.5,31,31.5,32,32.5,33,33.5,34,34.5,35,35.5,36,36.5,37,37.5,38,38.5,39,39.5,40,40.5]
        atkRange = range(16)
        defRange = range(16)
        stmRange = range(16)

        minIVSum = 0
        maxIVSum = 45
        if self.appraisal == 0:
            minIVSum = 0
            maxIVSum = 22
        elif self.appraisal == 1:
            minIVSum = 23
            maxIVSum = 29
        elif self.appraisal == 2:
            minIVSum = 30
            maxIVSum = 36
        elif self.appraisal == 3:
            minIVSum = 37
            maxIVSum = 45


        reducedRange = range(16)
        if self.statLevel == 3:
            reducedRange = [15]
        elif self.statLevel == 2:
            reducedRange = [13,14]
        elif self.statLevel == 1:
            reducedRange = [8,9,10,11,12]
        elif self.statLevel == 0:
            reducedRange = [0,1,2,3,4,5,6,7]

        if self.bestStat in [0,3,5,6]:
            atkRange = reducedRange           
        if self.bestStat in [1,3,4,6]:
            defRange = reducedRange           
        if self.bestStat in [2,4,5,6]:
            stmRange = reducedRange           

        for lvl in levelRange:
            for atk in atkRange:
                for dfn in defRange:
                    for stm in stmRange:
                        # Rule it out if the stats dont agree with the best-stat appraisal
                        if self.bestStat == 0 and not (atk > dfn and atk > stm):
                            continue
                        if self.bestStat == 1 and not (dfn > atk and dfn > stm):
                            continue
                        if self.bestStat == 2 and not (stm > atk and stm > dfn):
                            continue
                        if self.bestStat == 3 and not (atk == dfn and atk > stm):
                            continue
                        if self.bestStat == 4 and not (dfn == stm and dfn > atk):
                            continue
                        if self.bestStat == 5 and not (atk == stm and atk > dfn):
                            continue
                        if self.bestStat == 6 and not (atk == dfn and atk == stm):
                            continue

                        # Rule it out if the sum of the score is not within the appraised range
                        statSum = atk+dfn+stm
                        if not (minIVSum <= statSum and statSum <= maxIVSum):
                            continue

                        # Rule it out of the calculated HP and CP dont match
                        # print(lvl)
                        # print(Pokemon._fLvl(lvl))
                        # print(baseStm)
                        # print(stm)
                        hp = max(int(math.sqrt(Pokemon._fLvl(lvl)) * (baseStm + stm)), 10)
                        cp = max(int((baseAtk+atk) * math.sqrt(baseDef+dfn) * math.sqrt(baseStm+stm) * Pokemon._fLvl(lvl) / 10.0), 10)
                        if self.hp != -1 and hp != self.hp:
                            continue
                        if self.cp != -1 and cp != self.cp:
                            continue

                        # Entry is Valid
                        optString = str(lvl)+"_"+_int_to_hex(atk)+_int_to_hex(dfn)+_int_to_hex(stm)
                        options.append(optString)
        if len(self.IVOptions) == 0:
            self.IVOptions = options
        else:
            # For each value in the new list, look for the value in the old list.  If it's not there, toss it
            newOptionsList = []
            for newOp in options:
                newOpString = newOp.split("_")[1]
                for oldOp in self.IVOptions:
                    oldOpString = oldOp.split("_")[1]
                    if newOpString == oldOpString:
                        newOptionsList.append(newOp)
                        break
            self.IVOptions = newOptionsList

        ivMin = 45
        ivMax = 0
        if shouldPrint:
            print("Possible IV Scores:")
        for opt in self.IVOptions:
            st = opt.split("_")
            lvl = st[0]
            atk = _hex_to_int(st[1][0])
            dfn = _hex_to_int(st[1][1])
            stm = _hex_to_int(st[1][2])
            statSum = atk+dfn+stm
            if shouldPrint:
                print("- "+str(lvl)+', '+str(atk)+'/'+str(dfn)+'/'+str(stm)+"  ("+str(round(1000*statSum/45)/10)+"%)")
                # print("- "+str(lvl)+', '+str(atk)+'/'+str(dfn)+'/'+str(stm)+"  ("+str(round(100*statSum/45,1))+"%)"+"  "+str(hp)+"//"+str(cp))

            if statSum > ivMax:
                ivMax = statSum
            if statSum < ivMin:
                ivMin = statSum

        self.minIV = ivMin
        self.maxIV = ivMax


    @staticmethod
    def _fLvl(lvl):
        if 1 <= lvl and lvl <= 10:
            return ( 0.01885225 * lvl ) - 0.01001625
        if 10.5 <= lvl and lvl <= 20:
            return ( 0.01783805 * ( lvl - 10 ) ) + 0.17850625
        if 20.5 <= lvl and lvl <= 30:
            return ( 0.01784981 * ( lvl - 20 ) ) + 0.35688675
        if 30.5 <= lvl and lvl <= 40.5:
            return ( 0.00891892 * ( lvl - 30 ) ) + 0.53538485
        # TODO -> Should it be 1-10.5, etc?!


    def calculate_strengths_and_weaknesses(self):
        print self.name
        # TODO Implement


    """
        baseHP = speciesData[SPECIES.HP] # $W2    
        baseDefence = speciesData[SPECIES.Defense] # $V2        
        tankiness = self.calculate_tankiness_score_for_types(type1, type2) # AQ2
        gymOffense = max(noWeaveDmg,weaveDmg)*baseAttack # AU2
        noWeaveDmg = (mv1PowerScaled*(mv1STAB))*math.floor(100000/mv1Speed, 1) # AR2
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio,1)*(mv1PowerScaled*(mv1STAB))+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio,1)*mv1Speed))/mv1Speed,1)*(mv1PowerScaled*(mv1STAB)) # AS2
        baseAttack = speciesData[SPECIES.Attack] # $U2
        mv1PowerScaled = mv1Power*get_ratio_from_types(mv1Type, type1)*get_ratio_from_types(mv1Type, type2) # AO2
        mv1STAB = 1.25 if mv1Type == speciesData[SPECIES.Type1] or mv1Type == speciesData[SPECIES.Type2] else 1 # $X2
        mv1Speed = mv1Data[BASIC_MOVE.Duration] # $AB2
        mv1Power = mv1Data[BASIC_MOVE.PW] # $Z2
        mv1NrgGain = mv1Data[BASIC_MOVE.NRG] # $AD2
        mv2STAB = 1.25 if mv2Type == speciesData[SPECIES.Type1] or mv2Type == speciesData[SPECIES.Type2] else 1.0 # $Y2
        mv2PowerScaled = mv2Power*get_ratio_from_types(mv2Type, type1)*get_ratio_from_types(mv2Type, type2) # AP2
        mv2STAB = 1.25 if mv2Type == speciesData[SPECIES.Type1] or mv2Type == speciesData[SPECIES.Type2] else 1.0 # $Y2
        mv2Speed = mv2Data[CHARGE_MOVE.Duration] # $AC2
        mv2NrgCost = mv2Data[CHARGE_MOVE.NRG] # $AE2
        mv2CritChance = mv2Data[CHARGE_MOVE.Crit] # $AF2
        critDamageBonusConstant = 0.0 # 'Showing Work'!$AM$1
        chargeDelayConstant = 500 # 'Showing Work'!$AO$1
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain,1) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain) # IF(mv2NrgCost=100,CEILING(mv2NrgCost/mv1NrgGain,1),mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant) # $AG2
    """
    
    def calculate_duel_score_for_types(self, type1, type2):
        speciesData = SPECIES_DATA[get_id_from_species(self.species)-1]
        mv1Data = _get_basic_move_by_name(self.move_one)
        mv1Power = mv1Data[BASIC_MOVE.PW]
        mv1Type = mv1Data[BASIC_MOVE.Type]
        mv1PowerScaled = mv1Power*get_ratio_from_types(mv1Type, type1)*get_ratio_from_types(mv1Type, type2)
        mv1STAB = 1.25 if mv1Type == speciesData[SPECIES.Type1] or mv1Type == speciesData[SPECIES.Type2] else 1.0
        mv1Speed = mv1Data[BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[BASIC_MOVE.NRG]
        mv2Data = _get_charge_move_by_name(self.move_two)
        mv2Power = mv2Data[CHARGE_MOVE.PW]
        mv2Type = mv2Data[CHARGE_MOVE.Type]
        mv2PowerScaled = mv2Power*get_ratio_from_types(mv2Type, type1)*get_ratio_from_types(mv2Type, type2)
        mv2STAB = 1.25 if mv2Type == speciesData[SPECIES.Type1] or mv2Type == speciesData[SPECIES.Type2] else 1.0
        mv2Speed = mv2Data[CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[CHARGE_MOVE.Crit]
        noWeaveDmg = (mv1PowerScaled*(mv1STAB))*math.floor(100000/mv1Speed)
        critDamageBonusConstant = 0.0
        chargeDelayConstant = 500
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant)
        flWeaveTime = math.floor(100000/weaveCycleLengthTime)
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio)*(mv1PowerScaled*(mv1STAB))+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio)*mv1Speed))/mv1Speed)*(mv1PowerScaled*(mv1STAB))
        baseAttack = speciesData[SPECIES.Attack]
        gymOffense = max(noWeaveDmg,weaveDmg)*baseAttack
        tankiness = self.calculate_tankiness_score_for_types(type1, type2)
        duel = gymOffense*tankiness / 100000000
        # print(self.name+" Score: "+str(duel))
        return duel


    def get_level(self):
        count = 0
        countSum = 0
        for opt in self.IVOptions:
            level = float(opt.split("_")[0])
            countSum += level
            count += 1
        avgLevel = round(((countSum * 2)/count))/2.0
        return avgLevel


    def get_IVs(self):
        testMatrix = [range(16),range(16),range(16)]
        for x in range(3):
            for y in range(16):
                testMatrix[x][y] = 0

        for opt in self.IVOptions:
            st = opt.split("_")
            lvl = st[0]
            atk = _hex_to_int(st[1][0])
            dfn = _hex_to_int(st[1][1])
            stm = _hex_to_int(st[1][2])
            testMatrix[0][atk] += 1
            testMatrix[1][dfn] += 1
            testMatrix[2][stm] += 1

        result = [-1,-1,-1]
        for rng in range(3):
            best = -1
            bestCount = 0
            for iv in range(16):
                if testMatrix[rng][iv] > bestCount:
                    best = iv
                    bestCount = testMatrix[rng][iv]
            result[rng] = best

        return result


    @staticmethod
    def calculate_gym_attack_score_for_combatants(attacker, defender):
        # Check attacks
        if defender.move_one == "" or defender.move_two == "":
            # One or both of the moves is missing, so iterate over all of the moves 
            defSpeciesData = get_species_data_from_species(defender.species)
            m1 = defender.move_one
            m2 = defender.move_two
            if m1 == "": 
                bm = defSpeciesData[SPECIES.Quick_Moves]
            else:
                bm = [m1]
            if m2 == "": 
                cm = defSpeciesData[SPECIES.Charge_Moves]
            else:
                cm = [m2]

            # Iterate over all of the possible move combinations, and return the worst-case scenario
            worstCase = 1000
            for testMove1 in bm:
                for testMove2 in cm:
                    defender.move_one = testMove1
                    defender.move_two = testMove2
                    # print(defender.move_one)
                    # print(defender.move_two)
                    result = Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)
                    if result < worstCase:
                        worstCase = result

            defender.move_one = m1
            defender.move_two = m2
            # print(worstCase)
            return worstCase


        atkSpeciesData = get_species_data_from_species(attacker.species)
        defSpeciesData = get_species_data_from_species(defender.species)
        atkIVs = attacker.get_IVs()
        defIVs = defender.get_IVs()
        
        # Attacker's Tankiness
        atkTankiness = attacker.hp
        # print(atkTankiness)

        # Defenders's Tankiness
        if defender.hp != -1:
            defTankiness = 2 * defender.hp
        else:
            defTankiness = 2 * max(int(math.sqrt(Pokemon._fLvl(defender.get_level())) * (defSpeciesData[SPECIES.HP] + defIVs[2])), 10)
        # print(defTankiness)


        critDamageBonusConstant = 0.0
        chargeDelayConstant = 500

        # Attacker's Damage
        mv1Data = _get_basic_move_by_name(attacker.move_one)
        mv1Type = mv1Data[BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == atkSpeciesData[SPECIES.Type1] or mv1Type == atkSpeciesData[SPECIES.Type2] else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData[SPECIES.Attack]+atkIVs[0])/(defSpeciesData[SPECIES.Defense]+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())/Pokemon._fLvl(defender.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, defSpeciesData[SPECIES.Type1])*get_ratio_from_types(mv1Type, defSpeciesData[SPECIES.Type2])) * # Type
            mv1Data[BASIC_MOVE.PW]
            )
        mv1Speed = mv1Data[BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[BASIC_MOVE.NRG]
        # print("Power1:"+str(mv1PowerScaled))

        mv2Data = _get_charge_move_by_name(attacker.move_two)
        mv2Type = mv2Data[CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == atkSpeciesData[SPECIES.Type1] or mv2Type == atkSpeciesData[SPECIES.Type2] else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData[SPECIES.Attack]+atkIVs[0])/(defSpeciesData[SPECIES.Defense]+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())/Pokemon._fLvl(defender.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, defSpeciesData[SPECIES.Type1])*get_ratio_from_types(mv2Type, defSpeciesData[SPECIES.Type2])) * # Type
            mv2Data[BASIC_MOVE.PW]
            )
        # print("Power2:"+str(mv2PowerScaled))
        mv2Speed = mv2Data[CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[CHARGE_MOVE.Crit]
        noWeaveDmg = (mv1PowerScaled)*math.floor(100000/mv1Speed)
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant)
        flWeaveTime = math.floor(100000/weaveCycleLengthTime)
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio)*(mv1PowerScaled)+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio)*mv1Speed))/mv1Speed)*(mv1PowerScaled)
        atkDmg = max(noWeaveDmg,weaveDmg)
        # print(atkDmg)

        # Defender's Damage
        mv1Data = _get_basic_move_by_name(defender.move_one)
        mv1Type = mv1Data[BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == defSpeciesData[SPECIES.Type1] or mv1Type == defSpeciesData[SPECIES.Type2] else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData[SPECIES.Attack]+defIVs[0])/(atkSpeciesData[SPECIES.Defense]+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, atkSpeciesData[SPECIES.Type1])*get_ratio_from_types(mv1Type, atkSpeciesData[SPECIES.Type2])) * # Type
            mv1Data[BASIC_MOVE.PW]
            )
        # print("Power1:"+str(mv1PowerScaled))
        mv1Speed = mv1Data[BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[BASIC_MOVE.NRG]
        mv2Data = _get_charge_move_by_name(defender.move_two)
        mv2Type = mv2Data[CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == defSpeciesData[SPECIES.Type1] or mv2Type == defSpeciesData[SPECIES.Type2] else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData[SPECIES.Attack]+defIVs[0])*1.0/(atkSpeciesData[SPECIES.Defense]+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, atkSpeciesData[SPECIES.Type1])*get_ratio_from_types(mv2Type, atkSpeciesData[SPECIES.Type2])) * # Type
            mv2Data[BASIC_MOVE.PW]
            )
        # print("Power2:"+str(mv2PowerScaled))
        mv2Speed = mv2Data[CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[CHARGE_MOVE.Crit]

        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        gymWeaveCycleLengthValue = math.floor(100000/(nrgRatio*(mv1Speed+2000)+(mv2Speed+chargeDelayConstant)))
        defDmg = gymWeaveCycleLengthValue*(mv2PowerScaled*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(gymWeaveCycleLengthValue*nrgRatio)*mv1PowerScaled+math.floor((100000-(gymWeaveCycleLengthValue*(mv2Speed+chargeDelayConstant)+math.ceil(gymWeaveCycleLengthValue*nrgRatio)*(mv1Speed+2000)))/(mv1Speed+2000))*mv1PowerScaled
        # print(defDmg)


        # Calculate the scores
        atkScore = defTankiness/atkDmg
        # print(atkScore)
        defScore = atkTankiness/defDmg
        # print(defScore)
        score = defScore/atkScore
        # print(score)
        return score


    def calculate_tankiness_score_for_types(self, type1, type2):
        speciesData = SPECIES_DATA[get_id_from_species(self.species)-1]
        baseHP = speciesData[SPECIES.HP]
        baseDefence = speciesData[SPECIES.Defense]
        ratioT1_1 = get_ratio_from_types(type1, speciesData[SPECIES.Type1])
        ratioT1_2 = get_ratio_from_types(type1, speciesData[SPECIES.Type2])
        ratioT2_1 = get_ratio_from_types(type2, speciesData[SPECIES.Type1])
        ratioT2_2 = get_ratio_from_types(type2, speciesData[SPECIES.Type2])
        tankiness = baseHP*baseDefence/ratioT1_1/ratioT1_2/ratioT2_1/ratioT2_2
        return tankiness

    def calculate_gym_defence_score_for_types(self, type1, type2):
        speciesData = SPECIES_DATA[get_id_from_species(self.species)-1]



    def id(self):
        return get_id_from_species(self.species)

PKMN_FILE = "Lists/pkList.txt"
GENERATED_POKEMON_FILE_FULL_CP_RANGE = "Lists/generated_pokemon_full.txt"

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
        split = line.split(",")
        pkmn = Pokemon()
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
        pkmn.strengths = split[13].split(":")
        pkmn.weaknesses = split[14].split(":")
        # pkmn.calculate_iv_options() # Re-calculate IVs on read
        pkList.append(pkmn)
    file_in.close()
    return pkList


# Read in Pokemon file
def read_pokemon():
    global pkmnList
    pkmnList = read_pokemon_from_file(PKMN_FILE)

    # __VALIDATE_POKEMON_MOVES() # Validate Pokemon move sets.  Run this when 
    # Pokemon.calculate_gym_attack_score_for_combatants(pkmnList[342],pkmnList[356])

    # pkmn = Pokemon()
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
    # edit_pokemon(pkmn)
    # for pk in pkmnList:
    #     print(pk.name+" ("+pk.species+")\t"+str(Pokemon.calculate_gym_attack_score_for_combatants(pk,pkmn)))
    # generate_all_pokemon()


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
        serial += (":".join(pkmn.strengths)).strip() + ","
        serial += (":".join(pkmn.weaknesses)).strip()
        serial = serial.strip()
        file_out.write(serial+"\n")
    file_out.close()


def write_pokemon():
    sort_pokemon()
    write_pokemon_to_file(pkmnList, PKMN_FILE)


def sort_pokemon():
    pkmnList.sort(key=lambda pk: (pk.id()*5000)+(5000-int(pk.cp)))

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



def run():
    global pkmnList
    global filteredList
    global currentFilter
    while True:
        cmd = get_input(interface).lower()

        clear_screen()

        # Add Pokemon
        if cmd == "a":
            print("Adding new pokemon to the Collection")
            pkmn = Pokemon()
            pkmn.name = get_input("Pokemon Nickname?\n>  ")
            pkmn.species = input_species()
            pkmn.cp = input_cp()
            pkmn.hp = input_hp()
            pkmn.dust = input_dust()
            pkmn.move_one = input_quick_move()
            pkmn.move_two = input_charge_move()
            pkmn.appraisal = input_appraisal()
            pkmn.bestStat = input_bestStat()
            pkmn.statLevel = input_stat_level()
            print("\n")
            pkmn.calculate_iv_options()
            pkmnList.append(pkmn)
            write_pokemon()
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
            filteredIdxList = input_pkmn_list_index()            
            pkmn = filteredList[filteredIdxList]
            clear_screen()
            edit_pokemon(pkmn)
            print("\n")
            pkmn.calculate_iv_options()
            write_pokemon()
            print("Updated "+pkmn.species)


        # Mark Pokemon
        elif cmd == "m":
            cmd = get_input(mark_pokemon_interface).lower()
            if cmd == "t":
                loop_species = "NONE"
                for pkmn in pkmnList:
                    if pkmn.species != loop_species:
                        pkmn.marked = True
                        loop_species = pkmn.species
            elif cmd == "n":
                inp_name = get_input("Name?\n>  ")
                for pkmn in pkmnList:
                    if pkmn.name == inp_name:
                        pkmn.marked = True
            elif cmd == "s":
                inp_species = input_species()
                for pkmn in pkmnList:
                    if pkmn.species == inp_species:
                        pkmn.marked = True
            elif cmd == "in":
                inp_N = input_number("N?\n> ")
                inp_skip = input_tf("Skip currently marked pokemon?\n>  ")
                # Construct the IV list
                iv_list = []
                iv_list.append([]) # Skip 0                
                for species in SPECIES_DATA:
                    iv_list.append([])

                # Loop and collect the N highest IV values
                for pkmn in pkmnList:
                    if inp_skip and pkmn.marked:
                        continue
                    pkid = get_id_from_species(pkmn.species)
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
                    if pkmn.maxIV >= iv_list[get_id_from_species(pkmn.species)]:
                        pkmn.marked = True

            elif cmd == "em":
                for pkmn in pkmnList:
                    species = get_species_data_from_species(pkmn.species)
                    if species[SPECIES.Evolves_Into][0] == "":
                        pkmn.marked = True
            elif cmd == "en":
                for pkmn in pkmnList:
                    species = get_species_data_from_species(pkmn.species)
                    if species[SPECIES.Evolves_Into][0] != "":
                        pkmn.marked = True
            elif cmd == "gc":

                class Battle_Result(Structure):
                    _fields_ = [('defender', py_object), ('attackers', py_object), ('scores', py_object), ('ready', c_bool)]

                    def __init__(self):
                        self.defender = None
                        self.attackers = [[],[],[],[]]
                        self.scores = None
                        self.ready = False

                class Attacker_List:
                    def __init__(self):
                        self.attackers = [[],[],[],[]]


                def process_battle(defender, index, result):
                    # global pkmnList
                    # print("Battling "+defender.species+" "+str(defender.cp)+"cp ("+defender.move_one+"/"+defender.move_two+")")
                    bestAttackers = [[],[],[],[]]
                    bestScore = [-1, -1, -1, -1]
                    for attacker in pkmnList:
                        score = Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)
                        # Tier 0 - Half CP or less
                        if attacker.cp <= int(defender.cp*0.5):
                            if score > bestScore[0]:
                                bestAttackers[0] = []
                                bestAttackers[0].append(attacker)
                                bestScore[0] = score
                            elif score == bestScore[0]:
                                bestAttackers[0].append(attacker)
                                bestScore[0] = score
                        # Tier 1 - Three-quarters CP or less
                        if attacker.cp <= int(defender.cp*0.75):
                            if score > bestScore[1]:
                                bestAttackers[1] = []
                                bestAttackers[1].append(attacker)
                                bestScore[1] = score
                            elif score == bestScore[1]:
                                bestAttackers[1].append(attacker)
                                bestScore[1] = score
                        # Tier 2 - Same CP or less
                        if attacker.cp <= defender.cp:
                            if score > bestScore[2]:
                                bestAttackers[2] = []
                                bestAttackers[2].append(attacker)
                                bestScore[2] = score
                            elif score == bestScore[2]:
                                bestAttackers[2].append(attacker)
                                bestScore[2] = score
                        # Tier 3 - Any CP
                        if score > bestScore[3]:
                            bestAttackers[3] = []
                            bestAttackers[3].append(attacker)
                            bestScore[3] = score
                        elif score == bestScore[3]:
                            bestAttackers[3].append(attacker)
                            bestScore[3] = score

                    # Mark the top-scorers
                    for tier in range(4):
                        for pkmn in bestAttackers[tier]:
                            pkmn.marked = True
                            # print("  ["+str(tier)+"] "+pkmn.name+" ("+pkmn.species+") "+str(pkmn.cp)+"cp with a score of "+str(bestScore[tier]))
                    result.defender = defender
                    result.attackers[0].append("Test")
                    result.bestScore = bestScore
                    result.ready = True
                    # {
                    #     'defender': defender,
                    #     'attackers': bestAttackers,
                    #     'scores': bestScore,
                    # }
                    # results[index] = result
                    # # print("Thread: "+str(index)+"  "+str(results[index].ready))
                    while True:
                        print("THREAD >> "+str(result)+" "+str(result.ready))

                        time.sleep(1)

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
                            score = Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)
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

                        # # Mark the top-scorers
                        # for tier in range(4):
                        #     for pkmn in bestAttackers[tier]:
                        #         pkmn.marked = True
                        #         # print("  ["+str(tier)+"] "+pkmn.name+" ("+pkmn.species+") "+str(pkmn.cp)+"cp with a score of "+str(bestScore[tier]))
                        self.attackers.put(bestAttackers)
                        self.scores.put(bestScore)
                        self.ready.put(True)


                fullList = read_pokemon_from_file(GENERATED_POKEMON_FILE_FULL_CP_RANGE)
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

        # Delete Pokemon
        elif cmd == "d":
            list_pokemon()
            filteredIdxList = input_pkmn_list_index_list()
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
            write_pokemon()

        # Build Gym
        elif cmd == "b":
            clear_screen()
            isFriendlyGym = input_tf("Friendly Gym?\n> ")
            gymList = []
            while True:
                count = 0
                print("\n\nGym Pokemon:")
                for pk in gymList:
                    print("  ["+str(count)+"] "+pk.species+", "+str(pk.cp)+" cp   ("+pk.move_one+"/"+pk.move_two+")")
                    count += 1
                print("")
                cmd = get_input(gym_builder_interface).lower()
                if cmd == "a":
                    pkmn = Pokemon()
                    pkmn.species = input_species()
                    pkmn.cp = input_cp()
                    pkmn.IVOptions = []
                    pkmn.calculate_iv_options(False)
                    gymList.append(pkmn)

                elif cmd == "e":
                    if len(gymList) == 0:
                        print("No pokemon to edit!")
                        continue
                    idx = input_number("Idx? \n>  ",0,(len(gymList)-1))
                    pkmn = gymList[idx]
                    edit_pokemon(pkmn)
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
                    idx = input_number("Idx? (-1 for all)\n>  ",-1,(len(gymList)-1))
                    min_value = input_float("Minimum attacker score?\n> ", 0, None)
                    if isFriendlyGym:
                        max_CP = input_number("Maximum CP?\n> ",10)
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
                            score = Pokemon.calculate_gym_attack_score_for_combatants(pk,pkmn)
                            shouldAdd = False
                            if score >= min_value:
                                if isFriendlyGym and pk.cp > max_CP:
                                    continue
                                score = round(score * 1000)/1000
                                entry = {
                                    'pk': pk,
                                    'score': score
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
                            print(color+"  "+str(score)+" -- "+pk.name+" ("+pk.species+")  "+str(pk.cp)+"cp  "+str(pk.hp)+"hp  "+pk.move_one+"/"+pk.move_two+bcolors.Clear)
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
            cmd = get_input(filter_interface).lower()
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
            elif cmd == "m+": # Filter by Species
                currentFilter += "marked"
            elif cmd == "m-": # Filter by Species
                currentFilter += "nonmarked"

            # Sorts
            elif cmd == "sn": # Sort by Name
                currentFilter += "sortName"
            elif cmd == "sc": # Sort by CP
                currentFilter += "sortCP"

            else:
                print("Filter Command \'"+cmd+"\' not recognized")
            
            apply_active_filters()
            # print("CFilt: "+currentFilter)


        # Input commands
        elif cmd == "i":
            inp = get_input("Semi-colon separated user inputs\n> ")
            append_input = inp.split(";")
            consumable_input.extend(append_input)

        # Exit
        elif cmd == "x":
            sys.exit(0)

        # Command not found
        else:
            print("Command \'"+cmd+"\' not found.\n")

def edit_pokemon(pkmn):
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
            print "L "+sp[0]+"  "+str(_hex_to_int(sp[1][0]))+" / "+str(_hex_to_int(sp[1][1]))+" / "+str(_hex_to_int(sp[1][2]))
        print
        print "Moves: "+pkmn.move_one+"/"+pkmn.move_two
        print "Appraisal: "+str(pkmn.appraisal)+" / "+str(pkmn.bestStat)+" / "+str(pkmn.statLevel)
        cmd = get_input(edit_pokemon_interface).lower()
        if cmd == "n":
            pkmn.name = get_input("Pokemon Nickname?\n>  ")
        elif cmd == "s":
            pkmn.species = input_species()
        elif cmd == "c":
            pkmn.cp = input_cp()
        elif cmd == "h":
            pkmn.hp = input_hp()
        elif cmd == "d":
            pkmn.dust = input_dust()
        elif cmd == "m1":
            pkmn.move_one = input_quick_move()
        elif cmd == "m2":
            pkmn.move_two = input_charge_move()
        elif cmd == "a":
            pkmn.appraisal = input_appraisal()
            pkmn.bestStat = input_bestStat()
            pkmn.statLevel = input_stat_level()
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


def input_number(message, minVal=None, maxVal=None):
    inp = get_input(message)
    try:
        val = int(inp)
        if minVal != None and val < minVal:
            print("Number \'"+inp+"\' is too low")
            return input_number(message, minVal, maxVal)
        if maxVal != None and val > maxVal:
            print("Number \'"+inp+"\' is too high")
            return input_number(message, minVal, maxVal)
        return val
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_number(message, minVal, maxVal)


def input_float(message, minVal=None, maxVal=None):
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
    inp = get_input(message).lower()
    if inp == "y" or inp == "yes" or inp == "t" or inp == "true":
        return True
    elif inp == "n" or inp == "no" or inp == "f" or inp == "false":
        return False
    else:
        print("Invalid value \'"+inp+"\'")
        return input_tf(message)


def input_species():
    inp = get_input("Species? (Name or ID)\n>  ")
    try:
        # Maybe they entered a number?
        inp_num = int(inp)
        if inp_num < 1 or inp_num > len(SPECIES_DATA):
            print("Invalid Species ID #"+str(inp_num))
            return input_species()
        else:
            return SPECIES_DATA[inp_num-1][SPECIES.Name]
    except ValueError:
        # Maybe they entered a name?
        inp_num = get_id_from_species(inp)
        if inp_num == -1:
            print("Could not find Species Name or ID # for \'"+inp+"\'")
            print("Did you mean...")
            for species in SPECIES_DATA:
                if fuzzy_string_search(inp.lower(), species[SPECIES.Name].lower()):
                    print("? ["+str(species[SPECIES.Id])+"] "+species[SPECIES.Name])
            print("\n")
            return input_species()
        else:
            return SPECIES_DATA[inp_num-1][SPECIES.Name]


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
    for mv in BASIC_MOVE_DATA:
        if inp.lower() == mv[BASIC_MOVE.Name].lower():
            return mv[BASIC_MOVE.Name]
    # Couldn't find it
    print("Could not identify quick move \'"+inp+"\'")
    print("Did you mean...")
    for mv in BASIC_MOVE_DATA:
        if fuzzy_string_search(inp.lower(), mv[BASIC_MOVE.Name].lower()):
            print("? "+mv[BASIC_MOVE.Name])
    print("\n")
    return input_quick_move()


def input_charge_move():
    inp = get_input("Charge Move?\n>  ")
    for mv in CHARGE_MOVE_DATA:
        if inp.lower() == mv[CHARGE_MOVE.Name].lower():
            return mv[CHARGE_MOVE.Name]
    # Couldn't find it
    print("Could not identify charge move \'"+inp+"\'")
    print("Did you mean...")
    for mv in CHARGE_MOVE_DATA:
        if fuzzy_string_search(inp.lower(), mv[CHARGE_MOVE.Name].lower()):
            print("? "+mv[CHARGE_MOVE.Name])
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
        if inp < 0 or inp > 6:
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


def input_pkmn_list_index():
    inp = get_input("Idx? \n>  ")
    try:
        inp = int(inp)
        if inp >= len(filteredList) or inp < -1:
            print("Index value \'"+str(inp)+"\' is not valid! (Should be between 0-"+str(len(filteredList)-1)+", or -1 to cancel)")
            return input_pkmn_list_index()
        else:
            return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_pkmn_list_index()


def input_pkmn_list_index_list():
    inp = get_input("Comma-separated Idx List?\n>  ")
    inp = inp.split(",")
    try:
        for i in range(len(inp)):
            inp[i] = int(inp[i].strip())
            if inp[i] >= len(filteredList) or inp[i] < -1:
                print("Index value \'"+str(inp[i])+"\' is not valid! (Should be between 0-"+str(len(filteredList)-1)+", or -1 to cancel)")
                return input_pkmn_list_index_list()
        return inp
    except ValueError:
        print("Invalid number value \'"+inp+"\'")
        return input_pkmn_list_index_list()    


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
            species = apply_yn_filter(params,input_species)
            family = get_species_data_from_species(species)[SPECIES.Family]
            filteredList = [pk for pk in filteredList if get_species_data_from_species(pk.species)[SPECIES.Family] == family]
        elif params[0] == "species": # Pokemon Species Filter
            species = apply_yn_filter(params,input_species)
            filteredList = [pk for pk in filteredList if pk.species == species]
        elif params[0] == "minCP": # Minimum CP Filter
            cp = int(apply_yn_filter(params,input_cp))
            filteredList = [pk for pk in filteredList if pk.cp >= cp ]        
        elif params[0] == "maxCP": # Minimum CP Filter
            cp = int(apply_yn_filter(params,input_cp))
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
        remember = input_remember_setting()
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
        ad = input_ascending_descending()
    else:
        print("Invalid sort configuration for \'"+" ".join(params)+"\'")
        return
    if ad == "a":
        filteredList.sort(key=sortFunc)
    else:
        filteredList.sort(key=sortFunc, reverse=True)
    currentFilter += params[0]+" "+ad




# Adapted from the spreadsheet
class SPECIES:
    Name = 0
    Family = 1
    Id = 2
    HP = 3
    Attack = 4
    Defense = 5
    Min_CP = 6 # Outdated
    Max_CP = 7
    Type1 = 8
    Type2 = 9
    Evolves_Into = 10
    Evolves_From = 11
    Quick_Moves = 12
    Charge_Moves = 13

SPECIES_DATA = [
    # Name, Family, #, HP Ratio, Attack Ratio, Defense Ratio, Min CP Cap, Max CP Cap, Type1, Type2
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
    print("Validating pokemon moves...")
    for species in SPECIES_DATA:
        for qm in species[SPECIES.Quick_Moves]:
            if _get_basic_move_by_name(qm) is None:
                print("Invalid move "+qm+" for PKMN "+species[SPECIES.Name])
        for cm in species[SPECIES.Charge_Moves]:
            if _get_charge_move_by_name(cm) is None:
                print("Invalid move "+cm+" for PKMN "+species[SPECIES.Name])

def get_id_from_species(name):
    for species in SPECIES_DATA:
            if name.lower() == species[SPECIES.Name].lower():
                return int(species[SPECIES.Id])
    return -1

def get_species_data_from_species(name):
    return SPECIES_DATA[get_id_from_species(name)-1]

def generate_all_pokemon():
    pokeList = []
    for species in SPECIES_DATA:
        count = int(species[SPECIES.Max_CP]/100)
        for cpLevel in range(count):
            cp = (cpLevel+1)*100
            # print("Creating "+species[SPECIES.Name]+" "+str(cp))

            pkmn = Pokemon()
            pkmn.species = species[SPECIES.Name]
            pkmn.IVOptions = []
            pkmn.appraisal = 2
            # pkmn.bestStat = input_bestStat()
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
            pkmn.hp = max(int(math.sqrt(Pokemon._fLvl(lvl)) * (species[SPECIES.HP] + stm)), 10)
            pkmn.cp = max(int((species[SPECIES.Attack]+atk) * math.sqrt(species[SPECIES.Defense]+dfn) * math.sqrt(species[SPECIES.HP]+stm) * Pokemon._fLvl(lvl) / 10.0), 10)
            pkmn.IVOptions = [str(lvl)+"_AAA"]
            for mv1 in species[SPECIES.Quick_Moves]:
                for mv2 in species[SPECIES.Charge_Moves]:
                    pkmn2 = Pokemon()
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
    write_pokemon_to_file(pokeList, GENERATED_POKEMON_FILE_FULL_CP_RANGE)



class BASIC_MOVE:
    ID = 0
    Name = 1
    Type = 2
    PW = 3
    Duration = 4
    NRG = 5
    NRGPS = 6
    DPS = 7

BASIC_MOVE_DATA = [
    # ID, Name,Type, PW, Duration (ms), NRG, NRGPS, DPS
    [200,"Fury Cutter","Bug",3,400,6,15,7.50],
    [201,"Bug Bite","Bug",5,450,7,15.56,11.11],
    [202,"Bite","Dark",6,500,7,14,12.00],
    [203,"Sucker Punch","Dark",7,700,9,12.86,10.00],
    [204,"Dragon Breath","Dragon",6,500,7,14,12.00],
    [205,"Thunder Shock","Electric",5,600,8,13.33,8.33],
    [206,"Spark","Electric",7,700,8,11.43,10.00],
    [207,"Low Kick","Fighting",5,600,7,11.67,8.33],
    [208,"Karate Chop","Fighting",6,800,8,10,7.50],
    [209,"Ember","Fire",10,1050,10,9.52,9.52],
    [210,"Wing Attack","Flying",9,750,7,9.33,12.00],
    [211,"Peck","Flying",10,1150,10,8.7,8.70],
    [212,"Lick","Ghost",5,500,6,12,10.00],
    [213,"Shadow Claw","Ghost",11,950,8,8.42,11.58],
    [214,"Vine Whip","Grass",7,650,7,10.77,10.77],
    [215,"Razor Leaf","Grass",15,1450,12,8.28,10.34],
    [216,"Mud Shot","Ground",6,550,7,12.73,10.91],
    [217,"Ice Shard","Ice",15,1400,12,8.57,10.71],
    [218,"Frost Breath","Ice",9,810,7,8.64,11.11],
    [219,"Quick Attack","Normal",10,1330,12,9.02,7.52],
    [220,"Scratch","Normal",6,500,7,14,12.00],
    [221,"Tackle","Normal",12,1100,10,9.09,10.91],
    [222,"Pound","Normal",7,540,7,12.96,12.96],
    [223,"Cut","Normal",12,1130,10,8.85,10.62],
    [224,"Poison Jab","Poison",12,1050,10,9.52,11.43],
    [225,"Acid","Poison",10,1050,10,9.52,9.52],
    [226,"Psycho Cut","Psychic",7,570,7,12.28,12.28],
    [227,"Rock Throw","Rock",12,1360,15,11.03,8.82],
    [228,"Metal Claw","Steel",8,630,7,11.11,12.70],
    [229,"Bullet Punch","Steel",10,1200,10,8.33,8.33],
    [230,"Water Gun","Water",6,500,7,14,12.00],
    [231,"Splash","Water",0,1230,10,8.13,0.00],
    [232,"Water Gun (Blastoise)","Water",6,500,7,14,12.00],
    [233,"Mud Slap","Ground",15,1350,12,8.89,11.11],
    [234,"Zen Headbutt","Psychic",12,1050,9,8.57,11.43],
    [235,"Confusion","Psychic",15,1510,14,9.27,9.93],
    [236,"Poison Sting","Poison",6,575,8,13.91,10.43],
    [237,"Bubble","Water",25,2300,25,10.87,10.87],
    [238,"Feint Attack","Dark",12,1040,10,9.62,11.54],
    [239,"Steel Wing","Steel",15,1330,12,9.02,11.28],
    [240,"Fire Fang","Fire",10,840,8,9.52,11.90],
    [241,"Rock Smash","Fighting",15,1410,12,8.51,10.64],
    [242,"Transform","Normal",0,1200,7,5.83,0.5], # CREATED MANUALLY, BASICALLY MADE UP, PROBABLY ALL WRONG 
]
def _get_basic_move_by_name(name):
    for mv in BASIC_MOVE_DATA:
        if name == mv[BASIC_MOVE.Name]:
            return mv
    return None


class CHARGE_MOVE:
    ID = 0
    Name = 1
    Type = 2
    PW = 3
    Duration = 4
    Crit = 5
    NRG = 6
    
CHARGE_MOVE_DATA = [
    # ID    Name    Type    PW  Duration (ms)   Crit%   NRG Cost
    [13,"Wrap","Normal",25,4000,5,20],
    [14,"Hyper Beam","Dark",120,5000,5,100],
    [16,"Dark Pulse","Poison",45,3500,5,33],
    [18,"Sludge","Normal",30,2600,5,25],
    [20,"Vice Grip","Fire",25,2100,5,20],
    [21,"Flame Wheel","Bug",40,4600,5,25],
    [22,"Megahorn","Fire",80,3200,5,100],
    [24,"Flamethrower","Ground",55,2900,5,50],
    [26,"Dig","Fighting",70,5800,5,33],
    [28,"Cross Chop","Psychic",60,2000,25,100],
    [30,"Psybeam","Ground",40,3800,5,25],
    [31,"Earthquake","Rock",100,4200,5,100],
    [32,"Stone Edge","Ice",80,3100,50,100],
    [33,"Ice Punch","Psychic",45,3500,5,33],
    [34,"Heart Stamp","Electric",25,2550,5,25],
    [35,"Discharge","Steel",35,2500,5,33],
    [36,"Flash Cannon","Flying",60,3900,5,33],
    [38,"Drill Peck","Ice",40,2700,5,33],
    [39,"Ice Beam","Ice",65,3650,5,50],
    [40,"Blizzard","Fire",100,3900,5,100],
    [42,"Heat Wave","Flying",80,3800,5,100],
    [45,"Aerial Ace","Ground",30,2900,5,25],
    [46,"Drill Run","Grass",50,3400,25,33],
    [47,"Petal Blizzard","Grass",65,3200,5,50],
    [48,"Mega Drain","Bug",25,3200,5,20],
    [49,"Bug Buzz","Poison",75,4250,5,50],
    [50,"Poison Fang","Dark",25,2400,5,20],
    [51,"Night Slash","Water",30,2700,25,25],
    [53,"Bubble Beam","Fighting",30,2900,5,25],
    [54,"Submission","Fighting",30,2100,5,33],
    [56,"Low Sweep","Water",30,2250,5,25],
    [57,"Aqua Jet","Water",25,2350,5,20],
    [58,"Aqua Tail","Grass",45,2350,5,50],
    [59,"Seed Bomb","Psychic",40,2400,5,33],
    [60,"Psyshock","Rock",40,2700,5,33],
    [62,"Ancient Power","Rock",35,3600,5,25],
    [63,"Rock Tomb","Rock",30,3400,25,25],
    [64,"Rock Slide","Rock",50,3200,5,33],
    [65,"Power Gem","Ghost",40,2900,5,33],
    [66,"Shadow Sneak","Ghost",25,3100,5,20],
    [67,"Shadow Punch","Ghost",25,2100,5,25],
    [69,"Ominous Wind","Ghost",30,3100,5,25],
    [70,"Shadow Ball","Steel",45,3080,5,33],
    [72,"Magnet Bomb","Steel",30,2800,5,25],
    [74,"Iron Head","Electric",30,2000,5,33],
    [75,"Parabolic Charge","Electric",25,2100,5,20],
    [77,"Thunder Punch","Electric",40,2400,5,33],
    [78,"Thunder","Electric",100,4300,5,100],
    [79,"Thunderbolt","Dragon",55,2700,5,50],
    [80,"Twister","Dragon",25,2700,5,20],
    [82,"Dragon Pulse","Dragon",65,3600,5,50],
    [83,"Dragon Claw","Fairy",35,1500,25,50],
    [84,"Disarming Voice","Fairy",25,3900,5,20],
    [85,"Draining Kiss","Fairy",25,2800,5,20],
    [86,"Dazzling Gleam","Fairy",55,4200,5,33],
    [87,"Moonblast","Fairy",85,4100,5,100],
    [88,"Play Rough","Poison",55,2900,5,50],
    [89,"Cross Poison","Poison",25,1500,25,25],
    [90,"Sludge Bomb","Poison",55,2600,5,50],
    [91,"Sludge Wave","Poison",70,3400,5,100],
    [92,"Gunk Shot","Ground",65,3000,5,100],
    [94,"Bone Club","Ground",25,1600,5,25],
    [95,"Bulldoze","Ground",35,3400,5,25],
    [96,"Mud Bomb","Bug",30,2600,5,25],
    [99,"Signal Beam","Bug",45,3100,5,33],
    [100,"X-Scissor","Fire",35,2100,5,33],
    [101,"Flame Charge","Fire",25,3100,5,20],
    [102,"Flame Burst","Fire",30,2100,5,25],
    [103,"Fire Blast","Water",100,4100,5,100],
    [104,"Brine","Water",25,2400,5,25],
    [105,"Water Pulse","Water",35,3300,5,25],
    [106,"Scald","Water",55,4000,5,33],
    [107,"Hydro Pump","Psychic",90,3800,5,100],
    [108,"Psychic","Psychic",55,2800,5,50],
    [109,"Psystrike","Ice",100,5100,5,100],
    [111,"Icy Wind","Grass",25,3800,5,20],
    [114,"Giga Drain","Fire",50,3600,5,33],
    [115,"Fire Punch","Grass",40,2800,5,33],
    [116,"Solar Beam","Grass",120,4900,5,100],
    [117,"Leaf Blade","Grass",55,2800,25,50],
    [118,"Power Whip","Flying",70,2800,0,100],
    [121,"Air Cutter","Flying",30,3300,25,25],
    [122,"Hurricane","Fighting",80,3200,5,100],
    [123,"Brick Break","Normal",30,1600,25,33],
    [125,"Swift","Normal",30,3000,5,25],
    [126,"Horn Attack","Normal",25,2200,5,25],
    [127,"Stomp","Normal",30,2100,5,25],
    [129,"Hyper Fang","Normal",35,2100,5,33],
    [131,"Body Slam","Normal",40,1560,5,50],
    [132,"Rest","Normal",35,3100,0,33],
    [133,"Struggle","Water",15,1695,0,20],
    [134,"Scald (Blastoise)","Water",55,4000,5,33],
    [135,"Hydro Pump (Blastoise)","Normal",90,3800,5,100],
    [136,"Wrap (Green)","Normal",25,3700,5,20],
    [137,"Wrap (Pink)","Normal",25,3700,5,20],
]
def _get_charge_move_by_name(name):
    for mv in CHARGE_MOVE_DATA:
        if name == mv[CHARGE_MOVE.Name]:
            return mv
    return None



HEX_LIST = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
def _int_to_hex(i):
    global HEX_LIST
    return HEX_LIST[i]

def _hex_to_int(i):
    global HEX_LIST
    return HEX_LIST.index(i)



TYPE_ADVANTAGE_KEYS = ["normal","fighting","flying","poison","ground","rock","bug","ghost","steel","fire","water","grass","electric","psychic","ice","dragon","dark","fairy"]
TYPE_ADVANTAGE_BONUSES = [
    [1.00,1.00,1.00,1.00,1.00,0.80,1.00,0.80,0.80,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00],
    [1.25,1.00,0.80,0.80,1.00,1.25,0.80,0.80,1.25,1.00,1.00,1.00,1.00,0.80,1.25,1.00,1.25,0.80],
    [1.00,1.25,1.00,1.00,1.00,0.80,1.25,1.00,0.80,1.00,1.00,1.25,0.80,1.00,1.00,1.00,1.00,1.00],
    [1.00,1.00,1.00,0.80,0.80,0.80,1.00,0.80,0.80,1.00,1.00,1.25,1.00,1.00,1.00,1.00,1.00,1.25],
    [1.00,1.00,0.80,1.25,1.00,1.25,0.80,1.00,1.25,1.25,1.00,0.80,1.25,1.00,1.00,1.00,1.00,1.00],
    [1.00,0.80,1.25,1.00,0.80,1.00,1.25,1.00,0.80,1.25,1.00,1.00,1.00,1.00,1.25,1.00,1.00,1.00],
    [1.00,0.80,0.80,0.80,1.00,1.00,1.00,0.80,0.80,0.80,1.00,1.25,1.00,1.25,1.00,1.00,1.25,0.80],
    [0.80,1.00,1.00,1.00,1.00,1.00,1.00,1.25,1.00,1.00,1.00,1.00,1.00,1.25,1.00,1.00,0.80,1.00],
    [1.00,1.00,1.00,1.00,1.00,1.25,1.00,1.00,0.80,0.80,0.80,1.00,0.80,1.00,1.25,1.00,1.00,1.25],
    [1.00,1.00,1.00,1.00,1.00,0.80,1.25,1.00,1.25,0.80,0.80,1.25,1.00,1.00,1.25,0.80,1.00,1.00],
    [1.00,1.00,1.00,1.00,1.25,1.25,1.00,1.00,1.00,1.25,0.80,0.80,1.00,1.00,1.00,0.80,1.00,1.00],
    [1.00,1.00,0.80,0.80,1.25,1.25,0.80,1.00,0.80,0.80,1.25,0.80,1.00,1.00,1.00,0.80,1.00,1.00],
    [1.00,1.00,1.25,1.00,0.80,1.00,1.00,1.00,1.00,1.00,1.25,0.80,0.80,1.00,1.00,0.80,1.00,1.00],
    [1.00,1.25,1.00,1.25,1.00,1.00,1.00,1.00,0.80,1.00,1.00,1.00,1.00,0.80,1.00,1.00,0.80,1.00],
    [1.00,1.00,1.25,1.00,1.25,1.00,1.00,1.00,0.80,0.80,0.80,1.25,1.00,1.00,0.80,1.25,1.00,1.00],
    [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,0.80,1.00,1.00,1.00,1.00,1.00,1.00,1.25,1.00,0.80],
    [1.00,0.80,1.00,1.00,1.00,1.00,1.00,1.25,1.00,1.00,1.00,1.00,1.00,1.25,1.00,1.00,0.80,0.80],
    [1.00,1.25,1.00,0.80,1.00,1.00,1.00,1.00,0.80,0.80,1.00,1.00,1.00,1.00,1.00,1.25,1.25,1.00],
]

def get_ratio_from_types(type1,type2):
    try:
        idx_type1 = TYPE_ADVANTAGE_KEYS.index(type1.lower())
        idx_type2 = TYPE_ADVANTAGE_KEYS.index(type2.lower())
        return TYPE_ADVANTAGE_BONUSES[idx_type1][idx_type2]
    except ValueError:
        return 1


read_pokemon()
write_pokemon()
run()

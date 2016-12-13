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
import Data.species as Species
import Data.moves as Moves


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
        speciesData = Species.Species(self.species)
        baseAtk = int(speciesData.Attack)
        baseDef = int(speciesData.Defense)
        baseStm = int(speciesData.HP)
        if self.dust != -1: 
            baseLvl = UInp.LEVELS_FOR_DUST_VALUES[UInp.VALID_DUST_VALUES.index(self.dust)]
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
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration] # $AB2
        mv1Power = mv1Data[Moves.BASIC_MOVE.PW] # $Z2
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG] # $AD2
        mv2STAB = 1.25 if mv2Type == speciesData[SPECIES.Type1] or mv2Type == speciesData[SPECIES.Type2] else 1.0 # $Y2
        mv2PowerScaled = mv2Power*get_ratio_from_types(mv2Type, type1)*get_ratio_from_types(mv2Type, type2) # AP2
        mv2STAB = 1.25 if mv2Type == speciesData[SPECIES.Type1] or mv2Type == speciesData[SPECIES.Type2] else 1.0 # $Y2
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration] # $AC2
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG] # $AE2
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit] # $AF2
        critDamageBonusConstant = 0.0 # 'Showing Work'!$AM$1
        chargeDelayConstant = 500 # 'Showing Work'!$AO$1
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain,1) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain) # IF(mv2NrgCost=100,CEILING(mv2NrgCost/mv1NrgGain,1),mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant) # $AG2
    """
    
    def calculate_duel_score_for_types(self, type1, type2):
        speciesData = Species.Species(self.species)
        mv1Data = _get_basic_move_by_name(self.move_one)
        mv1Power = mv1Data[Moves.BASIC_MOVE.PW]
        mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
        mv1PowerScaled = mv1Power*get_ratio_from_types(mv1Type, type1)*get_ratio_from_types(mv1Type, type2)
        mv1STAB = 1.25 if mv1Type == speciesData.Type1 or mv1Type == speciesData.Type2 else 1.0
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG]
        mv2Data = _get_charge_move_by_name(self.move_two)
        mv2Power = mv2Data[Moves.CHARGE_MOVE.PW]
        mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
        mv2PowerScaled = mv2Power*get_ratio_from_types(mv2Type, type1)*get_ratio_from_types(mv2Type, type2)
        mv2STAB = 1.25 if mv2Type == speciesData.Type1 or mv2Type == speciesData.Type2 else 1.0
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit]
        noWeaveDmg = (mv1PowerScaled*(mv1STAB))*math.floor(100000/mv1Speed)
        critDamageBonusConstant = 0.0
        chargeDelayConstant = 500
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant)
        flWeaveTime = math.floor(100000/weaveCycleLengthTime)
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio)*(mv1PowerScaled*(mv1STAB))+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio)*mv1Speed))/mv1Speed)*(mv1PowerScaled*(mv1STAB))
        baseAttack = speciesData.Attack
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
            defSpeciesData = Species.Species(defender.species)
            m1 = defender.move_one
            m2 = defender.move_two
            if m1 == "": 
                bm = defSpeciesData.Quick_Moves
            else:
                bm = [m1]
            if m2 == "": 
                cm = defSpeciesData.Charge_Moves
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


        atkSpeciesData = Species.Species(attacker.species)
        defSpeciesData = Species.Species(defender.species)
        atkIVs = attacker.get_IVs()
        defIVs = defender.get_IVs()
        
        # Attacker's Tankiness
        atkTankiness = attacker.hp
        # print(atkTankiness)

        # Defenders's Tankiness
        if defender.hp != -1:
            defTankiness = 2 * defender.hp
        else:
            defTankiness = 2 * max(int(math.sqrt(Pokemon._fLvl(defender.get_level())) * (defSpeciesData.HP + defIVs[2])), 10)
        # print(defTankiness)


        critDamageBonusConstant = 0.0
        chargeDelayConstant = 500

        # Attacker's Damage
        mv1Data = Moves._get_basic_move_by_name(attacker.move_one)
        mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == atkSpeciesData.Type1 or mv1Type == atkSpeciesData.Type2 else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData.Attack+atkIVs[0])/(defSpeciesData.Defense+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())/Pokemon._fLvl(defender.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, defSpeciesData.Type1)*get_ratio_from_types(mv1Type, defSpeciesData.Type2)) * # Type
            mv1Data[Moves.BASIC_MOVE.PW]
            )
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG]
        # print("Power1:"+str(mv1PowerScaled))

        mv2Data = Moves._get_charge_move_by_name(attacker.move_two)
        mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == atkSpeciesData.Type1 or mv2Type == atkSpeciesData.Type2 else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData.Attack+atkIVs[0])/(defSpeciesData.Defense+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())/Pokemon._fLvl(defender.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, defSpeciesData.Type1)*get_ratio_from_types(mv2Type, defSpeciesData.Type2)) * # Type
            mv2Data[Moves.BASIC_MOVE.PW]
            )
        # print("Power2:"+str(mv2PowerScaled))
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit]
        noWeaveDmg = (mv1PowerScaled)*math.floor(100000/mv1Speed)
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant)
        flWeaveTime = math.floor(100000/weaveCycleLengthTime)
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio)*(mv1PowerScaled)+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio)*mv1Speed))/mv1Speed)*(mv1PowerScaled)
        atkDmg = max(noWeaveDmg,weaveDmg)
        # print(atkDmg)

        # Defender's Damage
        mv1Data = Moves._get_basic_move_by_name(defender.move_one)
        mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == defSpeciesData.Type1 or mv1Type == defSpeciesData.Type2 else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData.Attack+defIVs[0])/(atkSpeciesData.Defense+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, atkSpeciesData.Type1)*get_ratio_from_types(mv1Type, atkSpeciesData.Type2)) * # Type
            mv1Data[Moves.BASIC_MOVE.PW]
            )
        # print("Power1:"+str(mv1PowerScaled))
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG]
        mv2Data = Moves._get_charge_move_by_name(defender.move_two)
        mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == defSpeciesData.Type1 or mv2Type == defSpeciesData.Type2 else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData.Attack+defIVs[0])*1.0/(atkSpeciesData.Defense+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, atkSpeciesData.Type1)*get_ratio_from_types(mv2Type, atkSpeciesData.Type2)) * # Type
            mv2Data[Moves.BASIC_MOVE.PW]
            )
        # print("Power2:"+str(mv2PowerScaled))
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit]

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
        speciesData = Species.Species(self.species)
        baseHP = speciesData.HP
        baseDefence = speciesData.Defense
        ratioT1_1 = get_ratio_from_types(type1, speciesData.Type1)
        ratioT1_2 = get_ratio_from_types(type1, speciesData.Type2)
        ratioT2_1 = get_ratio_from_types(type2, speciesData.Type1)
        ratioT2_2 = get_ratio_from_types(type2, speciesData.Type2)
        tankiness = baseHP*baseDefence/ratioT1_1/ratioT1_2/ratioT2_1/ratioT2_2
        return tankiness

    def calculate_gym_defence_score_for_types(self, type1, type2):
        print('Implement')




    def id(self):
        return Species.get_id_from_species(self.species)

PKMN_FILE = "Lists/PoGoCollection.txt"
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


def run():
    global pkmnList
    global filteredList
    global currentFilter
    while True:
        cmd = UInp.get_input(interface).lower()

        clear_screen()

        # Add Pokemon
        if cmd == "a":
            print("Adding new pokemon to the Collection")
            pkmn = Pokemon()
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
            filteredIdxList = UInp.input_pkmn_list_index(len(filteredList))            
            pkmn = filteredList[filteredIdxList]
            clear_screen()
            edit_pokemon(pkmn)
            print("\n")
            pkmn.calculate_iv_options()
            write_pokemon()
            print("Updated "+pkmn.species)


        # Mark Pokemon
        elif cmd == "m":
            cmd = UInp.get_input(mark_pokemon_interface).lower()
            if cmd == "t":
                loop_species = "NONE"
                for pkmn in pkmnList:
                    if pkmn.species != loop_species:
                        pkmn.marked = True
                        loop_species = pkmn.species
            elif cmd == "n":
                inp_name = UInp.get_input("Name?\n>  ")
                for pkmn in pkmnList:
                    if pkmn.name == inp_name:
                        pkmn.marked = True
            elif cmd == "s":
                inp_species = UInp.input_species()
                for pkmn in pkmnList:
                    if pkmn.species == inp_species:
                        pkmn.marked = True
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
                        pkmn.marked = True

            elif cmd == "em":
                for pkmn in pkmnList:
                    species = Species.Species(pkmn.species)
                    if species.Evolves_Into[0] == "":
                        pkmn.marked = True
            elif cmd == "en":
                for pkmn in pkmnList:
                    species = Species.Species(pkmn.species)
                    if species.Evolves_Into[0] != "":
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
            write_pokemon()

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
                    pkmn = Pokemon()
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

            pkmn = Pokemon()
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

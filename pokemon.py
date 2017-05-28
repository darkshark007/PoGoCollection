import Data.species as Species
import Data.moves as Moves
import user_input as UInp
import math

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
        self.skin = ""

        # Calculated Properties
        self.IVOptions = []
        self.minIV = 0
        self.maxIV = 45
        self.strengths = []
        self.weaknesses = []
        self.marked = False
        self.typeAdvantages = None

    def clone(self):
        pk = Pokemon()
        pk.name = self.name
        pk.species = self.species
        pk.cp = self.cp
        pk.hp = self.hp
        pk.dust = self.dust
        pk.move_one = self.move_one
        pk.move_two = self.move_two
        pk.appraisal = self.appraisal
        pk.bestStat = self.bestStat
        pk.statLevel = self.statLevel
        pk.skin = self.skin

        # Calculated Properties
        pk.IVOptions = [s for s in self.IVOptions]
        pk.minIV = self.minIV
        pk.maxIV = self.maxIV
        pk.strengths = self.strengths
        pk.weaknesses = self.weaknesses
        pk.marked = self.marked
        return pk


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
        if count == 0:
            species = Species.Species(self.species)
            count = 1
            countSum = (((((self.cp-10)/(species.Max_CP-10))*79))/2)+1
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
        score_payload = {
            'attacker': attacker,
            'defender': defender,
            'atk_m1_power': 0,
            'atk_m2_power': 0,
            'atk_noweave_dmg': 0,
            'atk_weave_dmg': 0,
            'atk_tankiness': 0,
            'def_m1_power': 0,
            'def_m2_power': 0,
            'def_dmg': 0,
            'def_tankiness': 0,
            'atk_score': 0,
            'def_score': 0,
            'gym_score': 0,
        }

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
            worstCase = { 'gym_score': 1000 }
            for testMove1 in bm:
                for testMove2 in cm:
                    defender.move_one = testMove1
                    defender.move_two = testMove2
                    result = Pokemon.calculate_gym_attack_score_for_combatants(attacker, defender)
                    if result['gym_score'] < worstCase['gym_score']:
                        worstCase = result

            defender.move_one = m1
            defender.move_two = m2
            return worstCase


        atkSpeciesData = Species.Species(attacker.species)
        defSpeciesData = Species.Species(defender.species)
        atkIVs = attacker.get_IVs()
        defIVs = defender.get_IVs()
        
        # Attacker's Tankiness
        atkTankiness = attacker.hp
        score_payload['atk_tankiness'] = atkTankiness

        # Defenders's Tankiness
        if defender.hp != -1:
            defTankiness = 2 * defender.hp
        else:
            defTankiness = 2 * max(int(math.sqrt(Pokemon._fLvl(defender.get_level())) * (defSpeciesData.HP + defIVs[2])), 10)
        score_payload['def_tankiness'] = defTankiness


        critDamageBonusConstant = 0.0
        chargeDelayConstant = 500

        # Attacker's Damage
        mv1Data = Moves._get_basic_move_by_name(attacker.move_one)
        mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == atkSpeciesData.Type1 or mv1Type == atkSpeciesData.Type2 else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData.Attack+atkIVs[0])*1.0/(defSpeciesData.Defense+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())*1.0/Pokemon._fLvl(defender.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, defSpeciesData.Type1)*get_ratio_from_types(mv1Type, defSpeciesData.Type2)) * # Type
            mv1Data[Moves.BASIC_MOVE.PW]
            )
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG]
        if mv1NrgGain is 0:
            mv1NrgGain = 0.000001
        mv2Data = Moves._get_charge_move_by_name(attacker.move_two)
        mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == atkSpeciesData.Type1 or mv2Type == atkSpeciesData.Type2 else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((atkSpeciesData.Attack+atkIVs[0])*1.0/(defSpeciesData.Defense+defIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(attacker.get_level())*1.0/Pokemon._fLvl(defender.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, defSpeciesData.Type1)*get_ratio_from_types(mv2Type, defSpeciesData.Type2)) * # Type
            mv2Data[Moves.BASIC_MOVE.PW]
            )
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit]
        noWeaveDmg = (mv1PowerScaled)*math.floor(100000/mv1Speed)
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        weaveCycleLengthTime = nrgRatio*mv1Speed+(mv2Speed+chargeDelayConstant)
        flWeaveTime = math.floor(100000/weaveCycleLengthTime)
        weaveDmg = flWeaveTime*(mv2PowerScaled*(mv2STAB)*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(flWeaveTime*nrgRatio)*(mv1PowerScaled)+math.floor((100000-(flWeaveTime*(mv2Speed+chargeDelayConstant)+math.ceil(flWeaveTime*nrgRatio)*mv1Speed))/mv1Speed)*(mv1PowerScaled)
        atkDmg = max(noWeaveDmg,weaveDmg)
        # print("M1")
        # print("  PWS: "+str(mv1PowerScaled))
        # print("  ADScale: "+str(((atkSpeciesData.Attack+atkIVs[0])*1.0/(defSpeciesData.Defense+defIVs[1]))))
        # print("  CPM: "+str((Pokemon._fLvl(attacker.get_level())/Pokemon._fLvl(defender.get_level()))))
        # print("  STAB: "+str(mv1STAB))
        # print("  Type: "+str((get_ratio_from_types(mv1Type, defSpeciesData.Type1)*get_ratio_from_types(mv1Type, defSpeciesData.Type2))))
        # print("  Base: "+str(mv1Data[Moves.BASIC_MOVE.PW]))
        score_payload['atk_m1_power'] = mv1PowerScaled
        score_payload['atk_m2_power'] = mv2PowerScaled
        score_payload['atk_noweave_dmg'] = noWeaveDmg
        score_payload['atk_weave_dmg'] = weaveDmg


        # Defender's Damage
        mv1Data = Moves._get_basic_move_by_name(defender.move_one)
        mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
        mv1STAB = 1.25 if mv1Type == defSpeciesData.Type1 or mv1Type == defSpeciesData.Type2 else 1.0
        mv1PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData.Attack+defIVs[0])*1.0/(atkSpeciesData.Defense+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())*1.0/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv1STAB *
            (get_ratio_from_types(mv1Type, atkSpeciesData.Type1)*get_ratio_from_types(mv1Type, atkSpeciesData.Type2)) * # Type
            mv1Data[Moves.BASIC_MOVE.PW]
            )
        mv1Speed = mv1Data[Moves.BASIC_MOVE.Duration]
        mv1NrgGain = mv1Data[Moves.BASIC_MOVE.NRG]
        mv2Data = Moves._get_charge_move_by_name(defender.move_two)
        mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
        mv2STAB = 1.25 if mv2Type == defSpeciesData.Type1 or mv2Type == defSpeciesData.Type2 else 1.0
        mv2PowerScaled = 1 + math.floor(
            0.5 * 
            ((defSpeciesData.Attack+defIVs[0])*1.0/(atkSpeciesData.Defense+atkIVs[1])) * # Attack/Defense
            (Pokemon._fLvl(defender.get_level())*1.0/Pokemon._fLvl(attacker.get_level())) * # CPM
            mv2STAB *
            (get_ratio_from_types(mv2Type, atkSpeciesData.Type1)*get_ratio_from_types(mv2Type, atkSpeciesData.Type2)) * # Type
            mv2Data[Moves.BASIC_MOVE.PW]
            )
        mv2Speed = mv2Data[Moves.CHARGE_MOVE.Duration]
        mv2NrgCost = mv2Data[Moves.CHARGE_MOVE.NRG]
        mv2CritChance = mv2Data[Moves.CHARGE_MOVE.Crit]
        nrgRatio = math.ceil(mv2NrgCost/mv1NrgGain) if mv2NrgCost == 100 else (mv2NrgCost/mv1NrgGain)
        gymWeaveCycleLengthValue = math.floor(100000/(nrgRatio*(mv1Speed+2000)+(mv2Speed+chargeDelayConstant)))
        defDmg = gymWeaveCycleLengthValue*(mv2PowerScaled*(1+(critDamageBonusConstant*mv2CritChance/100)))+math.ceil(gymWeaveCycleLengthValue*nrgRatio)*mv1PowerScaled+math.floor((100000-(gymWeaveCycleLengthValue*(mv2Speed+chargeDelayConstant)+math.ceil(gymWeaveCycleLengthValue*nrgRatio)*(mv1Speed+2000)))/(mv1Speed+2000))*mv1PowerScaled
        score_payload['def_m1_power'] = mv1PowerScaled
        score_payload['def_m2_power'] = mv2PowerScaled
        score_payload['def_dmg'] = defDmg


        # Calculate the scores
        atkScore = defTankiness/atkDmg
        defScore = atkTankiness/defDmg
        score = defScore/atkScore
        score_payload['atk_score'] = atkScore
        score_payload['def_score'] = defScore
        score_payload['gym_score'] = score

        # print(
        #     "Atk: CP "+str(attacker.cp)+" "+attacker.name+" ("+attacker.species+")("+attacker.move_one+"/"+attacker.move_two+")  "+
        #     "vs  "+
        #     "Def: CP "+str(defender.cp)+" "+defender.species+" ("+defender.move_one+"/"+defender.move_two+")  "+
        #     " || "+
        #     "Atk_dmg: "+str(score_payload['atk_noweave_dmg'])+"/"+str(score_payload['atk_weave_dmg'])+"   "+
        #     "Atk_tankiness: "+str(score_payload['atk_tankiness'])+"   "+
        #     " || "+
        #     "Def_dmg: "+str(score_payload['def_dmg'])+"   "+
        #     "Def_tankiness: "+str(score_payload['def_tankiness'])+"   "+
        #     "")
        return score_payload


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

    def calculate_type_advantages(self):
        if self.typeAdvantages is not None:
            return self.typeAdvantages

        # print(self.name+"/"+self.species+"/"+str(self.cp)+"  "+self.move_one+"/"+self.move_two)
        speciesData = Species.Species(self.species)
        payload = {
            "min_score": 2000,
            "max_score": 0
        }
        for t in TYPE_ADVANTAGE_KEYS:
            entry = {}
            # print("for type "+t)
            
            def_score = get_ratio_from_types(speciesData.Type1,t)*get_ratio_from_types(speciesData.Type2,t)
            entry["def_score"] = def_score
            # print("  def_score:  "+str(def_score))

            mv1Data = Moves._get_basic_move_by_name(self.move_one)
            mv1Type = mv1Data[Moves.BASIC_MOVE.Type]
            atk_score_1 = get_ratio_from_types(mv1Type,t)
            if mv1Type == speciesData.Type1 or mv1Type == speciesData.Type2:
                atk_score_1 *= 1.25
            entry["atk_score_1"] = atk_score_1
            # print("  atk_score_1:  "+str(atk_score_1))

            mv2Data = Moves._get_charge_move_by_name(self.move_two)            
            mv2Type = mv2Data[Moves.CHARGE_MOVE.Type]
            atk_score_2 = get_ratio_from_types(mv2Type,t)
            if mv2Type == speciesData.Type1 or mv2Type == speciesData.Type2:
                atk_score_2 *= 1.25
            entry["atk_score_2"] = atk_score_2
            # print("  atk_score_2:  "+str(atk_score_2))

            overall_score = ((atk_score_1 + atk_score_2)/2.0)*def_score
            entry["overall_score"] = overall_score
            # print("  overall_score:  "+str(overall_score))

            if overall_score > payload["max_score"]:
                payload["max_score"] = overall_score
            payload[t] = entry
        
        self.typeAdvantages = payload
        return self.typeAdvantages



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

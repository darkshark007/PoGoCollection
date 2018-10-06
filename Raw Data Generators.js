for (var k in pkdata.itemTemplates) {
	var current = pkdata.itemTemplates[k];
	console.log(current.templateId);
}


function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function generateSpeciesData() {
	var output = "# Adapted from the GAME_MASTER_FILE Json Output at:\n# https://github.com/BrunnerLivio/pokemongo-game-master\n# https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/GAME_MASTER.json\nRAW_SPECIES_DATA = [\n";
	// Index them
	var index = {};
	for (var k in pkdata.itemTemplates) {
		var current = pkdata.itemTemplates[k];
		if (!current.hasOwnProperty("pokemonSettings")) continue;
		var idNum = parseInt(current.templateId.substring(1,5));
		var name = toTitleCase(current.templateId.substring(14));
		current.idNum = idNum;
		if (current.idNum === 29) name = "Nidoran F";
		if (current.idNum === 32) name = "Nidoran M";
		index[idNum] = current;
		index[name] = current;
	}
	console.log(index);
	for (var k in index) {
		if (k*0 === 0) continue;
		var current = index[k];
		var name = toTitleCase(current.templateId.substring(14));
		if (current.idNum === 29) name = "Nidoran F";
		if (current.idNum === 32) name = "Nidoran M";
		if (current.idNum === 122) name = "Mr Mime";
		if (current.idNum === 250) name = "Ho-oh";
		var familyName = toTitleCase(current.pokemonSettings.familyId.substring(7));

		var familyId;
		if (familyName === "Nidoran_female") {
			familyId = 29;
			familyName = "Nidoran F";
		} else if (familyName === "Nidoran_male") {
			familyId = 32;
			familyName = "Nidoran M";
		} else {
			familyId = index[familyName].idNum;
		}
		var formSplit = name.split('_');
		if (formSplit.length === 2) {
			familyId = familyId+"_"+formSplit[1]
		}
		var stam = current.pokemonSettings.stats.baseStamina;
		var atk = current.pokemonSettings.stats.baseAttack;
		var def = current.pokemonSettings.stats.baseDefense;
		var minCP = Math.max(Math.floor((atk) * Math.sqrt(stam) * Math.sqrt(def) * 0.62903351 / 10,1), 10);
		var maxCP = Math.max(Math.floor((atk+15) * Math.sqrt(stam+15) * Math.sqrt(def+15) * 0.62903351 / 10,1), 10);
		var type1 = current.pokemonSettings.type || "POKEMON_TYPE_"; type1 = type1.substring(13); type1 = toTitleCase(type1);
		var type2 = current.pokemonSettings.type2 || "POKEMON_TYPE_"; type2 = type2.substring(13); type2 = toTitleCase(type2);
		var evoString;
		if (!current.pokemonSettings.evolutionBranch) {
			evoString = "[\"\"]";
		} else {
			evoString = "["
			for (k2 in current.pokemonSettings.evolutionBranch) {
				var currentEvolution = current.pokemonSettings.evolutionBranch[k2];
				evoString += "\""+toTitleCase(currentEvolution.evolution)+"\",";
			}
			evoString = evoString.substring(0,evoString.length-1);
			evoString += "]";
		}
		var parent;
		if (!current.pokemonSettings.parentPokemonId) {
			parent = "\"\"";
		} else {
			parent = "\""+toTitleCase(current.pokemonSettings.parentPokemonId)+"\"";
			if (parent === "\"Nidoran_female\"") parent = "\"Nidoran F\"";
			if (parent === "\"Nidoran_male\"") parent = "\"Nidoran M\"";
		}
		var fastMoveString = "[";
		for (k2 in current.pokemonSettings.quickMoves) {
			var currentMove = current.pokemonSettings.quickMoves[k2];
			fastMoveString += "\""+toTitleCase(currentMove.substring(0,currentMove.length-5).replace("_"," "))+"\", ";
		}
		fastMoveString = fastMoveString.substring(0,fastMoveString.length-2)+"]";
		var chargeMoveString = "[";
		for (k2 in current.pokemonSettings.cinematicMoves) {
			var currentMove = current.pokemonSettings.cinematicMoves[k2];
			if (currentMove === "X_SCISSOR") {
				currentMove = "X-Scissor";
			} else {
				currentMove = toTitleCase(currentMove.replace("_"," "));
			}
			chargeMoveString += "\""+currentMove+"\", ";
		}
		chargeMoveString = chargeMoveString.substring(0,chargeMoveString.length-2)+"]";

		output += "    [";
		output += "\""+name+"\","; // Species name
		output += "\""+familyId+"\","; // Family id num
		output += current.idNum+","; // Species id num
		output += stam +","; // Base stamina
		output += atk+","; // Base attack
		output += def+","; // Base defense
		output += minCP+","; // Minimum CP
		output += maxCP+","; // Maximum CP
		output += "\""+type1+"\","; // Type 1
		output += "\""+type2+"\","; // Type 2
		output += evoString+","; // Evolutions
		output += parent+","; // Parent Species
		output += fastMoveString+","; // Fast moves
		output += chargeMoveString; // Fast moves
		output += "],\n";
	}
	output += "]\n";
	return output;
}


function generateFastmoveData() {
	var output = "BASIC_MOVE_DATA = [\n    # ID, Name,Type, PW, Duration (ms), NRG, NRGPS, DPS\n";
	for (var k in pkdata.itemTemplates) {
		var current = pkdata.itemTemplates[k];
		if (!current.hasOwnProperty("moveSettings") || current.moveSettings.movementId.indexOf("_FAST") === -1) continue;

		var idNum = parseInt(current.templateId.substring(1,5));
		var name = current.moveSettings.movementId.replace("_FAST","").replace("_"," ").replace("_"," ");
		name = toTitleCase(name);
		var type = toTitleCase(current.moveSettings.pokemonType.replace("POKEMON_TYPE_",""));
		var power = current.moveSettings.power || 0;
		var nrg = current.moveSettings.energyDelta || 0;
		var duration = current.moveSettings.durationMs/1000;
		var nrgps = (1/duration)*nrg;
		var dps = (1/duration)*power;

		output += "    [";
		output += idNum+",";
		output += "\""+name+"\",";
		output += "\""+type+"\",";
		output += power+",";
		output += current.moveSettings.durationMs+",";
		output += nrg+",";
		output += nrgps+",";
		output += dps;
		output += "],\n";
	}
	output += "]\n";
	return output;
}


function generateChargemoveData() {
	var output = "CHARGE_MOVE_DATA = [\n    # ID    Name    Type    PW  Duration (ms)   Crit%   NRG Cost\n";

	for (var k in pkdata.itemTemplates) {
		var current = pkdata.itemTemplates[k];
		if (!current.hasOwnProperty("moveSettings") || current.moveSettings.movementId.indexOf("_FAST") !== -1) continue;

		var idNum = parseInt(current.templateId.substring(1,5));
		var name = current.moveSettings.movementId.replace("_"," ").replace("_"," ");
		name = toTitleCase(name);
		if (name === "X Scissor") name = "X-Scissor";
		var type = toTitleCase(current.moveSettings.pokemonType.replace("POKEMON_TYPE_",""));
		var power = current.moveSettings.power || 0;
		var nrg = current.moveSettings.energyDelta || 0;


		output += "    [";
		output += idNum+",";
		output += "\""+name+"\",";
		output += "\""+type+"\",";
		output += power+",";
		output += current.moveSettings.durationMs+",";
		output += "5,";
		output += (-1*nrg);
		output += "],\n";
	}
	output += "]\n";
	return output;
}


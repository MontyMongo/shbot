from src.SH.definitions import *

def generate_preset(flags=None):
    data = {

    }
    players = flags["players"]

    _startingComponents = {
		"premise"      : "default",
		"tracker"      : "default",
		"nomination"   : "default",
		"voting"       : "default",
		"passed_gov"   : "default",
		"failed_gov"   : "default",
		"legislative"  : "default",
		"post_policy"  : "no_op",
		"policy_power" : "empty"
	}

    if "gamemode" in flags:
        _startingComponents["premise"] = "avalon"
    if "nodoubletd" in flags:
        _startingComponents["tracker"] = "no_double_td"

    _libBoard = ["empty"] * 5
    _fasBoard = ["empty"] * 6
    _fasBoard[3] = "execute"
    _fasBoard[4] = "execute"
    if players == 5 or players == 6:
        _fasBoard[2] = "peek_three"
    elif players == 7 or players == 8:
        _fasBoard[1] = "investigation"
        _fasBoard[2] = "special_elect"
    elif players == 9 or players == 10:
        _fasBoard[1] = "investigation"
        _fasBoard[1] = "investigation"
        _fasBoard[2] = "special_elect"
    
    _boards = {
        LIBERAL_POLICY: _libBoard,
        FASCIST_POLICY: _fasBoard
    }

    data["STARTING_COMPONENTS"] = _startingComponents
    data["BOARDS"] = _boards
    data["HZ_ENTRY"] = 3
    if "hz" in flags:
        _hz_entry = flags["hz"]
        if _hz_entry in [1, 2, 3, 4, 5, 6]:
            data["HZ_ENTRY"] = _hz_entry
    data["VZ_ENTRY"] = 5
    if "vz" in flags:
        _vz_entry = flags["vz"]
        if _vz_entry in [1, 2, 3, 4, 5, 6]:
            data["VZ_ENTRY"] = _vz_entry
        
    
    # any other game-wide constants should go here.
    return data
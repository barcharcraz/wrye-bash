# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2015 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""This module defines static data for use by other modules in the Wrye Bash package.
Its use should generally be restricted to large chunks of data and/or chunks of data
that are used by multiple objects."""

# Imports ---------------------------------------------------------------------
import collections
import struct
from . import game as game_init
from .bolt import GPath, Path, deprint
from .env import get_game_path
from .exception import BoltError

# Game detection --------------------------------------------------------------
game = None         # type: game_init
gamePath = None     # absolute bolt Path to the game directory
foundGames = {}     # 'name':Path dict used by the Settings switch game menu

# Module Cache
_allGames={} # 'name'->module
_registryGames={} # 'name'->path
_fsName_display = {}
_display_fsName = {}

def _supportedGames(useCache=True):
    """Set games supported by Bash and return their paths from the registry."""
    if useCache and _allGames: return _registryGames.copy()
    # rebuilt cache
    _allGames.clear()
    _registryGames.clear()
    _fsName_display.clear()
    _display_fsName.clear()
    import pkgutil
    # Detect the known games
    for importer, modname, ispkg in pkgutil.iter_modules(game_init.__path__):
        if not ispkg: continue # game support modules are packages
        # Equivalent of "from game import <modname>"
        try:
            module = __import__('game',globals(),locals(),[modname],-1)
            submod = getattr(module,modname)
            _allGames[submod.fsName] = submod
            _fsName_display[submod.fsName] = submod.displayName
            #--Get this game's install path
            game_path = get_game_path(submod)
        except (ImportError, AttributeError):
            deprint('Error in game support module:', modname, traceback=True)
            continue
        if game_path: _registryGames[submod.fsName] = game_path
        del module
    # unload some modules, _supportedGames is meant to run once
    del pkgutil
    _display_fsName.update({v: k for k, v in _fsName_display.items()})
    deprint('Detected the following supported games via Windows Registry:')
    for foundName in _registryGames:
        deprint(' %s:' % foundName, _registryGames[foundName])
    return _registryGames.copy()

def _detectGames(cli_path='', bash_ini_=None):
    """Detect which supported games are installed.

    - If Bash supports no games raise.
    - For each game supported by Bash check for a supported game executable
    in the following dirs, in decreasing precedence:
       - the path provided by the -o cli argument if any
       - the sOblivionPath Bash Ini entry if present
       - one directory up from Mopy
    If a game exe is found update the path to this game and return immediately.
    Return (foundGames, name)
      - foundGames: a dict from supported games to their paths (the path will
      default to the windows registry path to the game, if present)
      - name: the game found in the first installDir or None if no game was
      found - a 'suggestion' for a game to use (if no game is specified/found
      via -g argument).
    """
    #--Find all supported games and all games in the windows registry
    foundGames_ = _supportedGames() # sets _allGames if not set
    if not _allGames: # if allGames is empty something goes badly wrong
        raise BoltError(_('No game support modules found in Mopy/bash/game.'))
    # check in order of precedence the -o argument, the ini and our parent dir
    installPaths = collections.OrderedDict() #key->(path, found msg, error msg)
    #--First: path specified via the -o command line argument
    if cli_path != '':
        test_path = GPath(cli_path)
        if not test_path.isabs():
            test_path = Path.getcwd().join(test_path)
        installPaths['cmd'] = (test_path,
            _('Set game mode to %(gamename)s specified via -o argument') +
              ': ',
            _('No known game in the path specified via -o argument: ' +
              '%(path)s'))
    #--Second: check if sOblivionPath is specified in the ini
    if bash_ini_ and bash_ini_.has_option('General', 'sOblivionPath') \
               and not bash_ini_.get('General', 'sOblivionPath') == '.':
        test_path = GPath(bash_ini_.get('General', 'sOblivionPath').strip())
        if not test_path.isabs():
            test_path = Path.getcwd().join(test_path)
        installPaths['ini'] = (test_path,
            _('Set game mode to %(gamename)s based on sOblivionPath setting '
              'in bash.ini') + ': ',
            _('No known game in the path specified in sOblivionPath ini '
              'setting: %(path)s'))
    #--Third: Detect what game is installed one directory up from Mopy
    test_path = Path.getcwd()
    if test_path.cs[-4:] == 'mopy':
        test_path = GPath(test_path.s[:-5])
        if not test_path.isabs():
            test_path = Path.getcwd().join(test_path)
        installPaths['upMopy'] = (test_path,
            _('Set game mode to %(gamename)s found in parent directory of'
              ' Mopy') + ': ',
            _('No known game in parent directory of Mopy: %(path)s'))
    #--Detect
    deprint('Detecting games via the -o argument, bash.ini and relative path:')
    # iterate installPaths in insert order ('cmd', 'ini', 'upMopy')
    for test_path, foundMsg, errorMsg in installPaths.values():
        for name, module in list(_allGames.items()):
            if test_path.join(module.exe).exists():
                # Must be this game
                deprint(foundMsg % {'gamename':name}, test_path)
                foundGames_[name] = test_path
                return foundGames_, name
        # no game exe in this install path - print error message
        deprint(errorMsg % {'path': test_path.s})
    # no game found in installPaths - foundGames are the ones from the registry
    return foundGames_, None

def __setGame(name, msg):
    """Set bush game globals - raise if they are already set."""
    global gamePath, game
    if game is not None: raise BoltError('Trying to reset the game')
    gamePath = foundGames[name]
    game = _allGames[name]
    deprint(msg % {'gamename': name}, gamePath)
    # Unload the other modules from the cache
    for i in list(_allGames.keys()):
        if i != name: del _allGames[i]
    game.init()

def detect_and_set_game(cli_game_dir='', bash_ini_=None, name=None):
    if name is None: # detect available games
        foundGames_, name = _detectGames(cli_game_dir, bash_ini_)
        foundGames.update(foundGames_) # set the global name -> game path dict
    else:
        name = _display_fsName[name] # we are passed a display name in
    if name is not None: # try the game returned by detectGames() or specified
        __setGame(name, ' Using %(gamename)s game:')
        return None
    elif len(foundGames) == 1:
        __setGame(list(foundGames.keys())[0], 'Single game found [%(gamename)s]:')
        return None
    # No match found, return the list of possible games (may be empty if
    # nothing is found in registry)
    return [_fsName_display[k] for k in foundGames]

def game_path(display_name): return foundGames[_display_fsName[display_name]]
def get_display_name(fs_name): return _fsName_display[fs_name]

# Tes3 Group/Top Types --------------------------------------------------------
groupTypes = [
    _('Top (Type)'),
    _('World Children'),
    _('Int Cell Block'),
    _('Int Cell Sub-Block'),
    _('Ext Cell Block'),
    _('Ext Cell Sub-Block'),
    _('Cell Children'),
    _('Topic Children'),
    _('Cell Persistent Children'),
    _('Cell Temporary Children'),
    _('Cell Visible Distant Children'),
]

# Id Functions ----------------------------------------------------------------
def getIdFunc(modName):
    return lambda x: (GPath(modName),x)

ob = getIdFunc('Oblivion.esm')
cobl = getIdFunc('Cobl Main.esm')

# Default Eyes/Hair -----------------------------------------------------------
standardEyes = [ob(x) for x in (0x27306,0x27308,0x27309)] + [cobl(x) for x in (0x000821, 0x000823, 0x000825, 0x000828, 0x000834, 0x000837, 0x000839, 0x00084F, )]

defaultEyes = {
    #--Oblivion.esm
    ob(0x23FE9): #--Argonian
        [ob(0x3E91E)] + [cobl(x) for x in (0x01F407, 0x01F408, 0x01F40B, 0x01F40C, 0x01F410, 0x01F411, 0x01F414, 0x01F416, 0x01F417, 0x01F41A, 0x01F41B, 0x01F41E, 0x01F41F, 0x01F422, 0x01F424, )],
    ob(0x0224FC): #--Breton
        standardEyes,
    ob(0x0191C1): #--Dark Elf
        [ob(0x27307)] + [cobl(x) for x in (0x000861,0x000864,0x000851)],
    ob(0x019204): #--High Elf
        standardEyes,
    ob(0x000907): #--Imperial
        standardEyes,
    ob(0x022C37): #--Khajiit
        [ob(0x375c8)] + [cobl(x) for x in (0x00083B, 0x00083E, 0x000843, 0x000846, 0x000849, 0x00084C, )],
    ob(0x0224FD): #--Nord
        standardEyes,
    ob(0x0191C0): #--Orc
        [ob(0x2730A)]+[cobl(x) for x in (0x000853, 0x000855, 0x000858, 0x00085A, 0x00085C, 0x00085E, )],
    ob(0x000D43): #--Redguard
        standardEyes,
    ob(0x0223C8): #--Wood Elf
        standardEyes,
    #--Cobl
    cobl(0x07948): #--cobRaceAureal
        [ob(0x54BBA)],
    cobl(0x02B60): #--cobRaceHidden
        [cobl(x) for x in (0x01F43A, 0x01F438, 0x01F439, 0x0015A7, 0x01792C, 0x0015AC, 0x0015A8, 0x0015AB, 0x0015AA,)],
    cobl(0x07947): #--cobRaceMazken
        [ob(0x54BB9)],
    cobl(0x1791B): #--cobRaceOhmes
        [cobl(x) for x in (0x017901, 0x017902, 0x017903, 0x017904, 0x017905, 0x017906, 0x017907, 0x017908, 0x017909, 0x01790A, 0x01790B, 0x01790C, 0x01790D, 0x01790E, 0x01790F, 0x017910, 0x017911, 0x017912, 0x017913, 0x017914, 0x017915, 0x017916, 0x017917, 0x017918, 0x017919, 0x01791A, 0x017900,)],
    cobl(0x1F43C): #--cobRaceXivilai
        [cobl(x) for x in (0x01F437, 0x00531B, 0x00531C, 0x00531D, 0x00531E, 0x00531F, 0x005320, 0x005321, 0x01F43B, 0x00DBE1, )],
    }

# Magic Info ------------------------------------------------------------------
magicEffects = {
    'ABAT': [5,_('Absorb Attribute'),0.95],
    'ABFA': [5,_('Absorb Fatigue'),6],
    'ABHE': [5,_('Absorb Health'),16],
    'ABSK': [5,_('Absorb Skill'),2.1],
    'ABSP': [5,_('Absorb Magicka'),7.5],
    'BA01': [1,_('Bound Armor Extra 01'),0],#--Formid == 0
    'BA02': [1,_('Bound Armor Extra 02'),0],#--Formid == 0
    'BA03': [1,_('Bound Armor Extra 03'),0],#--Formid == 0
    'BA04': [1,_('Bound Armor Extra 04'),0],#--Formid == 0
    'BA05': [1,_('Bound Armor Extra 05'),0],#--Formid == 0
    'BA06': [1,_('Bound Armor Extra 06'),0],#--Formid == 0
    'BA07': [1,_('Bound Armor Extra 07'),0],#--Formid == 0
    'BA08': [1,_('Bound Armor Extra 08'),0],#--Formid == 0
    'BA09': [1,_('Bound Armor Extra 09'),0],#--Formid == 0
    'BA10': [1,_('Bound Armor Extra 10'),0],#--Formid == 0
    'BABO': [1,_('Bound Boots'),12],
    'BACU': [1,_('Bound Cuirass'),12],
    'BAGA': [1,_('Bound Gauntlets'),8],
    'BAGR': [1,_('Bound Greaves'),12],
    'BAHE': [1,_('Bound Helmet'),12],
    'BASH': [1,_('Bound Shield'),12],
    'BRDN': [0,_('Burden'),0.21],
    'BW01': [1,_('Bound Order Weapon 1'),1],
    'BW02': [1,_('Bound Order Weapon 2'),1],
    'BW03': [1,_('Bound Order Weapon 3'),1],
    'BW04': [1,_('Bound Order Weapon 4'),1],
    'BW05': [1,_('Bound Order Weapon 5'),1],
    'BW06': [1,_('Bound Order Weapon 6'),1],
    'BW07': [1,_('Summon Staff of Sheogorath'),1],
    'BW08': [1,_('Bound Priest Dagger'),1],
    'BW09': [1,_('Bound Weapon Extra 09'),0],#--Formid == 0
    'BW10': [1,_('Bound Weapon Extra 10'),0],#--Formid == 0
    'BWAX': [1,_('Bound Axe'),39],
    'BWBO': [1,_('Bound Bow'),95],
    'BWDA': [1,_('Bound Dagger'),14],
    'BWMA': [1,_('Bound Mace'),91],
    'BWSW': [1,_('Bound Sword'),235],
    'CALM': [3,_('Calm'),0.47],
    'CHML': [3,_('Chameleon'),0.63],
    'CHRM': [3,_('Charm'),0.2],
    'COCR': [3,_('Command Creature'),0.6],
    'COHU': [3,_('Command Humanoid'),0.75],
    'CUDI': [5,_('Cure Disease'),1400],
    'CUPA': [5,_('Cure Paralysis'),500],
    'CUPO': [5,_('Cure Poison'),600],
    'DARK': [3,_('DO NOT USE - Darkness'),0],
    'DEMO': [3,_('Demoralize'),0.49],
    'DGAT': [2,_('Damage Attribute'),100],
    'DGFA': [2,_('Damage Fatigue'),4.4],
    'DGHE': [2,_('Damage Health'),12],
    'DGSP': [2,_('Damage Magicka'),2.45],
    'DIAR': [2,_('Disintegrate Armor'),6.2],
    'DISE': [2,_('Disease Info'),0], #--Formid == 0
    'DIWE': [2,_('Disintegrate Weapon'),6.2],
    'DRAT': [2,_('Drain Attribute'),0.7],
    'DRFA': [2,_('Drain Fatigue'),0.18],
    'DRHE': [2,_('Drain Health'),0.9],
    'DRSK': [2,_('Drain Skill'),0.65],
    'DRSP': [2,_('Drain Magicka'),0.18],
    'DSPL': [4,_('Dispel'),3.6],
    'DTCT': [4,_('Detect Life'),0.08],
    'DUMY': [2,_('Mehrunes Dagon'),0], #--Formid == 0
    'FIDG': [2,_('Fire Damage'),7.5],
    'FISH': [0,_('Fire Shield'),0.95],
    'FOAT': [5,_('Fortify Attribute'),0.6],
    'FOFA': [5,_('Fortify Fatigue'),0.04],
    'FOHE': [5,_('Fortify Health'),0.14],
    'FOMM': [5,_('Fortify Magicka Multiplier'),0.04],
    'FOSK': [5,_('Fortify Skill'),0.6],
    'FOSP': [5,_('Fortify Magicka'),0.15],
    'FRDG': [2,_('Frost Damage'),7.4],
    'FRNZ': [3,_('Frenzy'),0.04],
    'FRSH': [0,_('Frost Shield'),0.95],
    'FTHR': [0,_('Feather'),0.1],
    'INVI': [3,_('Invisibility'),40],
    'LGHT': [3,_('Light'),0.051],
    'LISH': [0,_('Shock Shield'),0.95],
    'LOCK': [0,_('DO NOT USE - Lock'),30],
    'MYHL': [1,_('Summon Mythic Dawn Helm'),110],
    'MYTH': [1,_('Summon Mythic Dawn Armor'),120],
    'NEYE': [3,_('Night-Eye'),22],
    'OPEN': [0,_('Open'),4.3],
    'PARA': [3,_('Paralyze'),475],
    'POSN': [2,_('Poison Info'),0],
    'RALY': [3,_('Rally'),0.03],
    'REAN': [1,_('Reanimate'),10],
    'REAT': [5,_('Restore Attribute'),38],
    'REDG': [4,_('Reflect Damage'),2.5],
    'REFA': [5,_('Restore Fatigue'),2],
    'REHE': [5,_('Restore Health'),10],
    'RESP': [5,_('Restore Magicka'),2.5],
    'RFLC': [4,_('Reflect Spell'),3.5],
    'RSDI': [5,_('Resist Disease'),0.5],
    'RSFI': [5,_('Resist Fire'),0.5],
    'RSFR': [5,_('Resist Frost'),0.5],
    'RSMA': [5,_('Resist Magic'),2],
    'RSNW': [5,_('Resist Normal Weapons'),1.5],
    'RSPA': [5,_('Resist Paralysis'),0.75],
    'RSPO': [5,_('Resist Poison'),0.5],
    'RSSH': [5,_('Resist Shock'),0.5],
    'RSWD': [5,_('Resist Water Damage'),0], #--Formid == 0
    'SABS': [4,_('Spell Absorption'),3],
    'SEFF': [0,_('Script Effect'),0],
    'SHDG': [2,_('Shock Damage'),7.8],
    'SHLD': [0,_('Shield'),0.45],
    'SLNC': [3,_('Silence'),60],
    'STMA': [2,_('Stunted Magicka'),0],
    'STRP': [4,_('Soul Trap'),30],
    'SUDG': [2,_('Sun Damage'),9],
    'TELE': [4,_('Telekinesis'),0.49],
    'TURN': [1,_('Turn Undead'),0.083],
    'VAMP': [2,_('Vampirism'),0],
    'WABR': [0,_('Water Breathing'),14.5],
    'WAWA': [0,_('Water Walking'),13],
    'WKDI': [2,_('Weakness to Disease'),0.12],
    'WKFI': [2,_('Weakness to Fire'),0.1],
    'WKFR': [2,_('Weakness to Frost'),0.1],
    'WKMA': [2,_('Weakness to Magic'),0.25],
    'WKNW': [2,_('Weakness to Normal Weapons'),0.25],
    'WKPO': [2,_('Weakness to Poison'),0.1],
    'WKSH': [2,_('Weakness to Shock'),0.1],
    'Z001': [1,_('Summon Rufio\'s Ghost'),13],
    'Z002': [1,_('Summon Ancestor Guardian'),33.3],
    'Z003': [1,_('Summon Spiderling'),45],
    'Z004': [1,_('Summon Flesh Atronach'),1],
    'Z005': [1,_('Summon Bear'),47.3],
    'Z006': [1,_('Summon Gluttonous Hunger'),61],
    'Z007': [1,_('Summon Ravenous Hunger'),123.33],
    'Z008': [1,_('Summon Voracious Hunger'),175],
    'Z009': [1,_('Summon Dark Seducer'),1],
    'Z010': [1,_('Summon Golden Saint'),1],
    'Z011': [1,_('Wabba Summon'),0],
    'Z012': [1,_('Summon Decrepit Shambles'),45],
    'Z013': [1,_('Summon Shambles'),87.5],
    'Z014': [1,_('Summon Replete Shambles'),150],
    'Z015': [1,_('Summon Hunger'),22],
    'Z016': [1,_('Summon Mangled Flesh Atronach'),22],
    'Z017': [1,_('Summon Torn Flesh Atronach'),32.5],
    'Z018': [1,_('Summon Stitched Flesh Atronach'),75.5],
    'Z019': [1,_('Summon Sewn Flesh Atronach'),195],
    'Z020': [1,_('Extra Summon 20'),0],
    'ZCLA': [1,_('Summon Clannfear'),75.56],
    'ZDAE': [1,_('Summon Daedroth'),123.33],
    'ZDRE': [1,_('Summon Dremora'),72.5],
    'ZDRL': [1,_('Summon Dremora Lord'),157.14],
    'ZFIA': [1,_('Summon Flame Atronach'),45],
    'ZFRA': [1,_('Summon Frost Atronach'),102.86],
    'ZGHO': [1,_('Summon Ghost'),22],
    'ZHDZ': [1,_('Summon Headless Zombie'),56],
    'ZLIC': [1,_('Summon Lich'),350],
    'ZSCA': [1,_('Summon Scamp'),30],
    'ZSKA': [1,_('Summon Skeleton Guardian'),32.5],
    'ZSKC': [1,_('Summon Skeleton Champion'),152],
    'ZSKE': [1,_('Summon Skeleton'),11.25],
    'ZSKH': [1,_('Summon Skeleton Hero'),66],
    'ZSPD': [1,_('Summon Spider Daedra'),195],
    'ZSTA': [1,_('Summon Storm Atronach'),125],
    'ZWRA': [1,_('Summon Faded Wraith'),87.5],
    'ZWRL': [1,_('Summon Gloom Wraith'),260],
    'ZXIV': [1,_('Summon Xivilai'),200],
    'ZZOM': [1,_('Summon Zombie'),16.67],
    }

_strU = struct.Struct('I')

mgef_school = dict((x, y) for x, [y, z, _num] in list(magicEffects.items()))
mgef_name = dict((x, z) for x, [y, z, __num] in list(magicEffects.items()))
mgef_basevalue = dict((x,a) for x,[y,z,a] in list(magicEffects.items()))
mgef_school.update(dict((_strU.unpack(x)[0],y) for x,[y,z,a] in list(magicEffects.items())))
mgef_name.update(dict((_strU.unpack(x)[0],z) for x,[y,z,a] in list(magicEffects.items())))
mgef_basevalue.update(dict((_strU.unpack(x)[0],a) for x,[y,z,a] in list(magicEffects.items())))

hostileEffects = {
    'ABAT', #--Absorb Attribute
    'ABFA', #--Absorb Fatigue
    'ABHE', #--Absorb Health
    'ABSK', #--Absorb Skill
    'ABSP', #--Absorb Magicka
    'BRDN', #--Burden
    'DEMO', #--Demoralize
    'DGAT', #--Damage Attribute
    'DGFA', #--Damage Fatigue
    'DGHE', #--Damage Health
    'DGSP', #--Damage Magicka
    'DIAR', #--Disintegrate Armor
    'DIWE', #--Disintegrate Weapon
    'DRAT', #--Drain Attribute
    'DRFA', #--Drain Fatigue
    'DRHE', #--Drain Health
    'DRSK', #--Drain Skill
    'DRSP', #--Drain Magicka
    'FIDG', #--Fire Damage
    'FRDG', #--Frost Damage
    'FRNZ', #--Frenzy
    'PARA', #--Paralyze
    'SHDG', #--Shock Damage
    'SLNC', #--Silence
    'STMA', #--Stunted Magicka
    'STRP', #--Soul Trap
    'SUDG', #--Sun Damage
    'TURN', #--Turn Undead
    'WKDI', #--Weakness to Disease
    'WKFI', #--Weakness to Fire
    'WKFR', #--Weakness to Frost
    'WKMA', #--Weakness to Magic
    'WKNW', #--Weakness to Normal Weapons
    'WKPO', #--Weakness to Poison
    'WKSH', #--Weakness to Shock
    }
hostileEffects |= set((_strU.unpack(x)[0] for x in hostileEffects))

#Doesn't list mgefs that use actor values, but rather mgefs that have a generic name
#Ex: Absorb Attribute becomes Absorb Magicka if the effect's actorValue field contains 9
#    But it is actually using an attribute rather than an actor value
#Ex: Burden uses an actual actor value (encumbrance) but it isn't listed since its name doesn't change
genericAVEffects = {
    'ABAT', #--Absorb Attribute (Use Attribute)
    'ABSK', #--Absorb Skill (Use Skill)
    'DGAT', #--Damage Attribute (Use Attribute)
    'DRAT', #--Drain Attribute (Use Attribute)
    'DRSK', #--Drain Skill (Use Skill)
    'FOAT', #--Fortify Attribute (Use Attribute)
    'FOSK', #--Fortify Skill (Use Skill)
    'REAT', #--Restore Attribute (Use Attribute)
    }
genericAVEffects |= set((_strU.unpack(x)[0] for x in genericAVEffects))

actorValues = [
    _('Strength'), #--00
    _('Intelligence'),
    _('Willpower'),
    _('Agility'),
    _('Speed'),
    _('Endurance'),
    _('Personality'),
    _('Luck'),
    _('Health'),
    _('Magicka'),

    _('Fatigue'), #--10
    _('Encumbrance'),
    _('Armorer'),
    _('Athletics'),
    _('Blade'),
    _('Block'),
    _('Blunt'),
    _('Hand To Hand'),
    _('Heavy Armor'),
    _('Alchemy'),

    _('Alteration'), #--20
    _('Conjuration'),
    _('Destruction'),
    _('Illusion'),
    _('Mysticism'),
    _('Restoration'),
    _('Acrobatics'),
    _('Light Armor'),
    _('Marksman'),
    _('Mercantile'),

    _('Security'), #--30
    _('Sneak'),
    _('Speechcraft'),
    'Aggression',
    'Confidence',
    'Energy',
    'Responsibility',
    'Bounty',
    'UNKNOWN 38',
    'UNKNOWN 39',

    'MagickaMultiplier', #--40
    'NightEyeBonus',
    'AttackBonus',
    'DefendBonus',
    'CastingPenalty',
    'Blindness',
    'Chameleon',
    'Invisibility',
    'Paralysis',
    'Silence',

    'Confusion', #--50
    'DetectItemRange',
    'SpellAbsorbChance',
    'SpellReflectChance',
    'SwimSpeedMultiplier',
    'WaterBreathing',
    'WaterWalking',
    'StuntedMagicka',
    'DetectLifeRange',
    'ReflectDamage',

    'Telekinesis', #--60
    'ResistFire',
    'ResistFrost',
    'ResistDisease',
    'ResistMagic',
    'ResistNormalWeapons',
    'ResistParalysis',
    'ResistPoison',
    'ResistShock',
    'Vampirism',

    'Darkness', #--70
    'ResistWaterDamage',
    ]

acbs = {
    'Armorer': 0,
    'Athletics': 1,
    'Blade': 2,
    'Block': 3,
    'Blunt': 4,
    'Hand to Hand': 5,
    'Heavy Armor': 6,
    'Alchemy': 7,
    'Alteration': 8,
    'Conjuration': 9,
    'Destruction': 10,
    'Illusion': 11,
    'Mysticism': 12,
    'Restoration': 13,
    'Acrobatics': 14,
    'Light Armor': 15,
    'Marksman': 16,
    'Mercantile': 17,
    'Security': 18,
    'Sneak': 19,
    'Speechcraft': 20,
    'Health': 21,
    'Strength': 25,
    'Intelligence': 26,
    'Willpower': 27,
    'Agility': 28,
    'Speed': 29,
    'Endurance': 30,
    'Personality': 31,
    'Luck': 32,
    }

# Save File Info --------------------------------------------------------------
saveRecTypes = {
    6 : _('Faction'),
    19: _('Apparatus'),
    20: _('Armor'),
    21: _('Book'),
    22: _('Clothing'),
    25: _('Ingredient'),
    26: _('Light'),
    27: _('Misc. Item'),
    33: _('Weapon'),
    35: _('NPC'),
    36: _('Creature'),
    39: _('Key'),
    40: _('Potion'),
    48: _('Cell'),
    49: _('Object Ref'),
    50: _('NPC Ref'),
    51: _('Creature Ref'),
    58: _('Dialog Entry'),
    59: _('Quest'),
    61: _('AI Package'),
    }

#--Cleanup --------------------------------------------------------------------
#------------------------------------------------------------------------------
del _strU

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

"""This modules defines static data for use by bush, when Fallout 4 is set as
   the active game."""

from .constants import *
from .default_tweaks import default_tweaks
from .records import MreHeader, MreLvli, MreLvln
from ... import brec
from ...bolt import struct_pack, struct_unpack

#--Name of the game to use in UI.
displayName = 'Fallout 4'
#--Name of the game's filesystem folder.
fsName = 'Fallout4'
#--Alternate display name to use instead of "Wrye Bash for ***"
altName = 'Wrye Flash'
#--Name of game's default ini file.
defaultIniFile = 'Fallout4_default.ini'

#--Exe to look for to see if this is the right game
exe = 'Fallout4.exe'

#--Registry keys to read to find the install location
regInstallKeys = ('Bethesda Softworks\\Fallout4', 'Installed Path')

#--patch information
## URL to download patches for the main game.
# Update via steam
patchURL = ''
patchTip = 'Update via Steam'

#--URL to the Nexus site for this game
nexusUrl = 'http://www.nexusmods.com/fallout4/'
nexusName = 'Fallout 4 Nexus'
nexusKey = 'bash.installers.openFallout4Nexus.continue'

# Bsa info
allow_reset_bsa_timestamps = False
bsa_extension = r'ba2'
supports_mod_inis = True
vanilla_string_bsas = {
    'fallout4.esm': ['Fallout4 - Interface.ba2'],
    'dlcrobot.esm': ['DLCRobot - Main.ba2'],
    'dlcworkshop01.esm': ['DLCworkshop01 - Main.ba2'],
    'dlcworkshop02.esm': ['DLCworkshop02 - Main.ba2'],
    'dlcworkshop03.esm': ['DLCworkshop03 - Main.ba2'],
    'dlccoast.esm': ['DLCCoast - Main.ba2'],
    'dlcnukaworld.esm':  ['DLCNukaWorld - Main.ba2'],
}
resource_archives_keys = (
    'sResourceIndexFileList', 'sResourceStartUpArchiveList',
    'sResourceArchiveList', 'sResourceArchiveList2',
    'sResourceArchiveListBeta'
)

# plugin extensions
espm_extensions = {'.esp', '.esm', '.esl'}

# Load order info
using_txt_file = True

#--Creation Kit Set information
class cs:
    ## TODO:  When the Fallout 4 Creation Kit is actually released, double check
    ## that the filename is correct, and create an actual icon
    shortName = 'FO4CK'                 # Abbreviated name
    longName = 'Creation Kit'           # Full name
    exe = 'CreationKit.exe'             # Executable to run
    seArgs = None                        # u'-editor'
    imageName = 'creationkit%s.png'     # Image name template for the status bar

#--Script Extender information
class se:
    shortName = 'F4SE'                      # Abbreviated name
    longName = 'Fallout 4 Script Extender'  # Full name
    exe = 'f4se_loader.exe'                 # Exe to run
    steamExe = 'f4se_steam_loader.dll'      # Exe to run if a steam install
    url = 'http://f4se.silverlock.org/'     # URL to download from
    urlTip = 'http://f4se.silverlock.org/'  # Tooltip for mouse over the URL

#--Script Dragon
class sd:
    shortName = ''
    longName = ''
    installDir = ''

#--SkyProc Patchers
class sp:
    shortName = ''
    longName = ''
    installDir = ''

#--Quick shortcut for combining the SE and SD names
se_sd = se.shortName

#--Graphics Extender information
class ge:
    shortName = ''
    longName = ''
    ## exe is treated specially here.  If it is a string, then it should
    ## be the path relative to the root directory of the game
    ## if it is list, each list element should be an iterable to pass to Path.join
    ## relative to the root directory of the game.  In this case, each filename
    ## will be tested in reverse order.  This was required for Oblivion, as the newer
    ## OBGE has a different filename than the older OBGE
    exe = '**DNE**'
    url = ''
    urlTip = ''

#--4gb Launcher
class laa:
    # Skyrim has a 4gb Launcher, but as of patch 1.3.10, it is
    # no longer required (Bethsoft updated TESV.exe to already
    # be LAA)
    name = ''
    exe = '**DNE**'       # Executable to run
    launchesSE = False

# Files BAIN shouldn't skip
dontSkip = (
# Nothing so far
)

# Directories where specific file extensions should not be skipped by BAIN
dontSkipDirs = {
    # This rule is to allow mods with string translation enabled.
    'interface\\translations':['.txt']
}

#Folders BAIN should never check
SkipBAINRefresh = {
    #Use lowercase names
    'fo4edit backups',
}

#--Some stuff dealing with INI files
class ini:
    #--True means new lines are allowed to be added via INI Tweaks
    #  (by default)
    allowNewLines = True

    #--INI Entry to enable BSA Redirection
    bsaRedirection = ('','')

#--Save Game format stuff
class ess:
    # Save file capabilities
    canReadBasic = True         # All the basic stuff needed for the Saves Tab
    canEditMore = False         # No advanced editing
    ext = '.fos'               # Save file extension

#--INI files that should show up in the INI Edits tab
iniFiles = [
    'Fallout4.ini',
    'Fallout4Prefs.ini',
    'Fallout4Custom.ini',
    ]

#--INI setting to setup Save Profiles
saveProfilesKey = ('General','SLocalSavePath')

#--The main plugin Wrye Bash should look for
masterFiles = [
    'Fallout4.esm',
    ]

#The pickle file for this game. Holds encoded GMST IDs from the big list below.
pklfile = r'bash\db\Fallout4_ids.pkl'

#--BAIN: Directories that are OK to install to
dataDirs = {
    'interface',
    'lodsettings',
    'materials',
    'meshes',
    'misc',
    'music',
    'programs',
    'scripts',
    'seq',
    'shadersfx',
    'sound',
    'strings',
    'textures',
    'video',
    'vis',
}
dataDirsPlus = {
    'f4se',
    'ini',
    'tools', # bodyslide
    'mcm',   # FO4 MCM
}

# Installer -------------------------------------------------------------------
# ensure all path strings are prefixed with 'r' to avoid interpretation of
#   accidental escape sequences
wryeBashDataFiles = {
    'Bashed Patch.esp',
    'Bashed Patch, 0.esp',
    'Bashed Patch, 1.esp',
    'Bashed Patch, 2.esp',
    'Bashed Patch, 3.esp',
    'Bashed Patch, 4.esp',
    'Bashed Patch, 5.esp',
    'Bashed Patch, 6.esp',
    'Bashed Patch, 7.esp',
    'Bashed Patch, 8.esp',
    'Bashed Patch, 9.esp',
    'Bashed Patch, CBash.esp',
    'Bashed Patch, Python.esp',
    'Bashed Patch, Warrior.esp',
    'Bashed Patch, Thief.esp',
    'Bashed Patch, Mage.esp',
    'Bashed Patch, Test.esp',
    'Docs\\Bash Readme Template.html',
    'Docs\\wtxt_sand_small.css',
    'Docs\\wtxt_teal.css',
    'Docs\\Bash Readme Template.txt',
    'Docs\\Bashed Patch, 0.html',
    'Docs\\Bashed Patch, 0.txt',
}

wryeBashDataDirs = {
    'Bash Patches',
    'INI Tweaks'
}

ignoreDataFiles = set()
ignoreDataFilePrefixes = set()
ignoreDataDirs = set()

#--Tags supported by this game
allTags = sorted((
    'Delev', 'NoMerge', 'Relev',
    ))

#--Gui patcher classes available when building a Bashed Patch
patchers = (
    'ListsMerger',
    )

#--CBash Gui patcher classes available when building a Bashed Patch
CBash_patchers = tuple()

# Magic Info ------------------------------------------------------------------
weaponTypes = tuple()

# Race Info -------------------------------------------------------------------
raceNames = dict()
raceShortNames = dict()
raceHairMale = dict()
raceHairFemale = dict()

#--Plugin format stuff
class esp:
    #--Wrye Bash capabilities
    canBash = True          # Can create Bashed Patches
    canCBash = False        # CBash can handle this game's records
    canEditHeader = True    # Can edit anything in the TES4 record

    #--Valid ESM/ESP header versions
    validHeaderVersions = (0.95,)

    #--Strings Files
    stringsFiles = [
        (('Strings',), '%(body)s_%(language)s.STRINGS'),
        (('Strings',), '%(body)s_%(language)s.DLSTRINGS'),
        (('Strings',), '%(body)s_%(language)s.ILSTRINGS'),
    ]

#------------------------------------------------------------------------------
# These Are normally not mergable but added to brec.MreRecord.type_class
#
#       MreCell,
#------------------------------------------------------------------------------
# These have undefined FormIDs Do not merge them
#
#       MreNavi, MreNavm,
#------------------------------------------------------------------------------
# These need syntax revision but can be merged once that is corrected
#
#       MreAchr, MreDial, MreLctn, MreInfo, MreFact, MrePerk,
#------------------------------------------------------------------------------
#--Mergeable record types
mergeClasses = tuple()

#--Extra read classes: these record types will always be loaded, even if
# patchers don't need them directly (for example, MGEF for magic effects info)
readClasses = tuple()
writeClasses = tuple()

def init():
    # Due to a bug with py2exe, 'reload' doesn't function properly.  Instead of
    # re-executing all lines within the module, it acts like another 'import'
    # statement - in otherwords, nothing happens.  This means any lines that
    # affect outside modules must do so within this function, which will be
    # called instead of 'reload'

    #--Top types in Skyrim order.
    brec.RecordHeader.topTypes = [
        'GMST', 'KYWD', 'LCRT', 'AACT', 'TRNS', 'CMPO', 'TXST', 'GLOB', 'DMGT',
        'CLAS', 'FACT', 'HDPT', 'RACE', 'SOUN', 'ASPC', 'MGEF', 'LTEX', 'ENCH',
        'SPEL', 'ACTI', 'TACT', 'ARMO', 'BOOK', 'CONT', 'DOOR', 'INGR', 'LIGH',
        'MISC', 'STAT', 'SCOL', 'MSTT', 'GRAS', 'TREE', 'FLOR', 'FURN', 'WEAP',
        'AMMO', 'NPC_', 'LVLN', 'KEYM', 'ALCH', 'IDLM', 'NOTE', 'PROJ', 'HAZD',
        'BNDS', 'TERM', 'GRAS', 'TREE', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'LVLN',
        'KEYM', 'ALCH', 'IDLM', 'NOTE', 'PROJ', 'HAZD', 'BNDS', 'LVLI', 'WTHR',
        'CLMT', 'SPGD', 'RFCT', 'REGN', 'NAVI', 'CELL', 'WRLD', 'QUST', 'IDLE',
        'PACK', 'CSTY', 'LSCR', 'ANIO', 'WATR', 'EFSH', 'EXPL', 'DEBR', 'IMGS',
        'IMAD', 'FLST', 'PERK', 'BPTD', 'ADDN', 'AVIF', 'CAMS', 'CPTH', 'VTYP',
        'MATT', 'IPCT', 'IPDS', 'ARMA', 'ECZN', 'LCTN', 'MESG', 'DOBJ', 'DFOB',
        'LGTM', 'MUSC', 'FSTP', 'FSTS', 'SMBN', 'SMQN', 'SMEN', 'MUST', 'DLVW',
        'EQUP', 'RELA', 'ASTP', 'OTFT', 'ARTO', 'MATO', 'MOVT', 'SNDR', 'SNCT',
        'SOPM', 'COLL', 'CLFM', 'REVB', 'PKIN', 'RFGP', 'AMDL', 'LAYR', 'COBJ',
        'OMOD', 'MSWP', 'ZOOM', 'INNR', 'KSSM', 'AECH', 'SCCO', 'AORU', 'SCSN',
        'STAG', 'NOCM', 'LENS', 'GDRY', 'OVIS']

    #--Record types that don't appear at the top level (sub-GRUPs)
    brec.RecordHeader.recordTypes = (set(brec.RecordHeader.topTypes) |
                   {'GRUP','TES4','REFR','NAVM','PGRE','PHZD','LAND',
                       'PMIS','DLBR','DIAL','INFO','SCEN'})
    brec.RecordHeader.plugin_form_version = 131

    #--Record Types
    brec.MreRecord.type_class = dict((x.classType,x) for x in (
        MreLvli, MreLvln,
        ####### for debug
        MreHeader,
        ))

    #--Simple records
    brec.MreRecord.simpleTypes = (
        set(brec.MreRecord.type_class) - {'TES4',})

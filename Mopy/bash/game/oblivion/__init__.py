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

"""This modules defines static data for use by bush, when
   TES IV: Oblivion is set at the active game."""

from .constants import *
from .default_tweaks import default_tweaks
from .records import MreActi, MreAlch, MreAmmo, MreAnio, MreAppa, MreArmo, \
    MreBook, MreBsgn, MreClas, MreClot, MreCont, MreCrea, MreDoor, MreEfsh, \
    MreEnch, MreEyes, MreFact, MreFlor, MreFurn, MreGras, MreHair, MreIngr, \
    MreKeym, MreLigh, MreLscr, MreLvlc, MreLvli, MreLvsp, MreMgef, MreMisc, \
    MreNpc, MrePack, MreQust, MreRace, MreScpt, MreSgst, MreSlgm, MreSoun, \
    MreSpel, MreStat, MreTree, MreWatr, MreWeap, MreWthr, MreClmt, MreCsty, \
    MreIdle, MreLtex, MreRegn, MreSbsp, MreSkil, MreAchr, MreAcre, MreCell, \
    MreGmst, MreRefr, MreRoad, MreHeader, MreWrld, MreDial, MreInfo
from ... import brec
from ...bolt import struct_pack, struct_unpack
from ...brec import MreGlob

#--Name of the game to use in UI.
displayName = 'Oblivion'
#--Name of the game's filesystem folder.
fsName = 'Oblivion'
#--Alternate display name to use instead of "Wrye Bash for ***"
altName = 'Wrye Bash'
#--Name of game's default ini file.
defaultIniFile = 'Oblivion_default.ini'

#--Exe to look for to see if this is the right game
exe = 'Oblivion.exe'

#--Registry keys to read to find the install location
regInstallKeys = ('Bethesda Softworks\\Oblivion', 'Installed Path')

#--patch information
patchURL = 'http://www.elderscrolls.com/downloads/updates_patches.htm'
patchTip = 'http://www.elderscrolls.com/'

#--URL to the Nexus site for this game
nexusUrl = 'http://oblivion.nexusmods.com/'
nexusName = 'TES Nexus'
nexusKey = 'bash.installers.openTesNexus.continue'

# Bsa info
allow_reset_bsa_timestamps = True
bsa_extension = r'bsa'
supports_mod_inis = False
vanilla_string_bsas = {}
resource_archives_keys = ()

# plugin extensions
espm_extensions = {'.esp', '.esm'}

# Load order info
using_txt_file = False

#--Construction Set information
class cs:
    shortName = 'TESCS'            # Abbreviated name
    longName = 'Construction Set'  # Full name
    exe = 'TESConstructionSet.exe' # Executable to run
    seArgs = '-editor'             # Argument to pass to the SE to load the CS
    imageName = 'tescs%s.png'      # Image name template for the status bar

#--Script Extender information
class se:
    shortName = 'OBSE'                      # Abbreviated name
    longName = 'Oblivion Script Extender'   # Full name
    exe = 'obse_loader.exe'                 # Exe to run
    steamExe = 'obse_1_2_416.dll'           # Exe to run if a steam install
    url = 'http://obse.silverlock.org/'     # URL to download from
    urlTip = 'http://obse.silverlock.org/'  # Tooltip for mouse over the URL

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
    shortName = 'OBGE'
    longName = 'Oblivion Graphics Extender'
    exe = [('Data','obse','plugins','obge.dll'),
           ('Data','obse','plugins','obgev2.dll'),
           ]
    url = 'http://oblivion.nexusmods.com/mods/30054'
    urlTip = 'http://oblivion.nexusmods.com/'

#--4gb Launcher
class laa:
    name = ''           # Name
    exe = '**DNE**'     # Executable to run
    launchesSE = False  # Whether the launcher will automatically launch the SE as well

# Files BAIN shouldn't skip
dontSkip = (
# Nothing so far
)

# Directories where specific file extensions should not be skipped by BAIN
dontSkipDirs = {
# Nothing so far
}

#Folders BAIN should never check
SkipBAINRefresh = {
    'tes4edit backups',
    'bgsee',
    'conscribe logs',
    #Use lowercase names
}

#--Some stuff dealing with INI files
class ini:
    #--True means new lines are allowed to be added via INI Tweaks
    #  (by default)
    allowNewLines = False

    #--INI Entry to enable BSA Redirection
    bsaRedirection = ('Archive','sArchiveList')

#--Save Game format stuff
class ess:
    # Save file capabilities
    canReadBasic = True         # All the basic stuff needed for the Saves Tab
    canEditMore = True          # advanced editing
    ext = '.ess'               # Save file extension

#--INI files that should show up in the INI Edits tab
iniFiles = [
    'Oblivion.ini',
    ]

#--INI setting to setup Save Profiles
saveProfilesKey = ('General','SLocalSavePath')

#--The main plugin Wrye Bash should look for
masterFiles = [
    'Oblivion.esm',
    'Nehrim.esm',
    ]

#The pickle file for this game. Holds encoded GMST IDs from the big list below.
pklfile = r'bash\db\Oblivion_ids.pkl'

#--BAIN: Directories that are OK to install to
dataDirs = {
    'distantlod',
    'facegen',
    'fonts',
    'menus',
    'meshes',
    'music',
    'shaders',
    'sound',
    'textures',
    'trees',
    'video',
}
dataDirsPlus = {
    'streamline',
    '_tejon',
    'scripts',
    'pluggy',
    'ini',
    'obse',
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
    'Bashed Patch, FCOM.esp',
    'Bashed Patch, Warrior.esp',
    'Bashed Patch, Thief.esp',
    'Bashed Patch, Mage.esp',
    'Bashed Patch, Test.esp',
    'ArchiveInvalidationInvalidated!.bsa',
    'Docs\\Bash Readme Template.html',
    'Docs\\wtxt_sand_small.css',
    'Docs\\wtxt_teal.css',
    'Docs\\Bash Readme Template.txt'
}
wryeBashDataDirs = {
    'Bash Patches',
    'INI Tweaks'
}
ignoreDataFiles = {
    'OBSE\\Plugins\\Construction Set Extender.dll',
    'OBSE\\Plugins\\Construction Set Extender.ini'
}
ignoreDataFilePrefixes = {
    'Meshes\\Characters\\_Male\\specialanims\\0FemaleVariableWalk_'
}
ignoreDataDirs = {
    'OBSE\\Plugins\\ComponentDLLs\\CSE',
    'LSData'
}

#--Tags supported by this game
allTags = sorted((
    'Body-F', 'Body-M', 'Body-Size-M', 'Body-Size-F', 'C.Climate',
    'C.Light', 'C.Music', 'C.Name', 'C.RecordFlags', 'C.Owner',
    'C.Water', 'Deactivate', 'Delev', 'Eyes', 'Factions', 'Relations',
    'Filter', 'Graphics', 'Hair', 'IIM', 'Invent', 'Names', 'NoMerge',
    'NpcFaces', 'R.Relations', 'Relev', 'Scripts', 'ScriptContents',
    'Sound', 'SpellStats', 'Stats', 'Voice-F', 'Voice-M', 'R.Teeth',
    'R.Mouth', 'R.Ears', 'R.Head', 'R.Attributes-F', 'R.Attributes-M',
    'R.Skills', 'R.Description', 'R.AddSpells', 'R.ChangeSpells', 'Roads',
    'Actors.Anims', 'Actors.AIData', 'Actors.DeathItem',
    'Actors.AIPackages', 'Actors.AIPackagesForceAdd', 'Actors.Stats',
    'Actors.ACBS', 'NPC.Class', 'Actors.CombatStyle', 'Creatures.Blood',
    'Actors.Spells', 'Actors.SpellsForceAdd', 'NPC.Race',
    'Actors.Skeleton', 'NpcFacesForceFullImport', 'MustBeActiveIfImported',
    'Npc.HairOnly', 'Npc.EyesOnly')) ##, 'ForceMerge'

#--Gui patcher classes available when building a Bashed Patch
patchers = (
    'AliasesPatcher', 'AssortedTweaker', 'PatchMerger', 'AlchemicalCatalogs',
    'KFFZPatcher', 'ActorImporter', 'DeathItemPatcher', 'NPCAIPackagePatcher',
    'CoblExhaustion', 'UpdateReferences', 'CellImporter', 'ClothesTweaker',
    'GmstTweaker', 'GraphicsPatcher', 'ImportFactions', 'ImportInventory',
    'SpellsPatcher', 'TweakActors', 'ImportRelations', 'ImportScripts',
    'ImportActorsSpells', 'ListsMerger', 'MFactMarker', 'NamesPatcher',
    'NamesTweaker', 'NpcFacePatcher', 'RacePatcher', 'RoadImporter',
    'SoundPatcher', 'StatsPatcher', 'SEWorldEnforcer', 'ContentsChecker',
    )

#--CBash Gui patcher classes available when building a Bashed Patch
CBash_patchers = (
    'CBash_AliasesPatcher', 'CBash_AssortedTweaker', 'CBash_PatchMerger',
    'CBash_AlchemicalCatalogs', 'CBash_KFFZPatcher', 'CBash_ActorImporter',
    'CBash_DeathItemPatcher', 'CBash_NPCAIPackagePatcher',
    'CBash_CoblExhaustion', 'CBash_UpdateReferences', 'CBash_CellImporter',
    'CBash_ClothesTweaker', 'CBash_GmstTweaker', 'CBash_GraphicsPatcher',
    'CBash_ImportFactions', 'CBash_ImportInventory', 'CBash_SpellsPatcher',
    'CBash_TweakActors', 'CBash_ImportRelations', 'CBash_ImportScripts',
    'CBash_ImportActorsSpells', 'CBash_ListsMerger', 'CBash_MFactMarker',
    'CBash_NamesPatcher', 'CBash_NamesTweaker', 'CBash_NpcFacePatcher',
    'CBash_RacePatcher', 'CBash_RoadImporter', 'CBash_SoundPatcher',
    'CBash_StatsPatcher', 'CBash_SEWorldEnforcer', 'CBash_ContentsChecker',
    )

# Magic Info ------------------------------------------------------------------
weaponTypes = (
    _('Blade (1 Handed)'),
    _('Blade (2 Handed)'),
    _('Blunt (1 Handed)'),
    _('Blunt (2 Handed)'),
    _('Staff'),
    _('Bow'),
    )

# Race Info -------------------------------------------------------------------
raceNames = {
    0x23fe9 : _('Argonian'),
    0x224fc : _('Breton'),
    0x191c1 : _('Dark Elf'),
    0x19204 : _('High Elf'),
    0x00907 : _('Imperial'),
    0x22c37 : _('Khajiit'),
    0x224fd : _('Nord'),
    0x191c0 : _('Orc'),
    0x00d43 : _('Redguard'),
    0x00019 : _('Vampire'),
    0x223c8 : _('Wood Elf'),
    }

raceShortNames = {
    0x23fe9 : 'Arg',
    0x224fc : 'Bre',
    0x191c1 : 'Dun',
    0x19204 : 'Alt',
    0x00907 : 'Imp',
    0x22c37 : 'Kha',
    0x224fd : 'Nor',
    0x191c0 : 'Orc',
    0x00d43 : 'Red',
    0x223c8 : 'Bos',
    }

raceHairMale = {
    0x23fe9 : 0x64f32, #--Arg
    0x224fc : 0x90475, #--Bre
    0x191c1 : 0x64214, #--Dun
    0x19204 : 0x7b792, #--Alt
    0x00907 : 0x90475, #--Imp
    0x22c37 : 0x653d4, #--Kha
    0x224fd : 0x1da82, #--Nor
    0x191c0 : 0x66a27, #--Orc
    0x00d43 : 0x64215, #--Red
    0x223c8 : 0x690bc, #--Bos
    }

raceHairFemale = {
    0x23fe9 : 0x64f33, #--Arg
    0x224fc : 0x1da83, #--Bre
    0x191c1 : 0x1da83, #--Dun
    0x19204 : 0x690c2, #--Alt
    0x00907 : 0x1da83, #--Imp
    0x22c37 : 0x653d0, #--Kha
    0x224fd : 0x1da83, #--Nor
    0x191c0 : 0x64218, #--Orc
    0x00d43 : 0x64210, #--Red
    0x223c8 : 0x69473, #--Bos
    }

#--Plugin format stuff
class esp:
    #--Wrye Bash capabilities
    canBash = True          # Can create Bashed Patches
    canCBash = True         # CBash can handle this game's records
    canEditHeader = True    # Can edit anything in the TES4 record

    #--Valid ESM/ESP header versions
    validHeaderVersions = (0.8,1.0)

    stringsFiles = []

#------------------------------------------------------------------------------
#--Mergeable record types
mergeClasses = (
    MreActi, MreAlch, MreAmmo, MreAnio, MreAppa, MreArmo, MreBook, MreBsgn,
    MreClas, MreClot, MreCont, MreCrea, MreDoor, MreEfsh, MreEnch, MreEyes,
    MreFact, MreFlor, MreFurn, MreGlob, MreGras, MreHair, MreIngr, MreKeym,
    MreLigh, MreLscr, MreLvlc, MreLvli, MreLvsp, MreMgef, MreMisc, MreNpc,
    MrePack, MreQust, MreRace, MreScpt, MreSgst, MreSlgm, MreSoun, MreSpel,
    MreStat, MreTree, MreWatr, MreWeap, MreWthr, MreClmt, MreCsty, MreIdle,
    MreLtex, MreRegn, MreSbsp, MreSkil,
    )

#--Extra read classes: need info from magic effects
readClasses = (MreMgef, MreScpt,)
writeClasses = (MreMgef,)


def init():
    # Due to a bug with py2exe, 'reload' doesn't function properly.  Instead of
    # re-executing all lines within the module, it acts like another 'import'
    # statement - in otherwords, nothing happens.  This means any lines that
    # affect outside modules must do so within this function, which will be
    # called instead of 'reload'
    __rec_type = brec.RecordHeader
    __rec_type.rec_header_size = 20
    __rec_type.rec_pack_format = '=4s4I'
    __rec_type.pack_formats = {0: '=4sI4s2I'}
    __rec_type.pack_formats.update({x: '=4s4I' for x in {1, 6, 7, 8, 9, 10}})
    __rec_type.pack_formats.update({x: '=4sIi2I' for x in {2, 3}})
    __rec_type.pack_formats.update({x: '=4sIhh2I' for x in {4, 5}})

    #--Top types in Oblivion order.
    __rec_type.topTypes = [
        'GMST', 'GLOB', 'CLAS', 'FACT', 'HAIR', 'EYES', 'RACE', 'SOUN', 'SKIL',
        'MGEF', 'SCPT', 'LTEX', 'ENCH', 'SPEL', 'BSGN', 'ACTI', 'APPA', 'ARMO',
        'BOOK', 'CLOT', 'CONT', 'DOOR', 'INGR', 'LIGH', 'MISC', 'STAT', 'GRAS',
        'TREE', 'FLOR', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'CREA', 'LVLC', 'SLGM',
        'KEYM', 'ALCH', 'SBSP', 'SGST', 'LVLI', 'WTHR', 'CLMT', 'REGN', 'CELL',
        'WRLD', 'DIAL', 'QUST', 'IDLE', 'PACK', 'CSTY', 'LSCR', 'LVSP', 'ANIO',
        'WATR', 'EFSH']

    __rec_type.recordTypes = set(
        __rec_type.topTypes + ['GRUP', 'TES4', 'ROAD', 'REFR', 'ACHR', 'ACRE',
                               'PGRD', 'LAND', 'INFO'])

    #--Record Types
    brec.MreRecord.type_class = dict((x.classType,x) for x in (
        MreAchr, MreAcre, MreActi, MreAlch, MreAmmo, MreAnio, MreAppa, MreArmo,
        MreBook, MreBsgn, MreCell, MreClas, MreClot, MreCont, MreCrea, MreDoor,
        MreEfsh, MreEnch, MreEyes, MreFact, MreFlor, MreFurn, MreGlob, MreGmst,
        MreGras, MreHair, MreIngr, MreKeym, MreLigh, MreLscr, MreLvlc, MreLvli,
        MreLvsp, MreMgef, MreMisc, MreNpc, MrePack, MreQust, MreRace, MreRefr,
        MreRoad, MreScpt, MreSgst, MreSkil, MreSlgm, MreSoun, MreSpel, MreStat,
        MreTree, MreHeader, MreWatr, MreWeap, MreWrld, MreWthr, MreClmt,
        MreCsty, MreIdle, MreLtex, MreRegn, MreSbsp, MreDial, MreInfo,
        ))

    #--Simple records
    brec.MreRecord.simpleTypes = (
        set(brec.MreRecord.type_class) - {'TES4', 'ACHR', 'ACRE', 'REFR',
                                          'CELL', 'PGRD', 'ROAD', 'LAND',
                                          'WRLD', 'INFO', 'DIAL'})

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

"""This modules defines static data for use by bush, when TES V:
   Skyrim is set at the active game."""

from .constants import *
from .default_tweaks import default_tweaks
from .records import MreCell, MreWrld, MreFact, MreAchr, MreDial, MreInfo, \
    MreCams, MreWthr, MreDual, MreMato, MreVtyp, MreMatt, MreLvsp, MreEnch, \
    MreProj, MreDlbr, MreRfct, MreMisc, MreActi, MreEqup, MreCpth, MreDoor, \
    MreAnio, MreHazd, MreIdlm, MreEczn, MreIdle, MreLtex, MreQust, MreMstt, \
    MreNpc, MreFlst, MreIpds, MreGmst, MreRevb, MreClmt, MreDebr, MreSmbn, \
    MreLvli, MreSpel, MreKywd, MreLvln, MreAact, MreSlgm, MreRegn, MreFurn, \
    MreGras, MreAstp, MreWoop, MreMovt, MreCobj, MreShou, MreSmen, MreColl, \
    MreArto, MreAddn, MreSopm, MreCsty, MreAppa, MreArma, MreArmo, MreKeym, \
    MreTxst, MreHdpt, MreHeader, MreAlch, MreBook, MreSpgd, MreSndr, MreImgs, \
    MreScrl, MreMust, MreFstp, MreFsts, MreMgef, MreLgtm, MreMusc, MreClas, \
    MreLctn, MreTact, MreBptd, MreDobj, MreLscr, MreDlvw, MreTree, MreWatr, \
    MreFlor, MreEyes, MreWeap, MreIngr, MreClfm, MreMesg, MreLigh, MreExpl, \
    MreLcrt, MreStat, MreAmmo, MreSmqn, MreImad, MreSoun, MreAvif, MreCont, \
    MreIpct, MreAspc, MreRela, MreEfsh, MreSnct, MreOtft
from ... import brec
from ...bolt import struct_pack, struct_unpack
from ...brec import MreGlob

#--Name of the game to use in UI.
displayName = 'Skyrim'
#--Name of the game's filesystem folder.
fsName = 'Skyrim'
#--Alternate display name to use instead of "Wrye Bash for ***"
altName = 'Wrye Smash'
#--Name of game's default ini file.
defaultIniFile = 'Skyrim_default.ini'

#--Exe to look for to see if this is the right game
exe = 'TESV.exe'

#--Registry keys to read to find the install location
regInstallKeys = ('Bethesda Softworks\\Skyrim', 'Installed Path')

#--patch information
patchURL = '' # Update via steam
patchTip = 'Update via Steam'

#--URL to the Nexus site for this game
nexusUrl = 'http://www.nexusmods.com/skyrim/'
nexusName = 'Skyrim Nexus'
nexusKey = 'bash.installers.openSkyrimNexus.continue'

# Bsa info
allow_reset_bsa_timestamps = False
bsa_extension = r'bsa'
supports_mod_inis = True
vanilla_string_bsas = {
    'skyrim.esm': ['Skyrim - Interface.bsa'],
    'update.esm': ['Skyrim - Interface.bsa'],
    'dawnguard.esm': ['Dawnguard.bsa'],
    'hearthfires.esm': ['Hearthfires.bsa'],
    'dragonborn.esm': ['Dragonborn.bsa'],
}
resource_archives_keys = ('sResourceArchiveList', 'sResourceArchiveList2')

# plugin extensions
espm_extensions = {'.esp', '.esm'}

# Load order info
using_txt_file = True

#--Creation Kit Set information
class cs:
    shortName = 'CK'                # Abbreviated name
    longName = 'Creation Kit'       # Full name
    exe = 'CreationKit.exe'         # Executable to run
    seArgs = None # u'-editor'       # Argument to pass to the SE to load the CS # Not yet needed
    imageName = 'creationkit%s.png' # Image name template for the status bar

#--Script Extender information
class se:
    shortName = 'SKSE'                      # Abbreviated name
    longName = 'Skyrim Script Extender'     # Full name
    exe = 'skse_loader.exe'                 # Exe to run
    steamExe = 'skse_loader.exe'            # Exe to run if a steam install
    url = 'http://skse.silverlock.org/'     # URL to download from
    urlTip = 'http://skse.silverlock.org/'  # Tooltip for mouse over the URL

#--Script Dragon
class sd:
    shortName = 'SD'
    longName = 'Script Dragon'
    installDir = 'asi'

#--SkyProc Patchers
class sp:
    shortName = 'SP'
    longName = 'SkyProc'
    installDir = 'SkyProc Patchers'

#--Quick shortcut for combining the SE and SD names
se_sd = se.shortName+'/'+sd.longName

#--Graphics Extender information
class ge:
    shortName = ''
    longName = ''
    exe = '**DNE**'
    url = ''
    urlTip = ''

#--4gb Launcher
class laa:
    # Skyrim has a 4gb Launcher, but as of patch 1.3.10, it is
    # no longer required (Bethsoft updated TESV.exe to already
    # be LAA)
    name = ''
    exe = '**DNE**'
    launchesSE = False

# Files BAIN shouldn't skip
dontSkip = (
       # These are all in the Interface folder. Apart from the skyui_ files,
       # they are all present in vanilla.
       'skyui_cfg.txt',
       'skyui_translate.txt',
       'credits.txt',
       'credits_french.txt',
       'fontconfig.txt',
       'controlmap.txt',
       'gamepad.txt',
       'mouse.txt',
       'keyboard_english.txt',
       'keyboard_french.txt',
       'keyboard_german.txt',
       'keyboard_spanish.txt',
       'keyboard_italian.txt',
)

# Directories where specific file extensions should not be skipped by BAIN
dontSkipDirs = {
                # This rule is to allow mods with string translation enabled.
                'interface\\translations':['.txt']
}

#Folders BAIN should never check
SkipBAINRefresh = {
    #Use lowercase names
    'tes5edit backups',
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
    ext = '.ess'               # Save file extension

#--INI files that should show up in the INI Edits tab
iniFiles = [
    'Skyrim.ini',
    'SkyrimPrefs.ini',
    ]

#--INI setting to setup Save Profiles
saveProfilesKey = ('General','SLocalSavePath')

#--The main plugin Wrye Bash should look for
masterFiles = [
    'Skyrim.esm',
    'Update.esm',
    ]

#The pickle file for this game. Holds encoded GMST IDs from the big list below.
pklfile = r'bash\db\Skyrim_ids.pkl'

#--BAIN: Directories that are OK to install to
dataDirs = {
    'dialogueviews',
    'interface',
    'meshes',
    'strings',
    'textures',
    'video',
    'lodsettings',
    'grass',
    'scripts',
    'shadersfx',
    'music',
    'sound',
    'seq',
}
dataDirsPlus = {
    'skse',
    'ini',
    'asi',
    'skyproc patchers',
    'calientetools', # bodyslide
    'dyndolod',
    'tools',
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
ignoreDataFiles = {
}
ignoreDataFilePrefixes = {
}
ignoreDataDirs = {
    'LSData'
}

#--Tags supported by this game
allTags = sorted((
    'C.Acoustic', 'C.Climate', 'C.Encounter', 'C.ImageSpace', 'C.Light',
    'C.Location', 'C.SkyLighting', 'C.Music', 'C.Name', 'C.Owner',
    'C.RecordFlags', 'C.Regions', 'C.Water', 'Deactivate', 'Delev',
    'Filter', 'Graphics', 'Invent', 'NoMerge', 'Relev', 'Sound',
    'Stats', 'Names',
    ))

#--Gui patcher classes available when building a Bashed Patch
patchers = (
    'AliasesPatcher', 'CellImporter', 'GmstTweaker', 'GraphicsPatcher',
    'ImportInventory', 'ListsMerger', 'PatchMerger', 'SoundPatcher',
    'StatsPatcher', 'NamesPatcher',
    )

#--CBash Gui patcher classes available when building a Bashed Patch
CBash_patchers = tuple()

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
    0x13740 : _('Argonian'),
    0x13741 : _('Breton'),
    0x13742 : _('Dark Elf'),
    0x13743 : _('High Elf'),
    0x13744 : _('Imperial'),
    0x13745 : _('Khajiit'),
    0x13746 : _('Nord'),
    0x13747 : _('Orc'),
    0x13748 : _('Redguard'),
    0x13749 : _('Wood Elf'),
    }

raceShortNames = {
    0x13740 : 'Arg',
    0x13741 : 'Bre',
    0x13742 : 'Dun',
    0x13743 : 'Alt',
    0x13744 : 'Imp',
    0x13745 : 'Kha',
    0x13746 : 'Nor',
    0x13747 : 'Orc',
    0x13748 : 'Red',
    0x13749 : 'Bos',
    }

raceHairMale = {
    0x13740 : 0x64f32, #--Arg
    0x13741 : 0x90475, #--Bre
    0x13742 : 0x64214, #--Dun
    0x13743 : 0x7b792, #--Alt
    0x13744 : 0x90475, #--Imp
    0x13745 : 0x653d4, #--Kha
    0x13746 : 0x1da82, #--Nor
    0x13747 : 0x66a27, #--Orc
    0x13748 : 0x64215, #--Red
    0x13749 : 0x690bc, #--Bos
    }

raceHairFemale = {
    0x13740 : 0x64f33, #--Arg
    0x13741 : 0x1da83, #--Bre
    0x13742 : 0x1da83, #--Dun
    0x13743 : 0x690c2, #--Alt
    0x13744 : 0x1da83, #--Imp
    0x13745 : 0x653d0, #--Kha
    0x13746 : 0x1da83, #--Nor
    0x13747 : 0x64218, #--Orc
    0x13748 : 0x64210, #--Red
    0x13749 : 0x69473, #--Bos
    }

#--Plugin format stuff
class esp:
    #--Wrye Bash capabilities
    canBash = True          # Can create Bashed Patches
    canCBash = False        # CBash can handle this game's records
    canEditHeader = True    # Can edit anything in the TES4 record

    #--Valid ESM/ESP header versions
    validHeaderVersions = (0.94, 1.70,)

    #--Strings Files
    stringsFiles = [
        (('Strings',), '%(body)s_%(language)s.STRINGS'),
        (('Strings',), '%(body)s_%(language)s.DLSTRINGS'),
        (('Strings',), '%(body)s_%(language)s.ILSTRINGS'),
    ]

#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# CLDC ------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# HAIR ------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# PWAT ------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# RGDL ------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# SCOL ------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Unused records, they have empty GRUP in skyrim.esm---------------------------
# SCPT ------------------------------------------------------------------------
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
mergeClasses = (
    # MreAchr, MreDial, MreInfo,
    # MreFact,
    MreAact, MreActi, MreAddn, MreAlch, MreAmmo, MreAnio, MreAppa, MreArma,
    MreArmo, MreArto, MreAspc, MreAstp, MreAvif, MreBook, MreBptd, MreCams,
    MreClas, MreClfm, MreClmt, MreCobj, MreColl, MreCont, MreCpth, MreCsty,
    MreDebr, MreDlbr, MreDlvw, MreDobj, MreDoor, MreDual, MreEczn, MreEfsh,
    MreEnch, MreEqup, MreExpl, MreEyes, MreFlor, MreFlst, MreFstp, MreFsts,
    MreFurn, MreGlob, MreGmst, MreGras, MreHazd, MreHdpt, MreIdle, MreIdlm,
    MreImad, MreImgs, MreIngr, MreIpct, MreIpds, MreKeym, MreKywd, MreLcrt,
    MreLctn, MreLgtm, MreLigh, MreLscr, MreLtex, MreLvli, MreLvln, MreLvsp,
    MreMato, MreMatt, MreMesg, MreMgef, MreMisc, MreMovt, MreMstt, MreMusc,
    MreMust, MreNpc, MreOtft, MreProj, MreRegn, MreRela, MreRevb, MreRfct,
    MreScrl, MreShou, MreSlgm, MreSmbn, MreSmen, MreSmqn, MreSnct, MreSndr,
    MreSopm, MreSoun, MreSpel, MreSpgd, MreStat, MreTact, MreTree, MreTxst,
    MreVtyp, MreWatr, MreWeap, MreWoop, MreWthr,
    ####### for debug
    MreQust,
)

#--Extra read classes: these record types will always be loaded, even if
# patchers don't need them directly (for example, MGEF for magic effects info)
# MreScpt is Oblivion/FO3/FNV Only
# MreMgef, has not been verified to be used here for Skyrim
readClasses = ()
writeClasses = ()

def init():
    # Due to a bug with py2exe, 'reload' doesn't function properly.  Instead of
    # re-executing all lines within the module, it acts like another 'import'
    # statement - in otherwords, nothing happens.  This means any lines that
    # affect outside modules must do so within this function, which will be
    # called instead of 'reload'

    #--Top types in Skyrim order.
    brec.RecordHeader.topTypes = [
        'GMST', 'KYWD', 'LCRT', 'AACT', 'TXST', 'GLOB', 'CLAS', 'FACT', 'HDPT',
        'HAIR', 'EYES', 'RACE', 'SOUN', 'ASPC', 'MGEF', 'SCPT', 'LTEX', 'ENCH',
        'SPEL', 'SCRL', 'ACTI', 'TACT', 'ARMO', 'BOOK', 'CONT', 'DOOR', 'INGR',
        'LIGH', 'MISC', 'APPA', 'STAT', 'SCOL', 'MSTT', 'PWAT', 'GRAS', 'TREE',
        'CLDC', 'FLOR', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'LVLN', 'KEYM', 'ALCH',
        'IDLM', 'COBJ', 'PROJ', 'HAZD', 'SLGM', 'LVLI', 'WTHR', 'CLMT', 'SPGD',
        'RFCT', 'REGN', 'NAVI', 'CELL', 'WRLD', 'DIAL', 'QUST', 'IDLE', 'PACK',
        'CSTY', 'LSCR', 'LVSP', 'ANIO', 'WATR', 'EFSH', 'EXPL', 'DEBR', 'IMGS',
        'IMAD', 'FLST', 'PERK', 'BPTD', 'ADDN', 'AVIF', 'CAMS', 'CPTH', 'VTYP',
        'MATT', 'IPCT', 'IPDS', 'ARMA', 'ECZN', 'LCTN', 'MESG', 'RGDL', 'DOBJ',
        'LGTM', 'MUSC', 'FSTP', 'FSTS', 'SMBN', 'SMQN', 'SMEN', 'DLBR', 'MUST',
        'DLVW', 'WOOP', 'SHOU', 'EQUP', 'RELA', 'SCEN', 'ASTP', 'OTFT', 'ARTO',
        'MATO', 'MOVT', 'SNDR', 'DUAL', 'SNCT', 'SOPM', 'COLL', 'CLFM', 'REVB']

    #-> this needs updating for Skyrim
    brec.RecordHeader.recordTypes = set(
        brec.RecordHeader.topTypes + ['GRUP', 'TES4', 'REFR', 'ACHR', 'ACRE',
                                      'LAND', 'INFO', 'NAVM', 'PHZD', 'PGRE'])
    brec.RecordHeader.plugin_form_version = 43

    #--Record Types
    brec.MreRecord.type_class = dict((x.classType,x) for x in (
        MreAchr, MreDial, MreInfo, MreAact, MreActi, MreAddn, MreAlch, MreAmmo,
        MreAnio, MreAppa, MreArma, MreArmo, MreArto, MreAspc, MreAstp, MreAvif,
        MreBook, MreBptd, MreCams, MreClas, MreClfm, MreClmt, MreCobj, MreColl,
        MreCont, MreCpth, MreCsty, MreDebr, MreDlbr, MreDlvw, MreDobj, MreDoor,
        MreDual, MreEczn, MreEfsh, MreEnch, MreEqup, MreExpl, MreEyes, MreFact,
        MreFlor, MreFlst, MreFstp, MreFsts, MreFurn, MreGlob, MreGmst, MreGras,
        MreHazd, MreHdpt, MreIdle, MreIdlm, MreImad, MreImgs, MreIngr, MreIpct,
        MreIpds, MreKeym, MreKywd, MreLcrt, MreLctn, MreLgtm, MreLigh, MreLscr,
        MreLtex, MreLvli, MreLvln, MreLvsp, MreMato, MreMatt, MreMesg, MreMgef,
        MreMisc, MreMovt, MreMstt, MreMusc, MreMust, MreNpc, MreOtft, MreProj,
        MreRegn, MreRela, MreRevb, MreRfct, MreScrl, MreShou, MreSlgm, MreSmbn,
        MreSmen, MreSmqn, MreSnct, MreSndr, MreSopm, MreSoun, MreSpel, MreSpgd,
        MreStat, MreTact, MreTree, MreTxst, MreVtyp, MreWatr, MreWeap, MreWoop,
        MreWthr, MreCell, MreWrld,  # MreNavm, MreNavi
        ####### for debug
        MreQust, MreHeader,
    ))

    #--Simple records
    brec.MreRecord.simpleTypes = (
        set(brec.MreRecord.type_class) - {'TES4', 'ACHR', 'CELL', 'DIAL',
                                          'INFO', 'WRLD', })

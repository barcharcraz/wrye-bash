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
"""Constants and classes to define for each new game - still a WIP."""

from .. import brec
# from .constants import * # TODO(ut): create a .constants module

#--Name of the game to use in UI.
displayName = '' ## Example: u'Skyrim'
#--Name of the game's filesystem folder.
fsName = '' ## Example: u'Skyrim'
#--Alternate display name of Wrye Bash when managing this game
altName = '' ## Example: u'Wrye Smash'

#--Exe to look for to see if this is the right game
exe = '' ## Example: u'TESV.exe'

#--Registry keys to read to find the install location
## These are relative to:
##  HKLM\Software
##  HKLM\Software\Wow6432Node
##  HKCU\Software
##  HKCU\Software\Wow6432Node
## Example: (u'Bethesda Softworks\\Oblivion', u'Installed Path')
regInstallKeys = ()

#--Patch information
## URL to download patches for the main game.
patchURL = ''
## Tooltip to display over the URL when displayed
patchTip = ''

#--URL to the Nexus site for this game
nexusUrl = ''  #-- URL
nexusName = '' #-- Long Name
nexusKey = ''  #-- Key for the "always ask this question" setting in settings.dat

# Bsa info
allow_reset_bsa_timestamps = False
bsa_extension = r'bsa'
supports_mod_inis = True # this game supports mod ini files aka ini fragments
vanilla_string_bsas = {}
resource_archives_keys = ()

# plugin extensions
espm_extensions = {'.esp', '.esm'}

# Load order info
using_txt_file = True

#--Construction Set information
class cs:
    imageName = ''   # Image name template for the status bar
    longName = ''    # Full name
    exe = '*DNE*'    # Executable to run
    shortName = ''   # Abbreviated name
    seArgs = ''      # Argument to pass to the SE to load the CS

#--Script Extender information
class se:
    shortName = ''   # Abbreviated name.  If this is empty, it signals that no SE is available
    longname = ''    # Full name
    exe = ''         # Exe to run
    steamExe = ''    # Exe to run if a steam install
    url = ''         # URL to download from
    urlTip = ''      # Tooltip for mouse over the URL

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
se_sd = ''

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
    exe = ''
    url = ''
    urlTip = ''

#--4gb Launcher
class laa:
    name = ''          # Display name of the launcher
    exe = '*DNE*'      # Executable to run
    launchesSE = False  # Whether the launcher will automatically launch the SE

# Files BAIN shouldn't skip
dontSkip = (
# Nothing so far
)

# Directories where specific file extensions should not be skipped by BAIN
dontSkipDirs = {
# Nothing so far
}

#--Folders BAIN should never CRC check in the Data directory
SkipBAINRefresh = set((
    # Use lowercase names
))

#--Some stuff dealing with INI files
class ini:
    #--True means new lines are allowed to be added via INI tweaks
    #  (by default)
    allowNewLines = False

    #--INI Entry to enable BSA Redirection
    bsaRedirection = ('Archive','sArchiveList')

#--Save Game format stuff
class ess:
    # Save file capabilities
    canReadBasic = False    # Can read the info needed for the Save Tab display
    canEditMore = False     # Advanced editing
    ext = '.ess'           # Save file extension

#--The main plugin Wrye Bash should look for
masterFiles = [
    ]

#--INI files that should show up in the INI Edits tab
## Example: [u'Oblivion.ini']
iniFiles = [
    ]

#-- INI setting used to setup Save Profiles
## (section,key)
saveProfilesKey = ('General','SLocalSavePath')

#--BAIN:
## These are the allowed default data directories that BAIN can install to
dataDirs = set()
## These are additional special directories that BAIN can install to
dataDirsPlus = set()

# Installer -------------------------------------------------------------------
# ensure all path strings are prefixed with 'r' to avoid interpretation of
#   accidental escape sequences
wryeBashDataFiles = {'Bashed Patch.esp', 'Bashed Patch, 0.esp',
                     'Bashed Patch, 1.esp', 'Bashed Patch, 2.esp',
                     'Bashed Patch, 3.esp', 'Bashed Patch, 4.esp',
                     'Bashed Patch, 5.esp', 'Bashed Patch, 6.esp',
                     'Bashed Patch, 7.esp', 'Bashed Patch, 8.esp',
                     'Bashed Patch, 9.esp', 'Bashed Patch, CBash.esp',
                     'Bashed Patch, Python.esp', 'Bashed Patch, FCOM.esp',
                     'Bashed Patch, Warrior.esp', 'Bashed Patch, Thief.esp',
                     'Bashed Patch, Mage.esp', 'Bashed Patch, Test.esp',
                     'ArchiveInvalidationInvalidated!.bsa',
                     'Docs\\Bash Readme Template.html',
                     'Docs\\wtxt_sand_small.css', 'Docs\\wtxt_teal.css',
                     'Docs\\Bash Readme Template.txt'}
wryeBashDataDirs = {'Bash Patches\\', 'INI Tweaks\\'}
ignoreDataFiles = set()
ignoreDataFilePrefixes = set()
ignoreDataDirs = set()

#--Plugin format stuff
class esp:
    #--Wrye Bash capabilities
    canBash = False         # Can create Bashed Patches
    canEditHeader = False   # Can edit basic info in the TES4 record

    #--Valid ESM/ESP header versions
    ## These are the valid 'version' numbers for the game file headers
    validHeaderVersions = tuple()

    #--Class to use to read the TES4 record
    ## This is the class name in bosh.py to use for the TES4 record when reading
    ## Example: 'MreTes4'
    tes4ClassName = ''

#--The pickle file for this game.  Holds encoded GMST IDs from the big list below
pklfile = r'bash\db\*GAMENAME*_ids.pkl'

#--Bash Tags supported by this game
allTags = sorted(())

#--Patcher available when building a Bashed Patch (referenced by class name)
patchers = ()

#--CBash patchers available when building a Bashed Patch
CBash_patchers = ()

#--Mergeable record types
mergeClasses = (
)

#--Extra read classes: these record types will always be loaded, even if patchers
#  don't need them directly (for example, for MGEF info)
readClasses = ()
writeClasses = ()

def init():
    # Due to a bug with py2exe, 'reload' doesn't function properly.  Instead of
    # re-executing all lines within the module, it acts like another 'import'
    # statement - in other words, nothing happens.  This means any lines that
    # affect outside modules must do so within this function, which will be
    # called instead of 'reload'

    #--Top types in order of the main ESM
    brec.RecordHeader.topTypes = []
    brec.RecordHeader.recordTypes = set(
        brec.RecordHeader.topTypes + ['GRUP', 'TES4'])

    #--Record Types
    brec.MreRecord.type_class = dict((x.classType,x) for x in  (
	    ))

    #--Simple records
    brec.MreRecord.simpleTypes = (set(brec.MreRecord.type_class) - {'TES4'})

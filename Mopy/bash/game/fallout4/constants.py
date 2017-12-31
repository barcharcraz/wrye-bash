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

#--Game ESM/ESP/BSA files
#  These filenames need to be in lowercase,
bethDataFiles = {
    #--Vanilla
    'fallout4.esm',
    'fallout4.cdx',
    'fallout4 - animations.ba2',
    'fallout4 - geometry.csg',
    'fallout4 - interface.ba2',
    'fallout4 - materials.ba2',
    'fallout4 - meshes.ba2',
    'fallout4 - meshesextra.ba2',
    'fallout4 - misc.ba2',
    'fallout4 - nvflex.ba2',
    'fallout4 - shaders.ba2',
    'fallout4 - sounds.ba2',
    'fallout4 - startup.ba2',
    'fallout4 - textures1.ba2',
    'fallout4 - textures2.ba2',
    'fallout4 - textures3.ba2',
    'fallout4 - textures4.ba2',
    'fallout4 - textures5.ba2',
    'fallout4 - textures6.ba2',
    'fallout4 - textures7.ba2',
    'fallout4 - textures8.ba2',
    'fallout4 - textures9.ba2',
    'fallout4 - voices.ba2',
    'dlcrobot.esm',
    'dlcrobot.cdx',
    'dlcrobot - geometry.csg',
    'dlcrobot - main.ba2',
    'dlcrobot - textures.ba2',
    'dlcrobot - voices_en.ba2',
    'dlcworkshop01.esm',
    'dlcworkshop01.cdx',
    'dlcworkshop01 - geometry.csg',
    'dlcworkshop01 - main.ba2',
    'dlcworkshop01 - textures.ba2',
    'dlccoast.esm',
    'dlccoast.cdx',
    'dlccoast - geometry.csg',
    'dlccoast - main.ba2',
    'dlccoast - textures.ba2',
    'dlccoast - voices_en.ba2',
    'dlcworkshop02.esm',
    'dlcworkshop02 - main.ba2',
    'dlcworkshop02 - textures.ba2',
    'dlcworkshop03.esm',
    'dlcworkshop03.cdx',
    'dlcworkshop03 - geometry.csg',
    'dlcworkshop03 - main.ba2',
    'dlcworkshop03 - textures.ba2',
    'dlcworkshop03 - voices_en.ba2',
    'dlcnukaworld.esm',
    'dlcnukaworld.cdx',
    'dlcnukaworld - geometry.csg',
    'dlcnukaworld - main.ba2',
    'dlcnukaworld - textures.ba2',
    'dlcnukaworld - voices_en.ba2',
}

#--Every file in the Data directory from Bethsoft
allBethFiles = {
    # Section 1: Vanilla files
    'Fallout4.esm',
    'Fallout4.cdx',
    'Fallout4 - Animations.ba2',
    'Fallout4 - Geometry.csg',
    'Fallout4 - Interface.ba2',
    'Fallout4 - Materials.ba2',
    'Fallout4 - Meshes.ba2',
    'Fallout4 - MeshesExtra.ba2',
    'Fallout4 - Misc.ba2',
    'Fallout4 - Nvflex.ba2',
    'Fallout4 - Shaders.ba2',
    'Fallout4 - Sounds.ba2',
    'Fallout4 - Startup.ba2',
    'Fallout4 - Textures1.ba2',
    'Fallout4 - Textures2.ba2',
    'Fallout4 - Textures3.ba2',
    'Fallout4 - Textures4.ba2',
    'Fallout4 - Textures5.ba2',
    'Fallout4 - Textures6.ba2',
    'Fallout4 - Textures7.ba2',
    'Fallout4 - Textures8.ba2',
    'Fallout4 - Textures9.ba2',
    'Fallout4 - Voices.ba2',
    'DLCRobot.esm',
    'DLCRobot.cdx',
    'DLCRobot - Geometry.csg',
    'DLCRobot - Main.ba2',
    'DLCRobot - Textures.ba2',
    'DLCRobot - Voices_en.ba2',
    'DLCworkshop01.esm',
    'DLCworkshop01.cdx',
    'DLCworkshop01 - Geometry.csg',
    'DLCworkshop01 - Main.ba2',
    'DLCworkshop01 - Textures.ba2',
    'DLCCoast.esm',
    'DLCCoast.cdx',
    'DLCCoast - Geometry.csg',
    'DLCCoast - Main.ba2',
    'DLCCoast - Textures.ba2',
    'DLCCoast - Voices_en.ba2',
    'DLCworkshop02.esm',
    'DLCworkshop02 - Main.ba2',
    'DLCworkshop02 - Textures.ba2',
    'DLCworkshop03.esm',
    'DLCworkshop03.cdx',
    'DLCworkshop03 - Geometry.csg',
    'DLCworkshop03 - Main.ba2',
    'DLCworkshop03 - Textures.ba2',
    'DLCworkshop03 - Voices_en.ba2',
    'DLCNukaWorld.esm',
    'DLCNukaWorld.cdx',
    'DLCNukaWorld - Geometry.csg',
    'DLCNukaWorld - Main.ba2',
    'DLCNukaWorld - Textures.ba2',
    'DLCNukaWorld - Voices_en.ba2',
    # Section 2: Video Clips
    'Video\\AGILITY.bk2',
    'Video\\CHARISMA.bk2',
    'Video\\Endgame_FEMALE_A.bk2',
    'Video\\Endgame_FEMALE_B.bk2',
    'Video\\Endgame_MALE_A.bk2',
    'Video\\Endgame_MALE_B.bk2',
    'Video\\ENDURANCE.bk2',
    'Video\\GameIntro_V3_B.bk2',
    'Video\\INTELLIGENCE.bk2',
    'Video\\Intro.bk2',
    'Video\\LUCK.bk2',
    'Video\\MainMenuLoop.bk2',
    'Video\\PERCEPTION.bk2',
    'Video\\STRENGTH.bk2',
    # Section 3: F4SE INI File
    'F4SE\\f4se.ini',
    # Section 4: GECK files
	'Scripts\\Source\\Base\\Base.zip',
	'Scripts\\Source\\DLC01\\DLC01.zip',
	'Scripts\\Source\\DLC02\\DLC02.zip',
	'Scripts\\Source\\DLC03\\DLC03.zip',
	'Scripts\\Source\\DLC04\\DLC04.zip',
	'Scripts\\Source\\DLC05\\DLC05.zip',
	'Scripts\\Source\\DLC06\\DLC06.zip',
	# Section 5: Other Files
	'LSData\\DtC6dal.dat',
	'LSData\\DtC6dl.dat',
	'LSData\\Wt8S9bs.dat',
	'LSData\\Wt8S9fs.dat',
	'LSData\\Wt16M9bs.dat',
	'LSData\\Wt16M9fs.dat',
}

# Function Info ---------------------------------------------------------------
conditionFunctionData = tuple()

allConditions = set(entry[0] for entry in conditionFunctionData)
fid1Conditions = set(entry[0] for entry in conditionFunctionData if entry[2] == 2)
fid2Conditions = set(entry[0] for entry in conditionFunctionData if entry[3] == 2)
# Skip 3 and 4 because it needs to be set per runOn
fid5Conditions = set(entry[0] for entry in conditionFunctionData if entry[4] == 2)

#--List of GMST's in the main plugin (Fallout4.esm) that have 0x00000000
#  as the form id.  Any GMST as such needs it Editor Id listed here.
gmstEids = [
    ## TODO: Initial inspection did not seem to have any null FormID GMST's,
    ## double check before enabling the GMST Tweaker
    ]

"""
GLOB record tweaks used by patcher.patchers.multitweak_settings.GmstTweaker

Each entry is a tuple in the following format:
  (DisplayText, MouseoverText, GLOB EditorID, Option1, Option2, ..., OptionN)
  -EditorID can be a plain string, or a tuple of multiple Editor IDs.  If
  it's a tuple, then Value (below) must be a tuple of equal length, providing
  values for each GLOB
Each Option is a tuple:
  (DisplayText, Value)
  - If you enclose DisplayText in brackets like this: _(u'[Default]'),
  then the patcher will treat this option as the default value.
  - If you use _(u'Custom') as the entry, the patcher will bring up a number
  input dialog

To make a tweak Enabled by Default, enclose the tuple entry for the tweak in
a list, and make a dictionary as the second list item with {'defaultEnabled
':True}. See the UOP Vampire face fix for an example of this (in the GMST
Tweaks)
"""
GlobalsTweaks = list()

"""
GMST record tweaks used by patcher.patchers.multitweak_settings.GmstTweaker

Each entry is a tuple in the following format:
  (DisplayText, MouseoverText, GMST EditorID, Option1, Option2, ..., OptionN)
  - EditorID can be a plain string, or a tuple of multiple Editor IDs. If
  it's a tuple, then Value (below) must be a tuple of equal length, providing
  values for each GMST
Each Option is a tuple:
  (DisplayText, Value)
  - If you enclose DisplayText in brackets like this: _(u'[Default]'),
  then the patcher will treat this option as the default value.
  - If you use _(u'Custom') as the entry, the patcher will bring up a number
  input dialog

To make a tweak Enabled by Default, enclose the tuple entry for the tweak in
a list, and make a dictionary as the second list item with {'defaultEnabled
':True}. See the UOP Vampire facefix for an example of this (in the GMST
Tweaks)
"""
GmstTweaks = list()

#------------------------------------------------------------------------------
# ListsMerger
#------------------------------------------------------------------------------
listTypes = ('LVLI','LVLN',)
#------------------------------------------------------------------------------
# NamesPatcher
#------------------------------------------------------------------------------
# remaining to add: 'PERK', 'RACE',
namesTypes = set()
#------------------------------------------------------------------------------
# ItemPrices Patcher
#------------------------------------------------------------------------------
pricesTypes = dict()

#------------------------------------------------------------------------------
# StatsImporter
#------------------------------------------------------------------------------
statsTypes = dict()
statsHeaders = tuple()

#------------------------------------------------------------------------------
# SoundPatcher
#------------------------------------------------------------------------------
# Needs longs in SoundPatcher
soundsLongsTypes = set() # initialize with literal
soundsTypes = {}
#------------------------------------------------------------------------------
# CellImporter
#------------------------------------------------------------------------------
cellAutoKeys = set()
cellRecAttrs = {}
cellRecFlags = {}
#------------------------------------------------------------------------------
# GraphicsPatcher
#------------------------------------------------------------------------------
graphicsLongsTypes = set() # initialize with literal
graphicsTypes = {}
graphicsFidTypes = {}
graphicsModelAttrs = ()
#------------------------------------------------------------------------------
# Inventory Patcher
#------------------------------------------------------------------------------
inventoryTypes = ('NPC_','CONT',)

# Record type to name dictionary
record_type_name = {}

# xEdit menu string and key for expert setting
xEdit_expert = (_('FO4Edit Expert'), 'fo4View.iKnowWhatImDoing')

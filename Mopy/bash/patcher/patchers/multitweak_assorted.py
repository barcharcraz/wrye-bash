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

"""This module contains oblivion multitweak item patcher classes that belong
to the Assorted Multitweaker - as well as the AssortedTweaker itself."""
import collections
import random
import re
# Internal
from ...bolt import GPath
from ...brec import MreRecord
from ... import load_order
from ... import bush # from ....bush import game ? # should be set by now !
from ...cint import MGEFCode
from ...patcher.base import AMultiTweakItem
from ...patcher.patchers.base import MultiTweakItem, CBash_MultiTweakItem
from ...patcher.patchers.base import MultiTweaker, CBash_MultiTweaker

# Patchers: 30 ----------------------------------------------------------------
class AssortedTweak_ArmorShows(MultiTweakItem):
    """Fix armor to show amulets/rings."""
    tweak_read_classes = 'ARMO',

    #--Config Phase -----------------------------------------------------------
    def __init__(self,label,tip,key):
        super(AssortedTweak_ArmorShows, self).__init__(label,tip,key)
        self.hidesBit = {'armorShowsRings':16,'armorShowsAmulets':17}[key]
        self.logMsg = '* '+_('Armor Pieces Tweaked') + ': %d'

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.ARMO
        hidesBit = self.hidesBit
        for record in modFile.ARMO.getActiveRecords():
            if record.flags[hidesBit] and not record.flags.notPlayable:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        hidesBit = self.hidesBit
        for record in patchFile.ARMO.records:
            if record.flags[hidesBit] and not record.flags.notPlayable:
                record.flags[hidesBit] = False
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_ArmorShows(CBash_MultiTweakItem):
    """Fix armor to show amulets/rings."""
    name = _('Armor Tweaks')
    tweak_read_classes = 'ARMO',

    #--Config Phase -----------------------------------------------------------
    def __init__(self,label,tip,key):
        super(CBash_AssortedTweak_ArmorShows, self).__init__(label,tip,key)
        self.hideFlag = {'armorShowsRings': 'IsHideRings',
                         'armorShowsAmulets': 'IsHideAmulets'}[key]
        self.logMsg = '* '+_('Armor Pieces Tweaked') + ': %d'

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.IsNonPlayable:
            return
        if getattr(record, self.hideFlag):
            override = record.CopyAsOverride(self.patchFile)
            if override:
                setattr(override, self.hideFlag, False)
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AssortedTweak_ClothingShows(MultiTweakItem):
    """Fix robes, gloves and the like to show amulets/rings."""
    tweak_read_classes = 'CLOT',

    #--Config Phase -----------------------------------------------------------
    def __init__(self,label,tip,key):
        super(AssortedTweak_ClothingShows, self).__init__(label,tip,key)
        self.hidesBit = \
            {'ClothingShowsRings': 16, 'ClothingShowsAmulets': 17}[key]
        self.logMsg = '* '+_('Clothing Pieces Tweaked') + ': %d'

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.CLOT
        hidesBit = self.hidesBit
        for record in modFile.CLOT.getActiveRecords():
            if record.flags[hidesBit] and not record.flags.notPlayable:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        hidesBit = self.hidesBit
        for record in patchFile.CLOT.records:
            if record.flags[hidesBit] and not record.flags.notPlayable:
                record.flags[hidesBit] = False
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_ClothingShows(CBash_MultiTweakItem):
    """Fix robes, gloves and the like to show amulets/rings."""
    name = _('Clothing Tweaks')
    tweak_read_classes = 'CLOT',

    #--Config Phase -----------------------------------------------------------
    def __init__(self,label,tip,key):
        super(CBash_AssortedTweak_ClothingShows, self).__init__(label,tip,key)
        self.hideFlag = {'ClothingShowsRings': 'IsHideRings',
                         'ClothingShowsAmulets': 'IsHideAmulets'}[key]
        self.logMsg = '* '+_('Clothing Pieces Tweaked') + ': %d'

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.IsNonPlayable:
            return
        if getattr(record, self.hideFlag):
            override = record.CopyAsOverride(self.patchFile)
            if override:
                setattr(override, self.hideFlag, False)
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_BowReach(AMultiTweakItem):
    """Fix bows to have reach = 1.0."""
    tweak_read_classes = 'WEAP',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_BowReach, self).__init__(_("Bow Reach Fix"),
            _('Fix bows with zero reach. (Zero reach causes CTDs.)'),
            'BowReach',
            ('1.0',  '1.0'),
            )
        self.defaultEnabled = True
        self.logMsg = '* '+_('Bows fixed') + ': %d'

class AssortedTweak_BowReach(AAssortedTweak_BowReach,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.WEAP
        for record in modFile.WEAP.getActiveRecords():
            if record.weaponType == 5 and record.reach <= 0:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.WEAP.records:
            if record.weaponType == 5 and record.reach <= 0:
                record.reach = 1
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_BowReach(AAssortedTweak_BowReach,
                                   CBash_MultiTweakItem):
    name = _('Bow Reach Fix')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.IsBow and record.reach <= 0:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.reach = 1.0
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_SkyrimStyleWeapons(AMultiTweakItem):
    """Sets all one handed weapons as blades, two handed weapons as blunt."""
    tweak_read_classes = 'WEAP',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_SkyrimStyleWeapons, self).__init__(
            _("Skyrim-style Weapons"),
            _('Sets all one handed weapons as blades, two handed weapons '
              'as blunt.'), 'skyrimweaponsstyle', ('1.0', '1.0'), )
        self.logMsg = '* '+_('Weapons Adjusted') + ': %d'

class AssortedTweak_SkyrimStyleWeapons(AAssortedTweak_SkyrimStyleWeapons,
                                       MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.WEAP
        for record in modFile.WEAP.getActiveRecords():
            if record.weaponType in [1,2]:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.WEAP.records:
            if record.weaponType == 1:
                record.weaponType = 3
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
            elif record.weaponType == 2:
                record.weaponType = 0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_SkyrimStyleWeapons(AAssortedTweak_SkyrimStyleWeapons,
                                             CBash_MultiTweakItem):
    name = _('Skyrim-style Weapons')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.IsBlade2Hand or record.IsBlunt1Hand:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                if override.IsBlade2Hand:
                    override.IsBlunt2Hand = True
                else:
                    override.IsBlade1Hand = True
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_ConsistentRings(AMultiTweakItem):
    """Sets rings to all work on same finger."""
    tweak_read_classes = 'CLOT',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_ConsistentRings, self).__init__(
            _("Right Hand Rings"),
            _('Fixes rings to unequip consistently by making them prefer '
              'the right hand.'), 'ConsistentRings', ('1.0', '1.0'), )
        self.defaultEnabled = True
        self.logMsg = '* '+_('Rings fixed') + ': %d'

class AssortedTweak_ConsistentRings(AAssortedTweak_ConsistentRings,
                                    MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.CLOT
        for record in modFile.CLOT.getActiveRecords():
            if record.flags.leftRing:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.CLOT.records:
            if record.flags.leftRing:
                record.flags.leftRing = False
                record.flags.rightRing = True
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_ConsistentRings(AAssortedTweak_ConsistentRings,
                                          CBash_MultiTweakItem):
    name = _('Right Hand Rings')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsLeftRing:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.IsLeftRing = False
                override.IsRightRing = True
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID
#------------------------------------------------------------------------------
rePlayableSkips = re.compile(
    r'(?:skin)|(?:test)|(?:mark)|(?:token)|(?:willful)|(?:see.*me)|('
    r'?:werewolf)|(?:no wings)|(?:tsaesci tail)|(?:widget)|(?:dummy)|('
    r'?:ghostly immobility)|(?:corpse)', re.I)

class AAssortedTweak_ClothingPlayable(AMultiTweakItem):
    """Sets all clothes to playable"""
    tweak_read_classes = 'CLOT',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_ClothingPlayable, self).__init__(
            _("All Clothing Playable"),
            _('Sets all clothing to be playable.'), 'PlayableClothing',
            ('1.0', '1.0'), )
        self.logHeader = '=== '+_('Playable Clothes')
        self.logMsg = '* '+_('Clothes set as playable') + ': %d'

class AssortedTweak_ClothingPlayable(AAssortedTweak_ClothingPlayable,
                                     MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.CLOT
        for record in modFile.CLOT.getActiveRecords():
            if record.flags.notPlayable:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.CLOT.records:
            if record.flags.notPlayable:
                full = record.full
                if not full: continue
                if record.script: continue
                if rePlayableSkips.search(full): continue  # probably truly
                # shouldn't be playable
                # If only the right ring and no other body flags probably a
                # token that wasn't zeroed (which there are a lot of).
                if record.flags.leftRing != 0 or record.flags.foot != 0 or \
                                record.flags.hand != 0 or \
                                record.flags.amulet != 0 or \
                                record.flags.lowerBody != 0 or \
                                record.flags.upperBody != 0 or \
                                record.flags.head != 0 or record.flags.hair \
                        != 0 or record.flags.tail != 0:
                    record.flags.notPlayable = 0
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_ClothingPlayable(AAssortedTweak_ClothingPlayable,
                                           CBash_MultiTweakItem):
    scanOrder = 29 #Run before the show clothing tweaks
    editOrder = 29
    name = _('Playable Clothes')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsNonPlayable:
            full = record.full
            if not full: return
            if record.script: return
            if rePlayableSkips.search(full): return  # probably truly
            # shouldn't be playable
            # If only the right ring and no other body flags probably a
            # token that wasn't zeroed (which there are a lot of).
            if record.IsLeftRing or record.IsFoot or record.IsHand or \
                    record.IsAmulet or record.IsLowerBody or \
                    record.IsUpperBody or record.IsHead or record.IsHair or \
                    record.IsTail:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.IsNonPlayable = False
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

class AAssortedTweak_ArmorPlayable(AMultiTweakItem):
    """Sets all armors to be playable"""
    tweak_read_classes = 'ARMO',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_ArmorPlayable, self).__init__(
            _("All Armor Playable"), _('Sets all armor to be playable.'),
            'PlayableArmor', ('1.0', '1.0'), )
        self.logHeader = '=== '+_('Playable Armor')
        self.logMsg = '* '+_('Armor pieces set as playable') + ': %d'

class AssortedTweak_ArmorPlayable(AAssortedTweak_ArmorPlayable,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.ARMO
        for record in modFile.ARMO.getActiveRecords():
            if record.flags.notPlayable:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.ARMO.records:
            if record.flags.notPlayable:
                full = record.full
                if not full: continue
                if record.script: continue
                if rePlayableSkips.search(full): continue  # probably truly
                # shouldn't be playable
                # We only want to set playable if the record has at least
                # one body flag... otherwise most likely a token.
                if record.flags.leftRing != 0 or record.flags.rightRing != 0\
                        or record.flags.foot != 0 or record.flags.hand != 0 \
                        or record.flags.amulet != 0 or \
                                record.flags.lowerBody != 0 or \
                                record.flags.upperBody != 0 or \
                                record.flags.head != 0 or record.flags.hair \
                        != 0 or record.flags.tail != 0 or \
                                record.flags.shield != 0:
                    record.flags.notPlayable = 0
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_ArmorPlayable(AAssortedTweak_ArmorPlayable,
                                        CBash_MultiTweakItem):
    scanOrder = 29 #Run before the show armor tweaks
    editOrder = 29
    name = _('Playable Armor')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsNonPlayable:
            full = record.full
            if not full: return
            if record.script: return
            if rePlayableSkips.search(full): return  # probably truly
            # shouldn't be playable
            # If no body flags are set it is probably a token.
            if record.IsLeftRing or record.IsRightRing or record.IsFoot or \
                    record.IsHand or record.IsAmulet or record.IsLowerBody \
                    or record.IsUpperBody or record.IsHead or record.IsHair \
                    or record.IsTail or record.IsShield:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.IsNonPlayable = False
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_DarnBooks(AMultiTweakItem):
    """DarNifies books.""" ##: C and P implementations have very similar code
    reColor = re.compile(r'<font color="?([a-fA-F0-9]+)"?>',re.I+re.M)
    reTagInWord = re.compile(r'([a-z])<font face=1>',re.M)
    reFont1 = re.compile(r'(<?<font face=1( ?color=[0-9a-zA]+)?>)+',re.I|re.M)
    reDiv = re.compile(r'<div',re.I+re.M)
    reFont = re.compile(r'<font',re.I+re.M)
    reHead2 = re.compile(r'^(<<|\^\^|>>|)==\s*(\w[^=]+?)==\s*\r\n',re.M)
    reHead3 = re.compile(r'^(<<|\^\^|>>|)===\s*(\w[^=]+?)\r\n',re.M)
    reBold = re.compile(r'(__|\*\*|~~)')
    reAlign = re.compile(r'^(<<|\^\^|>>)',re.M)
    tweak_read_classes = 'BOOK',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_DarnBooks, self).__init__(_("DarNified Books"),
            _('Books will be reformatted for DarN UI.'),
            'DarnBooks',
            ('default',  'default'),
            )
        self.logMsg = '* '+_('Books DarNified') + ': %d'

class AssortedTweak_DarnBooks(AAssortedTweak_DarnBooks,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        # maxWeight = self.choiceValues[self.chosen][0] # TODO: is this
        # supposed to be used ?
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.BOOK
        id_records = patchBlock.id_records
        for record in modFile.BOOK.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if not record.enchantment:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        reColor = self.__class__.reColor
        reTagInWord = self.__class__.reTagInWord
        reFont1 = self.__class__.reFont1
        reDiv = self.__class__.reDiv
        reFont = self.__class__.reFont
        reHead2 = self.__class__.reHead2
        reHead3 = self.__class__.reHead3
        reBold = self.__class__.reBold
        reAlign = self.__class__.reAlign
        keep = patchFile.getKeeper()
        align_text = {'^^':'center','<<':'left','>>':'right'}
        self.inBold = False
        def replaceBold(mo):
            self.inBold = not self.inBold
            return '<font face=3 color=%s>' % (
                '440000' if self.inBold else '444444')
        def replaceAlign(mo):
            return '<div align=%s>' % align_text[mo.group(1)]
        for record in patchFile.BOOK.records:
            if record.text and not record.enchantment:
                text = record.text
                text = text.replace('\u201d', '')  # there are some FUNKY
                # quotes that don't translate properly. (they are in *latin*
                # encoding not even cp1252 or something normal but non-unicode)
                if reHead2.match(text):
                    self.inBold = False
                    text = reHead2.sub(
                        r'\1<font face=1 color=220000>\2<font face=3 '
                        r'color=444444>\r\n', text)
                    text = reHead3.sub(
                        r'\1<font face=3 color=220000>\2<font face=3 '
                        r'color=444444>\r\n',
                        text)
                    text = reAlign.sub(replaceAlign,text)
                    text = reBold.sub(replaceBold,text)
                    text = re.sub(r'\r\n',r'<br>\r\n',text)
                else:
                    maColor = reColor.search(text)
                    if maColor:
                        color = maColor.group(1)
                    elif record.flags.isScroll:
                        color = '000000'
                    else:
                        color = '444444'
                    fontFace = '<font face=3 color='+color+'>'
                    text = reTagInWord.sub(r'\1',text)
                    text.lower()
                    if reDiv.search(text) and not reFont.search(text):
                        text = fontFace+text
                    else:
                        text = reFont1.sub(fontFace,text)
                if text != record.text:
                    record.text = text
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_DarnBooks(AAssortedTweak_DarnBooks,
                                    CBash_MultiTweakItem):
    name = _('Books DarNified')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        def replaceBold(mo):
            self.inBold = not self.inBold
            return '<font face=3 color=%s>' % (
                '440000' if self.inBold else '444444')
        def replaceAlign(mo):
            return '<div align=%s>' % align_text[mo.group(1)]

        if record.text and not record.enchantment:
            text = record.text
            text = text.replace('\u201d', '')  # there are some FUNKY
            # quotes that don't translate properly. (they are in *latin*
            # encoding not even cp1252 or something normal but non-unicode)
            reColor = self.__class__.reColor
            reTagInWord = self.__class__.reTagInWord
            reFont1 = self.__class__.reFont1
            reDiv = self.__class__.reDiv
            reFont = self.__class__.reFont
            reHead2 = self.__class__.reHead2
            reHead3 = self.__class__.reHead3
            reBold = self.__class__.reBold
            reAlign = self.__class__.reAlign
            align_text = {'^^':'center','<<':'left','>>':'right'}
            self.inBold = False
            if reHead2.match(text):
                text = reHead2.sub(
                    r'\1<font face=1 color=220000>\2<font face=3 '
                    r'color=444444>\r\n', text)
                text = reHead3.sub(
                    r'\1<font face=3 color=220000>\2<font face=3 '
                    r'color=444444>\r\n', text)
                text = reAlign.sub(replaceAlign,text)
                text = reBold.sub(replaceBold,text)
                text = re.sub(r'\r\n',r'<br>\r\n',text)
            else:
                maColor = reColor.search(text)
                if maColor:
                    color = maColor.group(1)
                elif record.IsScroll:
                    color = '000000'
                else:
                    color = '444444'
                fontFace = '<font face=3 color='+color+'>'
                text = reTagInWord.sub(r'\1',text)
                text.lower()
                if reDiv.search(text) and not reFont.search(text):
                    text = fontFace+text
                else:
                    text = reFont1.sub(fontFace,text)
            if text != record.text:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.text = text
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_FogFix(AMultiTweakItem):
    """Fix fog in cell to be non-zero."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_FogFix, self).__init__(_("Nvidia Fog Fix"),
            _('Fix fog related Nvidia black screen problems.'),
            'FogFix',
            ('0.0001',  '0.0001'),
            )
        self.logMsg = '* '+_('Cells with fog tweaked to 0.0001') + ': %d'
        self.defaultEnabled = True

class AssortedTweak_FogFix(AAssortedTweak_FogFix,MultiTweakItem):
    tweak_read_classes = 'CELL', 'WRLD',

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self, modFile, progress,patchFile):
        """Add lists from modFile."""
        if 'CELL' not in modFile.tops: return
        patchCells = patchFile.CELL
        modFile.convertToLongFids(('CELL',))
        for cellBlock in modFile.CELL.cellBlocks:
            cell = cellBlock.cell
            if not (cell.fogNear or cell.fogFar or cell.fogClip):
                patchCells.setCell(cell)

    def buildPatch(self,log,progress,patchFile):
        """Adds merged lists to patchfile."""
        keep = patchFile.getKeeper()
        count = collections.defaultdict(int)
        for cellBlock in patchFile.CELL.cellBlocks:
            cell = cellBlock.cell
            if not (cell.fogNear or cell.fogFar or cell.fogClip):
                cell.fogNear = 0.0001
                keep(cell.fid)
                count[cell.fid[0]] += 1
        self._patchLog(log, count)

class CBash_AssortedTweak_FogFix(AAssortedTweak_FogFix,CBash_MultiTweakItem):
    name = _('Nvidia Fog Fix')
    tweak_read_classes = 'CELLS',  # or 'CELL', but we want this patcher to
    # run in the same group as the CellImporter, so we'll have to skip
    # worldspaces.  It shouldn't be a problem in those CELLs.

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.Parent:  # It's a CELL that showed up because we said
            # 'CELLS' instead of 'CELL'
            return
        if not (record.fogNear or record.fogFar or record.fogClip):
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.fogNear = 0.0001
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_NoLightFlicker(AMultiTweakItem):
    """Remove light flickering for low end machines."""
    tweak_read_classes = 'LIGH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_NoLightFlicker, self).__init__(
            _("No Light Flicker"),
            _('Remove flickering from lights. For use on low-end machines.'),
            'NoLightFlicker',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Lights unflickered') + ': %d'

class AssortedTweak_NoLightFlicker(AAssortedTweak_NoLightFlicker,
                                   MultiTweakItem):

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AssortedTweak_NoLightFlicker, self).__init__()
        self.flags = flags = MreRecord.type_class['LIGH']._flags()
        flags.flickers = flags.flickerSlow = flags.pulse = flags.pulseSlow =\
            True

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        flickerFlags = self.flags
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.LIGH
        for record in modFile.LIGH.getActiveRecords():
            if record.flags & flickerFlags:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        flickerFlags = self.flags
        notFlickerFlags = ~flickerFlags
        keep = patchFile.getKeeper()
        for record in patchFile.LIGH.records:
            if int(record.flags & flickerFlags):
                record.flags &= notFlickerFlags
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_NoLightFlicker(AAssortedTweak_NoLightFlicker,
                                         CBash_MultiTweakItem):
    name = _('No Light Flicker')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsFlickers or record.IsFlickerSlow or record.IsPulse or \
                record.IsPulseSlow:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.IsFlickers = False
                override.IsFlickerSlow = False
                override.IsPulse = False
                override.IsPulseSlow = False
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------

class AMultiTweakItem_Weight(AMultiTweakItem):

    @property
    def weight(self): return self.choiceValues[self.chosen][0]

    def _patchLog(self, log, count):
        """Will write to log for a class that has a weight field"""
        log.setHeader(self.logHeader)
        log(self.logWeightValue % self.weight)
        log(self.logMsg % sum(count.values()))
        for srcMod in load_order.get_ordered(list(count.keys())):
            log('  * %s: %d' % (srcMod.s,count[srcMod]))

class CBash_MultiTweakItem_Weight(CBash_MultiTweakItem,
                                  AMultiTweakItem_Weight): pass

class AAssortedTweak_PotionWeight(AMultiTweakItem_Weight):
    """Reweighs standard potions down to 0.1."""
    tweak_read_classes = 'ALCH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_PotionWeight, self).__init__(
            _("Reweigh: Potions (Maximum)"),
            _('Potion weight will be capped.'),
            'MaximumPotionWeight',
            ('0.1',  0.1),
            ('0.2',  0.2),
            ('0.4',  0.4),
            ('0.6',  0.6),
            (_('Custom'),0.0),
            )
        self.logWeightValue = _('Potions set to maximum weight of ') + '%f'
        self.logMsg = '* '+_('Potions Reweighed') + ': %d'

class AssortedTweak_PotionWeight(AAssortedTweak_PotionWeight,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        maxWeight = self.weight
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.ALCH
        id_records = patchBlock.id_records
        for record in modFile.ALCH.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if maxWeight < record.weight < 1:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        maxWeight = self.weight
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.ALCH.records:
            if maxWeight < record.weight < 1 and not (
                    'SEFF', 0) in record.getEffects():
                record.weight = maxWeight
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_AssortedTweak_PotionWeight(AAssortedTweak_PotionWeight,
                                       CBash_MultiTweakItem_Weight):
    name = _("Reweigh: Potions (Maximum)")

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_AssortedTweak_PotionWeight, self).__init__()
        # see https://github.com/wrye-bash/wrye-bash/commit/3aa3c941b2de6d751f71e50613ba20ac14f477e8
        # CBash only, PBash gets away with just knowing the FormID of SEFF
        # and always assuming it exists, since it's from Oblivion.esm. CBash
        #  handles this by making sure the MGEF records are almost always
        # read in, and always before patchers that will need them
        self.SEFF = MGEFCode('SEFF')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        maxWeight = self.weight
        if maxWeight < record.weight < 1.0:
            for effect in record.effects:
                if effect.name == self.SEFF:
                    return
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.weight = maxWeight
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_IngredientWeight(AMultiTweakItem_Weight):
    """Reweighs standard ingredients down to 0.1."""
    tweak_read_classes = 'INGR',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_IngredientWeight, self).__init__(
            _("Reweigh: Ingredients"),
            _('Ingredient weight will be capped.'),
            'MaximumIngredientWeight',
            ('0.1',  0.1),
            ('0.2',  0.2),
            ('0.4',  0.4),
            ('0.6',  0.6),
            (_('Custom'),0.0),
            )
        self.logWeightValue = _('Ingredients set to maximum weight of') + \
                              ' %f'
        self.logMsg = '* '+_('Ingredients Reweighed') + ': %d'

class AssortedTweak_IngredientWeight(AAssortedTweak_IngredientWeight,
                                     MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        maxWeight = self.weight
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.INGR
        id_records = patchBlock.id_records
        for record in modFile.INGR.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.weight > maxWeight:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        maxWeight = self.weight
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.INGR.records:
            if record.weight > maxWeight:
                record.weight = maxWeight
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_AssortedTweak_IngredientWeight(AAssortedTweak_IngredientWeight,
                                           CBash_MultiTweakItem_Weight):
    name = _('Reweigh: Ingredients')

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_AssortedTweak_IngredientWeight, self).__init__()
        self.SEFF = MGEFCode('SEFF')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        maxWeight = self.weight
        if record.weight > maxWeight:
            for effect in record.effects:
                if effect.name == self.SEFF:
                    return
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.weight = maxWeight
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_PotionWeightMinimum(AMultiTweakItem_Weight):
    """Reweighs any potions up to 4."""
    tweak_read_classes = 'ALCH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_PotionWeightMinimum, self).__init__(
            _("Reweigh: Potions (Minimum)"),
            _('Potion weight will be floored.'),
            'MinimumPotionWeight',
            ('1',  1),
            ('2',  2),
            ('3',  3),
            ('4',  4),
            (_('Custom'),0.0),
            )
        self.logWeightValue = _('Potions set to minimum weight of ') + '%f'
        self.logMsg = '* '+_('Potions Reweighed') + ': %d'

class AssortedTweak_PotionWeightMinimum(AAssortedTweak_PotionWeightMinimum,
                                        MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        minWeight = self.weight
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.ALCH
        id_records = patchBlock.id_records
        for record in modFile.ALCH.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.weight < minWeight:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        minWeight = self.weight
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.ALCH.records:
            if record.weight < minWeight:
                record.weight = minWeight
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_AssortedTweak_PotionWeightMinimum(
    AAssortedTweak_PotionWeightMinimum, CBash_MultiTweakItem_Weight):
    scanOrder = 33 #Have it run after the max weight for consistent results
    editOrder = 33
    name = _('Reweigh: Potions (Minimum)')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        minWeight = self.weight
        if record.weight < minWeight:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.weight = minWeight
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_StaffWeight(AMultiTweakItem_Weight):
    """Reweighs staffs."""
    tweak_read_classes = 'WEAP',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_StaffWeight, self).__init__(
            _("Reweigh: Staffs/Staves"),
            _('Staff weight will be capped.'),
            'StaffWeight',
            ('1',  1.0),
            ('2',  2.0),
            ('3',  3.0),
            ('4',  4.0),
            ('5',  5.0),
            ('6',  6.0),
            ('7',  7.0),
            ('8',  8.0),
            (_('Custom'),0.0),
            )
        self.logWeightValue = _('Staffs/Staves set to maximum weight of') + \
                              ' %f'
        self.logMsg = '* '+_('Staffs/Staves Reweighed') + ': %d'

class AssortedTweak_StaffWeight(AAssortedTweak_StaffWeight,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        maxWeight = self.weight
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.WEAP
        id_records = patchBlock.id_records
        for record in modFile.WEAP.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.weaponType == 4 and record.weight > maxWeight:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        maxWeight = self.weight
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.WEAP.records:
            if record.weaponType == 4 and record.weight > maxWeight:
                record.weight = maxWeight
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_AssortedTweak_StaffWeight(AAssortedTweak_StaffWeight,
                                      CBash_MultiTweakItem_Weight):
    name = _('Reweigh: Staffs/Staves')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        maxWeight = self.weight
        if record.IsStaff and record.weight > maxWeight:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.weight = maxWeight
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_ArrowWeight(AMultiTweakItem_Weight):
    tweak_read_classes = 'AMMO',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_ArrowWeight, self).__init__(_("Reweigh: Arrows"),
            _('Arrow weights will be capped.'),
            'MaximumArrowWeight',
            ('0',    0.0),
            ('0.1',  0.1),
            ('0.2',  0.2),
            ('0.4',  0.4),
            ('0.6',  0.6),
            (_('Custom'),0.0),
            )
        self.logWeightValue = _('Arrows set to maximum weight of ') + '%f'
        self.logMsg = '* '+_('Arrows Reweighed') + ': %d'

class AssortedTweak_ArrowWeight(AAssortedTweak_ArrowWeight,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        maxWeight = self.weight
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.AMMO
        id_records = patchBlock.id_records
        for record in modFile.AMMO.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.weight > maxWeight:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        maxWeight = self.weight
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.AMMO.records:
            if record.weight > maxWeight:
                record.weight = maxWeight
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_AssortedTweak_ArrowWeight(AAssortedTweak_ArrowWeight,
                                      CBash_MultiTweakItem_Weight):
    name = _('Reweigh: Arrows')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        maxWeight = self.weight
        if record.weight > maxWeight:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.weight = maxWeight
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_ScriptEffectSilencer(AMultiTweakItem):
    """Silences the script magic effect and gives it an extremely high
    speed."""
    tweak_read_classes = 'MGEF',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_ScriptEffectSilencer, self).__init__(
            _("Magic: Script Effect Silencer"),
            _('Script Effect will be silenced and have no graphics.'),
            'SilentScriptEffect',
            ('0',    0),
            )
        self.defaultEnabled = True

    def _patchLog(self,log):
        log.setHeader(self.logHeader)
        log(_('Script Effect silenced.'))

class AssortedTweak_ScriptEffectSilencer(AAssortedTweak_ScriptEffectSilencer,
                                         MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.MGEF
        id_records = patchBlock.id_records
        modFile.convertToLongFids(('MGEF',))
        for record in modFile.MGEF.getActiveRecords():
            fid = record.fid
            if not record.longFids: fid = mapper(fid)
            if fid in id_records: continue
            if record.eid != 'SEFF': continue
            patchBlock.setRecord(record.getTypeCopy(mapper))

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        nullRef = (GPath('Oblivion.esm'),0)
        silentattrs = {
            'model' : None,
            'projectileSpeed' : 9999,
            'light' : nullRef,
            'effectShader' : nullRef,
            'enchantEffect' : nullRef,
            'castingSound' : nullRef,
            'boltSound' : nullRef,
            'hitSound' : nullRef,
            'areaSound' : nullRef}
        keep = patchFile.getKeeper()
        for record in patchFile.MGEF.records:
            if record.eid != 'SEFF' or not record.longFids: continue
            record.flags.noHitEffect = True
            for attr in silentattrs:
                if getattr(record,attr) != silentattrs[attr]:
                    setattr(record,attr,silentattrs[attr])
                    keep(record.fid)
        self._patchLog(log)

class CBash_AssortedTweak_ScriptEffectSilencer(
    AAssortedTweak_ScriptEffectSilencer, CBash_MultiTweakItem):
    name = _('Magic: Script Effect Silencer')

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_AssortedTweak_ScriptEffectSilencer, self).__init__()
        self.attrs = ['modPath', 'modb', 'modt_p', 'projectileSpeed', 'light',
                      'effectShader', 'enchantEffect', 'castingSound',
                      'boltSound', 'hitSound', 'areaSound', 'IsNoHitEffect']
        self.newValues = [None, None, None, 9999, None, None, None, None, None,
                          None, None, True]
        self.SEFF = MGEFCode('SEFF')
        # TODO THIS IS ONE OF THE FEW THAT HAS no self.mod_count = {} - maybe
        # should call the constructor directly instead of super() ?
        self.buildPatchLog=self._patchLog # AAssortedTweak_ScriptEffectSilencer

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.eid == self.SEFF[0]:
            attrs = self.attrs
            newValues = self.newValues
            oldValues = list(map(record.__getattribute__, attrs))
            if oldValues != newValues:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    list(map(override.__setattr__, attrs, newValues))
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_HarvestChance(AMultiTweakItem):
    """Adjust Harvest Chances."""
    tweak_read_classes = 'FLOR',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_HarvestChance, self).__init__(
            _("Harvest Chance"),
            _('Harvest chances on all plants will be set to the chosen '
                'percentage.'),
            'HarvestChance',
            ('10%',  10),
            ('20%',  20),
            ('30%',  30),
            ('40%',  40),
            ('50%',  50),
            ('60%',  60),
            ('70%',  70),
            ('80%',  80),
            ('90%',  90),
            ('100%', 100),
            (_('Custom'),0),
            )
        self.logMsg = '* '+_('Harvest Chances Changed') + ': %d'

class AssortedTweak_HarvestChance(AAssortedTweak_HarvestChance,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        chance = self.choiceValues[self.chosen][0]
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.FLOR
        id_records = patchBlock.id_records
        for record in modFile.FLOR.getActiveRecords():
            if record.eid.startswith('Nirnroot'): continue #skip Nirnroots
            if mapper(record.fid) in id_records: continue
            for attr in ['spring','summer','fall','winter']:
                if getattr(record,attr) != chance:
                    record = record.getTypeCopy(mapper)
                    patchBlock.setRecord(record)
                    break

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        chance = self.choiceValues[self.chosen][0]
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.FLOR.records:
            record.spring, record.summer, record.fall, record.winter = \
                chance, chance, chance, chance
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_HarvestChance(AAssortedTweak_HarvestChance,
                                        CBash_MultiTweakItem):
    name = _('Harvest Chance')

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_AssortedTweak_HarvestChance, self).__init__()
        self.attrs = ['spring','summer','fall','winter']

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.eid.startswith('Nirnroot'): return #skip Nirnroots
        newValues = [self.choiceValues[self.chosen][0]] * 4
        oldValues = list(map(record.__getattribute__, self.attrs))
        if oldValues != newValues:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                list(map(override.__setattr__, self.attrs, newValues))
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_WindSpeed(AMultiTweakItem):
    """Disables Weather winds."""
    tweak_read_classes = 'WTHR',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_WindSpeed, self).__init__(_("Disable Wind"),
            _('Disables the wind on all weathers.'),
            'windSpeed',
            (_('Disable'),  0),
            )
        self.logMsg = '* '+_('Winds Disabled') + ': %d'

class AssortedTweak_WindSpeed(AAssortedTweak_WindSpeed,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.WTHR
        id_records = patchBlock.id_records
        for record in modFile.WTHR.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.windSpeed != 0:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.WTHR.records:
            if record.windSpeed != 0:
                record.windSpeed = 0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_WindSpeed(AAssortedTweak_WindSpeed,
                                    CBash_MultiTweakItem):
    name = _('Disable Wind')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.windSpeed != 0:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.windSpeed = 0
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_UniformGroundcover(AMultiTweakItem):
    """Eliminates random variation in groundcover."""
    tweak_read_classes = 'GRAS',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_UniformGroundcover, self).__init__(
            _("Uniform Groundcover"),
            _('Eliminates random variation in groundcover (grasses, '
              'shrubs, etc.).'),
            'UniformGroundcover',
            ('1.0', '1.0'),
            )
        self.logMsg = '* '+_('Grasses Normalized') + ': %d'

class AssortedTweak_UniformGroundcover(AAssortedTweak_UniformGroundcover,
                                       MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.GRAS
        id_records = patchBlock.id_records
        for record in modFile.GRAS.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.heightRange != 0:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.GRAS.records:
            if record.heightRange != 0:
                record.heightRange = 0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_UniformGroundcover(AAssortedTweak_UniformGroundcover,
                                             CBash_MultiTweakItem):
    name = _('Uniform Groundcover')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.heightRange != 0:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.heightRange = 0
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_SetCastWhenUsedEnchantmentCosts(AMultiTweakItem):
    """Sets Cast When Used Enchantment number of uses."""
    tweak_read_classes = 'ENCH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_SetCastWhenUsedEnchantmentCosts, self).__init__(
            _("Number of uses for pre-enchanted weapons and Staffs/Staves"),
            _('The charge amount and cast cost will be edited so that all '
              'enchanted weapons and Staffs/Staves have the amount of '
              'uses specified. Cost will be rounded up to 1 (unless set '
              'to unlimited) so number of uses may not exactly match for '
              'all weapons.'),
            'Number of uses:',
            ('1', 1),
            ('5', 5),
            ('10', 10),
            ('20', 20),
            ('30', 30),
            ('40', 40),
            ('50', 50),
            ('80', 80),
            ('100', 100),
            ('250', 250),
            ('500', 500),
            (_('Unlimited'), 0),
            (_('Custom'),0),
            )
        self.logHeader = '=== '+_('Set Enchantment Number of Uses')
        self.logMsg = '* '+_('Enchantments set') + ': %d'

class AssortedTweak_SetCastWhenUsedEnchantmentCosts(
    AAssortedTweak_SetCastWhenUsedEnchantmentCosts, MultiTweakItem):
    #info: 'itemType','chargeAmount','enchantCost'

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.ENCH
        id_records = patchBlock.id_records
        for record in modFile.ENCH.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.itemType in [1,2]:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.ENCH.records:
            if record.itemType in [1,2]:
                uses = self.choiceValues[self.chosen][0]
                cost = uses
                if uses != 0:
                    cost = max(record.chargeAmount/uses,1)
                record.enchantCost = cost
                record.chargeAmount = cost * uses
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_SetCastWhenUsedEnchantmentCosts(
    AAssortedTweak_SetCastWhenUsedEnchantmentCosts, CBash_MultiTweakItem):
    name = _('Set Enchantment Number of Uses')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsStaff or record.IsWeapon:
            uses = self.choiceValues[self.chosen][0]
            cost = uses
            if uses != 0:
                cost = max(record.chargeAmount/uses,1)
            amount = cost * uses
            if record.enchantCost != cost or record.chargeAmount != amount:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.enchantCost = cost
                    override.chargeAmount = amount
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_DefaultIcons(AMultiTweakItem):
    """Sets a default icon for any records that don't have any icon
    assigned."""
    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_DefaultIcons,self).__init__(_("Default Icons"),
            _("Sets a default icon for any records that don't have any icon"
              " assigned"),
            'icons',
            ('1', 1),
            )
        self.defaultEnabled = True
        self.logMsg = '* '+_('Default Icons set') + ': %d'

class AssortedTweak_DefaultIcons(AAssortedTweak_DefaultIcons,MultiTweakItem):
    tweak_read_classes = (
        'ALCH', 'AMMO', 'APPA', 'ARMO', 'BOOK', 'BSGN', 'CLAS', 'CLOT', 'FACT',
        'INGR', 'KEYM', 'LIGH', 'MISC', 'QUST', 'SGST', 'SLGM', 'WEAP',)

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        self.activeTypes = list(self.__class__.tweak_read_classes)
        super(AssortedTweak_DefaultIcons,self).__init__()

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        for blockType in self.activeTypes:
            if blockType not in modFile.tops: continue
            modBlock = getattr(modFile,blockType)
            patchBlock = getattr(patchFile,blockType)
            id_records = patchBlock.id_records
            for record in modBlock.getActiveRecords():
                if mapper(record.fid) not in id_records:
                    record = record.getTypeCopy(mapper)
                    patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        count = {}
        keep = patchFile.getKeeper()
        for type_ in self.activeTypes:
            if type_ not in patchFile.tops: continue
            for record in patchFile.tops[type_].records:
                if getattr(record, 'iconPath', None): continue
                if getattr(record, 'maleIconPath', None): continue
                if getattr(record, 'femaleIconPath', None): continue
                changed = False
                if type_ == 'ALCH':
                    record.iconPath = "Clutter\\Potions\\IconPotion01.dds"
                    changed = True
                elif type_ == 'AMMO':
                    record.iconPath = "Weapons\\IronArrow.dds"
                    changed = True
                elif type_ == 'APPA':
                    record.iconPath = "Clutter\\IconMortarPestle.dds"
                    changed = True
                elif type_ == 'AMMO':
                    record.iconPath = "Weapons\\IronArrow.dds"
                    changed = True
                elif type_ == 'ARMO':
                    if record.flags.notPlayable: continue
                    #choose based on body flags:
                    if record.flags.upperBody != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Cuirass.dds"
                        record.femaleIconPath = "Armor\\Iron\\F\\Cuirass.dds"
                        changed = True
                    elif record.flags.lowerBody != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Greaves.dds"
                        record.femaleIconPath = "Armor\\Iron\\F\\Greaves.dds"
                        changed = True
                    elif record.flags.head != 0 or record.flags.hair != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Helmet.dds"
                        changed = True
                    elif record.flags.hand != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Gauntlets.dds"
                        record.femaleIconPath ="Armor\\Iron\\F\\Gauntlets.dds"
                        changed = True
                    elif record.flags.foot != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Boots.dds"
                        changed = True
                    elif record.flags.shield != 0:
                        record.maleIconPath = "Armor\\Iron\\M\\Shield.dds"
                        changed = True
                    else: #Default icon, probably a token or somesuch
                        record.maleIconPath = "Armor\\Iron\\M\\Shield.dds"
                        changed = True
                elif type_ in ['BOOK', 'BSGN', 'CLAS']:  # just a random book
                    # icon for class/birthsign as well.
                    record.iconPath = "Clutter\\iconbook%d.dds" % (
                        random.randint(1, 13))
                    changed = True
                elif type_ == 'CLOT':
                    if record.flags.notPlayable: continue
                    #choose based on body flags:
                    if record.flags.upperBody != 0:
                        record.maleIconPath = \
                            "Clothes\\MiddleClass\\01\\M\\Shirt.dds"
                        record.femaleIconPath = \
                            "Clothes\\MiddleClass\\01\\F\\Shirt.dds"
                        changed = True
                    elif record.flags.lowerBody != 0:
                        record.maleIconPath = \
                            "Clothes\\MiddleClass\\01\\M\\Pants.dds"
                        record.femaleIconPath = \
                            "Clothes\\MiddleClass\\01\\F\\Pants.dds"
                        changed = True
                    elif record.flags.head or record.flags.hair:
                        record.maleIconPath = \
                            "Clothes\\MythicDawnrobe\\hood.dds"
                        changed = True
                    elif record.flags.hand != 0:
                        record.maleIconPath = \
                         "Clothes\\LowerClass\\Jail\\M\\JailShirtHandcuff.dds"
                        changed = True
                    elif record.flags.foot != 0:
                        record.maleIconPath = \
                            "Clothes\\MiddleClass\\01\\M\\Shoes.dds"
                        record.femaleIconPath = \
                            "Clothes\\MiddleClass\\01\\F\\Shoes.dds"
                        changed = True
                    elif record.flags.leftRing or record.flags.rightRing:
                        record.maleIconPath = "Clothes\\Ring\\RingNovice.dds"
                        changed = True
                    else: #amulet
                        record.maleIconPath = \
                            "Clothes\\Amulet\\AmuletSilver.dds"
                        changed = True
                elif type_ == 'FACT':
                    #todo
                    #changed = True
                    pass
                elif type_ == 'INGR':
                    record.iconPath = "Clutter\\IconSeeds.dds"
                    changed = True
                elif type_ == 'KEYM':
                    record.iconPath = \
                        ["Clutter\\Key\\Key.dds", "Clutter\\Key\\Key02.dds"][
                            random.randint(0, 1)]
                    changed = True
                elif type_ == 'LIGH':
                    if not record.flags.canTake: continue
                    record.iconPath = "Lights\\IconTorch02.dds"
                    changed = True
                elif type_ == 'MISC':
                    record.iconPath = "Clutter\\Soulgems\\AzurasStar.dds"
                    changed = True
                elif type_ == 'QUST':
                    if not record.stages: continue
                    record.iconPath = "Quest\\icon_miscellaneous.dds"
                    changed = True
                elif type_ == 'SGST':
                    record.iconPath = "IconSigilStone.dds"
                    changed = True
                elif type_ == 'SLGM':
                    record.iconPath = "Clutter\\Soulgems\\AzurasStar.dds"
                    changed = True
                elif type_ == 'WEAP':
                    if record.weaponType == 0:
                        record.iconPath = "Weapons\\IronDagger.dds"
                    elif record.weaponType == 1:
                        record.iconPath = "Weapons\\IronClaymore.dds"
                    elif record.weaponType == 2:
                        record.iconPath = "Weapons\\IronMace.dds"
                    elif record.weaponType == 3:
                        record.iconPath = "Weapons\\IronBattleAxe.dds"
                    elif record.weaponType == 4:
                        record.iconPath = "Weapons\\Staff.dds"
                    elif record.weaponType == 5:
                        record.iconPath = "Weapons\\IronBow.dds"
                    else: #Should never reach this point
                        record.iconPath = "Weapons\\IronDagger.dds"
                    changed = True
                if changed:
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_DefaultIcons(AAssortedTweak_DefaultIcons,
                                       CBash_MultiTweakItem):
    """Sets a default icon for any records that don't have any icon
    assigned."""
    name = _('Default Icons')
    type_defaultIcon = {
                'ALCH': "Clutter\\Potions\\IconPotion01.dds",
                'AMMO': "Weapons\\IronArrow.dds",
                'APPA': "Clutter\\IconMortarPestle.dds",
                'ARMO': (("Armor\\Iron\\M\\Cuirass.dds",
                          "Armor\\Iron\\F\\Cuirass.dds"),
                         ("Armor\\Iron\\M\\Greaves.dds",
                          "Armor\\Iron\\F\\Greaves.dds"),
                         ("Armor\\Iron\\M\\Helmet.dds",),
                         ("Armor\\Iron\\M\\Gauntlets.dds",
                          "Armor\\Iron\\F\\Gauntlets.dds"),
                         ("Armor\\Iron\\M\\Boots.dds",),
                         ("Armor\\Iron\\M\\Shield.dds",),
                         ("Armor\\Iron\\M\\Shield.dds",), #Default Armor icon
                         ),
                'BOOK': "Clutter\\iconbook%d.dds",
                'BSGN': "Clutter\\iconbook%d.dds",
                'CLAS': "Clutter\\iconbook%d.dds",
                'CLOT': (("Clothes\\MiddleClass\\01\\M\\Shirt.dds",
                          "Clothes\\MiddleClass\\01\\F\\Shirt.dds"),
                         ("Clothes\\MiddleClass\\01\\M\\Pants.dds",
                          "Clothes\\MiddleClass\\01\\F\\Pants.dds"),
                         ("Clothes\\MythicDawnrobe\\hood.dds",),
                         ("Clothes\\LowerClass\\Jail\\M\\"
                          "JailShirtHandcuff.dds",),
                         ("Clothes\\MiddleClass\\01\\M\\Shoes.dds",
                          "Clothes\\MiddleClass\\01\\F\\Shoes.dds"),
                         ("Clothes\\Ring\\RingNovice.dds",),
                         ("Clothes\\Amulet\\AmuletSilver.dds",),
                         ),
##                'FACT': u"", ToDo
                'INGR': "Clutter\\IconSeeds.dds",
                'KEYM': ("Clutter\\Key\\Key.dds","Clutter\\Key\\Key02.dds"),
                'LIGH': "Lights\\IconTorch02.dds",
                'MISC': "Clutter\\Soulgems\\AzurasStar.dds",
                'QUST': "Quest\\icon_miscellaneous.dds",
                'SGST': "IconSigilStone.dds",
                'SLGM': "Clutter\\Soulgems\\AzurasStar.dds",
                'WEAP': ("Weapons\\IronDagger.dds",
                         "Weapons\\IronClaymore.dds",
                         "Weapons\\IronMace.dds",
                         "Weapons\\IronBattleAxe.dds",
                         "Weapons\\Staff.dds",
                         "Weapons\\IronBow.dds",
                         ),
                }
    tweak_read_classes = list(type_defaultIcon)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if getattr(record, 'iconPath', None): return
        if getattr(record, 'maleIconPath', None): return
        if getattr(record, 'femaleIconPath', None): return
        if record._Type == 'LIGH' and not record.IsCanTake: return
        if record._Type == 'QUST' and not record.stages: return
        if record._Type in ['ARMO','CLOT'] and not record.IsPlayable: return
        override = record.CopyAsOverride(self.patchFile)
        if override:
            icons = self.type_defaultIcon[override._Type]
            if isinstance(icons, tuple):
                if override._Type == 'ARMO':
                    #choose based on body flags:
                    if override.IsUpperBody:
                        icons = icons[0]
                    elif override.IsLowerBody:
                        icons = icons[1]
                    elif override.IsHead or record.IsHair:
                        icons = icons[2]
                    elif override.IsHand:
                        icons = icons[3]
                    elif override.IsFoot:
                        icons = icons[4]
                    elif override.IsShield:
                        icons = icons[5]
                    else: #default icon, probably a token or somesuch
                        icons = icons[6]
                elif override._Type == 'CLOT':
                    #choose based on body flags:
                    if override.IsUpperBody:
                        icons = icons[0]
                    elif override.IsLowerBody:
                        icons = icons[1]
                    elif override.IsHead or record.IsHair:
                        icons = icons[2]
                    elif override.IsHand:
                        icons = icons[3]
                    elif override.IsFoot:
                        icons = icons[4]
                    elif override.IsLeftRing or override.IsRightRing:
                        icons = icons[5]
                    else:
                        icons = icons[6]
                elif override._Type == 'KEYM':
                    icons = icons[random.randint(0,1)]
                elif override._Type == 'WEAP':
                    #choose based on weapon type:
                    try:
                        icons = icons[override.weaponType]
                    except IndexError: #just in case
                        icons = icons[0]
            else:
                if override._Type in ['BOOK', 'BSGN', 'CLAS']:  # just a
                    # random book icon for class/birthsign as well.
                    icons = icons % (random.randint(1,13))
            try:
                if isinstance(icons, tuple):
                    if len(icons) == 1:
                        override.maleIconPath = icons[0]
                    else:
                        override.maleIconPath, override.femaleIconPath = icons
                else:
                    override.iconPath = icons
            except ValueError as error:
                print(override._Type)
                print(icons)
                print(error)
                print(self.patchFile.Current.Debug_DumpModFiles())
                raise
            self.mod_count[modFile.GName] += 1
            record.UnloadRecord()
            record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_SetSoundAttenuationLevels(AMultiTweakItem):
    """Sets Sound Attenuation Levels for all records except Nirnroots."""
    tweak_read_classes = 'SOUN',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_SetSoundAttenuationLevels,self).__init__(
            _("Set Sound Attenuation Levels"),
            _('The sound attenuation levels will be set to tweak%*current'
              ' level, thereby increasing (or decreasing) the sound volume.'),
            'Attenuation%:',
            ('0%', 0),
            ('5%', 5),
            ('10%', 10),
            ('20%', 20),
            ('50%', 50),
            ('80%', 80),
            (_('Custom'),0),
            )
        self.logMsg = '* '+_('Sounds Modified') + ': %d'

class AssortedTweak_SetSoundAttenuationLevels(
    AAssortedTweak_SetSoundAttenuationLevels, MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.SOUN
        id_records = patchBlock.id_records
        for record in modFile.SOUN.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.staticAtten:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.SOUN.records:
            if record.staticAtten:
                record.staticAtten = record.staticAtten * \
                                     self.choiceValues[self.chosen][0] / 100
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_SetSoundAttenuationLevels(
    AAssortedTweak_SetSoundAttenuationLevels, CBash_MultiTweakItem):
    name = _('Set Sound Attenuation Levels')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        choice = self.choiceValues[self.chosen][0] / 100
        if choice == 1:  # Prevent any pointless changes if a custom value
            # of 100 is used.
            return
        if record.staticAtten:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.staticAtten *= choice
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_SetSoundAttenuationLevels_NirnrootOnly(AMultiTweakItem):
    """Sets Sound Attenuation Levels for Nirnroots."""
    tweak_read_classes = 'SOUN',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_SetSoundAttenuationLevels_NirnrootOnly,
              self).__init__(
            _("Set Sound Attenuation Levels: Nirnroots Only"),
            _('The sound attenuation levels will be set to tweak%*current '
              'level, thereby increasing (or decreasing) the sound '
              'volume. This one only affects Nirnroots.'),
            'Nirnroot Attenuation%:',
            ('0%', 0),
            ('5%', 5),
            ('10%', 10),
            ('20%', 20),
            ('50%', 50),
            ('80%', 80),
            (_('Custom'),0),
            )
        self.logMsg = '* '+_('Sounds Modified') + ': %d'

class AssortedTweak_SetSoundAttenuationLevels_NirnrootOnly(
    AAssortedTweak_SetSoundAttenuationLevels_NirnrootOnly, MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.SOUN
        id_records = patchBlock.id_records
        for record in modFile.SOUN.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.staticAtten and 'nirnroot' in record.eid.lower():
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.SOUN.records:
            if record.staticAtten and 'nirnroot' in record.eid.lower():
                record.staticAtten = record.staticAtten * \
                                     self.choiceValues[self.chosen][0] / 100
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_SetSoundAttenuationLevels_NirnrootOnly(
    AAssortedTweak_SetSoundAttenuationLevels_NirnrootOnly,
    CBash_MultiTweakItem):
    name = _('Set Sound Attenuation Levels: Nirnroots Only')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        choice = self.choiceValues[self.chosen][0] / 100
        if choice == 1:  # Prevent any pointless changes if a custom value
            # of 100 is used.
            return
        if record.staticAtten and 'nirnroot' in record.eid.lower() :
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.staticAtten *= choice
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_FactioncrimeGoldMultiplier(AMultiTweakItem):
    """Fix factions with unset crimeGoldMultiplier to have a
    crimeGoldMultiplier of 1.0."""
    tweak_read_classes = 'FACT',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_FactioncrimeGoldMultiplier,self).__init__(
            _("Faction crime Gold Multiplier Fix"),
            _('Fix factions with unset crimeGoldMultiplier to have a '
              'crimeGoldMultiplier of 1.0.'),
            'FactioncrimeGoldMultiplier',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Factions fixed') + ': %d'

class AssortedTweak_FactioncrimeGoldMultiplier(
    AAssortedTweak_FactioncrimeGoldMultiplier, MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.FACT
        for record in modFile.FACT.getActiveRecords():
            if not isinstance(record.crimeGoldMultiplier,float):
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.FACT.records:
            if not isinstance(record.crimeGoldMultiplier,float):
                record.crimeGoldMultiplier = 1.0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_FactioncrimeGoldMultiplier(
    AAssortedTweak_FactioncrimeGoldMultiplier, CBash_MultiTweakItem):
    name = _('Faction crime Gold Multiplier Fix')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired."""
        if record.crimeGoldMultiplier is None:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.crimeGoldMultiplier = 1.0
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_LightFadeValueFix(AMultiTweakItem):
    """Remove light flickering for low end machines."""
    tweak_read_classes = 'LIGH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_LightFadeValueFix, self).__init__(
            _("No Light Fade Value Fix"),
            _("Sets Light's Fade values to default of 1.0 if not set."),
            'NoLightFadeValueFix',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Lights with fade values added') + ': %d'

class AssortedTweak_LightFadeValueFix(AAssortedTweak_LightFadeValueFix,
                                      MultiTweakItem):
    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.LIGH
        for record in modFile.LIGH.getActiveRecords():
            if not isinstance(record.fade,float):
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.LIGH.records:
            if not isinstance(record.fade,float):
                record.fade = 1.0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_LightFadeValueFix(AAssortedTweak_LightFadeValueFix,
                                            CBash_MultiTweakItem):
    name = _('No Light Fade Value Fix')

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.fade is None:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.fade = 1.0
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAssortedTweak_TextlessLSCRs(AMultiTweakItem):
    """Removes the description from loading screens."""
    tweak_read_classes = 'LSCR',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAssortedTweak_TextlessLSCRs, self).__init__(
            _("No Description Loading Screens"),
            _("Removes the description from loading screens."),
            'NoDescLSCR',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Loading screens tweaked') + ': %d'

class AssortedTweak_TextlessLSCRs(AAssortedTweak_TextlessLSCRs,MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.LSCR
        for record in modFile.LSCR.getActiveRecords():
            if record.text:
                record = record.getTypeCopy(mapper)
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.LSCR.records:
            if record.text:
                record.text = ''
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AssortedTweak_TextlessLSCRs(AAssortedTweak_TextlessLSCRs,
                                        CBash_MultiTweakItem):
    name = _("No Description Loading Screens")

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.text:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.text = ''
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

class AssortedTweaker(MultiTweaker):
    """Tweaks assorted stuff. Sub-tweaks behave like patchers themselves."""
    scanOrder = 32
    editOrder = 32
    name = _('Tweak Assorted')
    text = _("Tweak various records in miscellaneous ways.")

    if bush.game.fsName == 'Oblivion':
        tweaks = sorted([
            AssortedTweak_ArmorShows(_("Armor Shows Amulets"),
                _("Prevents armor from hiding amulets."),
                'armorShowsAmulets',
                ),
            AssortedTweak_ArmorShows(_("Armor Shows Rings"),
                _("Prevents armor from hiding rings."),
                'armorShowsRings',
                ),
            AssortedTweak_ClothingShows(_("Clothing Shows Amulets"),
                _("Prevents Clothing from hiding amulets."),
                'ClothingShowsAmulets',
                ),
            AssortedTweak_ClothingShows(_("Clothing Shows Rings"),
                _("Prevents Clothing from hiding rings."),
                'ClothingShowsRings',
                ),
            AssortedTweak_ArmorPlayable(),
            AssortedTweak_ClothingPlayable(),
            AssortedTweak_BowReach(),
            AssortedTweak_ConsistentRings(),
            AssortedTweak_DarnBooks(),
            AssortedTweak_FogFix(),
            AssortedTweak_NoLightFlicker(),
            AssortedTweak_PotionWeight(),
            AssortedTweak_PotionWeightMinimum(),
            AssortedTweak_StaffWeight(),
            AssortedTweak_SetCastWhenUsedEnchantmentCosts(),
            AssortedTweak_WindSpeed(),
            AssortedTweak_UniformGroundcover(),
            AssortedTweak_HarvestChance(),
            AssortedTweak_IngredientWeight(),
            AssortedTweak_ArrowWeight(),
            AssortedTweak_ScriptEffectSilencer(),
            AssortedTweak_DefaultIcons(),
            AssortedTweak_SetSoundAttenuationLevels(),
            AssortedTweak_SetSoundAttenuationLevels_NirnrootOnly(),
            AssortedTweak_FactioncrimeGoldMultiplier(),
            AssortedTweak_LightFadeValueFix(),
            AssortedTweak_SkyrimStyleWeapons(),
            AssortedTweak_TextlessLSCRs(),
            ],key=lambda a: a.label.lower())

    #--Patch Phase ------------------------------------------------------------
    def getReadClasses(self):
        """Returns load factory classes needed for reading."""
        if not self.isActive: return tuple()
        classNames = [tweak.getReadClasses() for tweak in self.enabledTweaks]
        return sum(classNames,tuple())

    def getWriteClasses(self):
        """Returns load factory classes needed for writing."""
        if not self.isActive: return tuple()
        classTuples = [tweak.getWriteClasses() for tweak in self.enabledTweaks]
        return sum(classTuples,tuple())

    def scanModFile(self,modFile,progress):
        if not self.isActive: return
        for tweak in self.enabledTweaks:
            tweak.scanModFile(modFile,progress,self.patchFile)

class CBash_AssortedTweaker(CBash_MultiTweaker):
    """Tweaks assorted stuff. Sub-tweaks behave like patchers themselves."""
    scanOrder = 32
    editOrder = 32
    name = _('Tweak Assorted')
    text = _("Tweak various records in miscellaneous ways.")

    tweaks = sorted([
        CBash_AssortedTweak_ArmorShows(_("Armor Shows Amulets"),
            _("Prevents armor from hiding amulets."),
            'armorShowsAmulets',
            ),
        CBash_AssortedTweak_ArmorShows(_("Armor Shows Rings"),
            _("Prevents armor from hiding rings."),
            'armorShowsRings',
            ),
        CBash_AssortedTweak_ClothingShows(_("Clothing Shows Amulets"),
            _("Prevents Clothing from hiding amulets."),
            'ClothingShowsAmulets',
            ),
        CBash_AssortedTweak_ClothingShows(_("Clothing Shows Rings"),
            _("Prevents Clothing from hiding rings."),
            'ClothingShowsRings',
            ),
        CBash_AssortedTweak_ArmorPlayable(),
        CBash_AssortedTweak_ClothingPlayable(),
        CBash_AssortedTweak_BowReach(),
        CBash_AssortedTweak_ConsistentRings(),
        CBash_AssortedTweak_DarnBooks(),
        CBash_AssortedTweak_FogFix(),
        CBash_AssortedTweak_NoLightFlicker(),
        CBash_AssortedTweak_PotionWeight(),
        CBash_AssortedTweak_PotionWeightMinimum(),
        CBash_AssortedTweak_StaffWeight(),
        CBash_AssortedTweak_SetCastWhenUsedEnchantmentCosts(),
        CBash_AssortedTweak_HarvestChance(),
        CBash_AssortedTweak_WindSpeed(),
        CBash_AssortedTweak_UniformGroundcover(),
        CBash_AssortedTweak_IngredientWeight(),
        CBash_AssortedTweak_ArrowWeight(),
        CBash_AssortedTweak_ScriptEffectSilencer(),
        CBash_AssortedTweak_DefaultIcons(),
        CBash_AssortedTweak_SetSoundAttenuationLevels(),
        CBash_AssortedTweak_SetSoundAttenuationLevels_NirnrootOnly(),
        CBash_AssortedTweak_FactioncrimeGoldMultiplier(),
        CBash_AssortedTweak_LightFadeValueFix(),
        CBash_AssortedTweak_SkyrimStyleWeapons(),
        CBash_AssortedTweak_TextlessLSCRs(),
        ],key=lambda a: a.label.lower())

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
"""Tmp module to get mergeability stuff out of bosh.__init__.py."""
# FIXME(ut): methods return True or a list resulting in if result == True tests and complicated logic
from .. import bass, bush
from ..bolt import GPath
from ..cint import ObCollection
from ..exception import ModError
from ..load_order import cached_is_active
from ..parsers import ModFile, LoadFactory

def _is_mergeable_no_load(modInfo, verbose):
    reasons = []
    if modInfo.isEsm():
        if not verbose: return False
        reasons.append('\n.    '+_('Is esm.'))
    #--Bashed Patch
    if modInfo.isBP():
        if not verbose: return False
        reasons.append('\n.    '+_('Is Bashed Patch.'))
    #--Bsa / voice?
    if tuple(modInfo.hasResources()) != (False, False):
        if not verbose: return False
        hasBsa, hasVoices = modInfo.hasResources()
        if hasBsa:
            reasons.append('\n.    '+_('Has BSA archive.'))
        if hasVoices:
            reasons.append('\n.    '+_('Has associated voice directory (Sound\\Voice\\%s).') % modInfo.name.s)
    # Client must make sure NoMerge tag not in tags - if in tags
    # don't show up as mergeable.
    if reasons: return reasons
    return True

def pbash_mergeable_no_load(modInfo, verbose):
    reasons = _is_mergeable_no_load(modInfo, verbose)
    if isinstance(reasons, list):
        reasons = ''.join(reasons)
    elif not reasons:
        return False # non verbose mode
    else: # True
        reasons = ''
    #--Missing Strings Files?
    if modInfo.isMissingStrings():
        if not verbose: return False
        from . import oblivionIni
        reasons += '\n.    '+_('Missing String Translation Files (Strings\\%s_%s.STRINGS, etc).') % (
            modInfo.name.sbody, oblivionIni.get_ini_language())
    if reasons: return reasons
    return True

def isPBashMergeable(modInfo, minfos, verbose):
    """Returns True or error message indicating whether specified mod is mergeable."""
    reasons = pbash_mergeable_no_load(modInfo, verbose)
    if isinstance(reasons, str):
        pass
    elif not reasons:
        return False # non verbose mode
    else: # True
        reasons = ''
    #--Load test
    mergeTypes = set(recClass.classType for recClass in bush.game.mergeClasses)
    modFile = ModFile(modInfo, LoadFactory(False, *mergeTypes))
    try:
        modFile.load(True,loadStrings=False)
    except ModError as error:
        if not verbose: return False
        reasons += '\n.    %s.' % error
    #--Skipped over types?
    if modFile.topsSkipped:
        if not verbose: return False
        reasons += '\n.    '+_('Unsupported types: ')+', '.join(sorted(modFile.topsSkipped))+'.'
    #--Empty mod
    elif not modFile.tops:
        if not verbose: return False
        reasons += '\n.    '+ 'Empty mod.'
    #--New record
    lenMasters = len(modFile.tes4.masters)
    newblocks = []
    for type,block in modFile.tops.items():
        for record in block.getActiveRecords():
            if record.fid >> 24 >= lenMasters:
                if record.flags1.deleted: continue #if new records exist but are deleted just skip em.
                if not verbose: return False
                newblocks.append(type)
                break
    if newblocks: reasons += '\n.    '+_('New record(s) in block(s): ')+', '.join(sorted(newblocks))+'.'
    dependent = [name.s for name, info in minfos.items()
                 if not info.isBP() and modInfo.name in info.header.masters]
    if dependent:
        if not verbose: return False
        reasons += '\n.    '+_('Is a master of mod(s): ')+', '.join(sorted(dependent))+'.'
    if reasons: return reasons
    return True

def _modIsMergeableLoad(modInfo, minfos, verbose):
    """Check if mod is mergeable, loading it and taking into account the
    rest of mods."""
    allowMissingMasters = {'Filter', 'IIM', 'InventOnly'}
    tags = modInfo.getBashTags()
    reasons = []

    #--Load test
    with ObCollection(ModsPath=bass.dirs['mods'].s) as Current:
        #MinLoad, InLoadOrder, AddMasters, TrackNewTypes, SkipAllRecords
        modFile = Current.addMod(modInfo.getPath().stail, Flags=0x00002129)
        Current.load()

        missingMasters = []
        nonActiveMasters = []
        masters = modFile.TES4.masters
        for master in masters:
            master = GPath(master)
            if not tags & allowMissingMasters:
                if master not in minfos:
                    if not verbose: return False
                    missingMasters.append(master.s)
                elif not cached_is_active(master):
                    if not verbose: return False
                    nonActiveMasters.append(master.s)
        #--masters not present in mod list?
        if len(missingMasters):
            if not verbose: return False
            reasons.append('\n.    '+_('Masters missing: ')+'\n    * %s' % ('\n    * '.join(sorted(missingMasters))))
        if len(nonActiveMasters):
            if not verbose: return False
            reasons.append('\n.    '+_('Masters not active: ')+'\n    * %s' % ('\n    * '.join(sorted(nonActiveMasters))))
        #--Empty mod
        if modFile.IsEmpty():
            if not verbose: return False
            reasons.append('\n.    '+_('Empty mod.'))
        #--New record
        else:
            if not tags & allowMissingMasters:
                newblocks = modFile.GetNewRecordTypes()
                if newblocks:
                    if not verbose: return False
                    reasons.append('\n.    '+_('New record(s) in block(s): %s.') % ', '.join(sorted(newblocks)))
        # dependent mods mergeability should be determined BEFORE their masters
        dependent = [name.s for name, info in minfos.items() if
                     not info.isBP() and modInfo.name in info.header.masters
                     and name not in minfos.mergeable]
        if dependent:
            if not verbose: return False
            reasons.append('\n.    '+_('Is a master of non-mergeable mod(s): %s.') % ', '.join(sorted(dependent)))
        if reasons: return reasons
        return True

def isCBashMergeable(modInfo, minfos, verbose):
    """Returns True or error message indicating whether specified mod is mergeable."""
    if modInfo.name.s == "Oscuro's_Oblivion_Overhaul.esp":
        if verbose: return '\n.    ' + _(
            'Marked non-mergeable at request of mod author.')
        return False
    canmerge = _is_mergeable_no_load(modInfo, verbose)
    if verbose:
        loadreasons = _modIsMergeableLoad(modInfo, minfos, verbose)
        reasons = []
        if canmerge != True:
            reasons = canmerge
        if loadreasons != True:
            reasons.extend(loadreasons)
        if reasons: return ''.join(reasons)
        return True
    else:
        if canmerge == True:
            return _modIsMergeableLoad(modInfo, minfos, verbose)
        return False

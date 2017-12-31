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

import re
from .. import bass, balt, bosh, bush, bolt, exception
from ..balt import ItemLink, RadioLink, ChoiceLink, OneItemLink
from ..bolt import GPath, formatDate

__all__ = ['Files_SortBy', 'Files_Unhide', 'File_Backup', 'File_Duplicate',
           'File_Snapshot', 'File_RevertToBackup', 'File_RevertToSnapshot',
           'File_ListMasters']

#------------------------------------------------------------------------------
# Files Links -----------------------------------------------------------------
#------------------------------------------------------------------------------
class Files_SortBy(RadioLink):
    """Sort files by specified key (sortCol)."""

    def __init__(self, sortCol):
        super(Files_SortBy, self).__init__()
        self.sortCol = sortCol
        self._text = bass.settings['bash.colNames'][sortCol]
        self.help = _('Sort by %s') % self._text

    def _check(self): return self.window.sort_column == self.sortCol

    def Execute(self): self.window.SortItems(self.sortCol, 'INVERT')

class Files_Unhide(ItemLink):
    """Unhide file(s). (Move files back to Data Files or Save directory.)"""
    _text = _("Unhide...")

    def __init__(self, files_type):
        super(Files_Unhide, self).__init__()
        self.help = _("Unhides hidden %ss.") % files_type

    @balt.conversation
    def Execute(self):
        #--File dialog
        destDir, srcDir, srcPaths = self.window.unhide()
        if not srcPaths: return
        #--Iterate over Paths
        srcFiles = []
        destFiles = []
        for srcPath in srcPaths:
            #--Copy from dest directory?
            (newSrcDir,srcFileName) = srcPath.headTail
            if newSrcDir == destDir:
                self._showError(
                    _("You can't unhide files from this directory."))
                return
            #--File already unhidden?
            destPath = destDir.join(srcFileName)
            if destPath.exists() or (destPath + '.ghost').exists():
                self._showWarning(_("File skipped: %s. File is already "
                                    "present.") % (srcFileName.s,))
            #--Move it?
            else:
                srcFiles.append(srcPath)
                destFiles.append(destPath)
        #--Now move everything at once
        if not srcFiles:
            return
        moved = self.window.data_store.move_infos(srcFiles, destFiles,
                                                  self.window, balt.Link.Frame)
        if moved:
            self.window.RefreshUI( # pick one at random to show details for
                detail_item=next(iter(moved)), refreshSaves=True)
            self.window.SelectItemsNoCallback(moved, deselectOthers=True)

#------------------------------------------------------------------------------
# File Links ------------------------------------------------------------------
#------------------------------------------------------------------------------
class File_Duplicate(ItemLink):
    """Create a duplicate of the file - mod, save or bsa."""

    def _initData(self, window, selection):
        super(File_Duplicate, self)._initData(window, selection)
        self._text = (_('Duplicate'), _('Duplicate...'))[len(selection) == 1]
        self.help = _("Make a copy of '%s'") % (selection[0])

    _bsaAndVoice = _("This mod has an associated archive (%s." +
                    bush.game.bsa_extension + ") and an "
        "associated voice directory (Sound\\Voices\\%s), which will not be "
        "attached to the duplicate mod.") + '\n\n' + _('Note that the BSA '
        'archive may also contain a voice directory (Sound\\Voices\\%s), '
        'which would remain detached even if a duplicate archive were also '
        'created.')
    _bsa = _('This mod has an associated archive (%s.' +
                    bush.game.bsa_extension + '), which will not be '
        'attached to the duplicate mod.') + '\n\n' + _('Note that this BSA '
        'archive may contain a voice directory (Sound\\Voices\\%s), which '
        'would remain detached even if a duplicate archive were also created.'
    )
    _voice = _(r'This mod has an associated voice directory (Sound\Voice\%s),'
        ' which will not be attached to the duplicate mod.')

    def _askResourcesOk(self, fileInfo):
        msg = bosh.modInfos.askResourcesOk(fileInfo,
                                           bsaAndVoice=self._bsaAndVoice,
                                           bsa=self._bsa, voice=self._voice)
        if not msg: return True  # resources ok
        return balt.askWarning(self.window, msg,
                               _('Duplicate ') + fileInfo.name.s)

    @balt.conversation
    def Execute(self):
        dests = []
        fileInfos = self.window.data_store
        for to_duplicate, fileInfo in self.iselected_pairs():
            #--Mod with resources? Warn on rename if file has bsa and/or dialog
            if not self._askResourcesOk(fileInfo): continue
            #--Continue copy
            if bosh.saveInfos.bak_file_pattern.match(to_duplicate.s):
                continue #YAK!
            (destDir, wildcard) = (fileInfo.dir, '*' + to_duplicate.ext)
            destName = self.window.new_path(
                GPath(to_duplicate.root + ' Copy' + to_duplicate.ext), destDir)
            destDir.makedirs()
            if len(self.selected) == 1:
                destPath = self._askSave(
                    title=_('Duplicate as:'), defaultDir=destDir,
                    defaultFile=destName.s, wildcard=wildcard)
                if not destPath: return
                destDir, destName = destPath.headTail
            if (destDir == fileInfo.dir) and (destName == to_duplicate):
                self._showError(
                    _("Files cannot be duplicated to themselves!"))
                continue
            fileInfos.copy_info(to_duplicate, destDir, destName)
            if fileInfo.isMod(): ##: move this inside copy_info
                fileInfos.cached_lo_insert_after(to_duplicate, destName)
            dests.append(destName)
        if dests:
            if fileInfo.isMod(): fileInfos.cached_lo_save_lo()
            fileInfos.refresh(refresh_infos=False)
            self.window.RefreshUI(redraw=dests, detail_item=dests[-1],
                                  refreshSaves=False) #(dup) saves not affected
            self.window.SelectItemsNoCallback(dests)

class File_ListMasters(OneItemLink):
    """Copies list of masters to clipboard."""
    _text = _("List Masters...")

    def _initData(self, window, selection):
        super(File_ListMasters, self)._initData(window, selection)
        self.help = _(
            "Copies list of %(filename)s's masters to the clipboard.") % (
                        {'filename': selection[0]})

    def Execute(self):
        list_of_mods = bosh.modInfos.getModList(fileInfo=self._selected_info)
        balt.copyToClipboard(list_of_mods)
        self._showLog(list_of_mods, title=self._selected_item.s,
                      fixedFont=False)

class File_Snapshot(ItemLink):
    """Take a snapshot of the file."""
    help = _("Creates a snapshot copy of the current mod in a subdirectory (Bash\Snapshots).")

    def _initData(self, window, selection):
        super(File_Snapshot, self)._initData(window, selection)
        self._text = (_('Snapshot'),_('Snapshot...'))[len(selection) == 1]

    def Execute(self):
        for fileName, fileInfo in self.iselected_pairs():
            (destDir,destName,wildcard) = fileInfo.getNextSnapshot()
            destDir.makedirs()
            if len(self.selected) == 1:
                destPath = self._askSave(
                    title=_('Save snapshot as:'), defaultDir=destDir,
                    defaultFile=destName, wildcard=wildcard)
                if not destPath: return
                (destDir,destName) = destPath.headTail
            #--Extract version number
            fileRoot = fileName.root
            destRoot = destName.root
            fileVersion = bolt.getMatch(
                re.search(r'[ _]+v?([.\d]+)$', fileRoot.s, re.U), 1)
            snapVersion = bolt.getMatch(
                re.search(r'-[\d.]+$', destRoot.s, re.U))
            fileHedr = fileInfo.header
            if fileInfo.isMod() and (fileVersion or snapVersion) and bosh.reVersion.search(fileHedr.description):
                if fileVersion and snapVersion:
                    newVersion = fileVersion+snapVersion
                elif snapVersion:
                    newVersion = snapVersion[1:]
                else:
                    newVersion = fileVersion
                newDescription = bosh.reVersion.sub('\\1 '+newVersion, fileHedr.description,1)
                fileInfo.writeDescription(newDescription)
                self.window.panel.SetDetails(fileName)
            #--Copy file
            self.window.data_store.copy_info(fileName, destDir, destName)

class File_RevertToSnapshot(OneItemLink): # MODS LINK !
    """Revert to Snapshot."""
    _text = _('Revert to Snapshot...')
    help = _("Revert to a previously created snapshot from the Bash/Snapshots dir.")

    @balt.conversation
    def Execute(self):
        """Revert to Snapshot."""
        fileName = self._selected_item
        #--Snapshot finder
        srcDir = self._selected_info.snapshot_dir
        wildcard = self._selected_info.getNextSnapshot()[2]
        #--File dialog
        srcDir.makedirs()
        snapPath = self._askOpen(_('Revert %s to snapshot:') % fileName.s,
                                 defaultDir=srcDir, wildcard=wildcard,
                                 mustExist=True)
        if not snapPath: return
        snapName = snapPath.tail
        #--Warning box
        message = (_("Revert %s to snapshot %s dated %s?") % (
            fileName.s, snapName.s, formatDate(snapPath.mtime)))
        if not self._askYes(message, _('Revert to Snapshot')): return
        with balt.BusyCursor():
            destPath = self._selected_info.getPath()
            current_mtime = destPath.mtime
            snapPath.copyTo(destPath)
            # keep load order but recalculate the crc
            self._selected_info.setmtime(current_mtime, crc_changed=True)
            try:
                self.window.data_store.new_info(fileName, notify_bain=True)
            except exception.FileError: # FIXME(ut) - we just lost the correct file
                balt.showError(self,_('Snapshot file is corrupt!'))
                self.window.panel.ClearDetails()
        # don't refresh saves as neither selection state nor load order change
        self.window.RefreshUI(redraw=[fileName], refreshSaves=False)

class File_Backup(ItemLink):
    """Backup file."""
    _text = _('Backup')
    help = _("Create a backup of the selected file(s).")

    def Execute(self):
        for fileInfo in self.iselected_infos():
            fileInfo.makeBackup(True)

class _RevertBackup(OneItemLink):

    def __init__(self, first=False):
        super(_RevertBackup, self).__init__()
        self._text = _('Revert to First Backup') if first else _(
            'Revert to Backup')
        self.first = first

    def _initData(self, window, selection):
        super(_RevertBackup, self)._initData(window, selection)
        self.backup_path = self._selected_info.backup_dir.join(
            self._selected_item) + ('f' if self.first else '')
        self.help = _("Revert %(file)s to its first backup") if self.first \
            else _("Revert %(file)s to its last backup")
        self.help %= {'file': self._selected_item}

    def _enable(self):
        return super(_RevertBackup,
                     self)._enable() and self.backup_path.exists()

    @balt.conversation
    def Execute(self):
        #--Warning box
        message = _("Revert %s to backup dated %s?") % (
            self._selected_item.s, formatDate(self.backup_path.mtime))
        if not self._askYes(message): return
        with balt.BusyCursor():
            try:
                self._selected_info.revert_backup(self.first)
                self.window.RefreshUI(redraw=[self._selected_item],
                                      refreshSaves=False)
            except exception.FileError:
                self._showError(_('Old file is corrupt!'))
                self.window.RefreshUI(refreshSaves=True)

class File_RevertToBackup(ChoiceLink):
    """Revert to last or first backup."""
    extraItems = [_RevertBackup(), _RevertBackup(first=True)]

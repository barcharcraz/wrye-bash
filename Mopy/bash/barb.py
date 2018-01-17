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

"""Rollback library.

Re: bass.AppVersion, bass.settings['bash.version']

The latter is read from the settings - so on upgrading Bash it's the version of
the previous Bash install, whereupon is based the backup-on-upgrade routine.
Later on, in basher.BashApp#InitVersion, bass.settings['bash.version'] is
set to bass.AppVersion. We save both in the settings we backup:
- bass.settings['bash.version'] is saved first and corresponds to the version
the settings were created with
- bass.AppVersion, saved second, is the version of Bash currently executing
the backup
"""

import pickle
from os.path import join as jo

from . import archives
from . import bash
from . import bass
from . import bolt
from . import bosh
from . import bush
from . import images_list
from .bolt import GPath, deprint
from .balt import askSave, askOpen, askWarning, showError, showWarning, \
    showInfo, Link, BusyCursor, askYes
from .exception import AbstractError

opts = None # command line arguments used when launching Bash, set on bash

def init_settings_files():
    """Construct a dict mapping directory paths to setting files. Keys are
    tuples of absolute paths to directories, paired with the relative paths
    in the backup file. Values are sets of setting files in those paths,
    or empty, meaning we have to list those paths and backup everything."""
    game, dirs = bush.game.fsName, bass.dirs
    settings_info = {
        (dirs['mopy'], jo(game, 'Mopy')): {'bash.ini', },
        (dirs['mods'].join('Bash'), jo(game, 'Data', 'Bash')): {
            'Table.dat', },
        (dirs['mods'].join('Docs'), jo(game, 'Data', 'Docs')): {
            'Bash Readme Template.txt', 'Bash Readme Template.html',
            'My Readme Template.txt', 'My Readme Template.html',
            'wtxt_sand_small.css', 'wtxt_teal.css', },
        (dirs['modsBash'], jo(game + ' Mods', 'Bash Mod Data')): {
            'Table.dat', },
        (dirs['modsBash'].join('INI Data'),
         jo(game + ' Mods', 'Bash Mod Data', 'INI Data')): {
           'Table.dat', },
        (dirs['bainData'], jo(game + ' Mods', 'Bash Installers', 'Bash')): {
           'Converters.dat', 'Installers.dat', },
        (dirs['saveBase'], jo('My Games', game)): {
            'BashProfiles.dat', 'BashSettings.dat', 'BashLoadOrders.dat',
            'People.dat', },
        # backup all files in Mopy\bash\l10n, Data\Bash Patches\ and
        # Data\INI Tweaks\
        (dirs['l10n'], jo(game, 'Mopy', 'bash', 'l10n')): {},
        (dirs['mods'].join('Bash Patches'),
         jo(game, 'Data', 'Bash Patches')): {},
        (dirs['mods'].join('INI Tweaks'),
         jo(game, 'Data', 'INI Tweaks')): {},
    }
    for setting_files in settings_info.values():
        for settings_file in set(setting_files):
            if settings_file.endswith('.dat'): # add corresponding bak file
                setting_files.add(settings_file + '.bak')
    return settings_info

#------------------------------------------------------------------------------
class BaseBackupSettings(object):

    def __init__(self, parent=None, settings_file=None, do_quit=False):
        self.quit = do_quit
        self._settings_file = settings_file
        self.parent = parent
        self.files = {}

    def Apply(self):
        raise AbstractError

    @classmethod
    def get_backup_instance(cls, parent, settings_file, do_quit=False):
        settings_file = GPath(settings_file)
        settings_file = cls._get_backup_filename(parent, settings_file,
                                                 do_quit)
        if not settings_file: return None
        with BusyCursor():
            return cls(parent, settings_file, do_quit)

    @staticmethod
    def _get_backup_filename(parent, filename, do_quit):
        raise AbstractError

def new_bash_version_prompt_backup():
    # return False if old version == 0 (as in not previously installed)
    if bass.settings['bash.version'] == 0: return False
    # return True if not same app version and user opts to backup settings
    return not SameAppVersion() and askYes(Link.Frame, '\n'.join([
        _('A different version of Wrye Bash was previously installed.'),
        _('Previous Version: ') + ('%s' % bass.settings['bash.version']),
        _('Current Version: ') + ('%s' % bass.AppVersion),
        _('Do you want to create a backup of your Bash settings before '
          'they are overwritten?')]))

def SameAppVersion(): return bass.AppVersion == bass.settings['bash.version']

#------------------------------------------------------------------------------
class BackupSettings(BaseBackupSettings):
    def __init__(self, parent=None, settings_file=None, do_quit=False):
        super(BackupSettings, self).__init__(parent, settings_file, do_quit)
        game, dirs = bush.game.fsName, bass.dirs
        for (bash_dir, tmpdir), setting_files in \
                init_settings_files().items():
            if not setting_files: # we have to backup everything in there
                setting_files = bash_dir.list()
            tmp_dir = GPath(tmpdir)
            for name in setting_files:
                fpath = bash_dir.join(name)
                if fpath.exists():
                    self.files[tmp_dir.join(name)] = fpath

        #backup save profile settings
        savedir = GPath('My Games').join(game)
        profiles = [''] + bosh.SaveInfos.getLocalSaveDirs()
        for profile in profiles:
            pluginsTxt = ('Saves', profile, 'plugins.txt')
            loadorderTxt = ('Saves', profile, 'loadorder.txt')
            for txt in (pluginsTxt, loadorderTxt):
                tpath = savedir.join(*txt)
                fpath = dirs['saveBase'].join(*txt)
                if fpath.exists(): self.files[tpath] = fpath
            table = ('Saves', profile, 'Bash', 'Table.dat')
            tpath = savedir.join(*table)
            fpath = dirs['saveBase'].join(*table)
            if fpath.exists(): self.files[tpath] = fpath
            if fpath.backup.exists(): self.files[tpath.backup] = fpath.backup

    def Apply(self):
        deprint('')
        deprint(_('BACKUP BASH SETTINGS: ') + self._settings_file.s)
        temp_settings_backup_dir = bolt.Path.tempDir()
        try:
            self._backup_settings(temp_settings_backup_dir)
        finally:
            if temp_settings_backup_dir:
                temp_settings_backup_dir.rmtree(safety='WryeBash_')

    def _backup_settings(self, temp_dir):
        with BusyCursor():
            # copy all files to ~tmp backup dir
            for tpath,fpath in self.files.items():
                deprint(tpath.s + ' <-- ' + fpath.s)
                fpath.copyTo(temp_dir.join(tpath))
            # dump the version info and file listing
            with temp_dir.join('backup.dat').open('wb') as out:
                # Bash version the settings were saved with, if this is newer
                # than the installed settings version, do not allow restore
                pickle.dump(bass.settings['bash.version'], out, -1)
                # app version, if this doesn't match the installed settings
                # version, warn the user on restore
                pickle.dump(bass.AppVersion, out, -1)
            # create the backup archive in 7z format WITH solid compression
            # may raise StateError
            backup_dir, dest7z = self._settings_file.head, \
                                 self._settings_file.tail
            command = archives.compressCommand(dest7z, backup_dir, temp_dir)
            archives.compress7z(command, backup_dir, dest7z, temp_dir)
            bass.settings['bash.backupPath'] = backup_dir
        if self.quit: return
        showInfo(self.parent, '\n'.join([
            _('Your Bash settings have been backed up successfully.'),
            _('Backup Path: ') + self._settings_file.s]),
            _('Backup File Created'))

    @staticmethod
    def _get_backup_filename(parent, filename, do_quit):
        if filename is None or filename.isfile(): # don't overwrite existing
            filename = 'Backup Bash Settings %s (%s) v%s-%s.7z' % (
                bush.game.fsName, bolt.timestamp(),
                bass.settings['bash.version'], bass.AppVersion)
            if not do_quit: # we are called from UI ask user for backup name
                base_dir = bass.settings['bash.backupPath'] or bass.dirs[
                    'modsBash']
                filename = askSave(parent, title=_('Backup Bash Settings'),
                                   defaultDir=base_dir, defaultFile=filename,
                                   wildcard='*.7z')
        return filename

    def WarnFailed(self):
        showWarning(self.parent, '\n'.join([
            _('There was an error while trying to backup the Bash settings!'),
            _('No backup was created.')]),
            _('Unable to create backup!'))

#------------------------------------------------------------------------------
class RestoreSettings(BaseBackupSettings):

    def Apply(self):
        temp_settings_restore_dir = bolt.Path.tempDir()
        try:
            self._Apply(temp_settings_restore_dir)
        finally:
            if temp_settings_restore_dir:
                temp_settings_restore_dir.rmtree(safety='WryeBash_')

    def incompatible_backup(self, temp_dir):
        # TODO add game check, bash.ini check
        with temp_dir.join('backup.dat').open('rb') as ins:
            # version of Bash that created the backed up settings
            saved_settings_version = pickle.load(ins)
            # version of Bash that created the backup
            settings_saved_with = pickle.load(ins)
        if saved_settings_version > bass.settings['bash.version']:
            # Disallow restoring settings saved on a newer version of bash # TODO(ut) drop?
            showError(self.parent, '\n'.join([
                _('The data format of the selected backup file is newer than '
                'the current Bash version!'),
                _('Backup v%s is not compatible with v%s') % (
                    saved_settings_version, bass.settings['bash.version']),'',
                _('You cannot use this backup with this version of Bash.')]),
                      _('Error: Settings are from newer Bash version'))
            self.WarnFailed()
            return True
        elif settings_saved_with != bass.settings['bash.version'] and not \
             askWarning(self.parent, '\n'.join([
                 _('The version of Bash used to create the selected backup '
                   'file does not match the current Bash version!'),
                 _('Backup v%s does not match v%s') % (
                     settings_saved_with, bass.settings['bash.version']), '',
                 _('Do you want to restore this backup anyway?')]),
                                           _('Warning: Version Mismatch!')):
            return True
        return False

    def _Apply(self, temp_dir):
        command = archives.extractCommand(self._settings_file, temp_dir)
        archives.extract7z(command, self._settings_file)
        if self.incompatible_backup(temp_dir): return

        deprint('')
        deprint(_('RESTORE BASH SETTINGS: ') + self._settings_file.s)

        # reinitialize bass.dirs using the backup copy of bash.ini if it exists
        game, dirs = bush.game.fsName, bass.dirs
        tmpBash = temp_dir.join(game, 'Mopy', 'bash.ini')

        bash.SetUserPath(tmpBash.s,opts.userPath)

        bashIni = bass.GetBashIni(tmpBash.s, reload_=True)
        bosh.initBosh(opts.personalPath, opts.localAppDataPath, bashIni)

        # restore all the settings files
<<<<<<< HEAD
        restore_paths = list(init_settings_files().keys())
        if self.restore_images:
            restore_paths += [
                (dirs['images'], jo(game, 'Mopy', 'bash', 'images'))]
=======
        restore_paths = init_settings_files().keys()
>>>>>>> upstream/dev
        for dest_dir, back_path in restore_paths:
            full_back_path = temp_dir.join(back_path)
            if full_back_path.exists():
                for name in full_back_path.list():
                    if full_back_path.join(name).isfile():
                        deprint(GPath(back_path).join(name).s + ' --> '
                                + dest_dir.join(name).s)
                        full_back_path.join(name).copyTo(dest_dir.join(name))

        #restore savegame profile settings
        back_path = GPath('My Games').join(game, 'Saves')
        saves_dir = dirs['saveBase'].join('Saves')
        full_back_path = temp_dir.join(back_path)
        if full_back_path.exists():
            for root_dir, folders, files in full_back_path.walk(True,None,True):
                root_dir = GPath('.'+root_dir.s)
                for name in files:
                    deprint(back_path.join(root_dir,name).s + ' --> '
                            + saves_dir.join(root_dir, name).s)
                    full_back_path.join(root_dir, name).copyTo(
                        saves_dir.join(root_dir, name))

        # tell the user the restore is complete and warn about restart
        self.WarnRestart()
        if Link.Frame: # should always exist
            Link.Frame.Destroy()

    @staticmethod
    def _get_backup_filename(parent, filename, do_quit):
        if filename is None or filename.cext != '.7z' or not filename.isfile():
            # former may be None
            base_dir = bass.settings['bash.backupPath'] or bass.dirs[
                'modsBash']
            filename = askOpen(parent, _('Restore Bash Settings'), base_dir,
                               '', '*.7z')
        return filename

    def WarnFailed(self):
        showWarning(self.parent, '\n'.join([
            _('There was an error while trying to restore your settings from '
              'the backup file!'), _('No settings were restored.')]),
                    _('Unable to restore backup!'))

    def WarnRestart(self):
        if self.quit: return
        showWarning(self.parent, '\n'.join([
            _('Your Bash settings have been successfully restored.'),
            _('Backup Path: ') + self._settings_file.s, '',
            _('Before the settings can take effect, Wrye Bash must restart.'),
            _('Click OK to restart now.')]), _('Bash Settings Restored'))
        Link.Frame.Restart()

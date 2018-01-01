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

"""This module starts the Wrye Bash application in console mode. Basically,
it runs some initialization functions and then starts the main application
loop."""

# Imports ---------------------------------------------------------------------
import atexit
import codecs
import os
import platform
import sys
import traceback
# Local
from . import bass
from . import exception
# NO OTHER LOCAL IMPORTS HERE (apart from the ones above) !
basher = balt = barb = bolt = None
_wx = None
is_standalone = hasattr(sys, 'frozen')

def _import_bolt(opts):
    """Import bolt or show a tkinter error and exit if unsuccessful.

    :param opts: command line arguments"""
    global bolt
    try:
        # First of all set the language, set on importing bolt
        bass.language = opts.language
        from . import bolt  # bass.language must be set
    except Exception as e:
        but_kwargs = {'text': "QUIT", 'fg': 'red'}  # foreground button color
        msg = '\n'.join([dump_environment(), '', 'Unable to load bolt:',
                          traceback.format_exc(e), 'Exiting.'])
        _tkinter_error_dial(msg, but_kwargs)
        sys.exit(1)

def _import_wx():
    """Import wxpython or show a tkinter error and exit if unsuccessful."""
    global _wx
    try:
        import wx as _wx
    except ImportError:
        but_kwargs = {'text': _("QUIT"),
                      'fg': 'red'}  # foreground button color
        msg = '\n'.join([dump_environment(), '',
            _('Unable to locate wxpython installation. Exiting.')])
        _tkinter_error_dial(msg, but_kwargs)
        sys.exit(1)

#------------------------------------------------------------------------------
def SetHomePath(homePath):
    drive,path = os.path.splitdrive(homePath)
    os.environ['HOMEDRIVE'] = drive
    os.environ['HOMEPATH'] = path

#------------------------------------------------------------------------------
def SetUserPath(iniPath=None, uArg=None):
#if uArg is None, then get the UserPath from the ini file
    if uArg:
        SetHomePath(uArg)
    else:
        bashIni = bass.GetBashIni(iniPath=iniPath, reload_=iniPath is not None)
        if bashIni and bashIni.has_option('General', 'sUserPath')\
                   and not bashIni.get('General', 'sUserPath') == '.':
            SetHomePath(bashIni.get('General', 'sUserPath'))

# Backup/Restore --------------------------------------------------------------
def cmdBackup(opts):
    # backup settings if app version has changed or on user request
    global basher, balt, barb
    if not basher: from . import basher, balt, barb
    path = (opts.backup and opts.filename) or None
    should_quit = opts.backup and opts.quietquit
    if barb.new_bash_version_prompt_backup() or opts.backup:
        frame = balt.Link.Frame
        backup = barb.BackupSettings.get_backup_instance(frame, path,
            should_quit, opts.backup_images)
        if not backup: return
        try:
            backup.Apply()
        except exception.StateError:
            if barb.SameAppVersion():
                backup.WarnFailed()
            elif balt.askYes(frame, '\n'.join([
            _('There was an error while trying to backup the Bash settings!'),
            _('If you continue, your current settings may be overwritten.'),
            _('Do you want to quit Wrye Bash now?')]),
                             title=_('Unable to create backup!')):
                return True # Quit
    return should_quit

def cmdRestore(opts):
    # restore settings on user request
    if not opts.restore: return False
    global basher, balt, barb
    if not basher: from . import basher, balt, barb
    should_quit = opts.quietquit
    backup = barb.RestoreSettings.get_backup_instance(balt.Link.Frame,
        opts.filename or None, should_quit, opts.backup_images)
    if not backup : return False
    backup.Apply()
    return should_quit

def assure_single_instance(instance):
    """Ascertain that only one instance of Wrye Bash is running.

    If this is the second instance running, then display an error message and
    exit.

    :type instance: wx.SingleInstanceChecker"""
    if instance.IsAnotherRunning():
        bolt.deprint('Only one instance of Wrye Bash can run. Exiting.')
        msg = _('Only one instance of Wrye Bash can run.')
        _app = _wx.App(False)
        with _wx.MessageDialog(None, msg, _('Wrye Bash'), _wx.OK) as dialog:
            dialog.ShowModal()
        sys.exit(1)

def exit_cleanup():
    # Cleanup temp installers directory
    import tempfile
    tmpDir = bolt.GPath(tempfile.tempdir)
    for file_ in tmpDir.list():
        if file_.cs.startswith('wryebash_'):
            file_ = tmpDir.join(file_)
            try:
                if file_.isdir():
                    file_.rmtree(safety=file_.stail)
                else:
                    file_.remove()
            except:
                pass

    if basher:
        from .basher import appRestart
        from .basher import uacRestart
        if appRestart:
            if not is_standalone:
                exePath = bolt.GPath(sys.executable)
                sys.argv = [exePath.stail] + sys.argv
            if '--restarting' not in sys.argv:
                sys.argv += ['--restarting']
            #--Assume if we're restarting that they don't want to be
            #  prompted again about UAC
            if '--no-uac' not in sys.argv:
                sys.argv += ['--no-uac']
            def updateArgv(args):
                if isinstance(args,(list,tuple)):
                    if len(args) > 0 and isinstance(args[0],(list,tuple)):
                        for arg in args:
                            updateArgv(arg)
                    else:
                        found = 0
                        for i in range(len(sys.argv)):
                            if not found and sys.argv[i] == args[0]:
                                found = 1
                            elif found:
                                if found < len(args):
                                    sys.argv[i] = args[found]
                                    found += 1
                                else:
                                    break
                        else:
                            sys.argv.extend(args)
            updateArgv(appRestart)
            try:
                if uacRestart:
                    if not is_standalone:
                        sys.argv = sys.argv[1:]
                    import win32api
                    if is_standalone:
                        win32api.ShellExecute(0,'runas',sys.argv[0],' '.join(
                            '"%s"' % x for x in sys.argv[1:]),None,True)
                    else:
                        args = ' '.join(
                            ['%s','"%s"'][' ' in x] % x for x in sys.argv)
                        win32api.ShellExecute(0,'runas',exePath.s,args,None,
                                              True)
                    return
                else:
                    import subprocess
                    if is_standalone:
                        subprocess.Popen(sys.argv,close_fds=bolt.close_fds)
                    else:
                        subprocess.Popen(sys.argv,executable=exePath.s,
                                         close_fds=bolt.close_fds)
                                         #close_fds is needed for the one
                                         # instance checker
            except Exception as error:
                print(error)
                print('Error Attempting to Restart Wrye Bash!')
                print('cmd line: %s %s' %(exePath.s, sys.argv))
                print()
                raise

def dump_environment():
    import locale
    fse = sys.getfilesystemencoding()
    msg = '\n'.join([
        'Wrye Bash starting',
        'Using Wrye Bash Version %s%s' % (bass.AppVersion,
            (' ' + _('(Standalone)')) if is_standalone else ''
        ),
        'OS info: %s' % platform.platform(),
        'Python version: %d.%d.%d' % (
            sys.version_info[0],sys.version_info[1],sys.version_info[2]
        ),
        'wxPython version: %s' % _wx.version() if _wx is not None else \
            'wxPython not found',
        # Standalone: stdout will actually be pointing to stderr, which has no
        # 'encoding' attribute
        'input encoding: %s; output encoding: %s; locale: %s' % (
            sys.stdin.encoding,getattr(sys.stdout,'encoding',None),
            locale.getdefaultlocale()
        ),
        'filesystem encoding: %s%s' % (fse,
            (' - using %s' % bolt.Path.sys_fs_enc) if bolt is not None
                                                       and not fse else '')
    ])
    if bolt.scandir is not None:
        msg = '\n'.join( [msg, 'Using scandir ' + bolt.scandir.__version__])
    print(msg)
    return msg

# Main ------------------------------------------------------------------------
def main(opts):
    """Run the Wrye Bash main loop.

    :param opts: command line arguments
    :type opts: Namespace"""
    # First import bolt, needed for localization of error messages
    _import_bolt(opts)
    # Then import wx so we can style our error messages nicely
    _import_wx()
    try:
        _main(opts)
    except Exception as e:
        msg = '\n'.join([
            _('Wrye Bash encountered an error.'),
            _('Please post the information below to the official thread at:'),
            _('https://afkmods.iguanadons.net/index.php?/topic/4966-wrye-bash-all-games/& or '),
            _('https://bethesda.net/community/topic/38798/relz-wrye-bash-oblivion-skyrim-skyrim-se-fallout-4/'),
            '',
            traceback.format_exc()
        ])
        _close_dialog_windows()
        _show_wx_error(msg)
        sys.exit(1)

def _main(opts):
    """Run the Wrye Bash main loop.

    This function is marked private because it should be inside a try-except
    block. Call main() from the outside.

    :param opts: command line arguments
    """
    from . import env # env imports bolt (this needs fixing)
    bolt.deprintOn = opts.debug
    # useful for understanding context of bug reports
    if opts.debug or is_standalone:
        # Standalone stdout is NUL no matter what.   Redirect it to stderr.
        # Also, setup stdout/stderr to the debug log if debug mode /
        # standalone before wxPython is up
        # errLog = io.open(os.path.join(os.getcwdu(),u'BashBugDump.log'),'w',encoding='utf-8')
        errLog = codecs.getwriter('utf-8')(
            open(os.path.join(os.getcwd(), 'BashBugDump.log'), 'w'))
        sys.stdout = errLog
        sys.stderr = errLog
        old_stderr = errLog

    if opts.debug:
        dump_environment()

    # ensure we are in the correct directory so relative paths will work
    # properly
    if is_standalone:
        pathToProg = os.path.dirname(
            str(sys.executable + bolt.Path.sys_fs_enc))
    else:
        pathToProg = os.path.dirname(
            str(sys.argv[0] + bolt.Path.sys_fs_enc))
    if pathToProg:
        os.chdir(pathToProg)
    del pathToProg

    # Check if there are other instances of Wrye Bash running
    instance = _wx.SingleInstanceChecker('Wrye Bash')
    assure_single_instance(instance)

    # Detect the game we're running for ---------------------------------------
    from . import bush
    bolt.deprint ('Searching for game to manage:')
    # set the Bash ini global in bass
    bashIni = bass.GetBashIni()
    ret = bush.detect_and_set_game(opts.oblivionPath, bashIni)
    if ret is not None: # None == success
        if len(ret) == 0:
            msgtext = _(
                "Wrye Bash could not find a game to manage. Please use "
                "-o command line argument to specify the game path")
        else:
            msgtext = _(
                "Wrye Bash could not determine which game to manage.  "
                "The following games have been detected, please select "
                "one to manage.")
            msgtext += '\n\n'
            msgtext += _(
                'To prevent this message in the future, use the -o command '
                'line argument or the bash.ini to specify the game path')
        retCode = _wxSelectGame(ret, msgtext)
        if retCode is None:
            bolt.deprint("No games were found or Selected. Aborting.")
            return
        # Add the game to the command line, so we use it if we restart
        sys.argv += ['-o', bush.game_path(retCode).s]
        bush.detect_and_set_game(opts.oblivionPath, bashIni, retCode)

    # from now on bush.game is set

    #--Initialize Directories and some settings
    #  required before the rest has imported
    SetUserPath(uArg=opts.userPath)

    # Force Python mode if CBash can't work with this game
    bolt.CBash = opts.mode if bush.game.esp.canCBash else 1 #1 = python mode...
    try:
        from . import bosh # this imports balt (DUH) which imports wx
        env.isUAC = env.testUAC(bush.gamePath.join('Data'))
        bosh.initBosh(opts.personalPath, opts.localAppDataPath, bashIni)

        # if HTML file generation was requested, just do it and quit
        if opts.genHtml is not None:
            msg1 = _("generating HTML file from: '%s'") % opts.genHtml
            msg2 = _('done')
            try: print(msg1)
            except UnicodeError: print(msg1.encode(bolt.Path.sys_fs_enc))
            from . import belt # this imports bosh which imports wx (DUH)
            bolt.WryeText.genHtml(opts.genHtml)
            try: print(msg2)
            except UnicodeError: print(msg2.encode(bolt.Path.sys_fs_enc))
            return
        global basher, balt, barb
        from . import basher
        from . import barb
        from . import balt
        barb.opts = opts
    except (exception.PermissionError,
            exception.BoltError, ImportError) as e:
        msg = '\n'.join([_('Error! Unable to start Wrye Bash.'), '\n', _(
            'Please ensure Wrye Bash is correctly installed.'), '\n',
                          traceback.format_exc(e)])
        _close_dialog_windows()
        _show_wx_error(msg)
        return

    atexit.register(exit_cleanup)
    basher.InitSettings()
    basher.InitLinks()
    basher.InitImages()
    #--Start application
    if opts.debug:
        if is_standalone:
            # Special case for py2exe version
            app = basher.BashApp()
            # Regain control of stdout/stderr from wxPython
            sys.stdout = old_stderr
            sys.stderr = old_stderr
        else:
            app = basher.BashApp(False)
    else:
        app = basher.BashApp()

    if not is_standalone and (
        not _rightWxVersion() or not _rightPythonVersion()): return

    # process backup/restore options
    # quit if either is true, but only after calling both
    should_quit = cmdBackup(opts)
    should_quit = cmdRestore(opts) or should_quit
    if should_quit: return
    if env.isUAC:
        uacRestart = False
        if not opts.noUac and not opts.uac:
            # Show a prompt asking if we should restart in Admin Mode
            message = _(
                "Wrye Bash needs Administrator Privileges to make changes "
                "to the %(gameName)s directory.  If you do not start Wrye "
                "Bash with elevated privileges, you will be prompted at "
                "each operation that requires elevated privileges.") % {
                          'gameName': bush.game.displayName}
            uacRestart = balt.ask_uac_restart(message,
                                              title=_('UAC Protection'),
                                              mopy=bass.dirs['mopy'])
        elif opts.uac:
            uacRestart = True
        if uacRestart:
            basher.appRestart = True
            basher.uacRestart = True
            return

    app.Init() # Link.Frame is set here !
    app.MainLoop()

def _show_wx_error(msg):
    """Shows an error message in a wx window."""
    try:
        class MessageBox(_wx.Dialog):
            def __init__(self, msg):
                _wx.Dialog.__init__(self, None, -1, title=_('Wrye Bash Error'),
                                    size=(400, 300),
                                    style=_wx.DEFAULT_DIALOG_STYLE |
                                          _wx.STAY_ON_TOP |
                                          _wx.DIALOG_NO_PARENT |
                                          _wx.RESIZE_BORDER)
                sizer = _wx.BoxSizer(_wx.VERTICAL)
                text = _wx.TextCtrl(self,
                                    style=_wx.TE_MULTILINE | _wx.TE_BESTWRAP |
                                          _wx.TE_READONLY | _wx.BORDER_NONE)
                text.SetValue(msg)
                text.SetBackgroundColour(_wx.SystemSettings.GetColour(4))
                sizer.Add(text, proportion=1, flag=_wx.GROW | _wx.ALL,
                          border=5)
                button = _wx.Button(self, _wx.ID_CANCEL, _('Quit'))
                button.SetDefault()
                sizer.Add(button, proportion=0,
                          flag=_wx.ALIGN_CENTER | _wx.ALL, border=5)
                self.SetSizer(sizer)
                # sizer.Fit(self)
                self.ShowModal()
                self.Destroy()

        print(msg) # Print msg into error log.
        app = _wx.GetApp() # wx.App is a singleton, get it if it exists.
        if app:
            MessageBox(msg)
            app.Exit()
        else:
            app = _wx.App(False) # wx.App is not instantiated, do so now .
            if app:
                MessageBox(msg)
                app.Exit()
            else:
                # Instantiating wx.App failed, fallback to tkinter.
                but_kwargs = {'text': _("QUIT"),
                              'fg': 'red'}  # foreground button color
                _tkinter_error_dial(msg, but_kwargs)

    except Exception as e:
        print('Wrye Bash encountered an error but could not display it.')
        print('The following is the error that occurred when displaying the '\
              'first error:')
        try:
            print(traceback.format_exc(e))
        except Exception:
            print('   An error occurred while displaying the second error.')

def _tkinter_error_dial(msg, but_kwargs):
    import tkinter
    root_widget = tkinter.Tk()
    frame = tkinter.Frame(root_widget)
    frame.pack()
    button = tkinter.Button(frame, command=root_widget.destroy, pady=15,
                            borderwidth=5, relief=tkinter.GROOVE, **but_kwargs)
    button.pack(fill=tkinter.BOTH, expand=1, side=tkinter.BOTTOM)
    w = tkinter.Text(frame)
    w.insert(tkinter.END, msg)
    w.config(state=tkinter.DISABLED)
    w.pack()
    root_widget.mainloop()

def _close_dialog_windows():
    """Close any additional windows opened by wrye bash (e.g Splash, Dialogs).

    This will not close the main bash window (BashFrame) because closing that
    results in virtual function call exceptions."""
    for window in _wx.GetTopLevelWindows():
        if basher is None or not isinstance(window, basher.BashFrame):
            if isinstance(window, _wx.Dialog):
                window.Destroy()
            window.Close()

class _AppReturnCode(object):
    def __init__(self, default=None): self.value = default
    def get(self): return self.value
    def set(self, value): self.value = value

def _wxSelectGame(ret, msgtext):

    class GameSelect(_wx.Frame):
        def __init__(self, gameNames, callback):
            _wx.Frame.__init__(self, None, title='Wrye Bash')
            self.callback = callback
            self.panel = panel = _wx.Panel(self)
            sizer = _wx.BoxSizer(_wx.VERTICAL)
            sizer.Add(_wx.TextCtrl(panel, value=msgtext,
                                   style=_wx.TE_MULTILINE | _wx.TE_READONLY |
                                         _wx.TE_BESTWRAP),
                      1, _wx.GROW | _wx.ALL, 5)
            for gameName in gameNames:
                gameName = gameName.title()
                sizer.Add(_wx.Button(panel, label=gameName), 0,
                          _wx.GROW | _wx.ALL ^ _wx.TOP, 5)
            button = _wx.Button(panel, _wx.ID_CANCEL, _('Quit'))
            button.SetDefault()
            sizer.Add(button, 0, _wx.GROW | _wx.ALL ^ _wx.TOP, 5)
            self.Bind(_wx.EVT_BUTTON, self.OnButton)
            panel.SetSizer(sizer)

        def OnButton(self, event):
            if event.GetId() != _wx.ID_CANCEL:
                self.callback(self.FindWindowById(event.GetId()).GetLabel())
            self.Close(True)

    _app = _wx.App(False)
    retCode = _AppReturnCode()
    frame = GameSelect(ret, retCode.set)
    frame.Show()
    frame.Center()
    _app.MainLoop()
    del _app
    return retCode.get()

# Version checks --------------------------------------------------------------
def _rightWxVersion():
    wxver = _wx.version()
    wxver_tuple = _wx.VERSION
    if wxver != '2.8.12.1 (msw-unicode)' and wxver_tuple < (2,9):
        return balt.askYes(
            None, 'Warning: you appear to be using a non-supported version '
            'of wxPython (%s).  This will cause problems!  It is highly '
            'recommended you use either version 2.8.12.1 (msw-unicode) or, '
            'at your discretion, a later version (untested). Do you still '
            'want to run Wrye Bash?' % wxver,
            'Warning: Non-Supported wxPython detected', )
    return True

def _rightPythonVersion():
    sysVersion = sys.version_info[:3]
    if sysVersion < (3, 6):
        balt.showError(None, _("Only Python 3.6 and newer is supported "
            "(%s.%s.%s detected). If you know what you're doing install the "
            "WB python version and edit this warning out. "
            "Wrye Bash will exit.") % sysVersion,
            title=_("Incompatible Python version detected"))
        return False
    return True

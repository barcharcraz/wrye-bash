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

import string
#from types import IntType, LongType
import wx
from . import bEnableWizard, tabInfo, BashFrame
from .constants import colorInfo, settingDefaults, installercons
from .. import bass, balt, bosh, bolt, bush, env
from ..balt import Button, hSizer, Link, colors, RoTextCtrl, vSizer, hspacer, \
    checkBox, StaticText, Image, bell, TextCtrl, tooltip, OkButton, \
    CancelButton, ApplyButton, hspace, vspace, Resources
from ..bosh import faces

class ColorDialog(balt.Dialog):
    """Color configuration dialog"""
    title = _('Color Configuration')

    _keys_to_tabs = {
        'mods': _('[Mods] '),
        'screens': _('[Saves, Screens] '),
        'installers': _('[Installers] '),
        'ini': _('[INI Edits] '),
        'tweak': _('[INI Edits] '),
        'default': _('[All] '),
    }

    def __init__(self):
        super(ColorDialog, self).__init__(parent=Link.Frame, resize=False)
        self.changes = dict()
        #--ComboBox
        keys = [x for x in colors]
        def _display_text(k):
            return _(self._keys_to_tabs[k.split('.')[0]]) + colorInfo[k][0]
        self.text_key = dict((_display_text(x), x) for x in keys)
        colored = list(self.text_key.keys())
        colored.sort(key=str.lower)
        combo_text = colored[0]
        choiceKey = self.text_key[combo_text]
        self.comboBox = balt.ComboBox(self, value=combo_text, choices=colored)
        #--Color Picker
        self.picker = wx.ColourPickerCtrl(self)
        self.picker.SetColour(colors[choiceKey])
        #--Description
        help_ = colorInfo[choiceKey][1]
        self.textCtrl = RoTextCtrl(self, help_)
        #--Buttons
        self.default = Button(self, _('Default'),
                              onButClickEventful=self.OnDefault)
        self.defaultAll = Button(self, _('All Defaults'),
                                 onButClickEventful=self.OnDefaultAll)
        self.apply = ApplyButton(self, onButClickEventful=self.OnApply)
        self.applyAll = Button(self, _('Apply All'),
                               onButClickEventful=self.OnApplyAll)
        self.export_config = Button(self, _('Export...'),
                                    onButClickEventful=self.OnExport)
        self.importConfig = Button(self, _('Import...'),
                                   onButClickEventful=self.OnImport)
        self.ok = OkButton(self, onButClickEventful=self.OnApplyAll,
                           default=True)
        #--Events
        self.comboBox.Bind(wx.EVT_COMBOBOX,self.OnComboBox)
        self.picker.Bind(wx.EVT_COLOURPICKER_CHANGED,self.OnColorPicker)
        #--Layout
        sizer = vSizer(
            (hSizer((self.comboBox,1,wx.EXPAND), hspace(5), self.picker,
                ),0,wx.EXPAND|wx.ALL,5),
            (self.textCtrl,1,wx.EXPAND|wx.ALL,5),
            (hSizer(self.defaultAll, hspace(5),
                    self.applyAll, hspace(5),
                    self.export_config,
                    ),0,wx.EXPAND|wx.ALL,5),
            (hSizer(self.default, hspace(5),
                    self.apply, hspace(5),
                    self.importConfig, hspacer, self.ok,
                    ),0,wx.EXPAND|wx.ALL,5),
            )
        self.comboBox.SetFocus()
        self.SetSizer(sizer)
        self.SetIcons(Resources.bashBlue)
        self.UpdateUIButtons()

    def GetColorKey(self):
        """Return balt.colors dict key for current combobox selection."""
        return self.text_key[self.comboBox.GetValue()]

    @staticmethod
    def UpdateUIColors():
        """Update the Bash Frame with the new colors"""
        with balt.BusyCursor():
            for (className,title,panel) in tabInfo.values():
                if panel is not None:
                    panel.RefreshUIColors()

    def UpdateUIButtons(self):
        # Apply All and Default All
        for key, val in list(self.changes.items()):
            if val == colors[key]:
                del self.changes[key]
        anyChanged = bool(self.changes)
        allDefault = True
        for key in colors:
            if key in self.changes:
                color = self.changes[key]
            else:
                color = colors[key]
            default = bool(color == settingDefaults['bash.colors'][key])
            if not default:
                allDefault = False
                break
        # Apply and Default
        color_key = self.GetColorKey()
        changed = bool(color_key in self.changes)
        if changed:
            color = self.changes[color_key]
        else:
            color = colors[color_key]
        default = bool(color == settingDefaults['bash.colors'][color_key])
        # Update the Buttons, ComboBox, and ColorPicker
        self.apply.Enable(changed)
        self.applyAll.Enable(anyChanged)
        self.default.Enable(not default)
        self.defaultAll.Enable(not allDefault)
        self.picker.SetColour(color)
        self.comboBox.SetFocusFromKbd()

    def OnDefault(self,event):
        event.Skip()
        color_key = self.GetColorKey()
        newColor = settingDefaults['bash.colors'][color_key]
        self.changes[color_key] = newColor
        self.UpdateUIButtons()

    def OnDefaultAll(self,event):
        event.Skip()
        for key in colors:
            default = settingDefaults['bash.colors'][key]
            if colors[key] != default:
                self.changes[key] = default
        self.UpdateUIButtons()

    def OnApply(self,event):
        event.Skip()
        color_key = self.GetColorKey()
        newColor = self.changes[color_key]
        #--Update settings and colors
        bass.settings['bash.colors'][color_key] = newColor
        bass.settings.setChanged('bash.colors')
        colors[color_key] = newColor
        self.UpdateUIButtons()
        self.UpdateUIColors()

    def OnApplyAll(self,event):
        event.Skip()
        for key,newColor in self.changes.items():
            bass.settings['bash.colors'][key] = newColor
            colors[key] = newColor
        bass.settings.setChanged('bash.colors')
        self.UpdateUIButtons()
        self.UpdateUIColors()

    def OnExport(self,event):
        event.Skip()
        outDir = bass.dirs['patches']
        outDir.makedirs()
        #--File dialog
        outPath = balt.askSave(self,_('Export color configuration to:'), outDir, _('Colors.txt'), '*.txt')
        if not outPath: return
        try:
            with outPath.open('w') as file:
                for key in colors:
                    if key in self.changes:
                        color = self.changes[key]
                    else:
                        color = colors[key]
                    file.write(key+': '+color+'\n')
        except Exception as e:
            balt.showError(self,_('An error occurred writing to ')+outPath.stail+':\n\n%s'%e)

    def OnImport(self,event):
        event.Skip()
        inDir = bass.dirs['patches']
        inDir.makedirs()
        #--File dialog
        inPath = balt.askOpen(self,_('Import color configuration from:'), inDir, _('Colors.txt'), '*.txt', mustExist=True)
        if not inPath: return
        try:
            with inPath.open('r') as file:
                for line in file:
                    # Format validation
                    if ':' not in line:
                        continue
                    split = line.split(':')
                    if len(split) != 2:
                        continue
                    key = split[0]
                    # Verify color exists
                    if key not in colors:
                        continue
                    # Color format verification
                    color = eval(split[1])
                    if not isinstance(color, tuple) or len(color) not in (3,4):
                        continue
                    ok = True
                    for value in color:
                        if not isinstance(value,int):
                            ok = False
                            break
                        if value < 0x00 or value > 0xFF:
                            ok = False
                            break
                    if not ok:
                        continue
                    # Save it
                    if color == colors[key]: continue
                    self.changes[key] = color
        except Exception as e:
            balt.showError(Link.Frame, _(
                'An error occurred reading from ') + inPath.stail +
                           ':\n\n%s' % e)
        self.UpdateUIButtons()

    def OnComboBox(self,event):
        event.Skip()
        self.UpdateUIButtons()
        color_key = self.GetColorKey()
        help = colorInfo[color_key][1]
        self.textCtrl.SetValue(help)

    def OnColorPicker(self,event):
        event.Skip()
        color_key = self.GetColorKey()
        newColor = self.picker.GetColour()
        self.changes[color_key] = newColor
        self.UpdateUIButtons()

#------------------------------------------------------------------------------
class ImportFaceDialog(balt.Dialog):
    """Dialog for importing faces."""
    def __init__(self, parent, title, fileInfo, faces):
        #--Data
        self.fileInfo = fileInfo
        if faces and isinstance(list(faces.keys())[0],(int)):
            self.data = dict(('%08X %s' % (key,face.pcName),face) for key,face in list(faces.items()))
        else:
            self.data = faces
        self.list_items = sorted(list(self.data.keys()),key=string.lower)
        #--GUI
        super(ImportFaceDialog, self).__init__(parent, title=title)
        self.SetSizeHints(550,300)
        #--List Box
        self.listBox = balt.listBox(self, choices=self.list_items,
                                    onSelect=self.EvtListBox)
        self.listBox.SetSizeHints(175,150)
        #--Name,Race,Gender Checkboxes
        flags = bosh.faces.PCFaces.flags(bass.settings.get('bash.faceImport.flags', 0x4))
        self.nameCheck = checkBox(self, _('Name'), checked=flags.name)
        self.raceCheck = checkBox(self, _('Race'), checked=flags.race)
        self.genderCheck = checkBox(self, _('Gender'), checked=flags.gender)
        self.statsCheck = checkBox(self, _('Stats'), checked=flags.stats)
        self.classCheck = checkBox(self, _('Class'), checked=flags.iclass)
        #--Name,Race,Gender Text
        self.nameText  = StaticText(self,'-----------------------------')
        self.raceText  = StaticText(self,'')
        self.genderText  = StaticText(self,'')
        self.statsText  = StaticText(self,'')
        self.classText  = StaticText(self,'')
        #--Other
        importButton = Button(self, label=_('Import'),
                              onButClick=self.DoImport, default=True)
        self.picture = balt.Picture(self,350,210,scaling=2)
        #--Layout
        fgSizer = wx.FlexGridSizer(3,2,2,4)
        fgSizer.AddGrowableCol(1,1)
        fgSizer.AddMany([
            self.nameCheck,
            self.nameText,
            self.raceCheck,
            self.raceText,
            self.genderCheck,
            self.genderText,
            self.statsCheck,
            self.statsText,
            self.classCheck,
            self.classText,
            ])
        sizer = hSizer(
            (self.listBox,1,wx.EXPAND|wx.TOP,4),
            (vSizer(
                self.picture, vspace(),
                (hSizer(
                    (fgSizer,1),
                    (vSizer(
                        (importButton,0,wx.ALIGN_RIGHT),
                        vspace(), CancelButton(self),
                        )),
                    ),0,wx.EXPAND),
                ),0,wx.EXPAND|wx.ALL,4),
            )
        #--Done
        if 'ImportFaceDialog' in balt.sizes:
            self.SetSizer(sizer)
            self.SetSize(balt.sizes['ImportFaceDialog'])
        else:
            self.SetSizerAndFit(sizer)

    def EvtListBox(self,event):
        """Responds to listbox selection."""
        itemDex = event.GetSelection()
        item = self.list_items[itemDex]
        face = self.data[item]
        self.nameText.SetLabel(face.pcName)
        self.raceText.SetLabel(face.getRaceName())
        self.genderText.SetLabel(face.getGenderName())
        self.statsText.SetLabel(_('Health ')+str(face.health))
        itemImagePath = bass.dirs['mods'].join('Docs', 'Images', '%s.jpg' % item)
        # TODO(ut): any way to get the picture ? see mod_links.Mod_Face_Import
        bitmap = itemImagePath.exists() and Image(
            itemImagePath.s).GetBitmap() or None
        self.picture.SetBitmap(bitmap)
        self.listBox.SetSelection(itemDex)

    def DoImport(self):
        """Imports selected face into save file."""
        selections = self.listBox.GetSelections()
        if not selections:
            bell()
            return
        itemDex = selections[0]
        item = self.list_items[itemDex]
        #--Do import
        flags = bosh.faces.PCFaces.flags()
        flags.hair = flags.eye = True
        flags.name = self.nameCheck.GetValue()
        flags.race = self.raceCheck.GetValue()
        flags.gender = self.genderCheck.GetValue()
        flags.stats = self.statsCheck.GetValue()
        flags.iclass = self.classCheck.GetValue()
        #deprint(flags.getTrueAttrs())
        bass.settings['bash.faceImport.flags'] = int(flags)
        bosh.faces.PCFaces.save_setFace(self.fileInfo,self.data[item],flags)
        balt.showOk(self,_('Face imported.'),self.fileInfo.name.s)
        self.EndModalOK()

#------------------------------------------------------------------------------
class CreateNewProject(balt.Dialog):
    title = _('Create New Project')
    def __init__(self,parent=None):
        super(CreateNewProject, self).__init__(parent, resize=False)
        #--Build a list of existing directories
        #  The text control will use this to change background color when name collisions occur
        self.existingProjects = [x for x in bass.dirs['installers'].list() if bass.dirs['installers'].join(x).isdir()]

        #--Attributes
        self.textName = TextCtrl(self, _('New Project Name-#####'),
                                 onText=self.OnCheckProjectsColorTextCtrl)
        self.checkEsp = checkBox(self, _('Blank.esp'),
                                 onCheck=self.OnCheckBoxChange, checked=True)
        self.checkEspMasterless = checkBox(self, _('Blank Masterless.esp'),
                                   onCheck=self.OnCheckBoxChange, checked=False)
        self.checkWizard = checkBox(self, _('Blank wizard.txt'),
                                    onCheck=self.OnCheckBoxChange)
        self.checkWizardImages = checkBox(self, _('Wizard Images Directory'))
        if not bEnableWizard:
            # pywin32 not installed
            self.checkWizard.Disable()
            self.checkWizardImages.Disable()
        self.checkDocs = checkBox(self,_('Docs Directory'))
        # self.checkScreenshot = checkBox(self,_(u'Preview Screenshot(No.ext)(re-enable for BAIT)'))
        # self.checkScreenshot.Disable() #Remove this when BAIT gets preview stuff done
        okButton = OkButton(self, onButClickEventful=self.OnClose)
        cancelButton = CancelButton(self, onButClickEventful=self.OnCancel)
        # Panel Layout
        hsizer = balt.hSizer()
        hsizer.Add(okButton,0,wx.ALL|wx.ALIGN_CENTER,10)
        hsizer.Add(cancelButton,0,wx.ALL|wx.ALIGN_CENTER,10)
        vsizer = balt.vSizer()
        vsizer.Add(StaticText(self,_('What do you want to name the New Project?'),style=wx.TE_RICH2),0,wx.ALL|wx.ALIGN_CENTER,10)
        vsizer.Add(self.textName,0,wx.ALL|wx.ALIGN_CENTER|wx.EXPAND,2)
        vsizer.Add(StaticText(self,_('What do you want to add to the New Project?')),0,wx.ALL|wx.ALIGN_CENTER,10)
        vsizer.Add(self.checkEsp,0,wx.ALL|wx.ALIGN_TOP,5)
        vsizer.Add(self.checkEspMasterless,0,wx.ALL|wx.ALIGN_TOP,5)
        vsizer.Add(self.checkWizard,0,wx.ALL|wx.ALIGN_TOP,5)
        vsizer.Add(self.checkWizardImages,0,wx.ALL|wx.ALIGN_TOP,5)
        vsizer.Add(self.checkDocs,0,wx.ALL|wx.ALIGN_TOP,5)
        # vsizer.Add(self.checkScreenshot,0,wx.ALL|wx.ALIGN_TOP,5)
        vsizer.Add(wx.StaticLine(self))
        vsizer.AddStretchSpacer()
        vsizer.Add(hsizer,0,wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer()
        self.SetSizer(vsizer)
        self.SetInitialSize()
        # Event Handlers
        self.textName.Bind(wx.EVT_TEXT,self.OnCheckProjectsColorTextCtrl)
        # Dialog Icon Handlers
        self.SetIcon(installercons.get_image('off.white.dir').GetIcon())
        self.OnCheckBoxChange()

    def OnCheckProjectsColorTextCtrl(self,event):
        projectName = bolt.GPath(self.textName.GetValue())
        if projectName in self.existingProjects: #Fill this in. Compare this with the self.existingprojects list
            self.textName.SetBackgroundColour('#FF0000')
            self.textName.SetToolTip(tooltip(_('There is already a project with that name!')))
        else:
            self.textName.SetBackgroundColour('#FFFFFF')
            self.textName.SetToolTip(None)
        self.textName.Refresh()
        event.Skip()

    def OnCheckBoxChange(self):
        """ Change the Dialog Icon to represent what the project status will
        be when created. """
        if self.checkEsp.IsChecked():
            if self.checkWizard.IsChecked():
                self.SetIcon(
                    installercons.get_image('off.white.dir.wiz').GetIcon())
            else:
                self.SetIcon(
                    installercons.get_image('off.white.dir').GetIcon())
        else:
            self.SetIcon(installercons.get_image('off.grey.dir').GetIcon())

    @staticmethod
    def OnCancel(event): event.Skip()

    def OnClose(self, event):
        """ Create the New Project and add user specified extras. """
        projectName = bolt.GPath(self.textName.GetValue().strip())
        projectDir = bass.dirs['installers'].join(projectName)

        if projectDir.exists():
            balt.showError(self, _(
                'There is already a project with that name!') + '\n' + _(
                'Pick a different name for the project and try again.'))
            return
        event.Skip()

        # Create project in temp directory, so we can move it via
        # Shell commands (UAC workaround)
        tmpDir = bolt.Path.tempDir()
        tempProject = tmpDir.join(projectName)
        if self.checkEsp.IsChecked():
            fileName = 'Blank, %s.esp' % bush.game.fsName
            bosh.modInfos.create_new_mod(fileName, directory=tempProject)
        if self.checkEspMasterless.IsChecked():
            fileName = 'Blank, %s (masterless).esp' % bush.game.fsName
            bosh.modInfos.create_new_mod(fileName, directory=tempProject,
                                         masterless=True)
        if self.checkWizard.IsChecked():
            # Create empty wizard.txt
            wizardPath = tempProject.join('wizard.txt')
            with wizardPath.open('w',encoding='utf-8') as out:
                out.write('; %s BAIN Wizard Installation Script\n' % projectName)
        if self.checkWizardImages.IsChecked():
            # Create 'Wizard Images' directory
            tempProject.join('Wizard Images').makedirs()
        if self.checkDocs.IsChecked():
            #Create the 'Docs' Directory
            tempProject.join('Docs').makedirs()
        # if self.checkScreenshot.IsChecked():
        #     #Copy the dummy default 'Screenshot' into the New Project
        #     extrasDir.join(u'Screenshot').copyTo(tempProject.join(u'Screenshot'))

        # Move into the target location
        try:
            env.shellMove(tempProject, projectDir, parent=self)
            # Move successful
            BashFrame.iPanel.ShowPanel(canCancel=False, scan_data_dir=True)
        except:
            pass
        finally:
            tmpDir.rmtree(tmpDir.s)

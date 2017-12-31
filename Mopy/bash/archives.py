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
import os
import re
import subprocess

from . import bass
from .bolt import startupinfo, GPath, deprint, walkdir
from .exception import StateError

exe7z = '7z.exe' if os.name == 'nt' else '7z'
defaultExt = '.7z'
writeExts = {'.7z': '7z', '.zip': 'zip'}
readExts = {'.rar', '.7z.001', '.001'}
readExts.update(set(writeExts))
noSolidExts = {'.zip'}
reSolid = re.compile(r'[-/]ms=[^\s]+', re.IGNORECASE)
regCompressMatch = re.compile(r'Compressing\s+(.+)', re.U).match
regExtractMatch = re.compile(r'- (.+)', re.U).match
regErrMatch = re.compile('^(Error:.+|.+     Data Error?|Sub items Errors:.+)',
    re.U).match
reListArchive = re.compile(
    '(Solid|Path|Size|CRC|Attributes|Method) = (.*?)(?:\r\n|\n)')

def compress7z(command, outDir, destArchive, srcDir, progress=None):
    outFile = outDir.join(destArchive)
    if progress is not None: #--Used solely for the progress bar
        length = sum([len(files) for x, y, files in walkdir(srcDir.s)])
        progress(0, destArchive.s + '\n' + _('Compressing files...'))
        progress.setFull(1 + length)
    #--Pack the files
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1,
                            stdin=subprocess.PIPE, # needed for some commands
                            startupinfo=startupinfo)
    #--Error checking and progress feedback
    index, errorLine = 0, ''
    with proc.stdout as out:
        for line in iter(out.readline, b''):
            line = str(line, 'utf8') # utf-8 is ok see bosh.compressCommand
            if regErrMatch(line):
                errorLine = line + ''.join(out)
                break
            if progress is None: continue
            maCompressing = regCompressMatch(line)
            if maCompressing:
                progress(index, destArchive.s + '\n' + _(
                    'Compressing files...') + '\n' + maCompressing.group(
                    1).strip())
                index += 1
    returncode = proc.wait()
    if returncode or errorLine:
        outFile.temp.remove()
        raise StateError(destArchive.s + ': Compression failed:\n' +
                '7z.exe return value: ' + str(returncode) + '\n' + errorLine)
    #--Finalize the file, and cleanup
    outFile.untemp()

def extract7z(command, srcFile, progress=None, readExtensions=None):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1,
                            stdin=subprocess.PIPE, startupinfo=startupinfo)
    # Error checking, progress feedback and subArchives for recursive unpacking
    index, errorLine, subArchives = 0, '', []
    with proc.stdout as out:
        for line in iter(out.readline, b''):
            line = str(line, 'utf8')
            if regErrMatch(line):
                errorLine = line + ''.join(out)
                break
            maExtracting = regExtractMatch(line)
            if maExtracting:
                extracted = GPath(maExtracting.group(1).strip())
                if readExtensions and extracted.cext in readExtensions:
                    subArchives.append(extracted)
                if not progress: continue
                progress(index, srcFile.s + '\n' + _(
                    'Extracting files...') + '\n' + extracted.s)
                index += 1
    returncode = proc.wait()
    if returncode or errorLine:
        raise StateError(srcFile.s + ': Extraction failed:\n' +
                '7z.exe return value: ' + str(returncode) + '\n' + errorLine)
    return subArchives

def wrapPopenOut(command, wrapper, errorMsg):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=-1,
                            stdin=subprocess.PIPE, startupinfo=startupinfo)
    out, unused_err = proc.communicate()
    wrapper(out)
    returncode = proc.returncode
    if returncode:
        raise StateError(errorMsg + '\nPopen return value: %d' + returncode)

#  WIP: http://sevenzip.osdn.jp/chm/cmdline/switches/method.htm
def compressionSettings(archive, blockSize, isSolid):
    archiveType = writeExts.get(archive.cext)
    if not archiveType:
        #--Always fall back to using the defaultExt
        archive = GPath(archive.sbody + defaultExt).tail
        archiveType = writeExts.get(archive.cext)
    if archive.cext in noSolidExts: # zip
        solid = ''
    else:
        if isSolid:
            if blockSize:
                solid = '-ms=on -ms=%dm' % blockSize
            else:
                solid = '-ms=on'
        else:
            solid = '-ms=off'
    userArgs = bass.inisettings['7zExtraCompressionArguments']
    if userArgs:
        if reSolid.search(userArgs):
            if not solid: # zip, will blow if ms=XXX is passed in
                old = userArgs
                userArgs = reSolid.sub('', userArgs).strip()
                if old != userArgs: deprint(
                    archive.s + ': 7zExtraCompressionArguments ini option '
                                '"' + old + '" -> "' + userArgs + '"')
            solid = userArgs
        else:
            solid += userArgs
    return archive, archiveType, solid

def compressCommand(destArchive, destDir, srcFolder, solid='-ms=on',
                    archiveType='7z'): # WIP - note solid on by default (7z)
    return [exe7z, 'a', destDir.join(destArchive).temp.s,
            '-t%s' % archiveType] + solid.split() + [
            '-y', '-r', # quiet, recursive
            '-o"%s"' % destDir.s,
            '-scsUTF-8', '-sccUTF-8', # encode output in unicode
            srcFolder.join('*').s] # add a wildcard at the end of the path

def extractCommand(archivePath, outDirPath):
    command = '"%s" x "%s" -y -bb1 -o"%s" -scsUTF-8 -sccUTF-8' % (
        exe7z, archivePath.s, outDirPath.s)
    return command

def list_archive(archive, parse_archive_line, __reList=reListArchive):
    """Client is responsible for closing the file ! See uses for
    _parse_archive_line examples."""
    command = r'"%s" l -slt -sccUTF-8 "%s"' % (exe7z, archive.s)
    ins, err = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                startupinfo=startupinfo).communicate()
    for line in ins.splitlines(True): # keepends=True
        maList = __reList.match(line)
        if maList:
            parse_archive_line(*(maList.groups()))

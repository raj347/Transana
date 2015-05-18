# Copyright (C) 2003 - 2005 The Board of Regents of the University of Wisconsin System 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

"""This module implements the Data Export for Transana based on the Transana XML schema."""

__author__ = 'David Woods <dwoods@wcer.wisc.edu>'

import wx

import Dialogs
import DBInterface
import TransanaGlobal
import os
import sys

class XMLExport(Dialogs.GenForm):
    """ This window displays a variety of GUI Widgets. """
    def __init__(self,parent,id,title):
        Dialogs.GenForm.__init__(self, parent, id, title, (550,150), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, HelpContext='Export Database')
        # Define the minimum size for this dialog as the initial size
        self.SetSizeHints(550, 150)

        # Emport Message Layout
        lay = wx.LayoutConstraints()
        lay.top.SameAs(self.panel, wx.Top, 10)
        lay.left.SameAs(self.panel, wx.Left, 10)
        lay.right.SameAs(self.panel, wx.Right, 10)
        lay.height.AsIs()
        # If the XML filename path is not empty, we need to tell the user.
        prompt = _('Please create an Transana XML File for export.')
        exportText = wx.StaticText(self.panel, -1, prompt)
        exportText.SetConstraints(lay)

        # XML Filename Layout
        lay = wx.LayoutConstraints()
        lay.top.Below(exportText, 10)
        lay.left.SameAs(self.panel, wx.Left, 10)
        lay.width.PercentOf(self.panel, wx.Width, 80)  # 80% width
        lay.height.AsIs()
        self.XMLFile = self.new_edit_box(_("XML Filename"), lay, '')
        self.XMLFile.SetDropTarget(EditBoxFileDropTarget(self.XMLFile))

        # Browse button layout
        lay = wx.LayoutConstraints()
        lay.top.SameAs(self.XMLFile, wx.Top)
        lay.left.RightOf(self.XMLFile, 10)
        lay.right.SameAs(self.panel, wx.Right, 10)
        lay.bottom.SameAs(self.XMLFile, wx.Bottom)
        browse = wx.Button(self.panel, wx.ID_FILE1, _("Browse"), wx.DefaultPosition)
        browse.SetConstraints(lay)
        wx.EVT_BUTTON(self, wx.ID_FILE1, self.OnBrowse)

        self.Layout()
        self.SetAutoLayout(True)
        self.CenterOnScreen()

        self.XMLFile.SetFocus()

    def Export(self):
        # use the LONGEST title here!  That determines the size of the Dialog Box.
        progress = wx.ProgressDialog(_('Transana XML Export'), _('Exporting Transcript records (This may be slow because of the size of Transcript records.)'), style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

        db = DBInterface.get_db()
        if db != None:
            # Begin Database Transaction 
            dbCursor = db.cursor()
            SQLText = 'BEGIN'
            dbCursor.execute(SQLText)
            dbCursor.close()
       
        try:
            fs = self.XMLFile.GetValue()
            if fs[-4:].lower() != '.xml':
                fs = fs + '.xml'
            # On the Mac, if no path is specified, the data is exported to a file INSIDE the application bundle, 
            # where no one will be able to find it.  Let's put it in the user's HOME directory instead.
            # I'm okay with not handling this on Windows, where it will be placed in the Program's folder
            # but it CAN be found.  (There's no easy way on Windows to determine the location of "My Documents"
            # especially if the user has moved it.)
            if "__WXMAC__" in wx.PlatformInfo:
                # if the specified file has no path specification ...
                if fs.find(os.sep) == -1:
                    # ... then prepend the HOME folder
                    fs = os.getenv("HOME") + os.sep + fs
            f = file(fs, 'w')
            progress.Update(0, _('Writing Headers'))
            f.write('<?xml version="1.0"?>\n');
            f.write('<!DOCTYPE TransanaData [\n');
            f.write('  <!ELEMENT TransanaXMLVersion (#PCDATA)>\n');
            f.write('  <!ELEMENT SeriesFile (Series)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT Num (#PCDATA)>\n');
            f.write('  <!ELEMENT ID (#PCDATA)>\n');
            f.write('  <!ELEMENT Comment (#PCDATA)>\n');
            f.write('  <!ELEMENT Owner (#PCDATA)>\n');
            f.write('  <!ELEMENT DefaultKeywordGroup (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Series (#PCDATA|Num|ID|Comment|Owner|DefaultKeywordGroup)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT EpisodeFile (Episode)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT SeriesNum (#PCDATA)>\n');
            f.write('  <!ELEMENT Date (#PCDATA)>\n');
            f.write('  <!ELEMENT MediaFile (#PCDATA)>\n');
            f.write('  <!ELEMENT Length (#PCDATA)>\n');
            f.write('  <!ELEMENT Comment (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Episode (#PCDATA|Num|ID|SeriesNum|Date|MediaFile|Length|Comment)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT CoreDataFile (CoreData)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT Title (#PCDATA)>\n');
            f.write('  <!ELEMENT Creator (#PCDATA)>\n');
            f.write('  <!ELEMENT Subject (#PCDATA)>\n');
            f.write('  <!ELEMENT Description (#PCDATA)>\n');
            f.write('  <!ELEMENT Publisher (#PCDATA)>\n');
            f.write('  <!ELEMENT Contributor (#PCDATA)>\n');
            f.write('  <!ELEMENT Type (#PCDATA)>\n');
            f.write('  <!ELEMENT Format (#PCDATA)>\n');
            f.write('  <!ELEMENT Source (#PCDATA)>\n');
            f.write('  <!ELEMENT Language (#PCDATA)>\n');
            f.write('  <!ELEMENT Relation (#PCDATA)>\n');
            f.write('  <!ELEMENT Coverage (#PCDATA)>\n');
            f.write('  <!ELEMENT Rights (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT CoreData (#PCDATA|Num|ID|Title|Creator|Subject|Description|Publisher|Contributor|Date|Type|Format|Source|Language|Relation|Coverage|Rights)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT TranscriptFile (Transcript)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT EpisodeNum (#PCDATA)>\n');
            f.write('  <!ELEMENT ClipNum (#PCDATA)>\n');
            f.write('  <!ELEMENT Transcriber (#PCDATA)>\n');
            f.write('  <!ELEMENT RTFText (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Transcript (#PCDATA|Num|ID|EpisodeNum|ClipNum|Transcriber|Comment|RTFText)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT CollectionFile (Collection)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT ParentCollectNum (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Collection (#PCDATA|Num|ID|ParentCollectNum|Comment|Owner|DefaultKeywordGroup)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT ClipFile (Clip)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT CollectNum (#PCDATA)>\n');
            f.write('  <!ELEMENT TranscriptNum (#PCDATA)>\n');
            f.write('  <!ELEMENT ClipStart (#PCDATA)>\n');
            f.write('  <!ELEMENT ClipStop (#PCDATA)>\n');
            f.write('  <!ELEMENT SortOrder (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Clip (#PCDATA|Num|ID|CollectNum|TranscriptNum|ClipStart|ClipStop|Comment|SortOrder)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT KeywordFile (KeywordRec)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT KeywordGroup (#PCDATA)>\n');
            f.write('  <!ELEMENT Keyword (#PCDATA)>\n');
            f.write('  <!ELEMENT Definition (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT KeywordRec (#PCDATA|KeywordGroup|Keyword|Definition)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT ClipKeywordFile (ClipKeyword)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT Example (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT ClipKeyword (#PCDATA|EpisodeNum|ClipNum|KeywordGroup|Keyword|Example)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT NoteFile (Note)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT NoteTaker (#PCDATA)>\n');
            f.write('  <!ELEMENT NoteText (#PCDATA)>\n');
            f.write('\n');
            f.write('  <!ELEMENT Note (#PCDATA|Num|ID|SeriesNum|EpisodeNum|CollectNum|ClipNum|TranscriptNum|NoteTaker|NoteText)*>\n');
            f.write('\n');
            f.write('  <!ELEMENT Transana (#PCDATA|SeriesFile|EpisodeFile|CoreDataFile|TranscriptFile|CollectionFile|ClipFile|KeywordFile|ClipKeywordFile|NoteFile)*>\n');
            f.write(']>\n');
            f.write('\n');
            f.write('<Transana>\n');
            f.write('  <TransanaXMLVersion>\n');
            f.write('    1.0\n');
            f.write('  </TransanaXMLVersion>\n');

            progress.Update(10, _('Writing Series Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT SeriesNum, SeriesID, SeriesComment, SeriesOwner, DefaultKeywordGroup FROM Series2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <SeriesFile>\n')
                for (SeriesNum, SeriesID, SeriesComment, SeriesOwner, DefaultKeywordGroup) in dbCursor.fetchall():
                    f.write('    <Series>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % SeriesNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % SeriesID)
                    f.write('      </ID>\n')
                    if SeriesComment != '':
                        f.write('      <Comment>\n')
                        f.write('        %s\n' % SeriesComment)
                        f.write('      </Comment>\n')
                    if SeriesOwner != '':
                        f.write('      <Owner>\n')
                        f.write('        %s\n' % SeriesOwner)
                        f.write('      </Owner>\n')
                    if DefaultKeywordGroup != '':
                        f.write('      <DefaultKeywordGroup>\n')
                        f.write('        %s\n' % DefaultKeywordGroup)
                        f.write('      </DefaultKeywordGroup>\n')
                    f.write('    </Series>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </SeriesFile>\n')
                dbCursor.close()

            progress.Update(20, _('Writing Episode Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT EpisodeNum, EpisodeID, SeriesNum, TapingDate, MediaFile, EpLength, EpComment FROM Episodes2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <EpisodeFile>\n')
                for (EpisodeNum, EpisodeID, SeriesNum, TapingDate, MediaFile, EpLength, EpComment) in dbCursor.fetchall():
                    f.write('    <Episode>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % EpisodeNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % EpisodeID)
                    f.write('      </ID>\n')
                    f.write('      <SeriesNum>\n')
                    f.write('        %s\n' % SeriesNum)
                    f.write('      </SeriesNum>\n')
                    if TapingDate != None:
                        f.write('      <Date>\n')
                        f.write('        %s\n' % TapingDate)
                        f.write('      </Date>\n')
                    f.write('      <MediaFile>\n')
                    f.write('        %s\n' % MediaFile)
                    f.write('      </MediaFile>\n')
                    if EpLength != '':
                        f.write('      <Length>\n')
                        f.write('        %s\n' % EpLength)
                        f.write('      </Length>\n')
                    if EpComment != '':
                        f.write('      <Comment>\n')
                        f.write('        %s\n' % EpComment)
                        f.write('      </Comment>\n')
                    f.write('    </Episode>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </EpisodeFile>\n')
                dbCursor.close()

            progress.Update(30, _('Writing Core Data Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = """SELECT CoreDataNum, Identifier, Title, Creator, Subject, Description, Publisher,
                                    Contributor, DCDate, DCType, Format, Source, Language, Relation, Coverage, Rights
                                    FROM CoreData2"""
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <CoreDataFile>\n')
                for (CoreDataNum, Identifier, Title, Creator, Subject, Description, Publisher,
                     Contributor, DCDate, DCType, Format, Source, Language, Relation, Coverage, Rights) in dbCursor.fetchall():
                    f.write('    <CoreData>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % CoreDataNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % Identifier)
                    f.write('      </ID>\n')
                    if Title != '':
                        f.write('      <Title>\n')
                        f.write('        %s\n' % Title)
                        f.write('      </Title>\n')
                    if Creator != '':
                        f.write('      <Creator>\n')
                        f.write('        %s\n' % Creator)
                        f.write('      </Creator>\n')
                    if Subject != '':
                        f.write('      <Subject>\n')
                        f.write('        %s\n' % Subject)
                        f.write('      </Subject>\n')
                    if Description != '':
                        f.write('      <Description>\n')
                        f.write('        %s\n' % Description)
                        f.write('      </Description>\n')
                    if Publisher != '':
                        f.write('      <Publisher>\n')
                        f.write('        %s\n' % Publisher)
                        f.write('      </Publisher>\n')
                    if Contributor != '':
                        f.write('      <Contributor>\n')
                        f.write('        %s\n' % Contributor)
                        f.write('      </Contributor>\n')
                    if DCDate != None:
                        f.write('      <Date>\n')
                        f.write('        %s/%s/%s\n' % (DCDate.month, DCDate.day, DCDate.year))
                        f.write('      </Date>\n')
                    if DCType != '':
                        f.write('      <Type>\n')
                        f.write('        %s\n' % DCType)
                        f.write('      </Type>\n')
                    if Format != '':
                        f.write('      <Format>\n')
                        f.write('        %s\n' % Format)
                        f.write('      </Format>\n')
                    if Source != '':
                        f.write('      <Source>\n')
                        f.write('        %s\n' % Source)
                        f.write('      </Source>\n')
                    if Language != '':
                        f.write('      <Language>\n')
                        f.write('        %s\n' % Language)
                        f.write('      </Language>\n')
                    if Relation != '':
                        f.write('      <Relation>\n')
                        f.write('        %s\n' % Relation)
                        f.write('      </Relation>\n')
                    if Coverage != '':
                        f.write('      <Coverage>\n')
                        f.write('        %s\n' % Coverage)
                        f.write('      </Coverage>\n')
                    if Rights != '':
                        f.write('      <Rights>\n')
                        f.write('        %s\n' % Rights)
                        f.write('      </Rights>\n')
                    f.write('    </CoreData>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </CoreDataFile>\n')
                dbCursor.close()

            progress.Update(40, _('Writing Collection Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT CollectNum, CollectID, ParentCollectNum, CollectComment, CollectOwner, DefaultKeywordGroup FROM Collections2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <CollectionFile>\n')
                for (CollectNum, CollectID, ParentCollectNum, CollectComment, CollectOwner, DefaultKeywordGroup) in dbCursor.fetchall():
                    f.write('    <Collection>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % CollectNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % CollectID)
                    f.write('      </ID>\n')
                    if ParentCollectNum != '':
                        f.write('      <ParentCollectNum>\n')
                        f.write('        %s\n' % ParentCollectNum)
                        f.write('      </ParentCollectNum>\n')
                    if CollectComment != '':
                        f.write('      <Comment>\n')
                        f.write('        %s\n' % CollectComment)
                        f.write('      </Comment>\n')
                    if CollectOwner != '':
                        f.write('      <Owner>\n')
                        f.write('        %s\n' % CollectOwner)
                        f.write('      </Owner>\n')
                    if DefaultKeywordGroup != '':
                        f.write('      <DefaultKeywordGroup>\n')
                        f.write('        %s\n' % DefaultKeywordGroup)
                        f.write('      </DefaultKeywordGroup>\n')
                    f.write('    </Collection>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </CollectionFile>\n')
                dbCursor.close()

            progress.Update(50, _('Writing Clip Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT ClipNum, ClipID, CollectNum, EpisodeNum, TranscriptNum, MediaFile, ClipStart, ClipStop, ClipComment, SortOrder FROM Clips2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <ClipFile>\n')
                for (ClipNum, ClipID, CollectNum, EpisodeNum, TranscriptNum, MediaFile, ClipStart, ClipStop, ClipComment, SortOrder) in dbCursor.fetchall():
                    f.write('    <Clip>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % ClipNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % ClipID)
                    f.write('      </ID>\n')
                    if CollectNum != None:
                        f.write('      <CollectNum>\n')
                        f.write('        %s\n' % CollectNum)
                        f.write('      </CollectNum>\n')
                    if EpisodeNum != None:
                        f.write('      <EpisodeNum>\n')
                        f.write('        %s\n' % EpisodeNum)
                        f.write('      </EpisodeNum>\n')
                    if TranscriptNum != None:
                        f.write('      <TranscriptNum>\n')
                        f.write('        %s\n' % TranscriptNum)
                        f.write('      </TranscriptNum>\n')
                    f.write('      <MediaFile>\n')
                    f.write('        %s\n' % MediaFile)
                    f.write('      </MediaFile>\n')
                    f.write('      <ClipStart>\n')
                    f.write('        %s\n' % ClipStart)
                    f.write('      </ClipStart>\n')
                    f.write('      <ClipStop>\n')
                    f.write('        %s\n' % ClipStop)
                    f.write('      </ClipStop>\n')
                    if ClipComment != '':
                        f.write('      <Comment>\n')
                        f.write('        %s\n' % ClipComment)
                        f.write('      </Comment>\n')
                    if SortOrder != '':
                        f.write('      <SortOrder>\n')
                        f.write('        %s\n' % SortOrder)
                        f.write('      </SortOrder>\n')
                    f.write('    </Clip>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </ClipFile>\n')
                dbCursor.close()

            progress.Update(60, _('Writing Transcript Records  (This will seem slow because of the size of the Transcript Records.)'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT TranscriptNum, TranscriptID, EpisodeNum, ClipNum, Transcriber, Comment, RTFText FROM Transcripts2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <TranscriptFile>\n')
                for (TranscriptNum, TranscriptID, EpisodeNum, ClipNum, Transcriber, Comment, RTFText) in dbCursor.fetchall():
                    f.write('    <Transcript>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % TranscriptNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % TranscriptID)
                    f.write('      </ID>\n')
                    if EpisodeNum != '':
                        f.write('      <EpisodeNum>\n')
                        f.write('        %s\n' % EpisodeNum)
                        f.write('      </EpisodeNum>\n')
                    if ClipNum != '':
                        f.write('      <ClipNum>\n')
                        f.write('        %s\n' % ClipNum)
                        f.write('      </ClipNum>\n')
                    if Transcriber != '':
                        f.write('      <Transcriber>\n')
                        f.write('        %s\n' % Transcriber)
                        f.write('      </Transcriber>\n')
                    if Comment != '':
                        f.write('      <Comment>\n')
                        f.write('        %s\n' % Comment)
                        f.write('      </Comment>\n')
                    if RTFText != '':
                        f.write('      <RTFText>\n')

#                        f.write('        %s\n' % RTFText)
                        for line in RTFText:
                            f.write('%s' % line)

                        f.write('      </RTFText>\n')
                    f.write('    </Transcript>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </TranscriptFile>\n')
                dbCursor.close()

            progress.Update(70, _('Writing Keyword Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT KeywordGroup, Keyword, Definition FROM Keywords2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <KeywordFile>\n')
                for (KeywordGroup, Keyword, Definition) in dbCursor.fetchall():
                    f.write('    <KeywordRec>\n')
                    f.write('      <KeywordGroup>\n')
                    f.write('        %s\n' % KeywordGroup)
                    f.write('      </KeywordGroup>\n')
                    f.write('      <Keyword>\n')
                    f.write('        %s\n' % Keyword)
                    f.write('      </Keyword>\n')
                    if Definition != '':
                        f.write('      <Definition>\n')
                        f.write('        %s\n' % Definition)
                        f.write('      </Definition>\n')
                    f.write('    </KeywordRec>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </KeywordFile>\n')
                dbCursor.close()

            progress.Update(80, _('Writing Clip Keyword Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT EpisodeNum, ClipNum, KeywordGroup, Keyword, Example FROM ClipKeywords2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <ClipKeywordFile>\n')
                for (EpisodeNum, ClipNum, KeywordGroup, Keyword, Example) in dbCursor.fetchall():
                    f.write('    <ClipKeyword>\n')
                    if EpisodeNum != '':
                        f.write('      <EpisodeNum>\n')
                        f.write('        %s\n' % EpisodeNum)
                        f.write('      </EpisodeNum>\n')
                    if ClipNum != '':
                        f.write('      <ClipNum>\n')
                        f.write('        %s\n' % ClipNum)
                        f.write('      </ClipNum>\n')
                    f.write('      <KeywordGroup>\n')
                    f.write('        %s\n' % KeywordGroup)
                    f.write('      </KeywordGroup>\n')
                    f.write('      <Keyword>\n')
                    f.write('        %s\n' % Keyword)
                    f.write('      </Keyword>\n')
                    if Example != '':
                        f.write('      <Example>\n')
                        f.write('        %s\n' % Example)
                        f.write('      </Example>\n')
                    f.write('    </ClipKeyword>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </ClipKeywordFile>\n')
                dbCursor.close()

            progress.Update(90, _('Writing Note Records'))
            if db != None:
                dbCursor = db.cursor()
                SQLText = 'SELECT NoteNum, NoteID, SeriesNum, EpisodeNum, CollectNum, ClipNum, TranscriptNum, NoteTaker, NoteText FROM Notes2'
                dbCursor.execute(SQLText)
                if dbCursor.rowcount > 0:
                    f.write('  <NoteFile>\n')
                for (NoteNum, NoteID, SeriesNum, EpisodeNum, CollectNum, ClipNum, TranscriptNum, NoteTaker, NoteText) in dbCursor.fetchall():
                    f.write('    <Note>\n')
                    f.write('      <Num>\n')
                    f.write('        %s\n' % NoteNum)
                    f.write('      </Num>\n')
                    f.write('      <ID>\n')
                    f.write('        %s\n' % NoteID)
                    f.write('      </ID>\n')
                    if SeriesNum != 0:
                        f.write('      <SeriesNum>\n')
                        f.write('        %s\n' % SeriesNum)
                        f.write('      </SeriesNum>\n')
                    if EpisodeNum != 0:
                        f.write('      <EpisodeNum>\n')
                        f.write('        %s\n' % EpisodeNum)
                        f.write('      </EpisodeNum>\n')
                    if CollectNum != 0:
                        f.write('      <CollectNum>\n')
                        f.write('        %s\n' % CollectNum)
                        f.write('      </CollectNum>\n')
                    if ClipNum != 0:
                        f.write('      <ClipNum>\n')
                        f.write('        %s\n' % ClipNum)
                        f.write('      </ClipNum>\n')
                    if TranscriptNum != 0:
                        f.write('      <TranscriptNum>\n')
                        f.write('        %s\n' % TranscriptNum)
                        f.write('      </TranscriptNum>\n')
                    if NoteTaker != '':
                        f.write('      <NoteTaker>\n')
                        f.write('        %s\n' % NoteTaker)
                        f.write('      </NoteTaker>\n')
                    if NoteText != '':
                        f.write('      <NoteText>\n')
                        f.write('        %s\n' % NoteText)
                        # for line in NoteText:
                        #     f.write('%s\n' % line)
                        f.write('      </NoteText>\n')
                    f.write('    </Note>\n')
                if dbCursor.rowcount > 0:
                    f.write('  </NoteFile>\n')
                dbCursor.close()

            f.write('</Transana>\n');

            f.flush()

            dbCursor = db.cursor()
            SQLText = 'COMMIT'
            dbCursor.execute(SQLText)
            dbCursor.close()
            
        except:
            errordlg = Dialogs.ErrorDialog(self, _('An error occurred during Database Export.\n%s\n%s') % (sys.exc_info()[0], sys.exc_info()[1]))
            errordlg.ShowModal()
            errordlg.Destroy()
            dbCursor = db.cursor()
            SQLText = 'ROLLBACK'
            dbCursor.execute(SQLText)
            dbCursor.close()

        f.close()
        progress.Update(100)
        progress.Destroy()


    def OnBrowse(self, evt):
        """Invoked when the user activates the Browse button."""
        fs = wx.FileSelector(_("Select an XML file for export"),
                        TransanaGlobal.programDir,
                        "",
                        "", 
                        _("XML Files (*.xml)|*.xml|All files (*.*)|*.*"), 
                        wx.SAVE)
        # If user didn't cancel ..
        if fs != "":
            self.XMLFile.SetValue(fs)


# This simple derrived class let's the user drop files onto an edit box
class EditBoxFileDropTarget(wx.FileDropTarget):
    def __init__(self, editbox):
        wx.FileDropTarget.__init__(self)
        self.editbox = editbox
    def OnDropFiles(self, x, y, files):
        """Called when a file is dragged onto the edit box."""
        self.editbox.SetValue(files[0])

from Screens.Screen import Screen
from os.path import exists
from Plugins.Plugin import PluginDescriptor
from imports import *
try:
    from Plugins.Extensions.EGAMIFaq.imports import *
    from Plugins.Extensions.EGAMIFaq.youtubeplayer import YoutubePlayer
except:
    pass

from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN
from boxbranding import getMachineBrand
config.egamifaq = ConfigSubsection()
skins = []
for skin in os.listdir('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIFaq/skins/'):
    if os.path.isdir(os.path.join('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIFaq/skins/', skin)) and skin != 'simpleplayer':
        skins.append(skin)

config.egamifaq.skin = ConfigSelection(default='simpleplayer', choices=skins)
config.egamifaq.sp_playmode = ConfigSelection(default='forward', choices=[('forward', _('Forward')), ('backward', _('Backward')), ('random', _('Random'))])
config.egamifaq.sp_scrsaver = ConfigSelection(default='off', choices=[('on', _('On')), ('off', _('Off')), ('automatic', _('Automatic'))])
config.egamifaq.sp_on_movie_stop = ConfigSelection(default='quit', choices=[('ask', _('Ask user')), ('quit', _('Return to previous service'))])
config.egamifaq.sp_on_movie_eof = ConfigSelection(default='quit', choices=[('ask', _('Ask user')), ('quit', _('Return to previous service')), ('pause', _('Pause movie at end'))])
config.egamifaq.sp_seekbar_sensibility = ConfigInteger(default=10, limits=(1, 50))
config.egamifaq.sp_infobar_cover_off = ConfigYesNo(default=False)
config.egamifaq.sp_show_errors = ConfigYesNo(default=False)
config.egamifaq.sp_use_number_seek = ConfigYesNo(default=True)
config.egamifaq.sp_pl_number = ConfigInteger(default=1, limits=(1, 99))
config.egamifaq.sp_mi_key = ConfigSelection(default='info', choices=[('info', _('EPG/INFO')), ('displayHelp', _('HELP')), ('showMovies', _('PVR/VIDEO'))])
config.egamifaq.restorelastservice = ConfigSelection(default='1', choices=[('1', _('after SimplePlayer quits')), ('2', _('after MediaPortal quits'))])
config.egamifaq.sp_on_movie_start = ConfigSelection(default='ask', choices=[('start', _('Start from the beginning')), ('ask', _('Ask user')), ('resume', _('Resume from last position'))])
config.egamifaq.sp_save_resumecache = ConfigYesNo(default=False)
USER_Version = _('EGAMI Support Channel')
USER_siteEncoding = 'utf-8'

def EGAMIFaq_YTChannelListEntry(entry):
    return [entry, (eListboxPythonMultiContent.TYPE_TEXT,
      20,
      0,
      495,
      25,
      0,
      RT_HALIGN_CENTER | RT_VALIGN_CENTER,
      entry[1],
      16777215,
      16777215)]


def EGAMIFaq_YTChannelListEntry2(entry):
    return [entry, (eListboxPythonMultiContent.TYPE_TEXT,
      50,
      0,
      495,
      25,
      0,
      RT_HALIGN_LEFT | RT_VALIGN_CENTER,
      entry[1])]


class EGAMIFaq_YTChannel(Screen):

    def __init__(self, session):
        self.session = session
        self.plugin_path = mp_globals.pluginPath
        self.skin_path = mp_globals.pluginPath + '/skins'
        self.skin = '\n\t\t<screen name="defaultGenre" position="center,center" size="900,655" backgroundColor="#00060606" flags="wfNoBorder">\n\t\t\t<widget name="title" position="20,10" size="500,40" backgroundColor="#00101214" transparent="1" zPosition="10" font="Regular; 26" valign="center" halign="left" />\n\t\t\t<widget source="global.CurrentTime" render="Label" position="730,8" size="150,30" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular; 26" valign="center" halign="right" foregroundColor="#00dcdcdc">\n\t\t\t\t<convert type="ClockToText">Format:%-H:%M</convert>\n\t\t\t</widget>\n\t\t\t<widget source="global.CurrentTime" render="Label" position="580,39" size="300,20" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right" foregroundColor="#00dcdcdc">\n\t\t\t\t<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>\n\t\t\t</widget>\n\t\t\t<widget name="ContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center" />\n\t\t\t<widget name="genreList" position="0,135" size="900,450" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" />\n\t\t\t<widget name="name" position="20,95" size="860,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />\n\t\t\t<ePixmap pixmap="buttons/red.png" position="60,630" size="25,25" alphatest="blend" />\n\t\t\t<widget name="key_red" position="60,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />\n\t\t</screen>'
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions',
         'ShortcutActions',
         'WizardActions',
         'ColorActions',
         'SetupActions',
         'NumberActions',
         'MenuActions'], {'ok': self.keyOK,
         'cancel': self.keyCancel,
         'red': self.keyGreen}, -1)
        self['title'] = Label(USER_Version)
        self['ContentTitle'] = Label(_('Channel selection'))
        self['name'] = Label('')
        self['key_red'] = Label(_('Load'))
        mypath = resolveFilename(SCOPE_PLUGINS)
        if getMachineBrand() == 'Miraclebox':
            self.user_path = mypath + 'Extensions/EGAMIFaq/channels_3.xml'
        elif getMachineBrand() == 'Sezam':
            self.user_path = mypath + 'Extensions/EGAMIFaq/channels_2.xml'
        elif getMachineBrand() == 'UNiBOX':
            self.user_path = mypath + 'Extensions/EGAMIFaq/channels_1.xml'
        else:
            self.user_path = mypath + 'Extensions/EGAMIFaq/channels.xml'
        self.keyLocked = True
        self.genreliste = []
        self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList.l.setItemHeight(25)
        self['genreList'] = self.chooseMenuList
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.genreliste.append((0, 'With this extension you can add your favorite Youtube channels themselves.', ''))
        self.genreliste.append((0, 'For each channel, only two entries are added:', ''))
        self.genreliste.append((0, "'<name> channel name </name>' and '<user> owner name </ user>'", ''))
        self.genreliste.append((0, ' ', ''))
        self.genreliste.append((0, "With the 'Green' button the user file:", ''))
        self.genreliste.append((0, "'" + self.user_path + "' is loaded.", ''))
        if not exists(self.user_path):
            self.getUserFile(fInit=True)
        self.getUserFile()
        self.chooseMenuList.setList(map(EGAMIFaq_YTChannelListEntry, self.genreliste))

    def getUserFile(self, fInit = False):
        mypath = resolveFilename(SCOPE_PLUGINS)
        fname = mypath + 'Extensions/EGAMIFaq/channels.xml'
        print 'fname: ', fname
        try:
            if fInit:
                shutil.copyfile(fname, self.user_path)
                return
            fp = open(self.user_path)
            data = fp.read()
            fp.close()
        except IOError as e:
            print 'File Error: ', e
            self.genreliste = []
            self.genreliste.append((0, str(e), ''))
            self.chooseMenuList.setList(map(EGAMIFaq_YTChannelListEntry, self.genreliste))
        else:
            self.userData(data)

    def userData(self, data):
        list = re.findall('<name>(.*?)</name>.*?<user>(.*?)</user>', data, re.S)
        self.genreliste = []
        if list:
            i = 1
            for name, user in list:
                self.genreliste.append((i, name.strip(), '/' + user.strip()))
                i += 1

            self.genreliste.sort(key=lambda t: t[1].lower())
            self.keyLocked = False
        else:
            self.genreliste.append((0, _('No user channels found!'), ''))
        self.chooseMenuList.setList(map(EGAMIFaq_YTChannelListEntry2, self.genreliste))

    def keyGreen(self):
        self.getUserFile()

    def keyOK(self):
        if self.keyLocked:
            return
        genreID = self['genreList'].getCurrent()[0][0]
        genre = self['genreList'].getCurrent()[0][1]
        stvLink = self['genreList'].getCurrent()[0][2]
        self.session.open(EGAMIFaq_ListChannel_ListScreen, genreID, stvLink, genre)

    def keyCancel(self):
        self.close()


def EGAMIFaq_ListChannel_ListEntry(entry):
    return [entry, (eListboxPythonMultiContent.TYPE_TEXT,
      20,
      0,
      495,
      25,
      0,
      RT_HALIGN_LEFT | RT_VALIGN_CENTER,
      entry[0] + entry[1],
      16777215,
      16777215)]


class EGAMIFaq_ListChannel_ListScreen(Screen):

    def __init__(self, session, genreID, stvLink, stvGenre):
        self.session = session
        self.genreID = genreID
        self.stvLink = stvLink
        self.genreName = stvGenre
        self.plugin_path = mp_globals.pluginPath
        self.skin_path = mp_globals.pluginPath + '/skins'
        self.skin = '\n\t\t<screen name="dokuList" position="center,center" size="900,655" backgroundColor="#00060606" flags="wfNoBorder">\n\t\t\t<widget name="title" position="20,10" size="500,40" backgroundColor="#00101214" transparent="1" zPosition="10" font="Regular; 26" valign="center" halign="left" />\n\t\t\t<widget source="global.CurrentTime" render="Label" position="730,8" size="150,30" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular; 26" valign="center" halign="right" foregroundColor="#00dcdcdc">\n\t\t\t\t<convert type="ClockToText">Format:%-H:%M</convert>\n\t\t\t</widget>\n\t\t\t<widget source="global.CurrentTime" render="Label" position="580,39" size="300,20" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right" foregroundColor="#00dcdcdc">\n\t\t\t\t<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>\n\t\t\t</widget>\n\t\t\t<widget name="ContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="0" foregroundColor="#00000000" font="Regular;22" halign="center" />\n\t\t\t<widget name="liste" position="0,86" size="900,303" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" />\n\t\t\t<eLabel position="20,390" size="860,2" backgroundColor="#00555556" />\n\t\t\t<widget name="coverArt" pixmap="~/original/images/no_coverArt.png" position="20,396" size="270,200" transparent="1" alphatest="blend" borderWidth="2" borderColor="#00555556" />\n\t\t\t<widget name="name" position="300,395" size="580,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" zPosition="0" />\n\t\t\t<widget name="handlung" position="300,425" size="580,170" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" zPosition="0" />\n\t\t\t<widget name="VideoPrio" position="745,605" size="105,24" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular; 20" valign="center" halign="right" zPosition="1" />\n\t\t\t<widget name="vPrio" position="855,605" size="25,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="center" halign="center" zPosition="1" foregroundColor="#00bab329" />\n\t\t\t<widget name="Page" position="700,605" size="56,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="center" halign="right" zPosition="0" />\n\t\t\t<widget name="page" position="755,605" size="95,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="center" halign="right" zPosition="0" />\n\t\t\t<ePixmap pixmap="buttons/red.png" position="60,630" size="25,25" alphatest="blend" />\n\t\t\t<ePixmap pixmap="buttons/green.png" position="205,630" size="25,25" alphatest="blend" />\n\t\t\t<ePixmap pixmap="buttons/yellow.png" position="350,630" size="25,25" alphatest="blend" />\n\t\t\t<ePixmap pixmap="buttons/blue.png" position="492,630" size="25,25" alphatest="blend" />\n\t\t\t<widget name="key_red" position="60,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />\n\t\t\t<widget name="key_green" position="205,605" size="100,30" transparent="1" backgroundColor="#00101214" font="Regular; 20" valign="bottom" halign="center" />\n\t\t\t<widget name="key_yellow" position="350,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />\n\t\t\t<widget name="key_blue" position="492,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />\n\t\t</screen>'
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions',
         'ShortcutActions',
         'WizardActions',
         'ColorActions',
         'SetupActions',
         'NumberActions',
         'MenuActions',
         'EPGSelectActions'], {'ok': self.keyOK,
         'cancel': self.keyCancel,
         'up': self.keyUp,
         'down': self.keyDown,
         'right': self.keyRight,
         'left': self.keyLeft,
         'nextBouquet': self.keyPageUpFast,
         'prevBouquet': self.keyPageDownFast,
         'red': self.keyTxtPageUp,
         'blue': self.keyTxtPageDown,
         'yellow': self.keyYellow,
         '1': self.key_1,
         '3': self.key_3,
         '4': self.key_4,
         '6': self.key_6,
         '7': self.key_7,
         '9': self.key_9}, -1)
        self['title'] = Label(USER_Version)
        self['ContentTitle'] = Label(self.genreName)
        self['name'] = Label('')
        self['handlung'] = ScrollLabel('')
        self['page'] = Label('')
        self['key_red'] = Label('Text-')
        self['key_green'] = Label('')
        self['key_yellow'] = Label('')
        self['key_blue'] = Label('Text+')
        self['VideoPrio'] = Label('')
        self['vPrio'] = Label('')
        self['Page'] = Label('Page')
        self['coverArt'] = Pixmap()
        self.keyLocked = True
        self.baseUrl = 'http://www.youtube.com'
        self.videoPrio = 1
        self.videoPrioS = ['L', 'M', 'H']
        self.setVideoPrio()
        self.keckse = {}
        self.filmliste = []
        self.start_idx = 1
        self.max_res = 12
        self.total_res = 0
        self.pages = 0
        self.page = 0
        self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList.l.setFont(0, gFont('Regular', 20))
        self.chooseMenuList.l.setItemHeight(25)
        self['liste'] = self.chooseMenuList
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.loadPageData()

    def loadPageData(self):
        self.keyLocked = True
        print 'getPage: ', self.stvLink
        self.filmliste = []
        self.filmliste.append(('Bitte warten...', '', '', '', ''))
        self.chooseMenuList.setList(map(EGAMIFaq_ListChannel_ListEntry, self.filmliste))
        url = 'http://gdata.youtube.com/feeds/api/users' + self.stvLink + '/uploads?' + 'start-index=%d&max-results=%d&v=2' % (self.start_idx, self.max_res)
        getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type': 'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

    def genreData(self, data):
        print 'genreData:'
        print 'genre: ', self.genreID
        if not self.pages:
            m = re.search('totalResults>(.*?)</', data)
            if m:
                a = int(m.group(1))
                self.pages = a // self.max_res
                if a % self.max_res:
                    self.pages += 1
                self.page = 1
        a = 0
        l = len(data)
        self.filmliste = []
        while a < l:
            mg = re.search('<media:group>(.*?)</media:group>', data[a:], re.S)
            if mg:
                a += mg.end()
                m1 = re.search("description type='plain'>(.*?)</", mg.group(1), re.S)
                if m1:
                    desc = decodeHtml(m1.group(1))
                    desc = urllib.unquote(desc)
                else:
                    desc = "No other info's available."
                m2 = re.search("<media:player url=.*?/watch\\?v=(.*?)&amp;feature=youtube_gdata_player.*?<media:thumbnail url='(.*?)'.*?<media:title type='plain'>(.*?)</.*?<yt:duration seconds='(.*?)'", mg.group(1), re.S)
                if m2:
                    vid = m2.group(1)
                    img = m2.group(2)
                    dura = int(m2.group(4))
                    vtim = str(datetime.timedelta(seconds=dura))
                    title = decodeHtml(m2.group(3))
                    self.filmliste.append((vtim + ' ',
                     title,
                     vid,
                     img,
                     desc))
            else:
                a = l

        if len(self.filmliste) == 0:
            print 'No audio drama found!'
            self.pages = 0
            self.filmliste.append(('No other infos available. !', '', '', '', ''))
        else:
            menu_len = len(self.filmliste)
            print 'Audio dramas found: ', menu_len
        self.chooseMenuList.setList(map(EGAMIFaq_ListChannel_ListEntry, self.filmliste))
        self.keyLocked = False
        self.showInfos()

    def dataError(self, error):
        print 'dataError: ', error

    def dataErrorP(self, error):
        print 'dataError:'
        printl(error, self, 'E')
        self.ShowCoverNone()

    def showInfos(self):
        self['page'].setText('%d / %d' % (self.page, self.pages))
        stvTitle = self['liste'].getCurrent()[0][1]
        stvImage = self['liste'].getCurrent()[0][3]
        desc = self['liste'].getCurrent()[0][4]
        print 'Img: ', stvImage
        self['name'].setText(stvTitle)
        self['handlung'].setText(desc)
        if stvImage != '':
            url = stvImage
            print 'Img: ', url
            downloadPage(url, '/tmp/Icon.jpg').addCallback(self.ShowCover).addErrback(self.dataErrorP)
        else:
            self.ShowCoverNone()

    def ShowCover(self, picData):
        print 'ShowCover:'
        picPath = '/tmp/Icon.jpg'
        self.ShowCoverFile(picPath)

    def ShowCoverNone(self):
        print 'ShowCoverNone:'
        picPath = '/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/no_coverArt.png'
        self.ShowCoverFile(picPath)

    def ShowCoverFile(self, picPath):
        print 'showCoverFile:'
        if fileExists(picPath):
            print 'picpath: ', picPath
            self['coverArt'].instance.setPixmap(gPixmapPtr())
            self.scale = AVSwitch().getFramebufferScale()
            self.picload = ePicLoad()
            size = self['coverArt'].instance.size()
            self.picload.setPara((size.width(),
             size.height(),
             self.scale[0],
             self.scale[1],
             False,
             1,
             '#FF000000'))
            if self.picload.startDecode(picPath, 0, 0, False) == 0:
                ptr = self.picload.getData()
                if ptr != None:
                    self['coverArt'].instance.setPixmap(ptr)
                    self['coverArt'].show()
                    del self.picload
        return

    def youtubeErr(self, error):
        print 'youtubeErr: ', error
        self['handlung'].setText('Unfortunately, this video can not be played!\n' + str(error))

    def setVideoPrio(self):
        self.videoPrio = 1
        self['vPrio'].setText(self.videoPrioS[self.videoPrio])

    def keyLeft(self):
        if self.keyLocked:
            return
        self['liste'].pageUp()
        self.showInfos()

    def keyRight(self):
        if self.keyLocked:
            return
        self['liste'].pageDown()
        self.showInfos()

    def keyUp(self):
        if self.keyLocked:
            return
        i = self['liste'].getSelectedIndex()
        if not i:
            self.keyPageDownFast()
        self['liste'].up()
        self.showInfos()

    def keyDown(self):
        if self.keyLocked:
            return
        i = self['liste'].getSelectedIndex()
        l = len(self.filmliste) - 1
        if l == i:
            self.keyPageUpFast()
        self['liste'].down()
        self.showInfos()

    def keyTxtPageUp(self):
        self['handlung'].pageUp()

    def keyTxtPageDown(self):
        self['handlung'].pageDown()

    def keyPageUpFast(self, step = 1):
        if self.keyLocked:
            return
        oldpage = self.page
        if self.page + step <= self.pages:
            self.page += step
            self.start_idx += self.max_res * step
        else:
            self.page = 1
            self.start_idx = 1
        if oldpage != self.page:
            self.loadPageData()

    def keyPageDownFast(self, step = 1):
        if self.keyLocked:
            return
        print 'keyPageDown: '
        oldpage = self.page
        if self.page - step >= 1:
            self.page -= step
            self.start_idx -= self.max_res * step
        else:
            self.page = self.pages
            self.start_idx = self.max_res * (self.pages - 1) + 1
        if oldpage != self.page:
            self.loadPageData()

    def keyYellow(self):
        self.setVideoPrio()

    def key_1(self):
        self.keyPageDownFast(2)

    def key_4(self):
        self.keyPageDownFast(5)

    def key_7(self):
        self.keyPageDownFast(10)

    def key_3(self):
        self.keyPageUpFast(2)

    def key_6(self):
        self.keyPageUpFast(5)

    def key_9(self):
        self.keyPageUpFast(10)

    def keyOK(self):
        if self.keyLocked:
            return
        self.session.openWithCallback(self.setVideoPrio, YoutubePlayer, self.filmliste, self['liste'].getSelectedIndex(), playAll=True, listTitle=self.genreName, title_inr=1)

    def keyCancel(self):
        self.close()


def SupperChannelMain(session, close = None, **kwargs):
    session.openWithCallback(close, EGAMIFaq_YTChannel)


def SupportChannelStart(menuid, **kwargs):
    if menuid == 'information':
        return [(_('EGAMI FAQ'),
          SupperChannelMain,
          'EGAMIFaq_YTChannel',
          35,
          True)]
    else:
        return []


def Plugins(**kwargs):
    return PluginDescriptor(name=_('EGAMI FAQ'), description='EGAMI Video Tutorials', where=PluginDescriptor.WHERE_MENU, needsRestart=False, fnc=SupportChannelStart)

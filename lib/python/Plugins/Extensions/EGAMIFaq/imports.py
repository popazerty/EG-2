from enigma import gFont, addFont, eTimer, eConsoleAppContainer, ePicLoad, loadPNG, getDesktop, eServiceReference, iPlayableService, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListbox, gPixmapPtr, getPrevAsciiCode
from Plugins.Plugin import PluginDescriptor
from twisted.internet import reactor, defer
from twisted.web.client import downloadPage, getPage, error
from Components.ActionMap import NumberActionMap, ActionMap
from Components.AVSwitch import AVSwitch
from Components.Button import Button
from Components.config import config, ConfigInteger, ConfigSelection, getConfigListEntry, ConfigText, ConfigDirectory, ConfigYesNo, configfile, ConfigSelection, ConfigSubsection, ConfigPIN, NoSave, ConfigNothing
from Components.ConfigList import ConfigListScreen
from Components.FileList import FileList, FileEntryComponent
from Components.GUIComponent import GUIComponent
from Components.Label import Label
from Components.Language import language
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap, MovingPixmap
from Components.PluginList import PluginEntryComponent, PluginList
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.Boolean import Boolean
from Components.Sources.StaticText import StaticText
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBar import MoviePlayer, InfoBar
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarNotifications
from Screens.InputBox import PinInput
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN, createDir
from Tools.LoadPixmap import LoadPixmap
import re, urllib, urllib2, os, cookielib, time, socket, sha, shutil, base64, datetime, math, hashlib, random, json, md5, string, xml.etree.cElementTree, bz2
from urllib2 import Request, URLError, urlopen as urlopen2
from socket import gaierror, error
from urllib import quote, unquote_plus, unquote, urlencode
from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
from base64 import b64decode
from binascii import unhexlify
from urlparse import parse_qs
from time import *
from bz2 import BZ2File
from debuglog import printlog as printl
import mp_globals
from simpleplayer import SimplePlayer
from coverhelper import CoverHelper
from mp_globals import std_headers

def registerFont(file, name, scale, replacement):
    try:
        addFont(file, name, scale, replacement)
    except Exception as ex:
        addFont(file, name, scale, replacement, 0)


def decodeHtml(text):
    text = text.replace('&auml;', '\xc3\xa4')
    text = text.replace('\\u00e4', '\xc3\xa4')
    text = text.replace('&#228;', '\xc3\xa4')
    text = text.replace('&Auml;', '\xc3\x84')
    text = text.replace('\\u00c4', '\xc3\x84')
    text = text.replace('&#196;', '\xc3\x84')
    text = text.replace('&ouml;', '\xc3\xb6')
    text = text.replace('\\u00f6', '\xc3\xb6')
    text = text.replace('&#246;', '\xc3\xb6')
    text = text.replace('&ouml;', '\xc3\x96')
    text = text.replace('&Ouml;', '\xc3\x96')
    text = text.replace('\\u00d6', '\xc3\x96')
    text = text.replace('&#214;', '\xc3\x96')
    text = text.replace('&uuml;', '\xc3\xbc')
    text = text.replace('\\u00fc', '\xc3\xbc')
    text = text.replace('&#252;', '\xc3\xbc')
    text = text.replace('&Uuml;', '\xc3\x9c')
    text = text.replace('\\u00dc', '\xc3\x9c')
    text = text.replace('&#220;', '\xc3\x9c')
    text = text.replace('&szlig;', '\xc3\x9f')
    text = text.replace('\\u00df', '\xc3\x9f')
    text = text.replace('&#223;', '\xc3\x9f')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&gt;', '>')
    text = text.replace('&apos;', "'")
    text = text.replace('&acute;', "'")
    text = text.replace('&ndash;', '-')
    text = text.replace('&bdquo;', '"')
    text = text.replace('&rdquo;', '"')
    text = text.replace('&ldquo;', '"')
    text = text.replace('&lsquo;', "'")
    text = text.replace('&rsquo;', "'")
    text = text.replace('&#034;', "'")
    text = text.replace('&#038;', '&')
    text = text.replace('&#039;', "'")
    text = text.replace('&#39;', "'")
    text = text.replace('&#160;', ' ')
    text = text.replace('\\u00a0', ' ')
    text = text.replace('\\u00b4', "'")
    text = text.replace('&#174;', '')
    text = text.replace('&#225;', 'a')
    text = text.replace('&#233;', 'e')
    text = text.replace('&#243;', 'o')
    text = text.replace('&#8211;', '-')
    text = text.replace('\\u2013', '-')
    text = text.replace('&#8216;', "'")
    text = text.replace('&#8217;', "'")
    text = text.replace('&#8220;', "'")
    text = text.replace('&#8221;', '"')
    text = text.replace('&#8222;', ',')
    text = text.replace('\\u201e', '"')
    text = text.replace('\\u201c', '"')
    text = text.replace('\\u201d', "'")
    text = text.replace('\\u2019s', "'")
    text = text.replace('\\u00e0', '\xc3\xa0')
    text = text.replace('\\u00e7', '\xc3\xa7')
    text = text.replace('\\u00e9', '\xc3\xa9')
    text = text.replace('&#xC4;', '\xc3\x84')
    text = text.replace('&#xD6;', '\xc3\x96')
    text = text.replace('&#xDC;', '\xc3\x9c')
    text = text.replace('&#xE4;', '\xc3\xa4')
    text = text.replace('&#xF6;', '\xc3\xb6')
    text = text.replace('&#xFC;', '\xc3\xbc')
    text = text.replace('&#xDF;', '\xc3\x9f')
    text = text.replace('&#xE9;', '\xc3\xa9')
    text = text.replace('&#xB7;', '\xc2\xb7')
    text = text.replace('&#x27;', "'")
    text = text.replace('&#x26;', '&')
    text = text.replace('&#xFB;', '\xc3\xbb')
    text = text.replace('&#xF8;', '\xc3\xb8')
    text = text.replace('&#x21;', '!')
    text = text.replace('&#x3f;', '?')
    text = text.replace('&#8230;', '...')
    text = text.replace('\\u2026', '...')
    text = text.replace('&hellip;', '...')
    text = text.replace('&#8234;', '')
    return text


def iso8859_Decode(txt):
    txt = txt.replace('\xe4', '\xc3\xa4').replace('\xf6', '\xc3\xb6').replace('\xfc', '\xc3\xbc').replace('\xdf', '\xc3\x9f')
    txt = txt.replace('\xc4', '\xc3\x84').replace('\xd6', '\xc3\x96').replace('\xdc', '\xc3\x9c')
    return txt


def decodeHtml2(txt):
    txt = iso8859_Decode(txt)
    txt = decodeHtml(txt).strip()
    return txt


def stripAllTags(html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', html)
    return cleantext


def make_closing(base, **attrs):
    if not hasattr(base, '__enter__'):
        attrs['__enter__'] = lambda self: self
    if not hasattr(base, '__exit__'):
        attrs['__exit__'] = lambda self, type, value, traceback: self.close()
    return type('Closing' + base.__name__, (base, object), attrs)

import os, re, shutil
from sqlite3 import dbapi2 as sqlite

import xbmc, xbmcaddon, xbmcvfs


#
# CONSTANTS AND GLOBALS #
#
SCRIPTNAME = 'Rom Collection Browser'
SCRIPTID = 'script.games.rom.collection.browser'
CURRENT_CONFIG_VERSION = "2.1.4"
CURRENT_DB_VERSION = "2.2.0"
ISTESTRUN = False

__addon__ = xbmcaddon.Addon(id='%s' %SCRIPTID)
__language__ = __addon__.getLocalizedString


#time to wait before automatic playback starts
WAITTIME_PLAYERSTART = 500
#time that xbmc needs to close the player (before we can load the list again)
WAITTIME_PLAYERSTOP = 500
#time that xbmc needs to update controls (before we can rely on position)
WAITTIME_UPDATECONTROLS = 100
#don't call onAction if last call was not more than x ms before
WAITTIME_ONACTION = 50
#don't call onAction if last call was not more than x ms before (we need higher values on xbox)
WAITTIME_ONACTION_XBOX = 600
#use a little delay before applying filter settings
WAITTIME_APPLY_FILTERS = 500


LOG_LEVEL_ERROR = 0
LOG_LEVEL_WARNING = 1
LOG_LEVEL_INFO = 2
LOG_LEVEL_DEBUG = 3

CURRENT_LOG_LEVEL = LOG_LEVEL_INFO

MAXNUMGAMES_ENUM = [0,100,250,500,1000,2500,5000,10000]

SETTING_RCB_VIEW_MODE = 'rcb_view_mode'
SETTING_RCB_SKIN = 'rcb_skin'
SETTING_RCB_CACHINGOPTION = 'rcb_cachingOption'
SETTING_RCB_MEMDB = 'rcb_memDB'
SETTING_RCB_LOGLEVEL = 'rcb_logLevel'
SETTING_RCB_ESCAPECOMMAND = 'rcb_escapeEmulatorCommand'
SETTING_RCB_PREFERLOCALNFO = 'rcb_PreferNfoFileIfAvailable'
SETTING_RCB_ENABLEFULLREIMPORT = 'rcb_enableFullReimport'
SETTING_RCB_ALLOWOVERWRITEWITHNULLVALUES = 'rcb_overwriteWithNullvalues'
SETTING_RCB_IGNOREGAMEWITHOUTDESC = 'rcb_ignoreGamesWithoutDesc'
SETTING_RCB_SHOWENTRYALLCONSOLES = 'rcb_showEntryAllConsoles'
SETTING_RCB_SHOWENTRYALLGENRES = 'rcb_showEntryAllGenres'
SETTING_RCB_SHOWENTRYALLYEARS = 'rcb_showEntryAllYears'
SETTING_RCB_SHOWENTRYALLPUBLISHER = 'rcb_showEntryAllPublisher'
SETTING_RCB_SHOWENTRYALLCHARS = 'rcb_showEntryAllChars'
SETTING_RCB_PREVENTUNFILTEREDSEARCH = 'rcb_preventUnfilteredSearch'
SETTING_RCB_USECLEARLOGOASTITLE = 'rcb_useClearlogoAsTitle'
SETTING_RCB_LOADGAMELISTARTWORK = 'rcb_loadGamelistArtwork'
SETTING_RCB_SAVEVIEWSTATEONEXIT = 'rcb_saveViewStateOnExit'
SETTING_RCB_SAVEVIEWSTATEONLAUNCHEMU = 'rcb_saveViewStateOnLaunchEmu'
SETTING_RCB_SHOWIMPORTOPTIONSDIALOG = 'rcb_showImportOptions'
SETTING_RCB_SCRAPINGMODE = 'rcb_scrapingMode'
SETTING_RCB_SCRAPONSTART = 'rcb_scrapOnStartUP'
SETTING_RCB_LAUNCHONSTARTUP = 'rcb_launchOnStartup'
SETTING_RCB_SCRAPEONSTARTUPACTION = 'rcb_scrapeOnStartupAction'
SETTING_RCB_SHOWFAVORITESTARS = 'rcb_showFavoriteStars'
SETTING_RCB_FAVORITESSELECTED = 'rcb_favoritesSelected'
SETTING_RCB_SEARCHTEXT = 'rcb_searchText'
SETTING_RCB_IMPORTOPTIONS_DISABLEROMCOLLECTIONS = 'rcb_disableRomcollections'
SETTING_RCB_IMPORTOPTIONS_ISRESCRAPE = 'rcb_isRescrape'
SETTING_RCB_EDITSCRAPER_DESCFILEPERGAME = 'rcb_editScraper_descFilePerGame'
SETTING_RCB_NFOFOLDER = 'rcb_nfoFolder'
SETTING_RCB_PRELAUNCHDELAY = 'rcb_prelaunchDelay'
SETTING_RCB_POSTLAUNCHDELAY = 'rcb_postlaunchDelay'
SETTING_RCB_USEVBINSOLOMODE = 'rcb_useVBInSoloMode'
SETTING_RCB_SUSPENDAUDIO = 'rcb_suspendAudio'
SETTING_RCB_TOGGLESCREENMODE = 'rcb_toggleScreenMode'
SETTING_RCB_EMUAUTOCONFIGPATH = 'rcb_pathToEmuAutoConfig'
SETTING_RCB_MAXNUMGAMESTODISPLAY = 'rcb_maxNumGames'


SCRAPING_OPTION_AUTO_ACCURATE = 0
SCRAPING_OPTION_INTERACTIVE = 1

SCRAPING_OPTION_AUTO_ACCURATE_TXT = 'Automatic: Accurate'
SCRAPING_OPTION_INTERACTIVE_TXT = 'Interactive: Select Matches'

#
# DB FIELDS #
#

ROW_ID = 0
ROW_NAME = 1

RCBSETTING_lastSelectedView = 1
RCBSETTING_lastSelectedConsoleIndex = 2
RCBSETTING_lastSelectedGenreIndex = 3
RCBSETTING_lastSelectedPublisherIndex = 4
RCBSETTING_lastSelectedYearIndex = 5
RCBSETTING_lastSelectedGameIndex = 6
RCBSETTING_autoexecBackupPath = 7	# This is a deprecated setting, unused in code
RCBSETTING_dbVersion = 8
RCBSETTING_lastFocusedControlMainView = 9
RCBSETTING_lastFocusedControlGameInfoView = 10
RCBSETTING_lastSelectedCharacterIndex = 11


GAME_description = 2
GAME_gameCmd = 3
GAME_alternateGameCmd = 4
GAME_romCollectionId = 5
GAME_publisherId = 6
GAME_developerId = 7
GAME_reviewerId = 8
GAME_yearId = 9
GAME_maxPlayers = 10
GAME_rating = 11
GAME_numVotes = 12
GAME_url = 13
GAME_region = 14
GAME_media = 15
GAME_perspective = 16
GAME_controllerType = 17
GAME_isFavorite = 18
GAME_launchCount = 19
GAME_originalTitle = 20
GAME_alternateTitle = 21
GAME_translatedBy = 22
GAME_version = 23

FILE_fileTypeId = 2
FILE_parentId = 3

GENREGAME_genreId = 1
GENREGAME_gameId = 2

#
# UI #
#

VIEW_MAINVIEW = 'mainView'
VIEW_GAMEINFOVIEW = 'gameInfoView'

IMAGE_CONTROL_BACKGROUND = 'background'
IMAGE_CONTROL_GAMELIST = 'gamelist'
IMAGE_CONTROL_GAMELISTSELECTED = 'gamelistselected'
IMAGE_CONTROL_GAMEINFO_BIG = 'gameinfobig'

IMAGE_CONTROL_GAMEINFO_UPPERLEFT = 'gameinfoupperleft'
IMAGE_CONTROL_GAMEINFO_UPPERRIGHT = 'gameinfoupperright'
IMAGE_CONTROL_GAMEINFO_LOWERLEFT = 'gameinfolowerleft'
IMAGE_CONTROL_GAMEINFO_LOWERRIGHT = 'gameinfolowerright'

IMAGE_CONTROL_GAMEINFO_UPPER = 'gameinfoupper'
IMAGE_CONTROL_GAMEINFO_LOWER = 'gameinfolower'
IMAGE_CONTROL_GAMEINFO_LEFT = 'gameinfoleft'
IMAGE_CONTROL_GAMEINFO_RIGHT = 'gameinforight'

IMAGE_CONTROL_1 = 'extraImage1'
IMAGE_CONTROL_2 = 'extraImage2'
IMAGE_CONTROL_3 = 'extraImage3'
VIDEO_CONTROL_VideoWindowBig = 'videowindowbig'
VIDEO_CONTROL_VideoWindowSmall = 'videowindowsmall'
VIDEO_CONTROL_VideoFullscreen = 'videofullscreen'

IMAGE_CONTROL_CLEARLOGO = 'clearlogo'

GAMEPROPERTY_Console = 'console'


FILETYPEPARENT_GAME = 'game'
FILETYPEPARENT_PUBLISHER = 'publisher'
FILETYPEPARENT_DEVELOPER = 'developer'
FILETYPEPARENT_CONSOLE = 'console'
FILETYPEPARENT_ROMCOLLECTION = 'romcollection'
				

html_unescape_table = {
		"&amp;" : "&",
		"&quot;" : '"' ,
		"&apos;" : "'",
		"&gt;" : ">",
		"&lt;" : "<",
		"&nbsp;" : " ",
		"&#x26;" : "&",
		"&#x27;" : "\'",
		"&#xB2;" : "2",
		"&#xB3;" : "3",		
		}

def html_unescape(text):
		
		for key in html_unescape_table.keys():
			text = text.replace(key, html_unescape_table[key])
			
		return text


"""
replace html tags with kodi tags in plot
"""
html_kodi_table = {
	"<i>" : "[I]",
	"</i>" : "[/I]",
	"<b>" : "[B]",
	"</b>" : "[/B]",
	"<br>" : "[CR]",
}

def html_to_kodi(text):
	for key in html_kodi_table.keys():
		text = text.replace(key, html_kodi_table[key])

	return text



def joinPath(part1, *parts):
	path = ''
	if(part1.startswith('smb://')):
		path = part1
		for part in parts:
			path = "%s/%s" %(path, part)
	else:
		path = os.path.join(part1, *parts)
		
	return path


#
# METHODS #
#

class KodiVersions(object):
	HELIX = 14
	ISENGARD = 15
	JARVIS = 16
	KRYPTON = 17
	LEIA = 18

	@classmethod
	def getKodiVersion(self):
		version = xbmc.getInfoLabel("System.BuildVersion")[:2]
		# Alternately:
		# version = xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')
		return int(version)

def localize(id):
	try:
		return __language__(id)
	except:
		return "Sorry. No translation available for string with id: " +str(id)

def getAddonDataPath():
	
	path = u''
	path = xbmc.translatePath('special://profile/addon_data/%s' %(SCRIPTID)).decode('utf-8')
	
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			path = ''	
	return path


def getAddonInstallPath():
	
	path = u''
	path = __addon__.getAddonInfo('path').decode('utf-8')
	
	return path

def getEmuAutoConfigPath():	
	
	settings = getSettings()
	path = settings.getSetting(SETTING_RCB_EMUAUTOCONFIGPATH)
	if(path == ''):
		path = os.path.join(getAddonDataPath(), u'emu_autoconfig.xml')
		
	if(not xbmcvfs.exists(path)):
		oldPath = os.path.join(getAddonInstallPath(), 'resources', 'emu_autoconfig.xml')
		xbmcvfs.copy(oldPath, path)
		
	return path


def getTempDir():
	tempDir = os.path.join(getAddonDataPath(), 'tmp')
	
	try:
		#check if folder exists
		if(not os.path.isdir(tempDir)):
			os.mkdir(tempDir)
		return tempDir
	except Exception, (exc):
		Logutil.log('Error creating temp dir: ' +str(exc), LOG_LEVEL_ERROR)
		return None


def getConfigXmlPath():
	if(not ISTESTRUN):
		addonDataPath = getAddonDataPath()
		configFile = os.path.join(addonDataPath, "config.xml")
	else:
		configFile = os.path.join(getAddonInstallPath(), "resources", "lib", "TestDataBase", "config.xml")
	
	Logutil.log('Path to configuration file: ' +str(configFile), LOG_LEVEL_INFO)
	return configFile
	
	
def getSettings():
	settings = xbmcaddon.Addon(id='%s' %SCRIPTID)
	return settings


#HACK: XBMC does not update labels with empty strings
def setLabel(label, control):
	if(label == ''):
		label = ' '
		
	control.setLabel(str(label))


#HACK: XBMC does not update labels with empty strings
def getLabel(control):
	label = control.getLabel()
	if(label == ' '):
		label = ''
		
	return label


def getConfiguredSkin():
	skin = "Default"
	settings = getSettings()
	skin = settings.getSetting(SETTING_RCB_SKIN)
	if(skin == "Estuary"):
		skin = "Default"
		
	return skin


RCBHOME = getAddonInstallPath()

#
# Logging
#

print("RCB_INFO: Loading sqlite3 as DB engine")


class Logutil(object):
	# Class variable
	currentLogLevel = None

	levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
	prefix = ['RCB_ERROR', 'RCB_WARNING', 'RCB_INFO', 'RCB_DEBUG']

	# Note that we don't call __init__ since we use class methods, not instance methods

	@classmethod
	def __log(cls, level, message):
		# Init if not already set
		if cls.currentLogLevel is None:
			xbmc.log("RCB: initialising log level")
			cls.currentLogLevel = cls.getCurrentLogLevel()
			xbmc.log("RCB: current log level initialised to " +str(cls.currentLogLevel))

		if Logutil.getCurrentLogLevel() < level:
			return

		try:
			xbmc.log(u"{0} {1}".format(str(cls.prefix[level]), message).encode('utf-8'))
		except Exception as e:
			xbmc.log(("Warning when trying to log in RCB: {0}".format(e)))

	@classmethod
	def debug(cls, message):
		cls.__log(LOG_LEVEL_DEBUG, message)

	@classmethod
	def info(cls, message):
		cls.__log(LOG_LEVEL_INFO, message)

	@classmethod
	def warn(cls, message):
		cls.__log(LOG_LEVEL_WARNING, message)

	@classmethod
	def error(cls, message):
		cls.__log(LOG_LEVEL_ERROR, message)

	@staticmethod
	def log(message, logLevel):
		# FIXME TODO this is deprecated in favour of the above methods
		if(Logutil.currentLogLevel == None):
			xbmc.log("RCB: init log level")
			Logutil.currentLogLevel = Logutil.getCurrentLogLevel()
			xbmc.log("RCB: current log level: " +str(Logutil.currentLogLevel))
		
		if(logLevel > Logutil.currentLogLevel):			
			return
			
		prefix = u''
		if(logLevel == LOG_LEVEL_DEBUG):
			prefix = u'RCB_DEBUG: '
		elif(logLevel == LOG_LEVEL_INFO):
			prefix = u'RCB_INFO: '
		elif(logLevel == LOG_LEVEL_WARNING):
			prefix = u'RCB_WARNING: '
		elif(logLevel == LOG_LEVEL_ERROR):
			prefix = u'RCB_ERROR: '
						
		try:
			# should be save as prefix is guaranteed to be unicode
			m = prefix + message
			xbmc.log(m.encode("utf-8"))
		except Exception, (exc):
			pass
	
	@staticmethod
	def getCurrentLogLevel():
		logLevel = 1
		try:
			settings = getSettings()
			logLevelStr = settings.getSetting(SETTING_RCB_LOGLEVEL)
			if(logLevelStr == 'ERROR'):
				logLevel = LOG_LEVEL_ERROR
			elif(logLevelStr == 'WARNING'):
				logLevel = LOG_LEVEL_WARNING
			elif(logLevelStr == 'INFO'):
				logLevel = LOG_LEVEL_INFO
			elif(logLevelStr == 'DEBUG'):
				logLevel = LOG_LEVEL_DEBUG
		except:
			pass
		return logLevel

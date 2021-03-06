# -*- coding: utf-8 -*-
#############################################################
#################### START ADDON IMPORTS ####################
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import Movies
import os
import re
import sys
import time
import json
import urllib
import random
import base64
import urllib2
import urlparse
import time
import threading
import webbrowser
import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon
import base64
import xml.etree.ElementTree as ET

#############################################################
#################### SET ADDON ID ###########################
_addon_id_	= 'plugin.video.area51x'
_self_		= xbmcaddon.Addon(id=_addon_id_)
addon		= Addon(_addon_id_, sys.argv)

#SET THE DEFAULT FOLDER FOR SKIN IMAGES
_images_	= '/resources/Red/'

#SET DIALOG TO = XBMCGUI DIALOG FUNCTION
Dialog = xbmcgui.Dialog()

#GET THE CURRENT DATE IN D/M FORMAT
Date = time.strftime("%d/%m")

#GET SOME NEEDED INFORMATION FROM ADDON SETTINGS

_BASE_ = 'http://'+ _self_.getSetting('Server')
_PORT_ = _self_.getSetting('Port')
_USERNAME_ = _self_.getSetting('Username')
_PASSWORD_ = _self_.getSetting('Password')
_TMDB_KEY_ = _self_.getSetting('Tmdb')
_LIVE_CAT_ = _self_.getSetting('LIVE_CAT')
pvrsettings	= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))

if _PORT_ == '':
	server_url = _BASE_
else:
	server_url = _BASE_ + ':' + _PORT_
	


#############################################################
#################### SET ADDON THEME IMAGES #################
Skin_Path = xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_))
Icon			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_, 'Icon.png'))
FanArt			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_, 'Fanart.png'))
Background_Image	= xbmc.translatePath(os.path.join(Skin_Path, 'Background.png'))
#Vert_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'vertical.png'))
Hori_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'horizontal.png'))
Header_bg		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'header-back.png'))
Nav_bg			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'nav.png'))
Guide_img		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tv-guide.png'))
Guide_img_selected		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'tv-guide-selected.png'))
od_img		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'on-demand.png'))
od_img_selected		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'on-demand-selected.png'))
Logo_img		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'logo-settings.png'))
Focused_Button	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'nav-selected.png'))
List_bg			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg.png'))
List_bg_catz			= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-catz.png'))
List_Focused	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected.png'))
List_Focused_EPG	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected-epg.png'))
List_Focused_default	= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected-default.png'))
Test_Icon		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'ch-icon.png'))
Arrow_Image		= xbmc.translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'arrow.png'))

def openpage(self):
	if myplatform == 'android':
		opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://area-51-hosting.host' ) )
	else:
		opensite = webbrowser . open('http://area-51-hosting.host')

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

def LiveWindow():
	#CREATE AND LOAD THE MAIN ADDON WINDOWS
	window = Main('area51x')
	window.doModal()
	del window
		
def PLAY(self):	
	Link_name = CH_Title
	Link_Image  =	CH_Logo
	Link = CH_Stream
	Show_List	=	xbmcgui.ListItem(Link_name, iconImage=Link_Image,thumbnailImage=Link_Image)
	xbmc.Player().play(Link, Show_List, False)
	
def killaddon(self):

	xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
def killkodi():
    Dialog.ok("[COLOR green]Area 51 X[/COLOR]","PVR Client Updated, Kodi needs to re-launch for changes to take effect, click ok to quit kodi and then please re launch")
    os._exit(1)
def pvr(self):

	#try:
		#set = open(pvrsettings).read().replace('\n', '').replace('\r','').replace('\t','')
		#check = re.compile ('<setting id="epgUrl" value="(.*?)" \/>').findall(set)[0]
		#if len(check) <= 1:
		jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
		IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
		nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
		loginurl   = "http://iptv-area-51.tv:2095/get.php?username=" + _USERNAME_ + "&password=" + _PASSWORD_ + "&type=m3u_plus&output=ts"
		EPGurl     = "http://iptv-area-51.tv:2095/xmltv.php?username=" + _USERNAME_ + "&password=" + _PASSWORD_ + "&type=m3u_plus&output=ts"

		xbmc.executeJSONRPC(jsonSetPVR)
		xbmc.executeJSONRPC(IPTVon)
		xbmc.executeJSONRPC(nulldemo)

		sexyaddon = xbmcaddon.Addon('pvr.iptvsimple')
		Dialog.ok("[COLOR green]Area 51 X[/COLOR]","Please click ok each time it says PVR needs to restart, It will say this 4 times")
		sexyaddon.setSetting(id='m3uUrl', value=loginurl)
		sexyaddon.setSetting(id='epgUrl', value=EPGurl)
		sexyaddon.setSetting(id='m3uCache', value="false")
		sexyaddon.setSetting(id='epgCache', value="false")
		killkodi()
			
		# else:
			# Dialog.ok('[COLOR green]Area 51 X PVR[/COLOR]','[COLOR white]PVR Already Setup[/COLOR]')
		
	#except:
		#Dialog.ok('[COLOR green]Area 51 X PVR[/COLOR]','[COLOR white]PVR Import Failed, Is PVR Client Enabled?[/COLOR]')
	
def tick(self):
	
	# UPDATE THE CURRENT TIME AND UPDATE THE CURRENT DATE
	# get the current local time from the PC
	time2 = time.strftime("%I:%M %p")
	self.DATE.setLabel("Today " + str(Date))
	self.TIME.setLabel(str(time2))	
	
def Open_VOD(self):
	Movies.MoviesWindow()
	self.close()
	
def Get_Data(URL):

	# USE URLLIB2 FOR ALL WEB REQUESTS WITH THE MOZILLA USER AGENT
    req = urllib2.Request(URL)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
    response = urllib2.urlopen(req, timeout=30)
    data = response.read()
    response.close()

    return data
	
def find_single_match(text,pattern):

	# USE RE TO FIND THE PATTERN THAT IS A SINGLE MATCH TO OUR REGEX
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result
	
def find_multiple_matches(text,pattern):
    
	# USE RE TO FIND ALL PATTERNS THAT MATCH OUT REGEX
    matches = re.findall(pattern,text,re.DOTALL)

    return matches
	
def decode_base64(data):
    missing_padding = len(data) % 4

    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
        return base64.b64decode(data)
    else:
        return base64.b64decode(data)
		
def getmessage():
	try:
		url = _self_.getSetting('messageurl')
		link = Get_Data(url)
		return link
	except:
		message = 'No News To Report At The Moment'
		return message
	
def footer_update(self):

	Control_Position = 0

		
	#IF THE MAIN LIST IF FOCUSEDRUN THE FOLLOWING CODE
	if self.getFocus() == self.LIST:
		Control_Position = int(self.LIST.getSelectedPosition())
	elif self.getFocus() == self.EPG2:
		Control_Position = int(self.EPG2.getSelectedPosition())
		
	Current_Show = str(Channel_Now[Control_Position])
	Current_Desc = str(Channel_Now_Desc[Control_Position])
		
			
	if '[HD]' in str(Channel_Title[int(Control_Position)]):
		Current_Quality = 'HD'
	elif '[FHD]' in str(Channel_Title[int(Control_Position)]):
		Current_Quality = 'FHD'
	else:
		Current_Quality = 'SD'
		
			
	TMDB_SEARCH_TERM	= Current_Show.replace(' ', '+')
	
	if _TMDB_KEY_ == '':
		_TMDB_API_KEY_ = '45937b7d04244a92494fea9c5e1f145a'
		
	else:
		_TMDB_API_KEY_  = _TMDB_KEY_
		
	TMDB_REQUEST		= Get_Data('https://api.themoviedb.org/3/search/tv?api_key=' + _TMDB_API_KEY_  + '&query=' + TMDB_SEARCH_TERM)
	TMDB_REGEX			= '"results":\[{"original_name":"(.*?)","id":(.*?),"name":"(.*?)","vote_count":(.*?),"vote_average":(.*?),"poster_path":"(.*?)","first_air_date":"(.*?)","popularity":(.*?),"genre_ids":\[(.*?)\],"original_language":"(.*?)","backdrop_path":"(.*?)","overview":"(.*?)","origin_country":\[(.*?)\]}'
	TMDB_DATA			= find_single_match(TMDB_REQUEST,TMDB_REGEX)
	
	if TMDB_DATA == '':
		TMDB_POSTER		= xbmc.translatePath(os.path.join(Skin_Path, 'POSTER.jpg'))
		TMDB_COUNTRY_IMAGE	= xbmc.translatePath(os.path.join(Skin_Path, 'NA.png'))
	else:
		TMDB_COUNTRY_IMAGE	= xbmc.translatePath(os.path.join(Skin_Path, TMDB_DATA[12].replace('"', '') + '.png')) 
		TMDB_POSTER		= 'https://image.tmdb.org/t/p/w500/' + TMDB_DATA[5].replace('\/', '/')
			
	self.tmdb_country.setImage(TMDB_COUNTRY_IMAGE)	
	self.Quality.setImage(xbmc.translatePath(os.path.join(Skin_Path, Current_Quality + '.png')))		
	self.CHANNEL_LOGO_FOOTER.setImage(TMDB_POSTER)
	
def Get_Catz(self):

	global Category_Names
	global Category_Ids
	
	Category_Names = []
	Category_Ids = []

	cats_url = server_url + '/player_api.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&action=get_live_categories'
	link = Get_Data(cats_url)
	data = json.loads(link)
	for i in data:
		catname = i['category_name']
		catid = i['category_id']
		Category_Names.append(catname)
		Category_Ids.append(catid)
		self.LEFTC.addItem(catname)

def Get_Live(self, CHID):
	
	#CREATE THE SERVER URL FROM MULTIPUL PARTS AND THEN CONNECT THE SERVER URL TO CHANNELS URL ELIMENTS TO CREATE FULL URL
	
	if CHID == '':
		ID = '3'
	elif CHID == 'CAT|':
		CATZ_POS = int(self.LEFTC.getSelectedPosition())
		
		ID = Category_Ids[CATZ_POS]
	else:
		ID = CHID
		
	channels_url = server_url + '/enigma2.php?username=' + _USERNAME_ + '&password=' + _PASSWORD_ + '&type=get_live_streams&cat_id=' + ID

	# SET THE GLOBAL VERIABLES THAT WILL BE USED IN THE ADDON
	# FOR CHANNEL INFORMATION AND LIST BOXES
	global Channel_Title
	global Channel_Logo
	global Channel_Now
	global Channel_Next
	global Channel_Now_Desc
	global Channel_Next_Desc
	global Channel_Stream

	#RESET OUT LISTS BACK TOP EMPTY SHOULD SOMETHING GLITCH
	self.LIST.reset()
	self.EPG2.reset()
	#MAKE SURE OUT LIST IS STILL SET TO VISIBLE
	self.LIST.setVisible(True)
	self.EPG2.setVisible(True)
	
	# CREATE THE ARRAYS THAT WILL HOLD OUR CHANNEL INFORMATION
	# THESE SHOULD MATCH YOUR GLOBAL VERIABLES
	Channel_Title		= []
	Channel_Logo		= []
	Channel_Now			= []
	Channel_Next		= []
	Channel_Now_Desc	= []
	Channel_Next_Desc	= []
	Channel_Stream		= []
	
	#GRAB THE CHANNEL INFORMATION
	Data = Get_Data(channels_url)
	
	#CREATE AN XML TREE FROM A LOADED STRING
	tree = ET.ElementTree(ET.fromstring(Data))
	
	#GET THE ROOT TAG OF THE XML WITCH IS ITEMS
	root = tree.getroot()

	#FOR EVERY CHANNEL TAG FOUND IN XML
	for channel in root.findall('channel'):

		# GRAB THE NEEDED CHANNEL TAGES FROM XML
		if not channel.find('title').text:
			Title = 'No Channel Title Found'
		else:
			Title = str(decode_base64(channel.find('title').text))

		if not channel.find('description').text:
			Desc = 'No Channel Description Found'
		else:
			Desc = str(decode_base64(channel.find('description').text))

		if not channel.find('desc_image').text:
			Logo = 'https://findicons.com/files/icons/2772/modern_ui/76/appbar_tv.png'
		else:
			Logo = channel.find('desc_image').text

		if not channel.find('stream_url').text:
			Stream = '0'
		else:
			Stream = channel.find('stream_url').text

		if not channel.find('category_id').text:
			Category = '0'
		else:
			Category = channel.find('category_id').text

		# CHECK IF THE CHANNEL HAS A DESCRIPTION IF IT DOSE NOT USE DEFAULT INFORMATION
		Desc_Regex = '\[\d+:\d+]\s+(.*?)\s+\((.*?)\)'
		Matches = find_multiple_matches(Desc, Desc_Regex)
		i = len(Matches)

		if i > 1 and i < 3:
			Data_Channel_Now = Matches[0][0]
			Data_Channel_Next = Matches[1][0]
			Data_Channel_Now_Desc = Matches[0][1]
			Data_Channel_Next_Desc = Matches[1][1]
		elif i > 0 and i < 2:
			Data_Channel_Now = Matches[0][0]
			Data_Channel_Next = 'No EPG Information Found!'
			Data_Channel_Now_Desc = Matches[0][1]
			Data_Channel_Next_Desc = 'No Information Is Avalable For This Channel In Our EPG DataBase.'
		else:
			Data_Channel_Now = 'No EPG Information Found!'
			Data_Channel_Next = 'No EPG Information Found!'
			Data_Channel_Now_Desc = 'No Information Is Avalable For This Channel In Our EPG DataBase.'
			Data_Channel_Next_Desc = 'No Information Is Avalable For This Channel In Our EPG DataBase.'

		if not "[" in Title:
			Data_Channel_Title = Title.replace('#', '')
		else:
			Title_Regex = '(.*?) \[\d+:\d+ - \d+:\d+] \+ [0-9-+.]+ min   (.*?)$'
			Channel_Data = re.match(Title_Regex, Title.decode('utf-8') , re.M)
			Data_Channel_Title = Channel_Data.group(1)

		if ID.isdigit():
			Channel_Title.append(Data_Channel_Title)
			Channel_Now.append(Data_Channel_Now)
			Channel_Now_Desc.append(Data_Channel_Now_Desc)
			Channel_Next.append(Data_Channel_Next)
			Channel_Next_Desc.append(Data_Channel_Next_Desc)
			Channel_Stream.append(Stream)
			Channel_Logo.append(Logo)

			# ADD THE CHANNEL TITLE NOW AND NEXT TO EACH LIST BOX
			li = xbmcgui.ListItem(Data_Channel_Now, iconImage=Logo)
			self.LIST.addItem(li)
			self.EPG2.addItem(Data_Channel_Next)
			
		else:
			if ID in Data_Channel_Title:
				# ADD THE INFORMATION WE HAVE TO THE ARRAYS WE CREATED
				Replaced = Data_Channel_Title.replace(ID,'')
				Channel_Title.append(Replaced)
				Channel_Now.append(Data_Channel_Now)
				Channel_Now_Desc.append(Data_Channel_Now_Desc)
				Channel_Next.append(Data_Channel_Next)
				Channel_Next_Desc.append(Data_Channel_Next_Desc)
				Channel_Stream.append(Stream)
				Channel_Logo.append(Logo)

				# ADD THE CHANNEL TITLE NOW AND NEXT TO EACH LIST BOX
				li = xbmcgui.ListItem(Data_Channel_Now, iconImage=Logo)
				self.LIST.addItem(li)
				self.EPG2.addItem(Data_Channel_Next)
myplatform = platform()
#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

	#CLOSE THE BUSY SPINNER THAT ALL WAYS APPEARS USING PYXBMCT
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	def __init__(self, title='area51x'):
		super(Main, self).__init__(title)
		
		#SET THE STARTING LOCATION AND SIZE OF THE ADDON WINDOW
		self.setGeometry(1280, 720, 111, 52)
		
		## SET THE ADDON BACKGROUND IMAGE AND HEADER AND NAV WITH PYXBMCT.IMAGE
		Background = pyxbmct.Image(Background_Image)
		Header = pyxbmct.Image(Header_bg)
		Nav = pyxbmct.Image(Nav_bg)
		
		## PLACE THE IMAGES ON SCREEN USING (X, Y, H, W)
		self.placeControl(Background, -9, -1, 140, 56)
		self.placeControl(Header, -11, -1, 12, 56)
		self.placeControl(Nav, -1, -1, 12, 56)
		
		## SET THE INFORMATION CONTROL THAT THE ADDON USES USUALY NO INTERACTIVE ELIMENTS
		self.set_info_controls()
		
		## SET THE ACTIVE CONTROL THAT USERS CAN CLICK OR CHANGE
		self.set_active_controls()
		
		## SET THE NAVIGATION BETWEEN INTERACTIVE CONTROLS UP, DOWN, LEFT AND RIGHT
		self.set_navigation()
		
		# SET THE LOGO FOR THE ADDON THIS IS PLACED HERSO ITS ABOVE THE BACKGROUND IMAGE
		Logo = pyxbmct.Image(Logo_img)
		self.placeControl(Logo, -11, -1, 12, 15)
		
		## SET THE CONNECTION EVEN THAT CALLS FUNCTIONS WHEN ACTIVE CONTROLS ARE PRESSED
		self.connect(pyxbmct.ACTION_NAV_BACK, lambda:killaddon(self))
		self.connect(self.ONDEMAND, lambda:openpage(self))
		self.connect(self.GUIDE, lambda:pvr(self))
		self.connect(self.LIST, lambda:PLAY(self))
		self.connect(self.EPG2, lambda:PLAY(self))
		self.connect(self.LEFTC, lambda:Get_Live(self, 'CAT|'))
		
		#CALL THE FUNCTION THAT FIRST UPDATES THE TIME AND DATE
		tick(self)
		Get_Catz(self)
		Get_Live(self, '')
		#SET FOCUSE TO ONE OF THE NAV ACTIVE ELIMENTS TO ALLOW USERS WITH REMOTES TO USE THE ADDON
		self.setFocus(self.LIST)
		self.UK.setText('[B]CURRENT NEWS[/B] ::\n' +  getmessage())
		self.UK.autoScroll(2000, 2000, 2000)

	def set_info_controls(self):
		
		#SET THE PYXBMCT LABLES THAT DISPLAY TEXT ON SCREEN
		self.TIME			=	pyxbmct.Label('',textColor='0xFF006400', font='font14')
		self.DATE			=	pyxbmct.Label('',textColor='0xFF006400')
		self.EPGNEXT		=	pyxbmct.Label('Now',textColor='0xFFFFFFFF')
		self.EPGLATER		=	pyxbmct.Label('Next',textColor='0xFFFFFFFF')
		self.DESCRIPTION	=	pyxbmct.TextBox(textColor='0xFF006400')

		
		#SIMPLE PLACE TO ENTER THE CHANNELS ICON FOR DISPLAYING IN THE FOOTER
		self.CHANNEL_LOGO_FOOTER	=	pyxbmct.Image('')
		self.tmdb_country =	pyxbmct.Image('')
		self.Quality =	pyxbmct.Image('')
		

		#PLACE THE PYXBMCT LABLES THAT DISPLAY TEXT ON SCREEN USING X, Y, H, W
		self.placeControl(self.DATE,  13, 1, 12, 15)
		self.placeControl(self.TIME,  -9, 48, 12, 15)
		#self.placeControl(self.EPGNOW,  14, 7, 10,4)
		self.placeControl(self.EPGNEXT,  14, 19, 10,4)
		self.placeControl(self.EPGLATER, 14, 33, 10,4)
		self.placeControl(self.DESCRIPTION, 107, 13, 20,35)
		#PLACE THE PYXBMCT IMAGE THAT DISPLAYS THE CHANNELS LOGO IN FOOTER WITH X, Y, H, W
		self.placeControl(self.CHANNEL_LOGO_FOOTER, 102, 1, 29, 4)
		self.placeControl(self.tmdb_country, 107, 50, 5, 2)
		self.placeControl(self.Quality, 107, 48, 5, 2)


	def set_active_controls(self):
		
		##SET THE PYXBMCT BUTTONS THAT USERS INTERACT WITH
		
		self.UK			=	pyxbmct.TextBox(textColor='0xFF006400')

		##############
		############## GUIDE AND LISTS
		self.GUIDE		=	pyxbmct.Button('',	focusTexture=Guide_img_selected, noFocusTexture=Guide_img)
		self.ONDEMAND	=	pyxbmct.Button('',	focusTexture=od_img_selected, noFocusTexture=od_img)
		self.LIST		=	pyxbmct.List(buttonFocusTexture=List_Focused_default, buttonTexture=List_bg, _imageWidth=90, _imageHeight=90, _space=-1, _itemHeight=80,  _itemTextXOffset=30, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
		self.LEFTC		=	pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_bg_catz, _space=-1, _itemHeight=80,  _itemTextXOffset=5, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
		self.EPG2		=	pyxbmct.List(buttonFocusTexture=List_Focused_EPG, buttonTexture=List_bg, _space=-1, _itemHeight=80,  _itemTextXOffset=10, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
		
		#PLACE THE PYXBMCT BUTTONS THAT DISPLAY TEXT ON SCREEN USING X, Y, H, W
		self.placeControl(self.UK, -1, 0, 12, 53)
		
		############
		############ GUIDE AND LISTS
		self.placeControl(self.ONDEMAND, -11, 19, 12, 9)
		self.placeControl(self.GUIDE, -11, 12, 12, 9)
		self.placeControl(self.EPG2, 21, 31, 90, 24)
		self.placeControl(self.LEFTC, 21, 0, 90, 12)
		self.placeControl(self.LIST, 21, 12, 90, 20)
		
		##THERE IMAGES ARE PLACED HERE TO MAKE SURE THEY DISPLAY ABOVE OTHER ELIMENTS
		#Vert = pyxbmct.Image(Vert_Image)
		Hori = pyxbmct.Image(Hori_Image)
		Hori1 = pyxbmct.Image(Hori_Image)
		Hori2 = pyxbmct.Image(Hori_Image)
		Hori3 = pyxbmct.Image(Hori_Image)
		Hori4 = pyxbmct.Image(Hori_Image)
		Hori5 = pyxbmct.Image(Hori_Image)
		self.Arrow = pyxbmct.Image(Arrow_Image)
		self.Arrow1 = pyxbmct.Image(Arrow_Image)
		self.Arrow2 = pyxbmct.Image(Arrow_Image)
		
		#PLACE THE PYXBMCT IMAGES THAT DISPLAY TEXT ON SCREEN USING X, Y, H, W
		#self.placeControl(Vert, 21, 12, 90,5)
		self.placeControl(Hori, 100, 0, 5,60)
		self.placeControl(Hori1, 84, 0, 5,60)
		self.placeControl(Hori2, 69, 0, 5,60)
		self.placeControl(Hori3, 53, 0, 5,60)
		self.placeControl(Hori4, 37, 0, 5,60)
		self.placeControl(Hori5, 21, 0, 5,60)
		self.placeControl(self.Arrow, 13, 19, 10,4)
		self.placeControl(self.Arrow1, 13, 20, 10,4)
		self.placeControl(self.Arrow2, 13, 33, 10,4)
		
		#CALL FUNCTION TO GET LIVE CHANNEL LIST AND EPG INFORMATION
		#Get_Live(self, '')
		#SET THE BLUE ARROWS FOR NOW AND NEXT TO VISABLE = FALSE TO HIDE THEM ON START UP
		self.Arrow1.setVisible(False)
		self.Arrow2.setVisible(False)
		
		#SET UP THE CONTROL LISTENER FOR MOUSE AND BUTTON CLICKS TO UPDATE LISTS
		self.connectEventList(
			[pyxbmct.ACTION_MOVE_DOWN,
			pyxbmct.ACTION_MOVE_UP,
			pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
			pyxbmct.ACTION_MOUSE_WHEEL_UP,
			pyxbmct.ACTION_MOUSE_MOVE],
			self.Multi_Update)
		
	def set_navigation(self):
	
		#CREATE THE NAVIGATION CONNECTIONS FOR UP, DOWN, LEFT, RIGHT

		############
		############ GUIDE AND LISTS
		self.ONDEMAND.controlRight(self.GUIDE)
		self.ONDEMAND.controlLeft(self.GUIDE)
		self.ONDEMAND.controlDown(self.LEFTC)
		self.GUIDE.controlDown(self.LEFTC)
		self.GUIDE.controlRight(self.ONDEMAND)
		self.GUIDE.controlLeft(self.ONDEMAND)
		self.LIST.controlUp(self.ONDEMAND)
		self.LEFTC.controlUp(self.ONDEMAND)
		self.EPG2.controlUp(self.ONDEMAND)
		self.LIST.controlRight(self.EPG2)
		self.LIST.controlLeft(self.LEFTC)
		self.LEFTC.controlRight(self.LIST)
		self.EPG2.controlLeft(self.LIST)
		
		
	def Multi_Update(self):
	
		# RUN FUNCTION TO UPDATE TIME AND DATE
		tick(self)
		#UPDATE THE LIST BASSED ON SELECTION
		self.list_update()

		
	def list_update(self):
	
		#SET THE GLOBALS USED FOR MEDIA INFORMATION TO UPDATE OTHER WINDOW
		#ELIMENTS WHEN LIST IS UPDATED
		global CH_Title
		global CH_Logo
		global CH_Now
		global CH_Next
		global CH_Desc
		global CH_Stream
		global CH_Position
		
		#TRY TO DETERMIN WHAT LIST IS FOCUSED TO UPDATE ELIMENTS APPROPRIATLY
		try:
			#IF THE MAIN LIST IF FOCUSEDRUN THE FOLLOWING CODE
			if self.getFocus() == self.LIST:

				CH_Position =	self.LIST.getSelectedPosition()
				self.Arrow.setVisible(True)
				self.Arrow1.setVisible(False)
				self.Arrow2.setVisible(False)
				self.EPG2.selectItem(CH_Position)
				self.LIST.selectItem(CH_Position)
				CH_Desc =  Channel_Now_Desc[CH_Position]

			#IF THE NEX EPG LIST IS FOCUSED RUN THE FOLLOWING CODE
			elif self.getFocus() == self.EPG2:
				CH_Position =	self.EPG2.getSelectedPosition()
				self.Arrow2.setVisible(True)
				self.Arrow1.setVisible(False)
				self.Arrow.setVisible(False)

				self.LIST.selectItem(CH_Position)
				self.EPG2.selectItem(CH_Position)
				CH_Desc =  Channel_Next_Desc[CH_Position]

			# UPDATE THE FOOTER INFORMATION BASED ON SELECTIONS
			footer_update(self)

			#SET THE CHANNEL TITLE, LOGO DESCRIPTION BASSED ON THE POSITION OF LIST ONE
			CH_Position =	self.LIST.getSelectedPosition()
			CH_Title	=	Channel_Title[CH_Position].decode('utf-8') + ' : ' + Channel_Now[CH_Position].decode('utf-8')
			CH_Stream	=	Channel_Stream[CH_Position]
			CH_Logo		=	Channel_Logo[CH_Position]
			CH_Combined = '[B]' + Channel_Title[CH_Position] + '[/B] : \n' + CH_Desc
			
			self.DESCRIPTION.setText(CH_Combined)	
			
			# Set auto-scrolling for long TexBox contents
			self.DESCRIPTION.autoScroll(1000, 1000, 1000)
			
		
		except (RuntimeError, SystemError):
			pass
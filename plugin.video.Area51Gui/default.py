#############################################################
#################### START ADDON IMPORTS ####################
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import os
import re
import sys
import Live


import pyxbmct.addonwindow as pyxbmct
from addon.common.addon import Addon

#############################################################
#################### SET ADDON ID ###########################
_addon_id_	= 'plugin.video.Area51Gui'
_self_		= xbmcaddon.Addon(id=_addon_id_)
addon		= Addon(_addon_id_, sys.argv)
Dialog		= xbmcgui.Dialog()
#Live.LiveWindow()
def START():

	try:
		if not _self_.getSetting('Username') or not _self_.getSetting('Password'):
			Dialog.ok('[COLOR lime]Area51 Gui[/COLOR]','There Seems To Be Some Information Missing From Your Account Settings Please Double Check You Have Entered Everything.')
			_self_.openSettings()
		else:
			Live.LiveWindow()

	except (RuntimeError, SystemError):
		pass

START()

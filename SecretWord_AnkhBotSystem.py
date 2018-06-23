#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs, re
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "SecretWord"
Website = ""
Creator = "Yaz12321"
Version = "0.1"
Description = "Select a secret word. Once someone says it in chat: they win."

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# Version 0.1:
    # Beta release. Game functions perfectly. Reset yet to be added. Secret word continues to work after it has been guessed.

#Future fixes:
    # disable game or reset secret word once it was guessed.


class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = ""
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.BaseResponse = "{0} has guessed the secret word. The word was {1}. {0} has won {2} {3}"
            self.Payout = 30
            self.SecretWord = "SecretWord"
            
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower():
       
        #check if command is in "live only mode"
        if MySettings.OnlyLive:

            #set run permission
            startCheck = data.IsLive() and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo)
            
        else: #set run permission
            startCheck = True
        
        #check if user has permission
        if startCheck and  Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):
            
            #check if user got enough points
                
            #Parent.SendTwitchMessage("yes") 
    
            #create a word counter
            wordnum = 0
            
            #for all the words in the message:
            wordcount = data.GetParamCount()
                
            while wordnum < wordcount:
                #check if word at wordnum matches secret word
                if data.GetParam(wordnum) == MySettings.SecretWord:
                    #give user points
                    Parent.AddPoints(data.User,data.UserName,MySettings.Payout)
                    #announce winner.
                    Parent.SendTwitchMessage(MySettings.BaseResponse.format(data.UserName,MySettings.SecretWord,MySettings.Payout,Parent.GetCurrencyName()))
                    #reset secret word to null
                    MySettings.SecretWord = ""
                    wordnum = wordnum + 1
                    #no match, and 1 to wordnum and end loop:
                else:
                    #Parent.SendTwitchMessage("test")
                    wordnum = wordnum + 1
                    #Parent.SendTwitchMessage(MySettings.NotEnoughResponse.format(wordnum))

    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return

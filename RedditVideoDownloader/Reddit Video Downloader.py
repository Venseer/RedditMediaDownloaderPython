import urllib.request
import json
import os
import subprocess
import tkinter as tkinter
import sys
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from nested_lookup import nested_lookup

#TK stuff you don't need
root = tkinter.Tk()
root.overrideredirect(1)
root.withdraw()

#Parameter
if (len(sys.argv) != 2) or (sys.argv[1].count('reddit.com') == 0):
    print('Please add a valid url as a parameter')
else:
    RedditUrl = sys.argv[1]
    if (RedditUrl[-1:] != '/'):
        RedditUrl = RedditUrl + '/'
        
    requestJson = json.loads(urllib.request.urlopen(RedditUrl+'.json').read())
    if (len(nested_lookup('fallback_url',requestJson)) != 0) and (nested_lookup('fallback_url',requestJson)[0].count('v.redd.it') != 0):

        #Variable Initializer
        TestFile = asksaveasfile(mode="wb", defaultextension=".mp4")
        TestFile.close()                                                    #Close so FFMPEG can write on it
        FullFileName = TestFile.name
        DownloadPath = FullFileName[0:FullFileName.rfind('/')+1]            #+1 to keep the /
        TempVideoFile = DownloadPath+'tempDownload.mp4'
        TempAudioFile = DownloadPath+'tempDownloadAudio.mp4'

        #RunCode
        FallbackUrl = nested_lookup('fallback_url',requestJson)[0]
        FallbackAudioUrl = FallbackUrl[0:FallbackUrl.rfind('/')] + '/audio'
        hasAudio = True
        
        try:
            urllib.request.urlopen(FallbackAudioUrl).read()
            hasAudio = True
        except urllib.error.HTTPError:
            hasAudio = False

        file = open(TempVideoFile,'wb')
        file.write(urllib.request.urlopen(FallbackUrl).read())
        file.close()
        if(hasAudio):
            file = open(TempAudioFile,'wb')
            file.write(urllib.request.urlopen(FallbackAudioUrl).read())
            file.close()
            subprocess.call('ffmpeg -y -i '+TempVideoFile+' -i '+TempAudioFile+' -vcodec copy -acodec copy '+FullFileName)
        else:
            subprocess.call('ffmpeg -y -i '+TempVideoFile+' -vcodec copy -acodec copy '+FullFileName)
        
        #Delete Temporary Files
        os.remove(TempVideoFile)
        if(hasAudio):
            os.remove(TempAudioFile)
    else:
        print('This is not a Video Thread')
input()
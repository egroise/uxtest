###############################################################################
# _   _ __  __  _____           _        
#| | | |\ \/ / |_   _|___  ___ | |_  ___ 
#| | | | \  /    | | / _ \/ __|| __|/ __|
#| |_| | /  \    | ||  __/\__ \| |_ \__ \
# \___/ /_/\_\   |_| \___||___/ \__||___/  v1.1 - May 2014
#                                        
###############################################################################
# Author: Eric GROISE
# More information: https://github.com/egroise/uxtest/wiki
# Documentation: https://github.com/egroise/uxtest/wiki/Documentation
# Under MIT License: https://github.com/egroise/uxtest/blob/master/LICENSE
###############################################################################                                                      

from sikuli.Sikuli import *
import os
import shutil
import javax.swing.JOptionPane
import org.sikuli.script.FindFailed as FindFailed

Settings.MinSimilarity = 0.9
Settings.MoveMouseDelay = 0.3
Settings.ObserveScanRate = 1
Settings.WaitScanRate = 1
setFindFailedResponse(ABORT)

#------------------------------------------------------------------------------
def startTest(outputPath,options=""):
#------------------------------------------------------------------------------
# Starts the tests session.
# Must be called first, before anything else.
#   outputPath : Path where the reports will be generated
#------------------------------------------------------------------------------
    from datetime import datetime
    global _UXTST_OUTPUT_PATH_
    global _UXTST_LOG_FILE_
    global _UXTST_HTML_FILE_
    global _UXTST_XML_FILE_
    global _UXTST_ASSERT_FAIL_COUNTER_
    global _UXTST_ASSERT_COUNTER_
    global _UXTST_SCREENSHOTS_COUNTER_
    global _UXTST_START_TIME_
    global _UXTST_SESSION_
    global _UXTST_BATCH_
    global _UXTST_OPENREPORT_
    global _UXTST_SPECIALMODE_
    global _UXTST_DEBUG_

    _UXTST_VERSION_ = "1.0"
    _out("UXTEST v"+_UXTST_VERSION_)

    if getNumberScreens() > 1:
        _out("Warning: You have multiple screens! Only primary monitor will be observed.")

    if (os.getenv("UXTST_OUTPUT_PATH","") != ""):
        outputPath = os.environ["UXTST_OUTPUT_PATH"]
        _out("-- Sikuli Test Launcher mode detected")                
        _out("-- Ignoring script path and using UXTST_OUTPUT_PATH env. provided path") 
        _out("-- Enabling SPECIAL mode")  
        _UXTST_SPECIALMODE_ = True
    else:
        _UXTST_SPECIALMODE_ = False                                 
    if outputPath.find(os.sep) == -1:
         _UXTST_OUTPUT_PATH_ = os.path.join(_getDesktopPath(),outputPath)
    else:
        _UXTST_OUTPUT_PATH_ = outputPath
    _out("Report output is " + _UXTST_OUTPUT_PATH_)
    if not _UXTST_OUTPUT_PATH_.endswith(os.sep):
        _UXTST_OUTPUT_PATH_  = _UXTST_OUTPUT_PATH_  + os.sep
    
    _UXTST_ASSERT_FAIL_COUNTER_ = 0
    _UXTST_ASSERT_COUNTER_ = 0
    _UXTST_SCREENSHOTS_COUNTER_ = 1
    _UXTST_LOG_FILE_ = "test.log"
    _UXTST_HTML_FILE_ = "test.html"     
    _UXTST_XML_FILE_ = "test.xml"     
    _UXTST_START_TIME_ = datetime.now()
    _UXTST_SESSION_ = "RUNNING"
    _UXTST_BATCH_ = ("BATCHMODE" in options)
    _UXTST_OPENREPORT_ = ("SHOW_REPORT" in options)
    _UXTST_DEBUG_ = ("DEBUG" in options)
   
    if _UXTST_SPECIALMODE_:
        _UXTST_BATCH_ = True
        _UXTST_OPENREPORT_ = False           
    try:
        file = open(os.path.join(_UXTST_OUTPUT_PATH_,_UXTST_LOG_FILE_),"w")
    except IOError:        
        if _UXTST_BATCH_ or (question("Reporting folder","Given reporting folder does not exist :\n"+_UXTST_OUTPUT_PATH_+"\nDo you want to create it?")):
            os.makedirs(_UXTST_OUTPUT_PATH_)
            file = open(os.path.join(_UXTST_OUTPUT_PATH_,_UXTST_LOG_FILE_),"w")
        else:
            sys.exit()

   
    file.write(str(datetime.now())+" Starting\n")
    file.close()
    if _UXTST_DEBUG_:
        _log("DEBUG log enabled")
    _debug_in("startTest")   
    _new_html("<HTML>")
    _html("<head>")
    _html("<style type='text/css'>thead {font-weight: bold;background-color: #F0F0F0;} html {font-family: Arial;} .error {background-color: red;color: #FFFFFF;} .success {background-color: green;color: #FFFFFF;} .comment {background-color: grey;color: #FFFFFF;} TD {border-style: solid solid;border-width: 1px;border-color: #AAAAAA #EEEEEE #AAAAAA #EEEEEE ;padding-left: 3px;padding-right:15px}table {border-collapse: collapse;}thead {padding-right: 20px;}</style>")
    _html("</head>")    
    _html("<body>")   
    _html("<div style='position:absolute;top:0px;right:10px'><font color=999999><a href='https://github.com/egroise/uxtest/wiki'>UXTEST</a><sup>"+_UXTST_VERSION_+"</sup></font></div>")
    _html("<H3><font color=999999>Tests started at </font>"+str(datetime.now())+"</H3>")
    _html("<TABLE><THEAD><TR><TD>Time</TD><TD>Assertion</TD><TD>Status</TD><TD>Message</TD><TD>Waited (Max)</TD><TD>Screenshot</TD><TD>Search pattern</TD></TR></THEAD>")
    _new_xml("<TEST>")
    _xml("<StartTime>" + datetime.now().strftime("%d %m %Y %H:%M:%S") + "</StartTime>")
    
#------------------------------------------------------------------------------
def endTest():
#------------------------------------------------------------------------------
# Ends the tests session. (Reports are finalized)
# The only function you can call after 
#------------------------------------------------------------------------------
    _debug_in("endTest")
    from datetime import datetime    
    _isrunning()
    global _UXTST_SESSION_
    _UXTST_SESSION_ = "ENDED"
    if (_UXTST_ASSERT_COUNTER_ != 0):
        frate = 1.0 * _UXTST_ASSERT_FAIL_COUNTER_ / _UXTST_ASSERT_COUNTER_
        srate = 1.0 - frate
    else:
        frate = 0
        srate = 0    
    _html("</TABLE><BR/><BR/>")
    _html("<b>" + str(_UXTST_ASSERT_COUNTER_) + "</b> tests run in <b>" + _seconds(datetime.now() - _UXTST_START_TIME_) + "s</b><BR/>")
    _html("<b>" + str(_UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_) + "</b> tests succeeded ("+("%.1f" % (srate*100))+"%)<br/>")
    _html("<b>" + str(_UXTST_ASSERT_FAIL_COUNTER_) + "</b> tests failed ("+("%.1f" % (frate*100))+"%)<br/>")
    _html("<table><tr>")
    if _UXTST_ASSERT_FAIL_COUNTER_ > 0:
        _html("<td width='"+str(1* (300.0 * frate))+"' style='background:red;'>.</td>")
    if _UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_ > 0:
        _html("<td width='"+str(1* (300.0 * srate))+"' style='background:green;'>.</td></tr></table>")    
    _html("</BODY></HTML>")   
    _xml("<TestCount>" + str(_UXTST_ASSERT_COUNTER_) + "</TestCount>")
    _xml("<EndTime>" + datetime.now().strftime("%d %m %Y %H:%M:%S") + "</EndTime>")
    _xml("<TestDurationInSeconds>"+str(int_seconds(datetime.now() - _UXTST_START_TIME_)) + "</TestDurationInSeconds>")    
    _xml("<FailedTestsCount>" + str(_UXTST_ASSERT_FAIL_COUNTER_) + "</FailedTestsCount>")    
    _xml("<SuccessfulTestsCount>" + str(_UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_) + "</SuccessfulTestsCount>")    
    _xml("</TEST>")    
    if _UXTST_OPENREPORT_:
        showTestReport()
      
#------------------------------------------------------------------------------
def showTestReport():
#------------------------------------------------------------------------------
# Opens the HTML report in the defauly browser.
# Must be called after end()
#------------------------------------------------------------------------------
    _debug_in("showTestReport")    
    _isended()
    if (_isOnWindows()):
        openApp("explorer.exe " + os.path.join(_UXTST_OUTPUT_PATH_,_UXTST_HTML_FILE_))
    else:
        os.system("open /Applications/Safari.app 'file://" + os.path.join(_UXTST_OUTPUT_PATH_,_UXTST_HTML_FILE_) + "'")

def assertVisible(pattern,param1 = "_UNDEFINED_", param2 = "_UNDEFINED_"):
    return visible(pattern, param1 , param2)
    
#------------------------------------------------------------------------------
def visible(pattern, param1 = "_UNDEFINED_", param2 = "_UNDEFINED_"):
#------------------------------------------------------------------------------
# Usage : expects(pattern)
#         expects(pattern, message)
#         expects(pattern, delay)
#         expects(pattern, delay, message)
# This test is successful is given pattern is visible in the screen. 
# If no delay is provided, it will not wait at all (pattern expected at call)
# Returns True if test is successful (False otherwise)
#------------------------------------------------------------------------------
    _debug_in("visible")
    _isrunning()
    delay = 0
    message = ""
    if param1 <> "_UNDEFINED_":
        if isinstance(param1,str):
            message = param1
        else:
            delay = param1
    if param2 <> "_UNDEFINED_":
        if isinstance(param2,str):
            message = param2
        else:
            delay = param2
    _isrunning()
    from datetime import datetime
    date = datetime.now()
    try:
        wait(pattern,delay)   
        delta = datetime.now() - date
        _reportTestSuccess("visible",message,delta,delay)
        return True
    except FindFailed:
        delta =datetime.now() - date    
        _reportTestFailure("visible",message,delta,delay) 
        _out(os.path.join(_UXTST_OUTPUT_PATH_,"visible Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        _out(_picfind(pattern))
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        return False  

def assertNotVisible(pattern, message = ""):
    return notVisible(pattern,message)

#------------------------------------------------------------------------------
def notVisible(pattern, message = ""):
#------------------------------------------------------------------------------
# This test is successful if the given pattern is not visible in the screen.
# Returns True if test is successful (False otherwise)
#------------------------------------------------------------------------------
    _debug_in("notVisible")
    _isrunning()
    if (not exists(pattern)):
        _reportTestSuccess("notVisible",message)
        return True
    else:
        _reportTestFailure("notVisible",message)
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        return False

#------------------------------------------------------------------------------
def assertFail(message):
#------------------------------------------------------------------------------
    _debug_in("assertFail")
    _reportTestFailure("(custom)",message) 

#------------------------------------------------------------------------------
def assertSucceeded(message):
#------------------------------------------------------------------------------
    _debug_in("assertSucceeded")
    _reportTestSuccess("(custom)",message) 

###############################################################################   
# UTILITIES FUNCTIONS
###############################################################################   

#------------------------------------------------------------------------------
def newClick(*args):
#------------------------------------------------------------------------------
# Same as the native click() function but supporting timeout. Default timeout is 1s.    
    _debug_in("newClick")
    nargs = len(args)
    if isinstance(args[nargs-1],int):
        timeout = args[nargs-1]
        nargs = nargs -1
    else:
        timeout = 1   
    for i in range(nargs):
        pattern = args[i]
        if exists(pattern,timeout):
            click(pattern)
        else:
            _reportTestFailure("newClick","Click failed after "+str(timeout)+"s") 
            shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

#------------------------------------------------------------------------------
def wClick(pattern,timeout = 1):
#------------------------------------------------------------------------------
    _debug_in("wClick")
    waitingClick(pattern,timeout)
    
#------------------------------------------------------------------------------
def waitingClick(pattern,timeout = 1):
#------------------------------------------------------------------------------
# Same as the native click() function but supporting timeout. Default timeout is 1s.
    _debug_in("waitingClick")
    if exists(pattern,timeout):
        click(pattern)
    else:
        _reportTestFailure("waitingClick","Click failed after "+str(timeout)+"s") 
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

#------------------------------------------------------------------------------
def wDoubleClick(pattern,timeout = 1):
#------------------------------------------------------------------------------
    _debug_in("wDoubleClick")
    waitingDoubleclick(pattern,timeout)
        
#------------------------------------------------------------------------------
def waitingDoubleClick(pattern,timeout = 1):
#------------------------------------------------------------------------------
# Same as the native click() function but supporting timeout. Default timeout is 1s.
    _debug_in("waitingDoubleClick")
    if exists(pattern,timeout):
        doubleClick(pattern)
    else:
        _reportTestFailure("waitingDoubleClick","Double click failed after "+str(timeout)+"s") 
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

#------------------------------------------------------------------------------
def oClick(pattern):
#------------------------------------------------------------------------------
   _debug_in("oClick")
   optionalClick(pattern)
    
#------------------------------------------------------------------------------
def optionalClick(pattern):    
#------------------------------------------------------------------------------
    _debug_in("optionalClick")
    if (pattern == False):
        return
    if exists(pattern,1):
        click(pattern)

#------------------------------------------------------------------------------
def oDoubleClick(pattern):
#------------------------------------------------------------------------------
    _debug_in("oDoubleClick")
    optionalDoubleClick(pattern)
    
#------------------------------------------------------------------------------
def optionalDoubleClick(pattern):
#------------------------------------------------------------------------------
    _debug_in("optionalDoubleClick")
    if (pattern == False):
        return
    if exists(pattern,1):
        doubleClick(pattern)   
            
#------------------------------------------------------------------------------
def takeScreenshot(name = "__NOT DEFINED___"):
#------------------------------------------------------------------------------
    _debug_in("takeScreenshot")
    from datetime import datetime
    global _UXTST_SCREENSHOTS_COUNTER_    
    if (name == "__NOT DEFINED___"):
        name = "Screenshot " + str(_UXTST_SCREENSHOTS_COUNTER_)
        _UXTST_SCREENSHOTS_COUNTER_ = _UXTST_SCREENSHOTS_COUNTER_ + 1
    sleep(1)
    _screenshot(name)
    _tr("",None,name,"",name)
    
#------------------------------------------------------------------------------
def findFirstFromLeft(pattern):
#------------------------------------------------------------------------------
    _debug_in("findFirstFromLeft")
    try:
        fs = findAll(pattern)
        sorted_fs = sorted(fs, key=lambda m:m.x)
        return sorted_fs[0]
    except FindFailed:
        return False

#------------------------------------------------------------------------------
def question(title,question): 
#------------------------------------------------------------------------------
    _debug_in("question")
    if _UXTST_BATCH_:
        _log("BATCHMODE enabled->question skipped and responsed True ("+question+")")
        return True
    response = javax.swing.JOptionPane.showConfirmDialog(None, question,"UX Tests: " + title, javax.swing.JOptionPane.YES_NO_OPTION,javax.swing.JOptionPane.QUESTION_MESSAGE)
    if response == 0:
        return True
    else:
        return False

#------------------------------------------------------------------------------
def alert(title,message):
#------------------------------------------------------------------------------
    _debug_in("alert")
    if _UXTST_BATCH_:
        return
    response = javax.swing.JOptionPane.showMessageDialog(None, question,"UX Tests: " + title, javax.swing.JOptionPane.YES_NO_OPTION,javax.swing.JOptionPane.ERROR_MESSAGE)

#------------------------------------------------------------------------------
def observeWholeScreen():
#------------------------------------------------------------------------------
    _debug_in("observeWholeScreen")
    morphTo(Screen())
    
#------------------------------------------------------------------------------
def restrictObservationTo(pattern):
#------------------------------------------------------------------------------
    _debug_in("restrictObservationTo")
    restrictScan(pattern)
    
#------------------------------------------------------------------------------
def restrictScanToWindowContaining(pattern):
#------------------------------------------------------------------------------
    _debug_in("restrictScanToWindowContaining")
    click(pattern)
    restrictScanToFocusedWindow()

#------------------------------------------------------------------------------
def restrictScanToFocusedWindow():
#------------------------------------------------------------------------------
    _debug_in("restrictScanToFocusedWindow")
    reg = App.focusedWindow()
    morphTo(reg)
    
#------------------------------------------------------------------------------
def openApplication(command):
#------------------------------------------------------------------------------
    _debug_in("openApplication")
    if command.find(os.path) == -1:
        command = os.path.join(_getDesktopPath,command)
    openApp(command)

#------------------------------------------------------------------------------
def AppLaunched():
#------------------------------------------------------------------------------
    _debug_in("AppLaunched")
    if (os.getenv("UXTST_APP_STARTED","") != ""):
        if os.environ["UXTST_APP_STARTED"] == "YES":
            return True;
    return False;

#------------------------------------------------------------------------------
def commentTest(comment):
#------------------------------------------------------------------------------
    _debug_in("commentTest")
    _isrunning()    
    _reportComment(comment)

###############################################################################   
# INTERNAL FUNCTIONS 
# (PLEASE DO NOT USE, they can change at any time)
###############################################################################        
   
def _screenshot(name):
    name = name.replace("<","-").replace(">","-").replace(":","-").replace("|","-").replace("*","-").replace("\"","-").replace("/","-").replace("\\","-")
    from java.awt import Toolkit,Robot,Rectangle
    from javax.imageio import ImageIO
    from java.io import File  
    screenRect = Rectangle(Toolkit.getDefaultToolkit().getScreenSize())
    capture = Robot().createScreenCapture(screenRect)
    ImageIO.write(capture, "png", File(_UXTST_OUTPUT_PATH_ + name+".png"))
                        
def _error(message):
    popup("Sorry, but you made a mistake using UXTST !\n\n" + message);

def _new_html(text):
    file = open(_UXTST_OUTPUT_PATH_ + _UXTST_HTML_FILE_,"w")
    file.write(text + "\n")
    file.close()
    
def _html(text):
    file = open(_UXTST_OUTPUT_PATH_ + _UXTST_HTML_FILE_,"a")
    file.write(text + "\n")
    file.close()

def _new_xml(text):
    file = open(_UXTST_OUTPUT_PATH_ + _UXTST_XML_FILE_,"w")
    file.write(text + "\n")
    file.close()   
    
def _xml(text):
    file = open(_UXTST_OUTPUT_PATH_ + _UXTST_XML_FILE_,"a")
    file.write(text + "\n")
    file.close()    
    
def _log(text):
    from datetime import datetime
    _out(text)
    file = open(_UXTST_OUTPUT_PATH_ + _UXTST_LOG_FILE_,"a")
    file.write(str(datetime.now())+" "+ text + "\n")
    file.close()

def _debug(text):
    if _UXTST_DEBUG_:
        _log("[DEBUG] " + text)

def _debug_in(function):
    _debug("in> " + function)

def _tr(assertion,status,message,waited,screenshot="",pattern="",isComment=False):
    from datetime import datetime
    if isComment:
        comment = " class='comment'"
    else:
        comment = ""
    if status == True:
        s = "<TD class='success'>Success</TD>";
    elif status == False:
        s = "<TD class='error'>Failure "+str(_UXTST_ASSERT_FAIL_COUNTER_)+"</TD>"
    else:
        s = "<TD></TD>"
    if assertion == "(custom)":
        _html("<TR" + comment + "><TD>" + str(datetime.now()) + "</TD><TD>" + assertion + "</TD>" + s +"<TD>"+ message + "</TD><TD>"+waited+"</TD><TD>"+_htmlimg(screenshot)+"</TD><TD></TD></TR>")
    else:
        _html("<TR" + comment + "><TD>" + str(datetime.now()) + "</TD><TD>" + assertion + "</TD>" + s +"<TD>"+ message + "</TD><TD>"+waited+"</TD><TD>"+_htmlimg(screenshot)+"</TD><TD>"+_htmlimg(pattern)+"</TD></TR>")
  
def _reportComment(comment):
    _log("# " + comment)
    _tr("",None,comment,"","","",True)
    
def _reportTestSuccess(origin,text,wait=0,delay=0):
    from datetime import datetime,timedelta
    global _UXTST_ASSERT_COUNTER_
    if wait == 0:
        wait = timedelta()
    if (delay == 0):
        delaystr = ""
    else:
        delaystr = " (&lt;"+str(delay)+"s)"
    _UXTST_ASSERT_COUNTER_ =_UXTST_ASSERT_COUNTER_ +1
    _log(origin + " succeeded: " + text)
    _tr(origin,True,text,_seconds(wait)+"s"+delaystr)

def _reportTestFailure(origin, text,wait=0,delay=0):
    from datetime import datetime,timedelta
    global _UXTST_ASSERT_FAIL_COUNTER_
    global _UXTST_ASSERT_COUNTER_
    if wait == 0:
        wait = timedelta()    
    if (delay == 0):
        delaystr = ""
    else:
        delaystr = " (&gt;"+str(delay)+"s)"
    _UXTST_ASSERT_FAIL_COUNTER_ =_UXTST_ASSERT_FAIL_COUNTER_ +1   
    _UXTST_ASSERT_COUNTER_ =_UXTST_ASSERT_COUNTER_ +1   
    _screenshot("Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_))
    _log("FAIL " + str(_UXTST_ASSERT_FAIL_COUNTER_)+", " + origin + " failed:" + text)
    _tr(origin,False,text,_seconds(wait)+"s"+delaystr,"Fail "+ str(_UXTST_ASSERT_FAIL_COUNTER_),"Fail "+ str(_UXTST_ASSERT_FAIL_COUNTER_) +" pattern")

def _htmlimg(name):
    if name != "":
        return "<A HREF='"+name+".png'><IMG src='"+name+".png' height='40' border=0></A>"
    else:
        return ""

def _seconds(date):
    s = date.seconds + date.days * 3600.0 * 24 + int(date.microseconds/100000)/10.0
    return str(s) 

def _now():
    return str(datetime.now())

def int_seconds(date):
    return date.seconds + date.days * 3600 * 24 + int(date.microseconds/10000)

def _picfind(pic):
    if isinstance(pic, str) :
        f = pic
    else:        
        f = pic.getFilename() 
    for p in getImagePath():
        pf = os.path.join(p,f) 
        if os.path.exists(pf):
            return pf

def _isrunning():
    initdone = False
    if '_UXTST_SESSION_' in globals():
      global _UXTST_SESSION_
      if _UXTST_SESSION_ == "RUNNING":
        initdone = True
    if not initdone:
      _error("You must call uxtst.start() before calling uxtst.end() !")
      sys.exit()
   
def _isended():
    enddone = False
    if '_UXTST_SESSION_' in globals():
      global _UXTST_SESSION_
      if _UXTST_SESSION_ == "ENDED":
        enddone = True
    if not enddone:
      _error("You must call uxtst.end() before calling showTestReport() !")
      sys.exit()

def _out(txt):
    print "[UXTST] " + txt

def _isOnWindows():
    return os.sep == "\\"

def _getDesktopPath():
    return os.path.join(os.path.expanduser("~"),'Desktop')
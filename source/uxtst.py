###############################################################################
# _   _ __  __  _____           _        
#| | | |\ \/ / |_   _|___  ___ | |_  ___ 
#| | | | \  /    | | / _ \/ __|| __|/ __|
#| |_| | /  \    | ||  __/\__ \| |_ \__ \
# \___/ /_/\_\   |_| \___||___/ \__||___/  v0.9 - December 2014
#                                        
###############################################################################
# Author : Eric GROISE
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

    if (os.getenv("UXTST_OUTPUT_PATH","") != ""):
        outputPath = os.environ["UXTST_OUTPUT_PATH"]
        _out("-- Sikuli Test Launcher mode detected")                
        _out("-- Ignoring script path and using UXTST_OUTPUT_PATH env. provided path") 
        _out("-- Enabling SPECIAL mode")  
        _UXTST_SPECIALMODE_ = True
    else:
        _UXTST_SPECIALMODE_ = False
                                
    if outputPath.find('\\') == -1:
         _UXTST_OUTPUT_PATH_ = os.environ["USERPROFILE"]+"\\Desktop\\"+outputPath
    else:
        _UXTST_OUTPUT_PATH_ = outputPath
    if not _UXTST_OUTPUT_PATH_.endswith("\\"):
        _UXTST_OUTPUT_PATH_ = _UXTST_OUTPUT_PATH_ + "\\"
    _out("Report output is " + _UXTST_OUTPUT_PATH_)

    MXUX_VERSION = "0.9"
    _UXTST_ASSERT_FAIL_COUNTER_ = 0
    _UXTST_ASSERT_COUNTER_ = 0
    _UXTST_SCREENSHOTS_COUNTER_ = 1
    _UXTST_LOG_FILE_ = "uitest.log"
    _UXTST_HTML_FILE_ = "uitest.html"     
    _UXTST_XML_FILE_ = "uitest.xml"     
    _UXTST_START_TIME_ = datetime.now()
    _UXTST_SESSION_ = "RUNNING"
    _UXTST_BATCH_ = ("BATCHMODE" in options)
    _UXTST_OPENREPORT_ = ("SHOW_REPORT" in options)

    if _UXTST_SPECIALMODE_:
        _UXTST_BATCH_ = True
        _UXTST_OPENREPORT_ = False
                
    try:
        file = open(_UXTST_OUTPUT_PATH_ + _UXTST_LOG_FILE_,"w")
    except IOError:        
        if _UXTST_BATCH_ or (question("Reporting folder","Given reporting folder does not exist :\n"+_UXTST_OUTPUT_PATH_+"\nDo you want to create it?")):
            os.makedirs(_UXTST_OUTPUT_PATH_)
            file = open(_UXTST_OUTPUT_PATH_ + _UXTST_LOG_FILE_,"w")
        else:
            sys.exit()
    file.write(str(datetime.now())+" Starting\n")
    file.close()
    _new_html("<HTML>")
    _html("<head>")
    _html("<style type='text/css'>thead {font-weight: bold;background-color: #F0F0F0;} html {font-family: Arial;}.error {background-color: #FFE6E7;color: #FF0000;}TD {border-style: solid solid;border-width: 1px;border-color: #AAAAAA #EEEEEE #AAAAAA #EEEEEE ;padding-left: 3px;padding-right:15px}table {border-collapse: collapse;}thead {padding-right: 20px;}</style>")
    _html("</head>")    
    _html("<body>")    
    _html("<H2><font color=999999 size=-1>MxUX "+MXUX_VERSION+" tests started at </font>"+str(datetime.now())+"</H2>")
    _html("<TABLE><THEAD><TR><TD>Time</TD><TD>Status</TD><TD>Message</TD><TD>Delay</TD><TD>Screenshot</TD><TD>Pattern</TD></TR></THEAD>")
    _new_xml("<UITEST>")
    _xml("<StartTime>" + datetime.now().strftime("%d %m %Y %H:%M:%S") + "</StartTime>")
    
#------------------------------------------------------------------------------
def endTest():
# Ends the tests session. (Reports are finalized)
# The only function you can call after 
#------------------------------------------------------------------------------
    from datetime import datetime    
    _isrunning()
    global _UXTST_SESSION_
    _UXTST_SESSION_ = "ENDED"
    _html("</TABLE><BR/><BR/>")
    _html("<b>" + str(_UXTST_ASSERT_COUNTER_) + "</b> tests run in <b>" + _seconds(datetime.now() - _UXTST_START_TIME_) + "s</b><BR/>")
    _xml("<TestCount>" + str(_UXTST_ASSERT_COUNTER_) + "</TestCount>")
    _xml("<EndTime>" + datetime.now().strftime("%d %m %Y %H:%M:%S") + "</EndTime>")
    _xml("<TestDurationInSeconds>"+str(int_seconds(datetime.now() - _UXTST_START_TIME_)) + "</TestDurationInSeconds>")    
    if (_UXTST_ASSERT_COUNTER_ != 0):
        frate = 1.0 * _UXTST_ASSERT_FAIL_COUNTER_ / _UXTST_ASSERT_COUNTER_
        srate = 1.0 - frate
    else:
        frate = 0
        srate = 0
    _html("<b>" + str(_UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_) + "</b> tests succeeded ("+("%.1f" % (srate*100))+"%)<br/>")
    _html("<b>" + str(_UXTST_ASSERT_FAIL_COUNTER_) + "</b> tests failed ("+("%.1f" % (frate*100))+"%)<br/>")
    _xml("<FailedTestsCount>" + str(_UXTST_ASSERT_FAIL_COUNTER_) + "</FailedTestsCount>")    
    _xml("<SuccessfulTestsCount>" + str(_UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_) + "</SuccessfulTestsCount>")    
    _html("<table><tr>")
    _xml("</UITEST>")    
    if _UXTST_ASSERT_FAIL_COUNTER_ > 0:
        _html("<td width='"+str(1* (300.0 * frate))+"' style='background:red;'>.</td>")
    if _UXTST_ASSERT_COUNTER_-_UXTST_ASSERT_FAIL_COUNTER_ > 0:
        _html("<td width='"+str(1* (300.0 * srate))+"' style='background:green;'>.</td></tr></table>")    
    _html("</BODY></HTML>")
    if _UXTST_OPENREPORT_:
        showReport()
      
#------------------------------------------------------------------------------
def showTestReport():
# Opens the HTML report in the defauly browser.
# Must be called after end()
#------------------------------------------------------------------------------
    _isended()
    openApp("explorer.exe " + os.path.join(_UXTST_OUTPUT_PATH_,_UXTST_HTML_FILE_))

def isVisible(pattern,param1 = "_UNDEFINED_", param2 = "_UNDEFINED_"):
    return visible(pattern, param1 , param2)
    
#------------------------------------------------------------------------------
def visible(pattern, param1 = "_UNDEFINED_", param2 = "_UNDEFINED_"):
# Usage : expects(pattern)
#         expects(pattern, message)
#         expects(pattern, delay, message)
# This test is successful is given pattern is visible in the screen. 
# If no delay is provided, it will not wait at all (pattern expected at call)
# Returns True if test is successful (False otherwise)
#------------------------------------------------------------------------------
    _isrunning()
    delay = 0
    message = "(undefined)"
    if param1 <> "_UNDEFINED_":
        if isinstance(param1,str):
            message = param1
        else:
            delay = param1
    if param2 <> "_UNDEFINED_":
        message = param2;
    _isrunning()
    from datetime import datetime
    date = datetime.now()
    try:
        wait(pattern,delay)   
        delay = datetime.now() - date
        _logOK(message,delay)
        return True
    except FindFailed:
        delay =datetime.now() - date    
        _logKO(message,delay) 
        _out(os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        _out(_picfind(pattern))
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        return False  

   
#------------------------------------------------------------------------------
def notVisible(pattern, name = "(undefined)"):
# This test is successful if the given pattern is not visible in the screen.
# Returns True if test is successful (False otherwise)
#------------------------------------------------------------------------------
    _isrunning()
    if (not exists(pattern)):
        _logOK(name)
        return True
    else:
        _logKO(name + " found when it should not")
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))
        return False

###############################################################################   
# UTILITIES FUNCTIONS
###############################################################################   

def newClick(*args):
    # Same as the native click() function but supporting timeout. Default timeout is 1s.    
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
            _logKO("Click failed after "+str(timeout)+"s") 
            shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

def wClick(pattern,timeout = 1):
    waitingClick(pattern,timeout)
    
def waitingClick(pattern,timeout = 1):
# Same as the native click() function but supporting timeout. Default timeout is 1s.
    if exists(pattern,timeout):
        click(pattern)
    else:
        _logKO("Click failed after "+str(timeout)+"s") 
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

def wDoubleClick(pattern,timeout = 1):
    waitingDoubleclick(pattern,timeout)
        
def waitingDoubleClick(pattern,timeout = 1):
# Same as the native click() function but supporting timeout. Default timeout is 1s.
    if exists(pattern,timeout):
        doubleClick(pattern)
    else:
        _logKO("Double click failed after "+str(timeout)+"s") 
        shutil.copy(_picfind(pattern),os.path.join(_UXTST_OUTPUT_PATH_,"Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_) + " pattern.png"))

def oClick(pattern):
    optionalClick(pattern)
    
def optionalClick(pattern):    
    if (pattern == False):
        return
    if exists(pattern,1):
        click(pattern)

def oDoubleClick(pattern):
    optionalDoubleClick(pattern)
    
def optionalDoubleClick(pattern):
    if (pattern == False):
        return
    if exists(pattern,1):
        doubleClick(pattern)   
            
def takeScreenshot(name = "__NOT DEFINED___"):
    global _UXTST_SCREENSHOTS_COUNTER_    
    if (name == "__NOT DEFINED___"):
        name = "Screenshot " + str(_UXTST_SCREENSHOTS_COUNTER_)
        _UXTST_SCREENSHOTS_COUNTER_ = _UXTST_SCREENSHOTS_COUNTER_ + 1
    sleep(1)
    _screenshot(name)
    _html("<tr><td></td><td></td><td>"+name+"</td><td></td><td>"+_htmlimg(name)+"</td><td></td></tr>")
    
def findFirstFromLeft(pattern):
    try:
        fs = findAll(text)
        sorted_fs = sorted(fs, key=lambda m:m.x)
        return sorted_fs[0]
    except FindFailed:
        return False

def question(title,question): 
    response = javax.swing.JOptionPane.showConfirmDialog(None, question,"WWUX Tests: " + title, javax.swing.JOptionPane.YES_NO_OPTION,javax.swing.JOptionPane.QUESTION_MESSAGE)
    if response == 0:
        return True
    else:
        return False

def alert(title,message):
    response = javax.swing.JOptionPane.showMessageDialog(None, question,"UX Tests: " + title, javax.swing.JOptionPane.YES_NO_OPTION,javax.swing.JOptionPane.ERROR_MESSAGE)

def observeWholeScreen():
    scanWholeScreen()
    
def scanWholeScreen():
    morphTo(Screen())

def restrictObservationTo(pattern):
    restrictScan(pattern)
    
def restrictScan(pattern):
    click(pattern)
    reg = App.focusedWindow()
    morphTo(reg)

def restrictScanToFocusedWindow():
    reg = App.focusedWindow()
    morphTo(reg)
    
def openApplication(command):
    if command.find('\\') == -1:
        command = os.environ["USERPROFILE"]+"\\Desktop\\"+command
    #popup("Sorry, but you made a mistake using MXUX !\n\n" + message);        
    openApp(command)

def AppLaunched():
    if (os.getenv("UXTST_APP_STARTED","") != ""):
        if os.environ["UXTST_APP_STARTED"] == "YES":
            return True;
    return False;
###############################################################################   
# INTERNAL FUNCTIONS (DO NOT USE)
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
    popup("Sorry, but you made a mistake using MXUX !\n\n" + message);

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

def _logOK(text,delay=0):
    from datetime import datetime,timedelta
    global _UXTST_ASSERT_COUNTER_
    if delay == 0:
        delay = timedelta()
    _UXTST_ASSERT_COUNTER_ =_UXTST_ASSERT_COUNTER_ +1
    _log("------ok: " + text)
    _html("<TR><TD>"+str(datetime.now())+"</TD><TD>Success</TD><TD>"+ text + "</TD><TD>"+_seconds(delay)+"</TD><TD></TD><TD></TD></TR>")

def _logKO(text,delay=0):
    from datetime import datetime,timedelta
    global _UXTST_ASSERT_FAIL_COUNTER_
    global _UXTST_ASSERT_COUNTER_
    if delay == 0:
        delay = timedelta()    
    _UXTST_ASSERT_FAIL_COUNTER_ =_UXTST_ASSERT_FAIL_COUNTER_ +1   
    _UXTST_ASSERT_COUNTER_ =_UXTST_ASSERT_COUNTER_ +1   
    _screenshot("Fail " + str(_UXTST_ASSERT_FAIL_COUNTER_))
    _log("*FAIL " + str(_UXTST_ASSERT_FAIL_COUNTER_)+"*: " + text)
    _html("<TR><TD>"+str(datetime.now())+"</TD><TD class='error'>Failure "+str(_UXTST_ASSERT_FAIL_COUNTER_)+"</TD><TD>"+ text + "</TD><TD>"+_seconds(delay)+"</TD><TD>" + _htmlimg("Fail "+ str(_UXTST_ASSERT_FAIL_COUNTER_))+"</TD>"+"<TD>"+_htmlimg("Fail "+ str(_UXTST_ASSERT_FAIL_COUNTER_) +" pattern")+"</TD></TR>")             

def _htmlimg(name):
    return "<A HREF='"+name+".png'><IMG src='"+name+".png' height='40' border=0></A>"

def _seconds(date):
    s = date.seconds + date.days * 3600.0 * 24 + int(date.microseconds/100000)/10.0
    return str(s) 

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
      _error("You must call uxtst.end() before calling showReport() !")
      sys.exit()

def _out(txt):
    print "UXTST>" + txt

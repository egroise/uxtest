# uxtst library 

sys.path.append("../../..")

import uxtst
reload(uxtst) 
from uxtst import *

startTest("uxtest Selftest")

commentTest("Selftesting takeScreenshot")
takeScreenshot()
takeScreenshot("Named screenshot")

commentTest("Selftesting assertions (3 sucess, 3 failures)")
visible("present.png","Should succeed",2)
visible("not present.png","Should fail",2)
notVisible("present.png","Should fail")
notVisible("not present.png","Should succeed")
reportTestFail("Report custom assertion fail")
reportTestSucceeded("Report custom assertion success")

commentTest("Selftesting clicks (3 fails)")
newClick("present.png",2)
hover(Screen())
type(Key.ESC)
newClick("not present.png",2)
waitingClick("present.png",2)
hover(Screen())
type(Key.ESC)
waitingClick("not present.png",2)
waitingDoubleClick("present.png",2)
hover(Screen())
type(Key.ESC)
waitingDoubleClick("not present.png",2)

commentTest("Selftesting utilities")
found = findFirstFromLeft("present.png")
restrictScanToWindowContaining("present.png")
restrictScanToFocusedWindow()
observeWholeScreen()
AppLaunched()

endTest()
showTestReport()

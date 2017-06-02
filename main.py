## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin User Import -----------------------------------------------------------

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPCP350')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
TLP3 = UIDevice('TouchPanelC')
## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
'''PANEL - ROOM Master ......................................................'''
'''PANEL - ROOM A ...........................................................'''
## Index
A_BtnIndex   = Button(TLP1, 1)
A_LblIndex   = Label(TLP1, 2)
## PIN
A_BtnPin0    = Button(TLP1, 1000)
A_BtnPin1    = Button(TLP1, 1001)
A_BtnPin2    = Button(TLP1, 1002)
A_BtnPin3    = Button(TLP1, 1003)
A_BtnPin4    = Button(TLP1, 1004)
A_BtnPin5    = Button(TLP1, 1005)
A_BtnPin6    = Button(TLP1, 1006)
A_BtnPin7    = Button(TLP1, 1007)
A_BtnPin8    = Button(TLP1, 1008)
A_BtnPin9    = Button(TLP1, 1009)
A_BtnPinD    = Button(TLP1, 1010, repeatTime = 0.1)
A_BtnPinX    = Button(TLP1, 1011)
A_LblPIN     = Label(TLP1, 1012)

## Main
A_BtnVideo   = Button(TLP1, 11)
A_BtnAudio   = Button(TLP1, 12)
A_BtnBlinds  = Button(TLP1, 13)
A_BtnLights  = Button(TLP1, 14)
A_BtnStatus  = Button(TLP1, 15)
A_BtnPwrOff  = Button(TLP1, 16) 
A_LblMaster  = Label(TLP1, 300)
A_LblRoom    = Label(TLP1, 301)
## Video
A_BtnVHDMI   = Button(TLP1, 21)
A_BtnVShare  = Button(TLP1, 22)
A_BtnVPwrOn  = Button(TLP1, 23)
A_BtnVPwrOff = Button(TLP1, 24)
A_BtnUp      = Button(TLP1, 25)
A_BtnStop    = Button(TLP1, 26)
A_BtnDown    = Button(TLP1, 27)
## Audio
A_BtnVolLess = Button(TLP1, 31, repeatTime = 0.1)
A_BtnVolPlus = Button(TLP1, 32, repeatTime = 0.1)
A_BtnMute    = Button(TLP1, 33)
A_LvlRoom    = Level(TLP1, 34)
## Persianas
A_BtnBUp     = Button(TLP1, 41)
A_BtnBStop   = Button(TLP1, 42)
A_BtnBDown   = Button(TLP1, 43)
## Luces
A_BtnLightOn = Button(TLP1, 51)
A_BtnLightOf = Button(TLP1, 52)
## Status
A_Btn232LCD1 = Button(TLP1, 61)
A_Btn232LCD2 = Button(TLP1, 62)
A_Btn232DXP  = Button(TLP1, 63)
A_Btn232Bimp = Button(TLP1, 64)
A_Btn232PTZ  = Button(TLP1, 65)
A_Btn232Cisc = Button(TLP1, 66)
A_BtnLANSMP  = Button(TLP1, 67)
A_BtnLANVadd = Button(TLP1, 68)
## PowerOff
A_BtnPwrAll  = Button(TLP1, 101, holdTime = 3)
A_LblPwrAll  = Label(TLP1, 102)
'''PANEL - ROOM B ...........................................................'''
'''PANEL - ROOM C ...........................................................'''
'''PANEL - Group Buttons ..................................................--'''
#--
PageIndex   = [A_BtnIndex]
#--
PagePIN     = [A_BtnPin0, A_BtnPin1, A_BtnPin2, A_BtnPin3, A_BtnPin4, A_BtnPin5,
             A_BtnPin6, A_BtnPin7, A_BtnPin8, A_BtnPin9, A_BtnPinD, A_BtnPinX]
#--
PageMain    = [A_BtnVideo, A_BtnAudio, A_BtnBlinds, A_BtnLights, A_BtnStatus, A_BtnPwrOff]
GroupMainA  = MESet([A_BtnVideo, A_BtnAudio, A_BtnBlinds, A_BtnLights, A_BtnStatus, A_BtnPwrOff])
#--
PageVideo   = [A_BtnVHDMI, A_BtnVShare, A_BtnVPwrOn, A_BtnVPwrOff, A_BtnUp, A_BtnStop, A_BtnDown]
GroupVideoA = MESet([A_BtnUp, A_BtnStop, A_BtnDown])
#--
PageAudio   = [A_BtnVolLess, A_BtnVolPlus, A_BtnMute]
#--
PageBlinds  = [A_BtnBUp, A_BtnBStop, A_BtnBDown]
GroupBlindsA = MESet(PageBlinds)
#--
PageLights = [A_BtnLightOn, A_BtnLightOf]
GroupLightsA = MESet(PageLights)
#--
PagePowerAll = [A_BtnPwrAll]
#--
#--
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------
def Initialize():
    #Index Variables
    global PIN_A
    global PIN_A_Secret
    global PIN_A_GUI
    #--
    PIN_A = []
    PIN_A_GUI = []
    PIN_A_Secret = '1414'
    #--
    A_LblIndex.SetText('Panel - Sala A')
    A_LblRoom.SetText('Panel A')
    A_LblPIN.SetText('')
    #--
    TLP1.ShowPage('Index')
    TLP1.HideAllPopups()
    GroupMainA.SetCurrent(None)
    pass

## Event Definitions -----------------------------------------------------------
## Index -----------------------------------------------------------------------
@event(PageIndex, ButtonEventList)
def IndexEvents(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnIndex and state == 'Pressed':            
            PIN_A = []
            PIN_A_GUI = []
            A_LblPIN.SetText('')
            TLP1.ShowPopup('PIN')
            print("Touch A: Index Pressed")
    pass

## PIN -------------------------------------------------------------------------
def PINValidationA(Number, Option): #This validate the PIN Security Panel
    global PIN_A, PIN_A_GUI
    #--
    if Number != None:                          #If user send a number
        Number = str(Number[3])                 #Extract the number of btn name
        if len(PIN_A) >= 0 and len(PIN_A) <= 3: #Ej= '1234'
            #--
            PIN_A.append(Number)        #Append the last number to internal list
            PIN_A_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(PIN_A)     #Convert the list to cleaned string data
            Clean2 = "".join(PIN_A_GUI) #Convert the list to cleaned string data
            A_LblPIN.SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == PIN_A_Secret: #If User enter the secret PIN:
                    TLP1.HideAllPopups()  #Panel actions:
                    TLP1.ShowPage('Main')
                    TLP1.ShowPopup('x_Welcome')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    PIN_A = []           #Erase each items in list [0-9]
                    PIN_A_GUI = []       #Erase each items in list [****]
                    A_LblPIN.SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        A_LblPIN.SetText('')
    #--
    if Option == 'PINDelete':           #If the user pulse Delete Button
        if len(PIN_A) > 0:              #If the list have data
            PIN_A.pop()                 #Delete the last number of the list
            PIN_A_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(PIN_A)     #Convert the list to cleaned string data
            Clean2 = "".join(PIN_A_GUI) #Convert the list to cleaned string data
            A_LblPIN.SetText(Clean2)    #Send the final '*' string to Panel
        else:
            print('Empty List')         #Notify to console
    #--
    if Option == 'PINExit':             #If the user pulse Exit Button
        TLP1.HidePopup('PIN')           #Show the Index Page
    pass

@event(PagePIN, ButtonEventList)
def PINEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if state == 'Pressed':
            button.SetState(1)
            #--
            if button.Name == 'PINDelete':         #PIN Delete Button
                PINValidationA(None, button.Name)  #Recall a validation function
            elif button.Name == 'PINExit':         #PIN Exit Button
                PINValidationA(None, button.Name)  #Recall a validation function
            else:                                  #PIN 0-9 Button
                PINValidationA(button.Name, None)  #Recall a validation function
        else:
            button.SetState(0)
    #--
    pass

## Main ------------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def PageMain(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnVideo and state == 'Pressed':
            A_LblMaster.SetText('Control de Video')
            TLP1.ShowPopup('Video')
            GroupMainA.SetCurrent(A_BtnVideo)
            print('Touch A: %s' % ('Video'))
        #--
        elif button is A_BtnAudio and state == 'Pressed':
            A_LblMaster.SetText('Control de Audio')
            TLP1.ShowPopup('Audio')
            GroupMainA.SetCurrent(A_BtnAudio)
            print('Touch A: %s' % ('Audio'))
        #--
        elif button is A_BtnBlinds and state == 'Pressed':
            A_LblMaster.SetText('Control de Persianas')
            TLP1.ShowPopup('Persianas')
            GroupMainA.SetCurrent(A_BtnBlinds)
            print('Touch A: %s' % ('Persianas'))
        #--
        elif button is A_BtnLights and state == 'Pressed':
            A_LblMaster.SetText('Control de Luces')
            TLP1.ShowPopup('Luces')
            GroupMainA.SetCurrent(A_BtnLights)
            print('Touch A: %s' % ('Luces'))
        #--
        elif button is A_BtnStatus and state == 'Pressed':
            A_LblMaster.SetText('Información de Dispositivos')
            TLP1.ShowPopup('Status')
            GroupMainA.SetCurrent(A_BtnStatus)
            print('Touch A: %s' % ('Status'))
        #--
        elif button is A_BtnPwrOff and state == 'Pressed':
            A_LblMaster.SetText('Apagado de Sala')
            TLP1.ShowPopup('x_PowerOff')
            GroupMainA.SetCurrent(A_BtnPwrOff)
            print('Touch A: %s' % ('PowerOff'))
    pass
## Video -----------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def PageVideo(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnVHDMI and state == 'Pressed':
            print('Touch A: %s' % ('HDMI'))
        elif button is A_BtnVShare and state == 'Pressed':
            print('Touch A: %s' % ('ShareLink'))
        elif button is A_BtnVPwrOn and state == 'Pressed':
            print('Touch A: %s' % ('PowerOn'))
        elif button is A_BtnVPwrOff and state == 'Pressed':
            print('Touch A: %s' % ('PowerOff'))
        elif button is A_BtnUp and state == 'Pressed':
            GroupVideoA.SetCurrent(A_BtnUp)
            print('Touch A: %s' % ('Screen Up'))
        elif button is A_BtnStop and state == 'Pressed':
            GroupVideoA.SetCurrent(A_BtnStop)
            print('Touch A: %s' % ('Screen Stop'))
        elif button is A_BtnDown and state == 'Pressed':
            GroupVideoA.SetCurrent(A_BtnDown)
            print('Touch A: %s' % ('Screen Down'))
    pass
## Audio -----------------------------------------------------------------------
@event(PageAudio, ButtonEventList)
def PageAudio(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnVolLess and state == 'Pressed':
            A_BtnVolLess.SetState(1)
            print('Touch A: %s' % ('Audio -'))
        elif button is A_BtnVolLess and state == 'Repeated':
            A_BtnVolLess.SetState(1)
            print('Touch A: %s' % ('Audio -'))        
        else:
            A_BtnVolLess.SetState(0)
        #--
        if button is A_BtnVolPlus and state == 'Pressed':
            A_BtnVolPlus.SetState(1)
            print('Touch A: %s' % ('Audio +'))
        if button is A_BtnVolPlus and state == 'Repeated':
            A_BtnVolPlus.SetState(1)
            print('Touch A: %s' % ('Audio +'))
        else:
            A_BtnVolPlus.SetState(0)
        #--
        if button is A_BtnMute and state == 'Pressed':
            print('Touch A: %s' % ('Audio Mute'))
    pass
## Persianas -------------------------------------------------------------------
@event(PageBlinds, ButtonEventList)
def PageBlinds(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnBUp and state == 'Pressed':
            GroupBlindsA.SetCurrent(A_BtnBUp)
            print('Touch A: %s' % ('Persianas Up'))
        elif button is A_BtnBStop and state == 'Pressed':
            GroupBlindsA.SetCurrent(A_BtnBStop)
            print('Touch A: %s' % ('Persianas Stop'))
        elif button is A_BtnBDown and state == 'Pressed':
            GroupBlindsA.SetCurrent(A_BtnBDown)
            print('Touch A: %s' % ('Persianas Down'))
    pass
## Lights ----------------------------------------------------------------------
@event(PageLights, ButtonEventList)
def PageLights(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnLightOn and state == 'Pressed':
            GroupLightsA.SetCurrent(A_BtnLightOn)
            print('Touch A: %s' % ('Lights On'))
        elif button is A_BtnLightOf and state == 'Pressed':
            GroupLightsA.SetCurrent(A_BtnLightOf)
            print('Touch A: %s' % ('Lights Off'))
    pass
## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------
@event(PagePowerAll, ButtonEventList)
def PageLights(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
    #--
        if button is A_BtnPwrAll and state == 'Pressed':
            print('Touch A: %s' % ('PowerAll Pressed'))
        elif button is A_BtnPwrAll and state == 'Held':
            TLP1.HideAllPopups()
            TLP1.ShowPage('Index')
            print('Touch A: %s' % ('PowerAll Ok'))
    pass
## End Events Definitions-------------------------------------------------------
Initialize()
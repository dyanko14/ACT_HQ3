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
#TLPM = UIDevice('TouchPanelM')
TLP1 = UIDevice('TouchPanelA')
#TLP2 = UIDevice('TouchPanelB')
#TLP3 = UIDevice('TouchPanelC')

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
'''PANEL - ROOM Master ......................................................'''
'''PANEL - ROOM A ...........................................................'''
## Index
A_BtnIndex   = Button(TLP1, 1)
#A_LblIndex   = Button(TLP1, 2)
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
A_BtnHDMI    = Button(TLP1, 21)
A_BtnShare   = Button(TLP1, 22)
A_BtnPwrOn   = Button(TLP1, 23)
A_BtnPwrOff  = Button(TLP1, 24)
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
A_BtnPwrAll  = Button(TLP1, 101)
#A_LblPwrAll  = Button(TLP1, 102)
'''PANEL - ROOM B ...........................................................'''
'''PANEL - ROOM C ...........................................................'''
'''PANEL - Group Buttons ..................................................--'''
#--
PageIndex = [A_BtnIndex]
#--
PagePIN   = [A_BtnPin0, A_BtnPin1, A_BtnPin2, A_BtnPin3, A_BtnPin4, A_BtnPin5,
             A_BtnPin6, A_BtnPin7, A_BtnPin8, A_BtnPin9, A_BtnPinD]
#--
PageMain  = [A_BtnVideo, A_BtnAudio, A_BtnBlinds, A_BtnLights, A_BtnStatus, A_BtnPwrOff]
#--
#--
#--
#--
#--
#--
#--
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------
def Initialize():
    #Index Variables
    global PIN_M
    global PIN_A
    global PIN_B
    global PIN_C
    #--
    PIN_M = []
    PIN_A = []
    PIN_B = []
    PIN_C = []
    #--
    PIN_M_Secret = 1414
    PIN_A_Secret = 1414
    PIN_B_Secret = 1414
    PIN_C_Secret = 1414    
    
    #Index GUI
    TLP1.ShowPage('Index')
    TLP1.HideAllPopups()
    pass

## Event Definitions -----------------------------------------------------------
## Index -----------------------------------------------------------------------
@event(PageIndex, ButtonEventList)
def IndexEvents(button, state):
    '''if button.Host.DeviceAlias == 'TouchPanelM':
        if button is M_BtnIndex and state == 'Pressed':
            print("Touch M: Index Pressed")
            TLPM.ShowPopup('PIN')'''
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnIndex and state == 'Pressed':            
            TLP1.ShowPopup('PIN')            
            print("Touch A: Index Pressed")
    '''if button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnIndex and state == 'Pressed':
            print("Touch B: Index Pressed")
            TLP2.ShowPopup('PIN')
    if button.Host.DeviceAlias == 'TouchPanelC':
        if button is C_BtnIndex and state == 'Pressed':
            print("Touch C: Index Pressed")
            TLP3.ShowPopup('PIN')'''
    pass

## PIN -------------------------------------------------------------------------
def PINValidation(Number):
    print('Longitud: ' + str(len(PIN_A)))
    if len(PIN_A) >= 0 and len(PIN_A) <= 3:
        PIN_A.append(Number)
        print(PIN_A)
    else:
        print(PIN_A)
        print('Only four position')
    pass

@event(PagePIN, ButtonEventList)
def PINEvents(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnPin0 and state == 'Pressed':
            A_BtnPin0.SetState(1)
            #--     
            PINValidation(0)
            print("Touch A: PIN 0 Pressed")
        else:
            A_BtnPin0.SetState(0)
        #--
        if button is A_BtnPin1 and state == 'Pressed':
            A_BtnPin1.SetState(1)
            #--
            PINValidation(1)
            print("Touch A: PIN 1 Pressed")
        else:
            A_BtnPin1.SetState(0)
        #--
        if button is A_BtnPin2 and state == 'Pressed':
            #--     
            PINValidation(2)
            print("Touch A: PIN 2 Pressed")
        else:
            A_BtnPin2.SetState(0)
        #--
        if button is A_BtnPin3 and state == 'Pressed':
            A_BtnPin3.SetState(1)
            #--     
            PINValidation(3)
            print("Touch A: PIN 3 Pressed")
        else:
            A_BtnPin3.SetState(0)
        #--
        if button is A_BtnPin4 and state == 'Pressed':
            A_BtnPin4.SetState(1)
            #--     
            PINValidation(4)
            print("Touch A: PIN 4 Pressed")
        else:
            A_BtnPin4.SetState(0)
        #--
        if button is A_BtnPin5 and state == 'Pressed':
            A_BtnPin5.SetState(1)
            #--     
            PINValidation(5)
            print("Touch A: PIN 5 Pressed")
        else:
            A_BtnPin5.SetState(0)
        #--
        if button is A_BtnPin6 and state == 'Pressed':
            A_BtnPin6.SetState(1)
            #--     
            PINValidation(6)
            print("Touch A: PIN 6 Pressed")
        else:
            A_BtnPin6.SetState(0)
        #--
        if button is A_BtnPin7 and state == 'Pressed':
            A_BtnPin7.SetState(1)
            #--     
            PINValidation(7)
            print("Touch A: PIN 7 Pressed")
        else:
            A_BtnPin7.SetState(0)
        #--
        if button is A_BtnPin8 and state == 'Pressed':
            A_BtnPin8.SetState(1)
            #--     
            PINValidation(8)
            print("Touch A: PIN 8 Pressed")
        else:
            A_BtnPin8.SetState(0)
        #--
        if button is A_BtnPin9 and state == 'Pressed':
            A_BtnPin9.SetState(1)
            #--     
            PINValidation(9)
            print("Touch A: PIN 9 Pressed")
        else:
            A_BtnPin9.SetState(0)
        #--
        if button is A_BtnPinD and state == 'Pressed':
            A_BtnPinD.SetState(1)
            PIN_A.pop()
            print(PIN_A)
            print("Touch A: PIN Delete Pressed")
        elif button is A_BtnPinD and state == 'Repeated':
            A_BtnPinD.SetState(1)
            PIN_A.pop()
            print(PIN_A)
            print("Touch A: PIN Delete Released")
        else:
            A_BtnPinD.SetState(0)
    pass

## End Events Definitions-------------------------------------------------------
Initialize()
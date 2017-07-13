"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | Mixed Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
from gui import TLPM, TLP1, TLP2, TLP3, BTN, BTNPAGE, BTNGROUP, BTNSTATE, LBL, LVL, POPUP, PAGE

## MODULE IMPORT ---------------------------------------------------------------
## IP:
import extr_matrix_DXP_Series_v1_2_3_0 as DeviceA
import biam_dsp_TesiraSeries_v1_5_20_0 as DeviceB
import biam_cs_Devio_CR1_v1_0_0_0A as DeviceC
import biam_cs_Devio_CR1_v1_0_0_0B as DeviceD
import biam_cs_Devio_CR1_v1_0_0_0C as DeviceE

## RS-232:
import extr_switcher_SW_HDMI_Series_v1_0_2_0 as DeviceF
import extr_switcher_SW_HDMI_Series_v1_0_2_0 as DeviceG
#import extr_switcher_SW_HDMI_Series_v1_0_2_0 as DeviceE

print(Version())

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## IP:
MATRIX = DeviceA.EthernetClass('10.10.10.10', 23, Model='DXP 88 HD 4k')
BIAMP = DeviceB.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
DEVIO1 = DeviceC.EthernetClass('10.10.10.11', 4030, Model='Devio CR-1')
DEVIO2 = DeviceD.EthernetClass('10.10.10.12', 4030, Model='Devio CR-1')
DEVIO3 = DeviceE.EthernetClass('10.10.10.13', 4030, Model='Devio CR-1')
## RS-232:
SWITCH1 = DeviceF.SerialClass(IPCP, 'COM1', Baud=9600, Model='SW4 HDMI')
SWITCH2 = DeviceG.SerialClass(IPCP, 'COM2', Baud=9600, Model='SW4 HDMI')
#SWITCH3 = DeviceE.SerialClass(IPCP, 'COM3', Baud=9600, Model='SW4 HDMI')

## INITIALIZATE ----------------------------------------------------------------
def initialize():
    """This is the last function that loads when starting the system """
    ## OPEN CONNECTION SOCKETS
    ## IP
    MATRIX.Connect()
    BIAMP.Connect()
    DEVIO1.Connect()
    DEVIO2.Connect()
    DEVIO3.Connect()
    ## RS-232
    SWITCH1.Initialize()
    SWITCH2.Initialize()
    #SWITCH3.Initialize()

    ## RECURSIVE FUNCTIONS

    ## POWER COUNTER VARIABLE

    ## DATA INITIALIZE
    ## TouchPanel Master Data
    global Pin_M
    global Pin_M_Secret
    global Pin_M_GUI
    Pin_M = []
    Pin_M_GUI = []
    Pin_M_Secret = '0000'
    ## TouchPanel Room A Data
    global Pin_A
    global Pin_A_Secret
    global Pin_A_GUI
    Pin_A = []
    Pin_A_GUI = []
    Pin_A_Secret = '1111'
    ## TouchPanel Room B Data
    global Pin_B
    global Pin_B_Secret
    global Pin_B_GUI
    Pin_B = []
    Pin_B_GUI = []
    Pin_B_Secret = '2222'
    ## TouchPanel Room C Data
    global Pin_C
    global Pin_C_Secret
    global Pin_C_GUI
    Pin_C = []
    Pin_C_GUI = []
    Pin_C_Secret = '3333'

    ## TOUCH PANEL FUNCTIONS
    ## TouchPanel Master
    LBL['M_Index'].SetText('Panel Master')
    LBL['M_Room'].SetText('Panel Master')
    LBL['M_PIN'].SetText('')
    ## TouchPanel Room A
    LBL['A_Index'].SetText('Bienvenido a Sala Everest')
    LBL['A_Room'].SetText('Panel A')
    LBL['A_PIN'].SetText('')
    ## TouchPanel Room B
    LBL['B_Index'].SetText('Bienvenido a Sala Orizaba')
    LBL['B_Room'].SetText('Panel B')
    LBL['B_PIN'].SetText('')
    ## TouchPanel Room C
    LBL['C_Index'].SetText('Bienvenido a Sala Aconcagua')
    LBL['C_Room'].SetText('Panel C')
    LBL['C_PIN'].SetText('')

    ## TOUCH PANEL PAGES
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    TLP3.ShowPage('Index')
    TLPM.ShowPage('Index')

    TLPM.ShowPage('Index')
    TLPM.HideAllPopups()

    TLP1.ShowPage('Index')
    TLP1.HideAllPopups()
    BTNGROUP['MainA'].SetCurrent(None)

    TLP2.ShowPage('Index')
    TLP2.HideAllPopups()
    BTNGROUP['MainB'].SetCurrent(None)

    TLP3.ShowPage('Index')
    TLP3.HideAllPopups()
    BTNGROUP['MainC'].SetCurrent(None)

    ## NOTIFY TO CONSOLE
    print('System Inicializate')
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------

## UPDATE FUNCTIONS ------------------------------------------------------------

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules
def devio1_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))

        if value == 'Connected':
            DEVIO1_DATA['ConexModule'] = True
            BTN['A_LANDevio'].SetState(1)
        else:
            DEVIO1_DATA['ConexModule'] = False
            BTN['A_LANDevio'].SetState(0)
            ## Disconnect the IP Socket
            DEVIO1.Disconnect()

    elif command == 'CallInProgress':
        print(value)
        if value == 'True':
            DEVIO1_DATA['CallInProgress'] = True
        else:
            DEVIO1_DATA['CallInProgress'] = False

    elif command == 'FarEndAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['FarEndAudioPresent'] = True
        else:
            DEVIO1_DATA['FarEndAudioPresent'] = False

    elif command == 'LineFault':
        print(value)
        if value == 'True':
            DEVIO1_DATA['LineFault'] = True
        else:
            DEVIO1_DATA['LineFault'] = False

    elif command == 'MasterMicrophoneMute':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MasterMicMute'] = True
        else:
            DEVIO1_DATA['MasterMicMute'] = True

    elif command == 'MicrophoneAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MicAudioPresent'] = True
        else:
            DEVIO1_DATA['MicAudioPresent'] = False
    pass

def devio2_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))

        if value == 'Connected':
            DEVIO1_DATA['ConexModule'] = True
            BTN['A_LANDevio'].SetState(1)
        else:
            DEVIO1_DATA['ConexModule'] = False
            BTN['A_LANDevio'].SetState(0)
            ## Disconnect the IP Socket
            DEVIO1.Disconnect()

    elif command == 'CallInProgress':
        print(value)
        if value == 'True':
            DEVIO1_DATA['CallInProgress'] = True
        else:
            DEVIO1_DATA['CallInProgress'] = False

    elif command == 'FarEndAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['FarEndAudioPresent'] = True
        else:
            DEVIO1_DATA['FarEndAudioPresent'] = False

    elif command == 'LineFault':
        print(value)
        if value == 'True':
            DEVIO1_DATA['LineFault'] = True
        else:
            DEVIO1_DATA['LineFault'] = False

    elif command == 'MasterMicrophoneMute':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MasterMicMute'] = True
        else:
            DEVIO1_DATA['MasterMicMute'] = True

    elif command == 'MicrophoneAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MicAudioPresent'] = True
        else:
            DEVIO1_DATA['MicAudioPresent'] = False
    pass

def devio3_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))

        if value == 'Connected':
            DEVIO1_DATA['ConexModule'] = True
            BTN['A_LANDevio'].SetState(1)
        else:
            DEVIO1_DATA['ConexModule'] = False
            BTN['A_LANDevio'].SetState(0)
            ## Disconnect the IP Socket
            DEVIO1.Disconnect()

    elif command == 'CallInProgress':
        print(value)
        if value == 'True':
            DEVIO1_DATA['CallInProgress'] = True
        else:
            DEVIO1_DATA['CallInProgress'] = False

    elif command == 'FarEndAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['FarEndAudioPresent'] = True
        else:
            DEVIO1_DATA['FarEndAudioPresent'] = False

    elif command == 'LineFault':
        print(value)
        if value == 'True':
            DEVIO1_DATA['LineFault'] = True
        else:
            DEVIO1_DATA['LineFault'] = False

    elif command == 'MasterMicrophoneMute':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MasterMicMute'] = True
        else:
            DEVIO1_DATA['MasterMicMute'] = True

    elif command == 'MicrophoneAudioPresent':
        print(value)
        if value == 'True':
            DEVIO1_DATA['MicAudioPresent'] = True
        else:
            DEVIO1_DATA['MicAudioPresent'] = False
    pass

## EVENT FUNCTIONS ----------------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send a Connect()
## CAUTION: If you never make a Connect(), the Module never work with Subscriptions

## RECURSIVE FUNCTIONS ------------------------------------------------------------
## Help´s when the device was Off in the first Connect() method when the code starts

## RECURSIVE LOOP FUNCTIONS -----------------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Module
## If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
## Generate 'Connected' / 'Disconnected'

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## IP
DEVIO1_DATA = {
    'ConexModule'        : None,
    'ConexEvent'         : None,
    ##
    'CallInProgress'     : None,
    'FarEndAudioPresent' : None,
    'LineFault'          : None,
    'MasterMicMute'      : None,
    'MicAudioPresent'    : None,
}

DEVIO2_DATA = {
    'ConexModule'        : None,
    'ConexEvent'         : None,
    ##
    'CallInProgress'     : None,
    'FarEndAudioPresent' : None,
    'LineFault'          : None,
    'MasterMicMute'      : None,
    'MicAudioPresent'    : None,
}

DEVIO3_DATA = {
    'ConexModule'        : None,
    'ConexEvent'         : None,
    ##
    'CallInProgress'     : None,
    'FarEndAudioPresent' : None,
    'LineFault'          : None,
    'MasterMicMute'      : None,
    'MicAudioPresent'    : None,
}

## RS-232
Room = {
    'Mode' : '',
}

## PAGE USER EVENTS ------------------------------------------------------------
## Page Index ------------------------------------------------------------------
@event(BTNPAGE['Index'], BTNSTATE['List'])
def index_events(button, state):
    """User Actions: Touch Index Page"""

    if button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_Index'] and state == 'Pressed':
            TLPM.ShowPopup('PIN')
            print("Touch Master: Index Pressed")

    elif button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_Index'] and state == 'Pressed':
            TLP1.ShowPopup('PIN')
            print("Touch A: Index Pressed")

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_Index'] and state == 'Pressed':
            TLP2.ShowPopup('PIN')
            print("Touch B: Index Pressed")

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_Index'] and state == 'Pressed':
            TLP3.ShowPopup('PIN')
            print("Touch C: Index Pressed")
    pass

## PIN A------------------------------------------------------------------------
def PINValidationA(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch A Validation"""
    global Pin_A, Pin_A_GUI

    if Pin_Button == 'PINDelete':
        if len(Pin_A) > 0:              #If the list have data
            Pin_A.pop()                 #Delete the last number of the list
            Pin_A_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_A)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_A_GUI) #Convert the list to cleaned string data
            LBL['A_PIN'].SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP1.HidePopup('PIN')           #Show the Index Page
        Pin_A = []                      #Erase each items in list [0-9]
        Pin_A_GUI = []                  #Erase each items in list [****]
        LBL['A_PIN'].SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_A) >= 0 and len(Pin_A) <= 3: #Ej= '1234'
            #--
            Pin_A.append(Number)        #Append the last number to internal list
            Pin_A_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_A)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_A_GUI) #Convert the list to cleaned string data
            LBL['A_PIN'].SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == Pin_A_Secret: #If User enter the secret PIN:
                    TLP1.HideAllPopups()  #Panel actions:
                    TLP1.ShowPage('Main')
                    TLP1.ShowPopup('x_Welcome')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    Pin_A = []           #Erase each items in list [0-9]
                    Pin_A_GUI = []       #Erase each items in list [****]
                    LBL['A_PIN'].SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LBL['A_PIN'].SetText('')
    pass

## PIN B -----------------------------------------------------------------------
def PINValidationB(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch B Validation"""
    global Pin_B, Pin_B_GUI

    if Pin_Button == 'PINDelete':
        if len(Pin_B) > 0:              #If the list have data
            Pin_B.pop()                 #Delete the last number of the list
            Pin_B_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_B)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_B_GUI) #Convert the list to cleaned string data
            LBL['B_PIN'].SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP2.HidePopup('PIN')           #Show the Index Page
        Pin_B = []                      #Erase each items in list [0-9]
        Pin_B_GUI = []                  #Erase each items in list [****]
        LBL['B_PIN'].SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_B) >= 0 and len(Pin_B) <= 3: #Ej= '1234'
            #--
            Pin_B.append(Number)        #Append the last number to internal list
            Pin_B_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_B)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_B_GUI) #Convert the list to cleaned string data
            LBL['B_PIN'].SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == Pin_B_Secret: #If User enter the secret PIN:
                    TLP2.HideAllPopups()  #Panel actions:
                    TLP2.ShowPage('Main')
                    TLP2.ShowPopup('x_Welcome')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    Pin_B = []           #Erase each items in list [0-9]
                    Pin_B_GUI = []       #Erase each items in list [****]
                    LBL['B_PIN'].SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LBL['B_PIN'].SetText('')
    pass

## PIN C -----------------------------------------------------------------------
def PINValidationC(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch C Validation"""
    global Pin_C, Pin_C_GUI

    if Pin_Button == 'PINDelete':
        if len(Pin_C) > 0:              #If the list have data
            Pin_C.pop()                 #Delete the last number of the list
            Pin_C_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_C)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_C_GUI) #Convert the list to cleaned string data
            LBL['C_PIN'].SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP3.HidePopup('PIN')           #Show the Index Page
        Pin_C = []                      #Erase each items in list [0-9]
        Pin_C_GUI = []                  #Erase each items in list [****]
        LBL['C_PIN'].SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_C) >= 0 and len(Pin_C) <= 3: #Ej= '1234'
            #--
            Pin_C.append(Number)        #Append the last number to internal list
            Pin_C_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_C)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_C_GUI) #Convert the list to cleaned string data
            LBL['C_PIN'].SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == Pin_C_Secret: #If User enter the secret PIN:
                    TLP3.HideAllPopups()  #Panel actions:
                    TLP3.ShowPage('Main')
                    TLP3.ShowPopup('x_Welcome')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    Pin_C = []           #Erase each items in list [0-9]
                    Pin_C_GUI = []       #Erase each items in list [****]
                    LBL['C_PIN'].SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LBL['C_PIN'].SetText('')
    pass

## PIN Master ------------------------------------------------------------------
def PINValidationM(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch M Validation"""
    global Pin_M, Pin_M_GUI

    if Pin_Button == 'PINDelete':
        if len(Pin_M) > 0:              #If the list have data
            Pin_M.pop()                 #Delete the last number of the list
            Pin_M_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_M)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_M_GUI) #Convert the list to cleaned string data
            LBL['M_PIN'].SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLPM.HidePopup('PIN')           #Show the Index Page
        Pin_M = []                      #Erase each items in list [0-9]
        Pin_M_GUI = []                  #Erase each items in list [****]
        LBL['M_PIN'].SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_M) >= 0 and len(Pin_M) <= 3: #Ej= '1234'
            #--
            Pin_M.append(Number)        #Append the last number to internal list
            Pin_M_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_M)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_M_GUI) #Convert the list to cleaned string data
            LBL['M_PIN'].SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == Pin_M_Secret: #If User enter the secret PIN:
                    TLPM.HideAllPopups()  #Panel actions:
                    TLPM.ShowPage('Main_Individual')
                    TLPM.ShowPopup('Main_Individual')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    Pin_M = []           #Erase each items in list [0-9]
                    Pin_M_GUI = []       #Erase each items in list [****]
                    LBL['M_PIN'].SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LBL['M_PIN'].SetText('')
    pass

## PIN Page --------------------------------------------------------------------
@event(BTNPAGE['PIN'], BTNSTATE['List']) #PagePIN = |[0-9]|Delete|Exit
def pin_events(button, state):
    """User Actions: PIN Page"""

    if button.Host.DeviceAlias == 'TouchPanelM':
        if state == 'Pressed' or state == 'Repeated':
            print('Panel Master: ' + button.Name)
            PINValidationM(button.Name)  #Recall a validation function
            button.SetState(1)
        else:
            button.SetState(0)

    elif button.Host.DeviceAlias == 'TouchPanelA':
        if state == 'Pressed':
            print('Panel A: ' + button.Name)
            PINValidationA(button.Name)  #Recall a validation function
            button.SetState(1)
        else:
            button.SetState(0)

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if state == 'Pressed':
            print('Panel B: ' + button.Name)
            PINValidationB(button.Name)  #Recall a validation function
            button.SetState(1)
        else:
            button.SetState(0)

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if state == 'Pressed':
            print('Panel C: ' + button.Name)
            PINValidationC(button.Name)  #Recall a validation function
            button.SetState(1)
        else:
            button.SetState(0)
    pass

## Room Master Mode ------------------------------------------------------------
@event(BTNPAGE['Room'], BTNSTATE['List'])
def room_master_events(button, state):
    """User Actions: Touch Room Page"""

    if button is BTN['M_Mode1'] and state == 'Pressed': #Individual Mode
        Room['Mode'] = 'Close' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Index')
        TLP2.ShowPage('Index')
        TLP3.ShowPage('Index')
        TLPM.ShowPage('Main_Individual')
        ##
        TLP1.ShowPopup('x_Welcome')
        TLP2.ShowPopup('x_Welcome')
        TLP3.ShowPopup('x_Welcome')
        TLPM.ShowPopup('1_Master')
        ## TurnOff Mutually Exclusive
        BTNGROUP['MainA'].SetCurrent(None)
        BTNGROUP['MainB'].SetCurrent(None)
        BTNGROUP['MainC'].SetCurrent(None)
        ## Activate Room Panel Main Indicators
        ## Panel A
        BTN['A_RoomA'].SetState(1)
        BTN['A_RoomB'].SetState(0)
        BTN['A_RoomC'].SetState(0)
        ## Panel B
        BTN['B_RoomA'].SetState(0)
        BTN['B_RoomB'].SetState(1)
        BTN['B_RoomC'].SetState(0)
        ## Panel C
        BTN['C_RoomA'].SetState(0)
        BTN['C_RoomB'].SetState(0)
        BTN['C_RoomC'].SetState(1)
        ## Activate Room Panel Main Full Indicators
        ## Panel M
        BTN['M_FRoomA'].SetState(0)
        BTN['M_FRoomB'].SetState(0)
        BTN['M_FRoomC'].SetState(0)
        ## Panel A
        BTN['A_FRoomA'].SetState(0)
        BTN['A_FRoomB'].SetState(0)
        BTN['A_FRoomC'].SetState(0)
        ## Panel B
        BTN['B_FRoomA'].SetState(0)
        BTN['B_FRoomB'].SetState(0)
        BTN['B_FRoomC'].SetState(0)
        ## Panel C
        BTN['C_FRoomA'].SetState(0)
        BTN['C_FRoomB'].SetState(0)
        BTN['C_FRoomC'].SetState(0)
        print('Touch Master: %s' % ('Room Mode A|B|C All Close'))

    elif button is BTN['M_Mode2'] and state == 'Pressed': #Executive Mode
        Room['Mode'] = 'Executive' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Main_Full')
        TLP2.ShowPage('Main_Full')
        TLP3.ShowPage('Index')
        TLPM.ShowPage('Main_Full')
        ##
        TLP1.ShowPopup('x_Welcome_Full')
        TLP2.ShowPopup('x_Welcome_Full')
        TLP3.ShowPopup('x_Welcome')
        TLPM.ShowPopup('x_Welcome_Full')
        ## TurnOff Mutually Exclusive
        BTNGROUP['MainFA'].SetCurrent(None)
        BTNGROUP['MainFB'].SetCurrent(None)
        BTNGROUP['MainFC'].SetCurrent(None)
        BTNGROUP['MainFM'].SetCurrent(None)
        ## Activate Room Panel Main Full Indicators
        ## Panel M
        BTN['M_FRoomA'].SetState(1)
        BTN['M_FRoomB'].SetState(1)
        BTN['M_FRoomC'].SetState(0)
        ## Panel A
        BTN['A_FRoomA'].SetState(1)
        BTN['A_FRoomB'].SetState(1)
        BTN['A_FRoomC'].SetState(0)
        ## Panel B
        BTN['B_FRoomA'].SetState(1)
        BTN['B_FRoomB'].SetState(1)
        BTN['B_FRoomC'].SetState(0)
        ## Panel C
        BTN['C_RoomA'].SetState(0)
        BTN['C_RoomB'].SetState(0)
        BTN['C_RoomC'].SetState(1)
        print('Touch Master: %s' % ('Room Mode A-B|C Executive'))

    elif button is BTN['M_Mode3'] and state == 'Pressed': #All Open Mode
        Room['Mode'] = 'Open' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Main_Full')
        TLP2.ShowPage('Main_Full')
        TLP3.ShowPage('Main_Full')
        TLPM.ShowPage('Main_Full')
        ##
        TLP1.ShowPopup('x_Welcome_Full')
        TLP2.ShowPopup('x_Welcome_Full')
        TLP3.ShowPopup('x_Welcome_Full')
        TLPM.ShowPopup('x_Welcome_Full')
        ## TurnOff Mutually Exclusive
        BTNGROUP['MainFA'].SetCurrent(None)
        BTNGROUP['MainFB'].SetCurrent(None)
        BTNGROUP['MainFC'].SetCurrent(None)
        BTNGROUP['MainFM'].SetCurrent(None)
        ## Activate Room Panel Main Full Indicators
        ## Panel M
        BTN['M_FRoomA'].SetState(1)
        BTN['M_FRoomB'].SetState(1)
        BTN['M_FRoomC'].SetState(1)
        ## Panel A
        BTN['A_FRoomA'].SetState(1)
        BTN['A_FRoomB'].SetState(1)
        BTN['A_FRoomC'].SetState(1)
        ## Panel B
        BTN['B_FRoomA'].SetState(1)
        BTN['B_FRoomB'].SetState(1)
        BTN['B_FRoomC'].SetState(1)
        ## Panel C
        BTN['C_FRoomA'].SetState(1)
        BTN['C_FRoomB'].SetState(1)
        BTN['C_FRoomC'].SetState(1)
        print('Touch Master: %s' % ('Room Mode A|B-C /All Open'))

    ## Mutually Exclusive Room Preset Buttons
    BTNGROUP['Room'].SetCurrent(button)
    pass

## Main ------------------------------------------------------------------------
@event(BTNPAGE['Main'], BTNSTATE['List'])
def page_main(button, state):
    """User Actions: Touch Main Page"""
    
    if button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_Config'] and state == 'Pressed':
            LBL['M_Room'].SetText('Control de Escenarios')
            TLPM.ShowPopup('1_Master')
            print('Touch M: %s' % ('Config Escenario'))

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_Video'] and state == 'Pressed':
            LBL['A_Room'].SetText('Control de Video')
            TLP1.ShowPopup('Video')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Video'])
            print('Touch A: %s' % ('Video'))

        elif button is BTN['A_Audio'] and state == 'Pressed':
            LBL['A_Room'].SetText('Control de Audio')
            TLP1.ShowPopup('Audio')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Audio'])
            print('Touch A: %s' % ('Audio'))

        elif button is BTN['A_Lights'] and state == 'Pressed':
            LBL['A_Room'].SetText('Control de Luces')
            TLP1.ShowPopup('Lights')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Lights'])
            print('Touch A: %s' % ('Luces'))

        elif button is BTN['A_PwrOff'] and state == 'Pressed':
            LBL['A_Room'].SetText('Apagado de Sala')
            TLP1.ShowPopup('x_PowerOff')
            BTNGROUP['MainA'].SetCurrent(BTN['A_PwrOff'])
            print('Touch A: %s' % ('PowerOff'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_Video'] and state == 'Pressed':
            LBL['B_Room'].SetText('Control de Video')
            TLP2.ShowPopup('Video')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Video'])
            print('Touch B: %s' % ('Video'))

        elif button is BTN['B_Audio'] and state == 'Pressed':
            LBL['B_Room'].SetText('Control de Audio')
            TLP2.ShowPopup('Audio')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Audio'])
            print('Touch B: %s' % ('Audio'))

        elif button is BTN['B_Lights'] and state == 'Pressed':
            LBL['B_Room'].SetText('Control de Luces')
            TLP2.ShowPopup('Lights')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Lights'])
            print('Touch B: %s' % ('Luces'))

        elif button is BTN['B_PwrOff'] and state == 'Pressed':
            LBL['B_Room'].SetText('Apagado de Sala')
            TLP2.ShowPopup('x_PowerOff')
            BTNGROUP['MainB'].SetCurrent(BTN['B_PwrOff'])
            print('Touch B: %s' % ('PowerOff'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_Video'] and state == 'Pressed':
            LBL['C_Room'].SetText('Control de Video')
            TLP3.ShowPopup('Video')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Video'])
            print('Touch C: %s' % ('Video'))

        elif button is BTN['C_Audio'] and state == 'Pressed':
            LBL['C_Room'].SetText('Control de Audio')
            TLP3.ShowPopup('Audio')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Audio'])
            print('Touch C: %s' % ('Audio'))

        elif button is BTN['C_Lights'] and state == 'Pressed':
            LBL['C_Room'].SetText('Control de Luces')
            TLP3.ShowPopup('Lights')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Lights'])
            print('Touch C: %s' % ('Luces'))

        elif button is BTN['C_PwrOff'] and state == 'Pressed':
            LBL['C_Room'].SetText('Apagado de Sala')
            TLP3.ShowPopup('x_PowerOff')
            BTNGROUP['MainC'].SetCurrent(BTN['C_PwrOff'])
            print('Touch C: %s' % ('PowerOff'))
    pass

## Main Full -------------------------------------------------------------------
@event(BTNPAGE['Main_F'], BTNSTATE['List'])
def page_main_full(button, state):
    """User Actions: Touch Main Page"""
    global Panels, Touch, Labels, TxtBox
    Panels = [TLP1, TLP2, TLP3, TLPM]
    Labels = [LBL['A_RoomFull'], LBL['B_RoomFull'], LBL['C_RoomFull'], LBL['M_RoomFull']]

    ## VIDEO PAGES -----------------------------
    if state == 'Pressed':
        if button.ID == 111: #VIDEO BUTTON IN EACH PANEL
            ## GLOBAL BUTTONS ACTIONS...........................
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FVideo'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FVideo'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FVideo'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FVideo'])
            ## Bucle to Notify to all Panels
            for TxtBox in Labels:
                TxtBox.SetText('Control de Video')
            if Room['Mode'] == 'Executive':
                ## Bucle to Show Popup in All Panels
                for Touch in Panels:
                    Touch.ShowPopup('Video_Executive')
                print('Touch: %s' % ('Video Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                ## Bucle to Show Popup in All Panels
                for Touch in Panels:
                    Touch.ShowPopup('Video_Full')
                print('Touch: %s' % ('Video Modo Abierto'))

    ## AUDIO PAGES -----------------------------
        elif button.ID == 112: #AUDIO BUTTON IN EACH PANEL
            ## GLOBAL BUTTONS ACTIONS...........................
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FAudio'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FAudio'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FAudio'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FAudio'])
            ## Bucle to Notify to all Panels
            for TxtBox in Labels:
                TxtBox.SetText('Control de Audio')
            ## Bucle to Show Popup in All Panels
            for Touch in Panels:
                Touch.ShowPopup('Audio_Full')
            #
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Audio Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Audio Modo Abierto'))

    ## LIGHT PAGES -----------------------------
        elif button.ID == 113: #LIGHTS BUTTON IN EACH PANEL
            ## GLOBAL BUTTONS ACTIONS...........................
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FLights'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FLights'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FLights'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FLights'])
            ## Bucle to Notify to all Panels
            for TxtBox in Labels:
                TxtBox.SetText('Control de Luces')
            if Room['Mode'] == 'Executive':
                ## Bucle to Show Popup in All Panels
                for Touch in Panels:
                    Touch.ShowPopup('Lights_Executive')
                print('Touch: %s' % ('Luces Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                ## Bucle to Show Popup in All Panels
                for Touch in Panels:
                    Touch.ShowPopup('Lights_Full')
                print('Touch: %s' % ('Luces Modo Abierto'))

    ## VoIP PAGES -----------------------------
        elif button.ID == 114: #LIGHTS BUTTON IN EACH PANEL
            ## GLOBAL BUTTONS ACTIONS...........................
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_VoIP'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_VoIP'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_VoIP'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_VoIP'])
            ## Bucle to Notify to all Panels
            for TxtBox in Labels:
                TxtBox.SetText('Control de Telefonía IP')
            ## Bucle to Show Popup in All Panels
            for Touch in Panels:
                Touch.ShowPopup('VoIP')
            #
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('VoIP Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('VoIP Modo Abierto'))

    ## VoIP PAGES -----------------------------
        elif button.ID == 115: #POWER BUTTON IN EACH PANEL
            ## GLOBAL BUTTONS ACTIONS...........................
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FPwrOff'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FPwrOff'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FPwrOff'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FPwrOff'])
            ## Bucle to Notify to all Panels
            for TxtBox in Labels:
                TxtBox.SetText('Apagado del Sistema')
            ## Bucle to Show Popup in All Panels
            for Touch in Panels:
                Touch.ShowPopup('x_PowerOff_Full')
            #
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('PowerOff Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('PowerOff Modo Abierto'))
    pass

## Video -----------------------------------------------------------------------
@event(BTNPAGE['Video'], BTNSTATE['List'])
def page_main_video(button, state):
    """User Actions: Touch Main Video Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_VHDMI'] and state == 'Pressed':
            #SWITCH1.Set('Input','1')
            print('Touch A: %s' % ('HDMI'))
        elif button is BTN['A_VShare'] and state == 'Pressed':
            #SWITCH1.Set('Input','2')
            print('Touch A: %s' % ('ShareLink'))
        elif button is BTN['A_VPwrOn'] and state == 'Pressed':
            #ProjOn
            print('Touch A: %s' % ('Proj PowerOn'))
        elif button is BTN['A_VPwrOff'] and state == 'Pressed':
            #ProjOff
            print('Touch A: %s' % ('Proj PowerOff'))
        elif button is BTN['A_Up'] and state == 'Pressed':
            #ScreenUpA()
            print('Touch A: %s' % ('Screen Up'))
        elif button is BTN['A_Stop'] and state == 'Pressed':
            #ScreenStopA()
            print('Touch A: %s' % ('Screen Stop'))
        elif button is BTN['A_Down'] and state == 'Pressed':
            #ScreenDownA()
            print('Touch A: %s' % ('Screen Down'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_VHDMI'] and state == 'Pressed':
            #SWITCH1.Set('Input','1')
            print('Touch B: %s' % ('HDMI'))
        elif button is BTN['B_VShare'] and state == 'Pressed':
            #SWITCH1.Set('Input','2')
            print('Touch B: %s' % ('ShareLink'))
        elif button is BTN['B_VPwrOn'] and state == 'Pressed':
            #ProjOn
            print('Touch B: %s' % ('Proj PowerOn'))
        elif button is BTN['B_VPwrOff'] and state == 'Pressed':
            #ProjOff
            print('Touch B: %s' % ('Proj PowerOff'))
        elif button is BTN['B_Up'] and state == 'Pressed':
            #ScreenUpB()
            print('Touch B: %s' % ('Screen Up'))
        elif button is BTN['B_Stop'] and state == 'Pressed':
            #ScreenStopB()
            print('Touch B: %s' % ('Screen Stop'))
        elif button is BTN['B_Down'] and state == 'Pressed':
            #ScreenDownB()
            print('Touch B: %s' % ('Screen Down'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_VHDMI'] and state == 'Pressed':
            #SWITCH1.Set('Input','1')
            print('Touch C: %s' % ('HDMI'))
        elif button is BTN['C_VShare'] and state == 'Pressed':
            #SWITCH1.Set('Input','2')
            print('Touch C: %s' % ('ShareLink'))
        elif button is BTN['C_VPwrOn'] and state == 'Pressed':
            #ProjOn
            print('Touch C: %s' % ('Proj PowerOn'))
        elif button is BTN['C_VPwrOff'] and state == 'Pressed':
            #ProjOff
            print('Touch C: %s' % ('Proj PowerOff'))
        elif button is BTN['C_Up'] and state == 'Pressed':
            #ScreenUpC()
            print('Touch C: %s' % ('Screen Up'))
        elif button is BTN['C_Stop'] and state == 'Pressed':
            #ScreenStopC()
            print('Touch C: %s' % ('Screen Stop'))
        elif button is BTN['C_Down'] and state == 'Pressed':
            #ScreenDownC()
            print('Touch C: %s' % ('Screen Down'))
    pass

## Audio -----------------------------------------------------------------------
@event(BTNPAGE['Audio'], BTNSTATE['List'])
def page_main_audio(button, state):
    """User Actions: Touch Main Audio Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_VolLess'] and state == 'Pressed':
            print('Touch A: %s' % ('Vol -'))
        elif button is BTN['A_VolPlus'] and state == 'Pressed':
            print('Touch A: %s' % ('Vol +'))
        elif button is BTN['A_Mute'] and state == 'Pressed':
            print('Touch A: %s' % ('Vol Mute'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_VolLess'] and state == 'Pressed':
            print('Touch B: %s' % ('Vol -'))
        elif button is BTN['B_VolPlus'] and state == 'Pressed':
            print('Touch B: %s' % ('Vol +'))
        elif button is BTN['B_Mute'] and state == 'Pressed':
            print('Touch B: %s' % ('Vol Mute'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_VolLess'] and state == 'Pressed':
            print('Touch C: %s' % ('Vol -'))
        elif button is BTN['C_VolPlus'] and state == 'Pressed':
            print('Touch C: %s' % ('Vol +'))
        elif button is BTN['C_Mute'] and state == 'Pressed':
            print('Touch C: %s' % ('Vol Mute'))
    pass

## Lights ----------------------------------------------------------------------
@event(BTNPAGE['Lights'], BTNSTATE['List'])
def page_main_lights(button, state):
    """User Actions: Touch Main Lights Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_Light1'] and state == 'Pressed':
            print('Touch A: %s' % ('Lights 1'))
        elif button is BTN['A_Light2'] and state == 'Pressed':
            print('Touch A: %s' % ('Lights 2'))
        elif button is BTN['A_Light3'] and state == 'Pressed':
            print('Touch A: %s' % ('Lights 3'))
        elif button is BTN['A_Light4'] and state == 'Pressed':
            print('Touch A: %s' % ('Lights 4'))
        elif button is BTN['A_BUp'] and state == 'Pressed':
            print('Touch A: %s' % ('Blinds Up'))
        elif button is BTN['A_BStop'] and state == 'Pressed':
            print('Touch A: %s' % ('Blinds Stop'))
        elif button is BTN['A_BDown'] and state == 'Pressed':
            print('Touch A: %s' % ('Blinds Down'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_Light1'] and state == 'Pressed':
            print('Touch B: %s' % ('Lights 1'))
        elif button is BTN['B_Light2'] and state == 'Pressed':
            print('Touch B: %s' % ('Lights 2'))
        elif button is BTN['B_Light3'] and state == 'Pressed':
            print('Touch B: %s' % ('Lights 3'))
        elif button is BTN['B_Light4'] and state == 'Pressed':
            print('Touch B: %s' % ('Lights 4'))
        elif button is BTN['B_BUp'] and state == 'Pressed':
            print('Touch B: %s' % ('Blinds Up'))
        elif button is BTN['B_BStop'] and state == 'Pressed':
            print('Touch B: %s' % ('Blinds Stop'))
        elif button is BTN['B_BDown'] and state == 'Pressed':
            print('Touch B: %s' % ('Blinds Down'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_Light1'] and state == 'Pressed':
            print('Touch C: %s' % ('Lights 1'))
        elif button is BTN['C_Light2'] and state == 'Pressed':
            print('Touch C: %s' % ('Lights 2'))
        elif button is BTN['C_Light3'] and state == 'Pressed':
            print('Touch C: %s' % ('Lights 3'))
        elif button is BTN['C_Light4'] and state == 'Pressed':
            print('Touch C: %s' % ('Lights 4'))
        elif button is BTN['C_BUp'] and state == 'Pressed':
            print('Touch C: %s' % ('Blinds Up'))
        elif button is BTN['C_BStop'] and state == 'Pressed':
            print('Touch C: %s' % ('Blinds Stop'))
        elif button is BTN['C_BDown'] and state == 'Pressed':
            print('Touch C: %s' % ('Blinds Down'))
    pass

## PowerOff --------------------------------------------------------------------
@event(BTNPAGE['Power'], BTNSTATE['List'])
def page_main_poweroff(button, state):
    """User Actions: Touch Main PowerOff Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_PwrAll'] and state == 'Pressed':
            print('Touch A: %s' % ('PowerOff'))

    if button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_PwrAll'] and state == 'Pressed':
            print('Touch B: %s' % ('PowerOff'))

    if button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_PwrAll'] and state == 'Pressed':
            print('Touch C: %s' % ('PowerOff'))
    pass



## Video Functions
def ProjToAll(IDProj, IDPanel):
    """Open the Projector Controls in All Panels selected by the user"""
    global Panels, Touch, Labels, TxtBox

    ## TouchPanel Actions
    Panels = [TLP1, TLP2, TLP3, TLPM]
    for Touch in Panels:
        Touch.ShowPopup('Video_Full_%s' % (IDProj))
    ## Label Actions
    Labels = [LBL['A_RoomFull'], LBL['B_RoomFull'], LBL['C_RoomFull'], LBL['M_RoomFull']]
    for TxtBox in Labels:
        TxtBox.SetText('Control de Proyección %s' % (IDProj))

    ## Notify to Console
    print('Touch %s: Proj%s Modo Ejecutivo' % (IDPanel, IDProj))
    pass

## Video Executive -------------------------------------------------------------
@event(BTNPAGE['VideoE'], BTNSTATE['List'])
def page_main_video_executive(button, state):
    """User Actions: Touch Main Video Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_EProjA'] and state == 'Pressed':
            ProjToAll('A', 'A')
        elif button is BTN['A_EProjB'] and state == 'Pressed':
            ProjToAll('B', 'A')
        elif button is BTN['A_EProjD'] and state == 'Pressed':
            ProjToAll('D', 'A')

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_EProjA'] and state == 'Pressed':
            ProjToAll('A', 'B')
        elif button is BTN['B_EProjB'] and state == 'Pressed':
            ProjToAll('B', 'B')
        elif button is BTN['B_EProjD'] and state == 'Pressed':
            ProjToAll('D', 'B')

    elif button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_EProjA'] and state == 'Pressed':
            ProjToAll('A', 'M')
        elif button is BTN['M_EProjB'] and state == 'Pressed':
            ProjToAll('B', 'M')
        elif button is BTN['M_EProjD'] and state == 'Pressed':
            ProjToAll('D','M')
    pass

## Video Full ------------------------------------------------------------------
@event(BTNPAGE['VideoF'], BTNSTATE['List'])
def page_main_video_full(button, state):
    """User Actions: Touch Main Video Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_ProjA'] and state == 'Pressed':
            ProjToAll('A', 'A')
        elif button is BTN['A_ProjB'] and state == 'Pressed':
            ProjToAll('B', 'A')
        elif button is BTN['A_ProjC'] and state == 'Pressed':
            ProjToAll('C', 'A')
        elif button is BTN['A_ProjD'] and state == 'Pressed':
            ProjToAll('D', 'A')
        elif button is BTN['A_ProjM'] and state == 'Pressed':
            ProjToAll('M', 'A')

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_ProjA'] and state == 'Pressed':
            ProjToAll('A', 'B')
        elif button is BTN['B_ProjB'] and state == 'Pressed':
            ProjToAll('B', 'B')
        elif button is BTN['B_ProjC'] and state == 'Pressed':
            ProjToAll('C', 'B')
        elif button is BTN['B_ProjD'] and state == 'Pressed':
            ProjToAll('D', 'B')
        elif button is BTN['B_ProjM'] and state == 'Pressed':
            ProjToAll('M', 'B')

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_ProjA'] and state == 'Pressed':
            ProjToAll('A', 'C')
        elif button is BTN['C_ProjB'] and state == 'Pressed':
            ProjToAll('B', 'C')
        elif button is BTN['C_ProjC'] and state == 'Pressed':
            ProjToAll('C', 'C')
        elif button is BTN['C_ProjD'] and state == 'Pressed':
            ProjToAll('D', 'C')
        elif button is BTN['C_ProjM'] and state == 'Pressed':
            ProjToAll('M', 'C')

    elif button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_ProjA'] and state == 'Pressed':
            ProjToAll('A', 'M')
        elif button is BTN['M_ProjB'] and state == 'Pressed':
            ProjToAll('B', 'M')
        elif button is BTN['M_ProjC'] and state == 'Pressed':
            ProjToAll('C', 'M')
        elif button is BTN['M_ProjD'] and state == 'Pressed':
            ProjToAll('D', 'M')
        elif button is BTN['M_ProjM'] and state == 'Pressed':
            ProjToAll('M', 'M')
    pass

## Video Full A-----------------------------------------------------------------
@event(BTNPAGE['VideoFA'], BTNSTATE['List'])
def page_main_video_a(button, state):
    """User Actions: Touch Main Full Video A Page"""
    if button.ID == 151 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A HDMI'))
    elif button.ID == 152 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A ShareLink'))
    elif button.ID == 155 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A PowerOn'))
    elif button.ID == 156 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A PowerOff'))
    elif button.ID == 157 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A Screen Up'))
    elif button.ID == 158 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A Screen Stop'))
    elif button.ID == 159 and state == 'Pressed':
        print('Touch: %s' % ('Proj-A Screen Down'))
    elif button.ID == 160 and state == 'Pressed':
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch: %s' % ('Proj-A Back'))
    pass

## Video Full B-----------------------------------------------------------------
@event(BTNPAGE['VideoFB'], BTNSTATE['List'])
def page_main_video_b(button, state):
    """User Actions: Touch Main Full Video B Page"""
    if button.ID == 161 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B HDMI'))
    elif button.ID == 162 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B ShareLink'))
    elif button.ID == 165 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B PowerOn'))
    elif button.ID == 166 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B PowerOff'))
    elif button.ID == 167 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B Screen Up'))
    elif button.ID == 168 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B Screen Stop'))
    elif button.ID == 169 and state == 'Pressed':
        print('Touch: %s' % ('Proj-B Screen Down'))
    elif button.ID == 170 and state == 'Pressed':
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch: %s' % ('Proj-B Back'))
    pass

## Video Full C-----------------------------------------------------------------
@event(BTNPAGE['VideoFC'], BTNSTATE['List'])
def page_main_video_c(button, state):
    """User Actions: Touch Main Full Video C Page"""
    if button.ID == 171 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C HDMI'))
    elif button.ID == 172 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C ShareLink'))
    elif button.ID == 175 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C PowerOn'))
    elif button.ID == 176 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C PowerOff'))
    elif button.ID == 177 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C Screen Up'))
    elif button.ID == 178 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C Screen Stop'))
    elif button.ID == 179 and state == 'Pressed':
        print('Touch: %s' % ('Proj-C Screen Down'))
    elif button.ID == 180 and state == 'Pressed':
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch: %s' % ('Proj-C Back'))
    pass

## Video Full D-----------------------------------------------------------------
@event(BTNPAGE['VideoFD'], BTNSTATE['List'])
def page_main_video_d(button, state):
    """User Actions: Touch Main Full Video D Page"""
    if button.ID == 181 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D HDMI'))
    elif button.ID == 182 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D ShareLink'))
    elif button.ID == 185 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D PowerOn'))
    elif button.ID == 186 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D PowerOff'))
    elif button.ID == 187 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D Screen Up'))
    elif button.ID == 188 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D Screen Stop'))
    elif button.ID == 189 and state == 'Pressed':
        print('Touch: %s' % ('Proj-D Screen Down'))
    elif button.ID == 190 and state == 'Pressed':
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch: %s' % ('Proj-D Back'))
    pass

## Video Full Global ------------------------------------------------------------
@event(BTNPAGE['VideoFG'], BTNSTATE['List'])
def page_main_video_global(button, state):
    """User Actions: Touch Main Full Video Global Page"""
    if button.ID == 191 and state == 'Pressed':
        print('Touch: %s' % ('Proj-Global HDMI'))
    elif button.ID == 193 and state == 'Pressed':
        print('Touch: %s' % ('Proj-Global ShareLink'))
    elif button.ID == 195 and state == 'Pressed':
        print('Touch: %s' % ('Proj-Global Screen Up'))
    elif button.ID == 196 and state == 'Pressed':
        print('Touch: %s' % ('Proj-Global Screen Stop'))
    elif button.ID == 197 and state == 'Pressed':
        print('Touch: %s' % ('Proj-Global Screen Down'))
    elif button.ID == 198 and state == 'Pressed':
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch: %s' % ('Proj-Global Back'))
    pass

## Audio Full Global ------------------------------------------------------------
@event(BTNPAGE['AudioF'], BTNSTATE['List'])
def page_main_audio_full(button, state):
    """User Actions: Touch Main Full Audio Page"""

    if button is BTN['A_.HDMI'] or button is BTN['B_.HDMI'] or button is BTN['C_.HDMI'] or button is BTN['M_.HDMI']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('HDMI Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('HDMI Modo Abierto'))

    elif button is BTN['A_.Share'] or button is BTN['B_.Share'] or button is BTN['C_.Share'] or button is BTN['M_.Share']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('ShareLink Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('ShareLink Modo Abierto'))

    elif button is BTN['A_.VolLess'] or button is BTN['B_.VolLess'] or button is BTN['C_.VolLess'] or button is BTN['M_.VolLess']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Vol- Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Vol- Modo Abierto'))
    
    elif button is BTN['A_.VolPlus'] or button is BTN['B_.VolPlus'] or button is BTN['C_.VolPlus'] or button is BTN['M_.VolPlus']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Vol+ Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Vol+ Modo Abierto'))

    elif button is BTN['A_.MuteSpk'] or button is BTN['B_.MuteSpk'] or button is BTN['C_.MuteSpk'] or button is BTN['M_.MuteSpk']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Mute Spk Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Mute Spk Modo Abierto'))

    elif button is BTN['A_.MuteMiM'] or button is BTN['B_.MuteMiM'] or button is BTN['C_.MuteMiM'] or button is BTN['M_.MuteMiM']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Mute Mic Mano Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Mute Mic Mano Modo Abierto'))

    elif button is BTN['A_.MuteMiT'] or button is BTN['B_.MuteMiT'] or button is BTN['C_.MuteMiT'] or button is BTN['M_.MuteMiT']:
        if state == 'Pressed':
            if Room['Mode'] == 'Executive':
                print('Touch: %s' % ('Mute Mic Techo Modo Ejecutivo'))
            elif Room['Mode'] == 'Open':
                print('Touch: %s' % ('Mute Mic Techo Modo Abierto'))
    pass

## End Events Definitions-------------------------------------------------------
initialize()

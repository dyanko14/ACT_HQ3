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
                    TLPM.ShowPopup('x_Welcome')
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
        Room['Mode'] = 'A|B|C' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Index')
        TLP2.ShowPage('Index')
        TLP3.ShowPage('Index')
        TLPM.ShowPage('Main_Individual')
        ## Activate Room Panel Indicators
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
        print('Touch Master: %s' % ('Room Mode A|B|C /All Close'))

    elif button is BTN['M_Mode2'] and state == 'Pressed': #Executive Mode
        Room['Mode'] = 'A-B|C' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Index')
        TLP2.ShowPage('Main_Full')
        TLP3.ShowPage('Main_Full')
        TLPM.ShowPage('Main_Full')
        print('Touch Master: %s' % ('Room Mode A-B|C /Executive'))

    elif button is BTN['M_Mode3'] and state == 'Pressed': #All Open Mode
        Room['Mode'] = 'A-B-C' ##Store in Dictionary
        ## TouchPanel Actions
        TLP1.ShowPage('Main_Full')
        TLP2.ShowPage('Main_Full')
        TLP3.ShowPage('Main_Full')
        TLPM.ShowPage('Main_Full')
        print('Touch Master: %s' % ('Room Mode A|B-C /All Open'))

    ## Mutually Exclusive
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
    #--
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
    #--
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

## Main ------------------------------------------------------------------------
@event(BTNPAGE['Main_F'], BTNSTATE['List'])
def page_main(button, state):
    """User Actions: Touch Main Page"""
    
    ## VIDEO PAGES -----------------------------
    if button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_FVideo'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Video_Full')
            TLP1.ShowPopup('Video_Full')
            TLP2.ShowPopup('Video_Full')
            TLP3.ShowPopup('Video_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FVideo'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FVideo'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FVideo'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FVideo'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Video')
            LBL['A_RoomFull'].SetText('Control de Video')
            LBL['B_RoomFull'].SetText('Control de Video')
            LBL['C_RoomFull'].SetText('Control de Video')
            ## Notify to Console
            print('Touch M: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_FVideo'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Video_Full')
            TLP1.ShowPopup('Video_Full')
            TLP2.ShowPopup('Video_Full')
            TLP3.ShowPopup('Video_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FVideo'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FVideo'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FVideo'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FVideo'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Video')
            LBL['A_RoomFull'].SetText('Control de Video')
            LBL['B_RoomFull'].SetText('Control de Video')
            LBL['C_RoomFull'].SetText('Control de Video')
            ## Notify to Console
            print('Touch A: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_FVideo'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Video_Full')
            TLP1.ShowPopup('Video_Full')
            TLP2.ShowPopup('Video_Full')
            TLP3.ShowPopup('Video_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FVideo'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FVideo'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FVideo'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FVideo'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Video')
            LBL['A_RoomFull'].SetText('Control de Video')
            LBL['B_RoomFull'].SetText('Control de Video')
            LBL['C_RoomFull'].SetText('Control de Video')
            ## Notify to Console
            print('Touch B: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_FVideo'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Video_Full')
            TLP1.ShowPopup('Video_Full')
            TLP2.ShowPopup('Video_Full')
            TLP3.ShowPopup('Video_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FVideo'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FVideo'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FVideo'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FVideo'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Video')
            LBL['A_RoomFull'].SetText('Control de Video')
            LBL['B_RoomFull'].SetText('Control de Video')
            LBL['C_RoomFull'].SetText('Control de Video')
            ## Notify to Console
            print('Touch C: %s' % ('Video A-B-C'))

    ## AUDIO PAGES -----------------------------
    if button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_FAudio'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Audio_Full')
            TLP1.ShowPopup('Audio_Full')
            TLP2.ShowPopup('Audio_Full')
            TLP3.ShowPopup('Audio_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FAudio'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FAudio'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FAudio'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FAudio'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Audio')
            LBL['A_RoomFull'].SetText('Control de Audio')
            LBL['B_RoomFull'].SetText('Control de Audio')
            LBL['C_RoomFull'].SetText('Control de Audio')
            ## Notify to Console
            print('Touch M: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_FAudio'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Audio_Full')
            TLP1.ShowPopup('Audio_Full')
            TLP2.ShowPopup('Audio_Full')
            TLP3.ShowPopup('Audio_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FAudio'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FAudio'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FAudio'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FAudio'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Audio')
            LBL['A_RoomFull'].SetText('Control de Audio')
            LBL['B_RoomFull'].SetText('Control de Audio')
            LBL['C_RoomFull'].SetText('Control de Audio')
            ## Notify to Console
            print('Touch A: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_FAudio'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Audio_Full')
            TLP1.ShowPopup('Audio_Full')
            TLP2.ShowPopup('Audio_Full')
            TLP3.ShowPopup('Audio_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FAudio'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FAudio'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FAudio'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FAudio'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Audio')
            LBL['A_RoomFull'].SetText('Control de Audio')
            LBL['B_RoomFull'].SetText('Control de Audio')
            LBL['C_RoomFull'].SetText('Control de Audio')
            ## Notify to Console
            print('Touch B: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_FAudio'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Audio_Full')
            TLP1.ShowPopup('Audio_Full')
            TLP2.ShowPopup('Audio_Full')
            TLP3.ShowPopup('Audio_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FAudio'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FAudio'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FAudio'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FAudio'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Audio')
            LBL['A_RoomFull'].SetText('Control de Audio')
            LBL['B_RoomFull'].SetText('Control de Audio')
            LBL['C_RoomFull'].SetText('Control de Audio')
            ## Notify to Console
            print('Touch C: %s' % ('Video A-B-C'))

    ## LIGHT PAGES -----------------------------
    if button.Host.DeviceAlias == 'TouchPanelM':
        if button is BTN['M_FLights'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Lights_Full')
            TLP1.ShowPopup('Lights_Full')
            TLP2.ShowPopup('Lights_Full')
            TLP3.ShowPopup('Lights_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FLights'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FLights'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FLights'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FLights'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Luces')
            LBL['A_RoomFull'].SetText('Control de Luces')
            LBL['B_RoomFull'].SetText('Control de Luces')
            LBL['C_RoomFull'].SetText('Control de Luces')
            ## Notify to Console
            print('Touch M: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_FLights'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Lights_Full')
            TLP1.ShowPopup('Lights_Full')
            TLP2.ShowPopup('Lights_Full')
            TLP3.ShowPopup('Lights_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FLights'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FLights'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FLights'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FLights'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Luces')
            LBL['A_RoomFull'].SetText('Control de Luces')
            LBL['B_RoomFull'].SetText('Control de Luces')
            LBL['C_RoomFull'].SetText('Control de Luces')
            ## Notify to Console
            print('Touch A: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_FLights'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Lights_Full')
            TLP1.ShowPopup('Lights_Full')
            TLP2.ShowPopup('Lights_Full')
            TLP3.ShowPopup('Lights_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FLights'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FLights'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FLights'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FLights'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Luces')
            LBL['A_RoomFull'].SetText('Control de Luces')
            LBL['B_RoomFull'].SetText('Control de Luces')
            LBL['C_RoomFull'].SetText('Control de Luces')
            ## Notify to Console
            print('Touch B: %s' % ('Video A-B-C'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_FLights'] and state == 'Pressed':
            ## Show Popup in All Panels
            TLPM.ShowPopup('Lights_Full')
            TLP1.ShowPopup('Lights_Full')
            TLP2.ShowPopup('Lights_Full')
            TLP3.ShowPopup('Lights_Full')
            ## Mutually Exclusive on All Panels
            BTNGROUP['MainFM'].SetCurrent(BTN['M_FLights'])
            BTNGROUP['MainFA'].SetCurrent(BTN['A_FLights'])
            BTNGROUP['MainFB'].SetCurrent(BTN['B_FLights'])
            BTNGROUP['MainFC'].SetCurrent(BTN['C_FLights'])
            ## Notify to all Panels
            LBL['M_RoomFull'].SetText('Control de Luces')
            LBL['A_RoomFull'].SetText('Control de Luces')
            LBL['B_RoomFull'].SetText('Control de Luces')
            LBL['C_RoomFull'].SetText('Control de Luces')
            ## Notify to Console
            print('Touch C: %s' % ('Video A-B-C'))
    pass

## End Events Definitions-------------------------------------------------------
initialize()

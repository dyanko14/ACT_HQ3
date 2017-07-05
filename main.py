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
## RS-232:

print(Version())

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## IP:
## RS-232:

## INITIALIZATE ----------------------------------------------------------------
def initialize():
    """This is the last function that loads when starting the system """
    ## OPEN CONNECTION SOCKETS
    ## IP
    ## RS-232

    ## RECURSIVE FUNCTIONS

    ## POWER COUNTER VARIABLE

    ## DATA INITIALIZE

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
    ## TouchPanel Master Functions
    LBL['M_Index'].SetText('Panel Master')
    LBL['M_Room'].SetText('Panel Master')
    LBL['M_PIN'].SetText('')
    ## TouchPanel Room A Functions
    LBL['A_Index'].SetText('Bienvenido a Sala Everest')
    LBL['A_Room'].SetText('Panel A')
    LBL['A_PIN'].SetText('')
    ## TouchPanel Room B Functions
    LBL['B_Index'].SetText('Bienvenido a Sala Orizaba')
    LBL['B_Room'].SetText('Panel B')
    LBL['B_PIN'].SetText('')
    ## TouchPanel Room C Functions
    LBL['C_Index'].SetText('Bienvenido a Sala Aconcagua')
    LBL['C_Room'].SetText('Panel C')
    LBL['C_PIN'].SetText('')

    TLPM.ShowPage('Index')
    TLPM.HideAllPopups()
    #GroupMainM.SetCurrent(None)

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
                    TLPM.ShowPage('Main')
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

    if button is BTN['M_Room1'] and state == 'Pressed':
        Room['Mode'] = 'A|B|C' ##Store in Dictionary
        TLP1.ShowPage('Index')
        TLP2.ShowPage('Index')
        TLP3.ShowPage('Index')
        BTNGROUP['Room'].SetCurrent(BTN['M_Room1'])
        print('Touch Master: %s' % ('Room Mode A|B|C /All Close'))

    elif button is BTN['M_Room2'] and state == 'Pressed':
        Room['Mode'] = 'A-B|C' ##Store in Dictionary
        TLP1.ShowPage('Inactive')
        TLP2.ShowPage('Inactive')
        TLP3.ShowPage('Index')
        BTNGROUP['Room'].SetCurrent(BTN['M_Room2'])
        print('Touch Master: %s' % ('Room Mode A-B|C /Separed'))
    
    elif button is BTN['M_Room3'] and state == 'Pressed':
        Room['Mode'] = 'A|B-C' ##Store in Dictionary
        TLP1.ShowPage('Index')
        TLP2.ShowPage('Inactive')
        TLP3.ShowPage('Inactive')
        BTNGROUP['Room'].SetCurrent(BTN['M_Room3'])
        print('Touch Master: %s' % ('Room Mode A|B-C /Separed'))   
    
    elif button is BTN['M_Room4'] and state == 'Pressed':
        Room['Mode'] = 'A-B-C' ##Store in Dictionary
        TLP1.ShowPage('Inactive')
        TLP2.ShowPage('Inactive')
        TLP3.ShowPage('Inactive')
        BTNGROUP['Room'].SetCurrent(BTN['M_Room4'])
        print('Touch Master: %s' % ('Room Mode A-B-C /All Open'))
    pass

## Main ------------------------------------------------------------------------
@event(BTNPAGE['Main'], BTNSTATE['List'])
def page_main(button, state):
    """User Actions: Touch Main Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_Video'] and state == 'Pressed':
            A_LblMaster.SetText('Control de Video')
            TLP1.ShowPopup('Video')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Video'])
            print('Touch A: %s' % ('Video'))

        elif button is BTN['A_Audio'] and state == 'Pressed':
            A_LblMaster.SetText('Control de Audio')
            TLP1.ShowPopup('Audio')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Audio'])
            print('Touch A: %s' % ('Audio'))

        elif button is BTN['A_Blinds'] and state == 'Pressed':
            A_LblMaster.SetText('Control de Persianas')
            TLP1.ShowPopup('Persianas')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Blinds'])
            print('Touch A: %s' % ('Persianas'))

        elif button is BTN['A_Lights'] and state == 'Pressed':
            A_LblMaster.SetText('Control de Luces')
            TLP1.ShowPopup('Luces')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Lights'])
            print('Touch A: %s' % ('Luces'))

        elif button is BTN['A_Status'] and state == 'Pressed':
            A_LblMaster.SetText('Información de Dispositivos')
            TLP1.ShowPopup('Status')
            BTNGROUP['MainA'].SetCurrent(BTN['A_Status'])
            print('Touch A: %s' % ('Status'))

        elif button is BTN['A_PwrOff'] and state == 'Pressed':
            A_LblMaster.SetText('Apagado de Sala')
            TLP1.ShowPopup('x_PowerOff')
            BTNGROUP['MainA'].SetCurrent(BTN['A_PwrOff'])
            print('Touch A: %s' % ('PowerOff'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
    #--
        if button is BTN['B_Video'] and state == 'Pressed':
            B_LblMaster.SetText('Control de Video')
            TLP2.ShowPopup('Video')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Video'])
            print('Touch B: %s' % ('Video'))

        elif button is BTN['B_Audio'] and state == 'Pressed':
            B_LblMaster.SetText('Control de Audio')
            TLP2.ShowPopup('Audio')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Audio'])
            print('Touch B: %s' % ('Audio'))

        elif button is B_BtnBlinds and state == 'Pressed':
            B_LblMaster.SetText('Control de Persianas')
            TLP2.ShowPopup('Persianas')
            BTNGROUP['MainB'].SetCurrent(B_BtnBlinds)
            print('Touch B: %s' % ('Persianas'))

        elif button is BTN['B_Lights'] and state == 'Pressed':
            B_LblMaster.SetText('Control de Luces')
            TLP2.ShowPopup('Luces')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Lights'])
            print('Touch B: %s' % ('Luces'))

        elif button is BTN['B_Status'] and state == 'Pressed':
            B_LblMaster.SetText('Información de Dispositivos')
            TLP2.ShowPopup('Status')
            BTNGROUP['MainB'].SetCurrent(BTN['B_Status'])
            print('Touch B: %s' % ('Status'))

        elif button is BTN['B_PwrOff'] and state == 'Pressed':
            B_LblMaster.SetText('Apagado de Sala')
            TLP2.ShowPopup('x_PowerOff')
            BTNGROUP['MainB'].SetCurrent(BTN['B_PwrOff'])
            print('Touch B: %s' % ('PowerOff'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
    #--
        if button is BTN['C_Video'] and state == 'Pressed':
            C_LblMaster.SetText('Control de Video')
            TLP3.ShowPopup('Video')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Video'])
            print('Touch C: %s' % ('Video'))

        elif button is BTN['C_Audio'] and state == 'Pressed':
            C_LblMaster.SetText('Control de Audio')
            TLP3.ShowPopup('Audio')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Audio'])
            print('Touch C: %s' % ('Audio'))

        elif button is BTN['C_Blinds'] and state == 'Pressed':
            C_LblMaster.SetText('Control de Persianas')
            TLP3.ShowPopup('Persianas')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Blinds'])
            print('Touch C: %s' % ('Persianas'))

        elif button is BTN['C_Lights'] and state == 'Pressed':
            C_LblMaster.SetText('Control de Luces')
            TLP3.ShowPopup('Luces')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Lights'])
            print('Touch C: %s' % ('Luces'))

        elif button is BTN['C_Status'] and state == 'Pressed':
            C_LblMaster.SetText('Información de Dispositivos')
            TLP3.ShowPopup('Status')
            BTNGROUP['MainC'].SetCurrent(BTN['C_Status'])
            print('Touch C: %s' % ('Status'))

        elif button is BTN['C_PwrOff'] and state == 'Pressed':
            C_LblMaster.SetText('Apagado de Sala')
            TLP3.ShowPopup('x_PowerOff')
            BTNGROUP['MainC'].SetCurrent(BTN['C_PwrOff'])
            print('Touch C: %s' % ('PowerOff'))
    pass

## Video -----------------------------------------------------------------------
@event(BTNPAGE['Video'], BTNSTATE['List'])
def page_video(button, state):
    """User Actions: Touch Video Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_VHDMI'] and state == 'Pressed':
            print('Touch A: %s' % ('HDMI'))
        elif button is BTN['A_VShare'] and state == 'Pressed':
            print('Touch A: %s' % ('ShareLink'))
        elif button is BTN['A_VPwrOn'] and state == 'Pressed':
            print('Touch A: %s' % ('PowerOn'))
        elif button is BTN['A_VPwrOff'] and state == 'Pressed':
            print('Touch A: %s' % ('PowerOff'))
        elif button is BTN['A_Up'] and state == 'Pressed':
            BTNGROUP['VideoA'].SetCurrent(BTN['A_Up'])
            print('Touch A: %s' % ('Screen Up'))
        elif button is BTN['A_Stop'] and state == 'Pressed':
            BTNGROUP['VideoA'].SetCurrent(BTN['A_Stop'])
            print('Touch A: %s' % ('Screen Stop'))
        elif button is BTN['A_Down'] and state == 'Pressed':
            BTNGROUP['VideoA'].SetCurrent(BTN['A_Down'])
            print('Touch A: %s' % ('Screen Down'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_VHDMI'] and state == 'Pressed':
            print('Touch B: %s' % ('HDMI'))
        elif button is BTN['B_VShare'] and state == 'Pressed':
            print('Touch B: %s' % ('ShareLink'))
        elif button is BTN['B_VPwrOn'] and state == 'Pressed':
            print('Touch B: %s' % ('PowerOn'))
        elif button is BTN['B_VPwrOff'] and state == 'Pressed':
            print('Touch B: %s' % ('PowerOff'))
        elif button is BTN['B_Up'] and state == 'Pressed':
            BTNGROUP['VideoB'].SetCurrent(BTN['B_Up'])
            print('Touch B: %s' % ('Screen Up'))
        elif button is BTN['B_Stop'] and state == 'Pressed':
            BTNGROUP['VideoB'].SetCurrent(BTN['B_Stop'])
            print('Touch B: %s' % ('Screen Stop'))
        elif button is BTN['B_Down'] and state == 'Pressed':
            BTNGROUP['VideoB'].SetCurrent(BTN['B_Down'])
            print('Touch B: %s' % ('Screen Down'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_VHDMI'] and state == 'Pressed':
            print('Touch C: %s' % ('HDMI'))
        elif button is BTN['C_VShare'] and state == 'Pressed':
            print('Touch C: %s' % ('ShareLink'))
        elif button is BTN['C_VPwrOn'] and state == 'Pressed':
            print('Touch C: %s' % ('PowerOn'))
        elif button is BTN['C_VPwrOff'] and state == 'Pressed':
            print('Touch C: %s' % ('PowerOff'))
        elif button is BTN['C_Up'] and state == 'Pressed':
            BTNGROUP['VideoC'].SetCurrent(BTN['C_Up'])
            print('Touch C: %s' % ('Screen Up'))
        elif button is BTN['C_Stop'] and state == 'Pressed':
            BTNGROUP['VideoC'].SetCurrent(BTN['C_Stop'])
            print('Touch C: %s' % ('Screen Stop'))
        elif button is BTN['C_Down'] and state == 'Pressed':
            BTNGROUP['VideoC'].SetCurrent(BTN['C_Down'])
            print('Touch C: %s' % ('Screen Down'))
    pass

## Audio -----------------------------------------------------------------------
@event(BTNPAGE['Audio'], BTNSTATE['List'])
def page_audio(button, state):
    """User Actions: Touch Audio Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_VolLess'] and state == 'Pressed':
            BTN['A_VolLess'].SetState(1)
            print('Touch A: %s' % ('Audio -'))
        elif button is BTN['A_VolLess'] and state == 'Repeated':
            BTN['A_VolLess'].SetState(1)
            print('Touch A: %s' % ('Audio -'))        
        else:
            BTN['A_VolLess'].SetState(0)
        #--
        if button is BTN['A_VolPlus'] and state == 'Pressed':
            BTN['A_VolPlus'].SetState(1)
            print('Touch A: %s' % ('Audio +'))
        if button is BTN['A_VolPlus'] and state == 'Repeated':
            BTN['A_VolPlus'].SetState(1)
            print('Touch A: %s' % ('Audio +'))
        else:
            BTN['A_VolPlus'].SetState(0)
        #--
        if button is A_BtnMute and state == 'Pressed':
            print('Touch A: %s' % ('Audio Mute'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_VolLess'] and state == 'Pressed':
            BTN['B_VolLess'].SetState(1)
            print('Touch B: %s' % ('Audio -'))
        elif button is BTN['B_VolLess'] and state == 'Repeated':
            BTN['B_VolLess'].SetState(1)
            print('Touch B: %s' % ('Audio -'))        
        else:
            BTN['B_VolLess'].SetState(0)
        #--
        if button is BTN['B_VolPlus'] and state == 'Pressed':
            BTN['B_VolPlus'].SetState(1)
            print('Touch B: %s' % ('Audio +'))
        if button is BTN['B_VolPlus'] and state == 'Repeated':
            BTN['B_VolPlus'].SetState(1)
            print('Touch B: %s' % ('Audio +'))
        else:
            BTN['B_VolPlus'].SetState(0)
        #--
        if button is B_BtnMute and state == 'Pressed':
            print('Touch B: %s' % ('Audio Mute'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_VolLess'] and state == 'Pressed':
            BTN['C_VolLess'].SetState(1)
            print('Touch C: %s' % ('Audio -'))
        elif button is BTN['C_VolLess'] and state == 'Repeated':
            BTN['C_VolLess'].SetState(1)
            print('Touch C: %s' % ('Audio -'))        
        else:
            BTN['C_VolLess'].SetState(0)
        #--
        if button is BTN['C_VolPlus'] and state == 'Pressed':
            BTN['C_VolPlus'].SetState(1)
            print('Touch C: %s' % ('Audio +'))
        if button is BTN['C_VolPlus'] and state == 'Repeated':
            BTN['C_VolPlus'].SetState(1)
            print('Touch C: %s' % ('Audio +'))
        else:
            BTN['C_VolPlus'].SetState(0)
        #--
        if button is C_BtnMute and state == 'Pressed':
            print('Touch C: %s' % ('Audio Mute'))
    pass

## Persianas -------------------------------------------------------------------
@event(BTNPAGE['Blinds'], BTNSTATE['List'])
def page_blinds(button, state):
    """User Actions: Touch Blinds Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_BUp'] and state == 'Pressed':
            BTNGROUP['BlindsA'].SetCurrent(BTN['A_BUp'])
            print('Touch A: %s' % ('Persianas Up'))
        elif button is BTN['A_BStop'] and state == 'Pressed':
            BTNGROUP['BlindsA'].SetCurrent(BTN['A_BStop'])
            print('Touch A: %s' % ('Persianas Stop'))
        elif button is BTN['A_BDown'] and state == 'Pressed':
            BTNGROUP['BlindsA'].SetCurrent(BTN['A_BDown'])
            print('Touch A: %s' % ('Persianas Down'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_BUp'] and state == 'Pressed':
            BTNGROUP['BlindsB'].SetCurrent(BTN['B_BUp'])
            print('Touch B: %s' % ('Persianas Up'))
        elif button is BTN['B_BStop'] and state == 'Pressed':
            BTNGROUP['BlindsB'].SetCurrent(BTN['B_BStop'])
            print('Touch B: %s' % ('Persianas Stop'))
        elif button is BTN['B_BDown'] and state == 'Pressed':
            BTNGROUP['BlindsB'].SetCurrent(BTN['B_BDown'])
            print('Touch B: %s' % ('Persianas Down'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_BUp'] and state == 'Pressed':
            BTNGROUP['BlindsC'].SetCurrent(BTN['C_BUp'])
            print('Touch C: %s' % ('Persianas Up'))
        elif button is BTN['C_BStop'] and state == 'Pressed':
            BTNGROUP['BlindsC'].SetCurrent(BTN['C_BStop'])
            print('Touch C: %s' % ('Persianas Stop'))
        elif button is BTN['C_BDown'] and state == 'Pressed':
            BTNGROUP['BlindsC'].SetCurrent(BTN['C_BDown'])
            print('Touch C: %s' % ('Persianas Down'))
    pass

## Lights ----------------------------------------------------------------------
@event(BTNPAGE['Lights'], BTNSTATE['List'])
def page_lights(button, state):
    """User Actions: Touch Lights Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_LightOn'] and state == 'Pressed':
            BTNGROUP['LightsA'].SetCurrent(BTN['A_LightOn'])
            print('Touch A: %s' % ('Lights On'))
        elif button is BTN['A_LightOf'] and state == 'Pressed':
            BTNGROUP['LightsA'].SetCurrent(BTN['A_LightOf'])
            print('Touch A: %s' % ('Lights Off'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_LightOn'] and state == 'Pressed':
            BTNGROUP['LightsB'].SetCurrent(BTN['B_LightOn'])
            print('Touch B: %s' % ('Lights On'))
        elif button is BTN['B_LightOf'] and state == 'Pressed':
            BTNGROUP['LightsB'].SetCurrent(BTN['B_LightOf'])
            print('Touch B: %s' % ('Lights Off'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_LightOn'] and state == 'Pressed':
            BTNGROUP['LightsC'].SetCurrent(BTN['C_LightOn'])
            print('Touch C: %s' % ('Lights On'))
        elif button is BTN['C_LightOf'] and state == 'Pressed':
            BTNGROUP['LightsC'].SetCurrent(BTN['C_LightOf'])
            print('Touch C: %s' % ('Lights Off'))
    pass

## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------
@event(BTNPAGE['PowerAll'], BTNSTATE['List'])
def page_power_all(button, state):
    """User Actions: Touch Power Page"""

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is BTN['A_PwrAll'] and state == 'Pressed':
            print('Touch A: %s' % ('PowerAll Pressed'))
        elif button is BTN['A_PwrAll'] and state == 'Held':
            TLP1.HideAllPopups()
            TLP1.ShowPage('Index')
            print('Touch A: %s' % ('PowerAll Ok'))

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is BTN['B_PwrAll'] and state == 'Pressed':
            print('Touch B: %s' % ('PowerAll Pressed'))
        elif button is BTN['B_PwrAll'] and state == 'Held':
            TLP2.HideAllPopups()
            TLP2.ShowPage('Index')
            print('Touch B: %s' % ('PowerAll Ok'))

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is BTN['C_PwrAll'] and state == 'Pressed':
            print('Touch C: %s' % ('PowerAll Pressed'))
        elif button is BTN['C_PwrAll'] and state == 'Held':
            TLP3.HideAllPopups()
            TLP3.ShowPage('Index')
            print('Touch C: %s' % ('PowerAll Ok'))
    pass
## End Events Definitions-------------------------------------------------------
initialize()

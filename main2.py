## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

# UI Device
TLPM = UIDevice('TouchPanelM')
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
TLP3 = UIDevice('TouchPanelC')

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin User Import -----------------------------------------------------------

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------

## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------

## End Communication Interface Definition --------------------------------------

def Initialize():
    ## DATA INITIALIZE
    global PWRCOUNT
    PWRCOUNT = 3

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

    global Panels, Touch
    Panels = [TLP1, TLP2, TLP3, TLPM]
    
    ## TOUCH PANEL FUNCTIONS
    ##Index Page
    for Touch in Panels:
        Touch.HideAllPopups()
        Touch.ShowPage('Index')
    ## TouchPanel Master
    Label(TLPM, 2).SetText('Panel Master') #Index Label
    Label(TLPM, 1012).SetText('') #PIN Label
    ## TouchPanel Room A
    Label(TLP1, 2).SetText('Bienvenido a Sala Everest') #Index Label
    Label(TLP1, 21).SetText('Panel A') #Main Individual Label
    Label(TLP1, 1012).SetText('') #PIN Label
    ## TouchPanel Room B
    Label(TLP2, 2).SetText('Bienvenido a Sala Orizaba') #Index Label
    Label(TLP2, 21).SetText('Panel B') #Main Individual Label
    Label(TLP2, 1012).SetText('') #PIN Label
    ## TouchPanel Room C
    Label(TLP3, 2).SetText('Bienvenido a Sala Aconcagua') #Index Label
    Label(TLP3, 21).SetText('Panel C') #Main Individual Label
    Label(TLP3, 1012).SetText('') #PIN Label
    pass

## Event Definitions -----------------------------------------------------------
Room = {
    'Mode' : '',
}

## Individual Index ------------------------------------------------------------
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

Index = [Button(TLPM, 1), Button(TLP1, 1), Button(TLP2, 1), Button(TLP3, 1)]

@event(Index, ButtonEventList)
def index_events(button, state):
    """First Panel Page"""
    if state == 'Pressed':
        if button.Host.DeviceAlias == 'TouchPanelM':
            TLPM.ShowPopup('PIN')
            print("Touch M: {0}".format("Index"))
        
        elif button.Host.DeviceAlias == 'TouchPanelA':
            TLP1.ShowPopup('PIN')
            print("Touch A: {0}".format("Index"))
        
        elif button.Host.DeviceAlias == 'TouchPanelB':
            TLP2.ShowPopup('PIN')
            print("Touch B: {0}".format("Index"))
        
        elif button.Host.DeviceAlias == 'TouchPanelC':
            TLP3.ShowPopup('PIN')
            print("Touch C: {0}".format("Index"))
    pass

## PIN Validation --------------------------------------------------------------
## Dynamic Buttons Assignement
global ID, M_PIN, A_PIN, B_PIN, C_PIN
M_PIN = []
A_PIN = []
B_PIN = []
C_PIN = []

for ID in range(1000, 1012):
    M_PIN.append(Button(TLPM, ID))

for ID in range(1000, 1012):
    A_PIN.append(Button(TLP1, ID))

for ID in range(1000, 1012):
    B_PIN.append(Button(TLP2, ID))

for ID in range(1000, 1012):
    C_PIN.append(Button(TLP3, ID))

## PIN A------------------------------------------------------------------------
def PINValidationA(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch A Validation"""
    global Pin_A, Pin_A_GUI
    LblA_PIN = Label(TLP1, 1012)
    
    if Pin_Button == 'PINDelete':
        if len(Pin_A) > 0:              #If the list have data
            Pin_A.pop()                 #Delete the last number of the list
            Pin_A_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_A)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_A_GUI) #Convert the list to cleaned string data
            LblA_PIN.SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP1.HidePopup('PIN')           #Show the Index Page
        Pin_A = []                      #Erase each items in list [0-9]
        Pin_A_GUI = []                  #Erase each items in list [****]
        LblA_PIN.SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_A) >= 0 and len(Pin_A) <= 3: #Ej= '1234'
            #--
            Pin_A.append(Number)        #Append the last number to internal list
            Pin_A_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_A)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_A_GUI) #Convert the list to cleaned string data
            LblA_PIN.SetText(Clean2)    #Send the final '*' string to Panel
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
                    LblA_PIN.SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LblA_PIN.SetText('')
    pass

## PIN B -----------------------------------------------------------------------
def PINValidationB(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch B Validation"""
    global Pin_B, Pin_B_GUI
    LblB_PIN = Label(TLP2, 1012)

    if Pin_Button == 'PINDelete':
        if len(Pin_B) > 0:              #If the list have data
            Pin_B.pop()                 #Delete the last number of the list
            Pin_B_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_B)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_B_GUI) #Convert the list to cleaned string data
            LblB_PIN.SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP2.HidePopup('PIN')           #Show the Index Page
        Pin_B = []                      #Erase each items in list [0-9]
        Pin_B_GUI = []                  #Erase each items in list [****]
        LblB_PIN.SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_B) >= 0 and len(Pin_B) <= 3: #Ej= '1234'
            #--
            Pin_B.append(Number)        #Append the last number to internal list
            Pin_B_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_B)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_B_GUI) #Convert the list to cleaned string data
            LblB_PIN.SetText(Clean2)    #Send the final '*' string to Panel
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
                    LblB_PIN.SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LblB_PIN.SetText('')
    pass

## PIN C -----------------------------------------------------------------------
def PINValidationC(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch C Validation"""
    global Pin_C, Pin_C_GUI
    LblC_PIN = Label(TLP3, 1012)

    if Pin_Button == 'PINDelete':
        if len(Pin_C) > 0:              #If the list have data
            Pin_C.pop()                 #Delete the last number of the list
            Pin_C_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_C)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_C_GUI) #Convert the list to cleaned string data
            LblC_PIN.SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLP3.HidePopup('PIN')           #Show the Index Page
        Pin_C = []                      #Erase each items in list [0-9]
        Pin_C_GUI = []                  #Erase each items in list [****]
        LblC_PIN.SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_C) >= 0 and len(Pin_C) <= 3: #Ej= '1234'
            #--
            Pin_C.append(Number)        #Append the last number to internal list
            Pin_C_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_C)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_C_GUI) #Convert the list to cleaned string data
            LblC_PIN.SetText(Clean2)    #Send the final '*' string to Panel
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
                    LblC_PIN.SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LblC_PIN.SetText('')
    pass

## PIN Master ------------------------------------------------------------------
def PINValidationM(Pin_Button): #This validate the PIN Security Panel
    """User Actions: PIN Touch M Validation"""
    global Pin_M, Pin_M_GUI
    LblM_PIN = Label(TLPM, 1012)

    if Pin_Button == 'PINDelete':
        if len(Pin_M) > 0:              #If the list have data
            Pin_M.pop()                 #Delete the last number of the list
            Pin_M_GUI.pop()             #Delete the last '*' of the list
            Clean  = "".join(Pin_M)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_M_GUI) #Convert the list to cleaned string data
            LblM_PIN.SetText(Clean2)    #Send the final '*' string to Panel            
        else:
            print('Empty List')         #Notify to console

    elif Pin_Button == 'PINExit':
        TLPM.HidePopup('PIN')           #Show the Index Page
        Pin_M = []                      #Erase each items in list [0-9]
        Pin_M_GUI = []                  #Erase each items in list [****]
        LblM_PIN.SetText('')            #Erase each items in panel

    else:                                       #If the user push a number [0-9]:
        Number = str(Pin_Button[3])             #Extract the number of btn name
        if len(Pin_M) >= 0 and len(Pin_M) <= 3: #Ej= '1234'
            #--
            Pin_M.append(Number)        #Append the last number to internal list
            Pin_M_GUI.append('*')       #Append a '*' instead a number in Panel
            Clean  = "".join(Pin_M)     #Convert the list to cleaned string data
            Clean2 = "".join(Pin_M_GUI) #Convert the list to cleaned string data
            LblM_PIN.SetText(Clean2)    #Send the final '*' string to Panel
            #--
            if len(Clean) == 4:           #If user type all numbers in the Panel
                if Clean == Pin_M_Secret: #If User enter the secret PIN:
                    TLPM.HideAllPopups()  #Panel actions:
                    TLPM.ShowPage('Main_Individual')
                    TLPM.ShowPopup('1_Master')
                else:                    #If User enter incorrect PIN:
                    print('Full List')   #Notify to console
                    Pin_M = []           #Erase each items in list [0-9]
                    Pin_M_GUI = []       #Erase each items in list [****]
                    LblM_PIN.SetText('Incorrect') #Show error msj to Panel
                    @Wait(1)                      #Wait 1s
                    def EraseText():              #Erase data from Panel
                        LblM_PIN.SetText('')
    pass

## PIN Page --------------------------------------------------------------------
@event(M_PIN + A_PIN + B_PIN + C_PIN, ButtonEventList) #M_PIN = |[0-9]|Delete|Exit
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



## Global Room Select Master Panel ---------------------------------------------
## Dynamic Buttons Assignement
global ID, M_Room
M_Room = []
for ID in range(401, 404):
    M_Room.append(Button(TLPM, ID))
GroupRoom = MESet(M_Room)


## Dynamic Buttons Assignement
global ID, A_Main, B_Main2, C_Main3, M_Main
A_Main = []
B_Main = []
C_Main = []
#
for ID in range(11, 15):
    A_Main.append(Button(TLP1, ID))
for ID in range(11, 15):
    B_Main.append(Button(TLP2, ID))
for ID in range(11, 15):
    C_Main.append(Button(TLP3, ID))
#
GroupMainA = MESet(A_Main)
GroupMainB = MESet(B_Main)
GroupMainC = MESet(C_Main)

@event(M_Room, ButtonEventList)
def room_master_events(button, state):
    """User Actions: Touch Room Page"""
    if state == 'Pressed':
        if button.ID == 401: #INDIVIDUAL MODE
            Room['Mode'] = 'Close' ##Store in Dictionary
            ## TouchPanel Actions
            for Touch in [TLP1, TLP2, TLP3]:
                Touch.ShowPage('Index')
            TLPM.ShowPage('Main_Individual')
            ##
            for Touch in [TLP1, TLP2, TLP3]:
                Touch.ShowPopup('x_Welcome')
            TLPM.ShowPopup('1_Master')
            ## TurnOff Mutually Exclusive
            GroupMainA.SetCurrent(None)
            GroupMainB.SetCurrent(None)
            GroupMainC.SetCurrent(None)
            ## Activate Room Panel Main Indicators
            ## Panel A
            Button(TLP1, 22).SetState(1) #Room A - Indicator
            Button(TLP1, 23).SetState(0) #Room B - Indicator
            Button(TLP1, 24).SetState(0) #Room C - Indicator
            ## Panel B
            Button(TLP2, 22).SetState(0) #Room A - Indicator
            Button(TLP2, 23).SetState(1) #Room B - Indicator
            Button(TLP2, 24).SetState(0) #Room C - Indicator
            ## Panel C
            Button(TLP3, 22).SetState(0) #Room A - Indicator
            Button(TLP3, 23).SetState(0) #Room B - Indicator
            Button(TLP3, 24).SetState(1) #Room C - Indicator
            ## Activate Room Panel Main Full Indicators
            ## Panel M
            Button(TLPM, 122).SetState(0) #Room A - Indicator
            Button(TLPM, 123).SetState(0) #Room B - Indicator
            Button(TLPM, 124).SetState(0) #Room C - Indicator
            ## Panel A
            Button(TLP1, 122).SetState(0) #Room A - Indicator
            Button(TLP1, 123).SetState(0) #Room B - Indicator
            Button(TLP1, 124).SetState(0) #Room C - Indicator
            ## Panel B
            Button(TLP2, 122).SetState(0) #Room A - Indicator
            Button(TLP2, 123).SetState(0) #Room B - Indicator
            Button(TLP2, 124).SetState(0) #Room C - Indicator
            ## Panel C
            Button(TLP3, 122).SetState(0) #Room A - Indicator
            Button(TLP3, 123).SetState(0) #Room B - Indicator
            Button(TLP3, 124).SetState(0) #Room C - Indicator
            print('Touch Master: %s' % ('Room Mode A|B|C All Close'))

        elif button.ID == 402: #EXECUTIVE MODE
            Room['Mode'] = 'Executive' ##Store in Dictionary
            ## TouchPanel Actions
            for Touch in [TLP1, TLP2, TLPM]:
                Touch.ShowPage('Main_Full')
            TLP3.ShowPage('Index')
            ##
            for Touch in [TLP1, TLP2, TLPM]:
                Touch.ShowPopup('x_Welcome_Full')
            TLP3.ShowPopup('x_Welcome')

            ## TurnOff Mutually Exclusive
            """BTNGROUP['MainFA'].SetCurrent(None)
            BTNGROUP['MainFB'].SetCurrent(None)
            BTNGROUP['MainFC'].SetCurrent(None)
            BTNGROUP['MainFM'].SetCurrent(None)"""
            ## Activate Room Panel Main Indicators
            ## Panel A
            Button(TLP1, 22).SetState(0) #Room A - Indicator
            Button(TLP1, 23).SetState(0) #Room B - Indicator
            Button(TLP1, 24).SetState(0) #Room C - Indicator
            ## Panel B
            Button(TLP2, 22).SetState(0) #Room A - Indicator
            Button(TLP2, 23).SetState(0) #Room B - Indicator
            Button(TLP2, 24).SetState(0) #Room C - Indicator
            ## Panel C
            Button(TLP3, 22).SetState(0) #Room A - Indicator
            Button(TLP3, 23).SetState(0) #Room B - Indicator
            Button(TLP3, 24).SetState(1) #Room C - Indicator
            ## Activate Room Panel Main Full Indicators
            ## Panel M
            Button(TLPM, 122).SetState(1) #Room A - Indicator
            Button(TLPM, 123).SetState(1) #Room B - Indicator
            Button(TLPM, 124).SetState(0) #Room C - Indicator
            ## Panel A
            Button(TLP1, 122).SetState(1) #Room A - Indicator
            Button(TLP1, 123).SetState(1) #Room B - Indicator
            Button(TLP1, 124).SetState(0) #Room C - Indicator
            ## Panel B
            Button(TLP2, 122).SetState(1) #Room A - Indicator
            Button(TLP2, 123).SetState(1) #Room B - Indicator
            Button(TLP2, 124).SetState(0) #Room C - Indicator
            ## Panel C
            Button(TLP3, 122).SetState(0) #Room A - Indicator
            Button(TLP3, 123).SetState(0) #Room B - Indicator
            Button(TLP3, 124).SetState(1) #Room C - Indicator
            print('Touch Master: %s' % ('Room Mode A-B|C Executive'))

        elif button.ID == 403: #ALL OPEN MODE
            Room['Mode'] = 'Open' ##Store in Dictionary
            ## TouchPanel Actions
            for Touch in [TLP1, TLP2, TLP3, TLPM]:
                Touch.ShowPage('Main_Full')
            ##
            for Touch in [TLP1, TLP2, TLP3, TLPM]:
                Touch.ShowPopup('x_Welcome_Full')
            ## TurnOff Mutually Exclusive
            """BTNGROUP['MainFA'].SetCurrent(None)
            BTNGROUP['MainFB'].SetCurrent(None)
            BTNGROUP['MainFC'].SetCurrent(None)
            BTNGROUP['MainFM'].SetCurrent(None)"""
            ## Activate Room Panel Main Full Indicators
            ## Panel M
            Button(TLPM, 122).SetState(1) #Room A - Indicator
            Button(TLPM, 123).SetState(1) #Room B - Indicator
            Button(TLPM, 124).SetState(1) #Room C - Indicator
            ## Panel A
            Button(TLP1, 122).SetState(1) #Room A - Indicator
            Button(TLP1, 123).SetState(1) #Room B - Indicator
            Button(TLP1, 124).SetState(1) #Room C - Indicator
            ## Panel B
            Button(TLP2, 122).SetState(1) #Room A - Indicator
            Button(TLP2, 123).SetState(1) #Room B - Indicator
            Button(TLP2, 124).SetState(1) #Room C - Indicator
            ## Panel C
            Button(TLP3, 122).SetState(1) #Room A - Indicator
            Button(TLP3, 123).SetState(1) #Room B - Indicator
            Button(TLP3, 124).SetState(1) #Room C - Indicator
            print('Touch Master: %s' % ('Room Mode A|B-C /All Open'))
    ## Mutually Exclusive Room Preset Buttons
    GroupRoom.SetCurrent(button)
    pass

## Individual Main -------------------------------------------------------------

## Main Page Help Functions
def MainEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global ID, Group

    if DeviceAlias == 'TouchPanelM':
        DeviceAlias = TLPM
        ID = 'M'

    elif DeviceAlias == 'TouchPanelA':
        DeviceAlias = TLP1
        ID = 'A'

    elif DeviceAlias == 'TouchPanelB':
        DeviceAlias = TLP2
        ID = 'B'

    elif DeviceAlias == 'TouchPanelC':
        DeviceAlias = TLP3
        ID = 'C'
    #
    if IDButton == 11:
        Label(DeviceAlias, 21).SetText('Control de Video')
        DeviceAlias.ShowPopup('Video')
        print('Touch %s: Video' % (ID))

    elif IDButton == 12:
        Label(DeviceAlias, 21).SetText('Control de Audio')
        DeviceAlias.ShowPopup('Audio')
        print('Touch %s: Audio' % (ID))

    elif IDButton == 13:
        Label(DeviceAlias, 21).SetText('Control de Luces')
        DeviceAlias.ShowPopup('Lights')
        print('Touch %s: Lights' % (ID))

    elif IDButton == 14:
        Label(DeviceAlias, 21).SetText('Control de Apagado')
        DeviceAlias.ShowPopup('x_PowerOff')
        print('Touch %s: PowerOff' % (ID))

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_Main + B_Main + C_Main, ButtonEventList)
def room_master_events(button, state):
    """User Actions: Touch Main Page"""
    if state == 'Pressed':
        MainEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass
## Individual Video ------------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_Video, B_Video, C_Video
A_Video = []
B_Video = []
C_Video = []
for ID in range(31, 40):
    A_Video.append(Button(TLP1, ID))
for ID in range(31, 40):
    B_Video.append(Button(TLP2, ID))
for ID in range(31, 40):
    C_Video.append(Button(TLP3, ID))

## Main Page Help Functions
def VideoEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global ID, Group

    if DeviceAlias == 'TouchPanelM':
        DeviceAlias = TLPM
        ID = 'M'

    elif DeviceAlias == 'TouchPanelA':
        DeviceAlias = TLP1
        ID = 'A'

    elif DeviceAlias == 'TouchPanelB':
        DeviceAlias = TLP2
        ID = 'B'

    elif DeviceAlias == 'TouchPanelC':
        DeviceAlias = TLP3
        ID = 'C'
    #
    if IDButton == 31:
        print('Touch %s: HDMI' % (ID))

    elif IDButton == 32:
        print('Touch %s: ShareLink' % (ID))

    elif IDButton == 35:
        print('Touch %s: PowerOn' % (ID))

    elif IDButton == 36:
        print('Touch %s: PowerOFF' % (ID))

    elif IDButton == 37:
        print('Touch %s: ScreenUp' % (ID))

    elif IDButton == 38:
        print('Touch %s: ScreenStop' % (ID))

    elif IDButton == 39:
        print('Touch %s: ScreenDown' % (ID))

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_Video + B_Video + C_Video, ButtonEventList)
def video_events(button, state):
    """User Actions: Touch Video Page"""
    if state == 'Pressed':
        VideoEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass
## Individual Audio -------------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_Audio, B_Audio, C_Audio
A_Audio = []
B_Audio = []
C_Audio = []
for ID in range(41, 44):
    A_Audio.append(Button(TLP1, ID))
for ID in range(41, 44):
    B_Audio.append(Button(TLP2, ID))
for ID in range(41, 44):
    C_Audio.append(Button(TLP3, ID))

## Main Page Help Functions
def AudioEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global ID, Group

    if DeviceAlias == 'TouchPanelM':
        DeviceAlias = TLPM
        ID = 'M'

    elif DeviceAlias == 'TouchPanelA':
        DeviceAlias = TLP1
        ID = 'A'

    elif DeviceAlias == 'TouchPanelB':
        DeviceAlias = TLP2
        ID = 'B'

    elif DeviceAlias == 'TouchPanelC':
        DeviceAlias = TLP3
        ID = 'C'
    #
    if IDButton == 41:
        print('Touch %s: Vol-' % (ID))

    elif IDButton == 42:
        print('Touch %s: Vol+' % (ID))

    elif IDButton == 43:
        print('Touch %s: Mute' % (ID))
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_Audio + B_Audio + C_Audio, ButtonEventList)
def audio_events(button, state):
    """User Actions: Touch Audio Page"""
    if state == 'Pressed':
        AudioEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass
## Individual Lights -----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_Lights, B_Lights, C_Lights
A_Lights = []
B_Lights = []
C_Lights = []
for ID in range(51, 58):
    A_Lights.append(Button(TLP1, ID))
for ID in range(51, 58):
    B_Lights.append(Button(TLP2, ID))
for ID in range(51, 58):
    C_Lights.append(Button(TLP3, ID))

## Main Page Help Functions
def LightsEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global ID, Group

    if DeviceAlias == 'TouchPanelM':
        DeviceAlias = TLPM
        ID = 'M'

    elif DeviceAlias == 'TouchPanelA':
        DeviceAlias = TLP1
        ID = 'A'

    elif DeviceAlias == 'TouchPanelB':
        DeviceAlias = TLP2
        ID = 'B'

    elif DeviceAlias == 'TouchPanelC':
        DeviceAlias = TLP3
        ID = 'C'
    #
    if IDButton == 51:
        print('Touch %s: Escene 1' % (ID))

    elif IDButton == 52:
        print('Touch %s: Escene 2' % (ID))

    elif IDButton == 53:
        print('Touch %s: Escene 3' % (ID))

    elif IDButton == 54:
        print('Touch %s: Escene 4' % (ID))

    elif IDButton == 55:
        print('Touch %s: Blinds Up' % (ID))

    elif IDButton == 56:
        print('Touch %s: Blinds Stop' % (ID))

    elif IDButton == 57:
        print('Touch %s: Blinds Down' % (ID))

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_Lights + B_Lights + C_Lights, ButtonEventList)
def audio_events(button, state):
    """User Actions: Touch Audio Page"""
    if state == 'Pressed':
        LightsEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Individual PowerOff ---------------------------------------------------------
A_Power = Button(TLP1, 61, repeatTime=1)
B_Power = Button(TLP2, 61, repeatTime=1)
C_Power = Button(TLP3, 61, repeatTime=1)

@event([A_Power, B_Power, C_Power], ButtonEventList)
def power_events(button, state):
    """User Actions: Touch Power Page"""
    print(state)
    global PWRCOUNT

    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_Power and state == 'Pressed':
            button.SetState(3)
            Label(TLP1, 63).SetText('3')
            print('Touch A: Pressed PowerOff')
        elif button is A_Power and state == 'Repeated':
            print(PWRCOUNT)
            PWRCOUNT = PWRCOUNT - 1
            button.SetState(PWRCOUNT)
            Label(TLP1, 63).SetText(str(PWRCOUNT))
            print('Touch A: Repeated PowerOff')
            if PWRCOUNT == 0:
                TLP1.ShowPage('Index')
        elif button is A_Power and state == 'Released':
            PWRCOUNT = 4
            button.SetState(0)
            Label(TLP1, 63).SetText('')
            print('Touch A: Released PowerOff')

    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_Power and state == 'Pressed':
            button.SetState(3)
            Label(TLP2, 63).SetText('3')
            print('Touch B: Pressed PowerOff')
        elif button is B_Power and state == 'Repeated':
            print(PWRCOUNT)
            PWRCOUNT = PWRCOUNT - 1
            button.SetState(PWRCOUNT)
            Label(TLP2, 63).SetText(str(PWRCOUNT))
            print('Touch B: Repeated PowerOff')
            if PWRCOUNT == 0:
                TLP2.ShowPage('Index')
        elif button is B_Power and state == 'Released':
            PWRCOUNT = 4
            button.SetState(0)
            Label(TLP3, 63).SetText('')
            print('Touch C: Released PowerOff')

    elif button.Host.DeviceAlias == 'TouchPanelC':
        if button is C_Power and state == 'Pressed':
            button.SetState(3)
            Label(TLP3, 63).SetText('3')
            print('Touch C: Pressed PowerOff')
        elif button is C_Power and state == 'Repeated':
            print(PWRCOUNT)
            PWRCOUNT = PWRCOUNT - 1
            button.SetState(PWRCOUNT)
            Label(TLP3, 63).SetText(str(PWRCOUNT))
            print('Touch C: Repeated PowerOff')
            if PWRCOUNT == 0:
                TLP3.ShowPage('Index')
        elif button is C_Power and state == 'Released':
            PWRCOUNT = 4
            button.SetState(0)
            Label(TLP3, 63).SetText('')
            print('Touch C: Released PowerOff')
    pass

## Main Full Mode -------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullMain, B_FullMain, C_FullMain, M_FullMain
A_FullMain = []
B_FullMain = []
C_FullMain = []
M_FullMain = [Button(TLPM, 400)]
#
for ID in range(111, 116):
    A_FullMain.append(Button(TLP1, ID))
for ID in range(111, 116):
    B_FullMain.append(Button(TLP2, ID))
for ID in range(111, 116):
    C_FullMain.append(Button(TLP3, ID))
for ID in range(111, 116):
    M_FullMain.append(Button(TLPM, ID))
#
GroupMainA = MESet(A_FullMain)
GroupMainB = MESet(B_FullMain)
GroupMainC = MESet(C_FullMain)
GroupMainM = MESet(M_FullMain)
## Main Page Help Functions
def MainFullEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global Touch, PanelsF, PanelsE, TxtBox, LabelsF, LabelsE
    PanelsF = [TLP1, TLP2, TLP3, TLPM]
    LabelsF = [Label(TLP1, 121), Label(TLP2, 121), Label(TLP3, 121), Label(TLPM, 121), ]
    PanelsE = [TLP1, TLP2, TLPM]
    LabelsE = [Label(TLP1, 121), Label(TLP2, 121), Label(TLPM, 121), ]

    if IDButton == 400:
        TLPM.ShowPopup('1_Master')
        print('Touch: Master Room')

    elif IDButton == 111:
        if Room['Mode'] == 'Open':
            for TxtBox in LabelsF:
                TxtBox.SetText('Control de Video')
            for Touch in PanelsF:
                Touch.ShowPopup('Video_Full')
            print('Touch Full: Video')
        elif Room['Mode'] == 'Executive':
            for TxtBox in LabelsE:
                TxtBox.SetText('Control de Video')
            for Touch in PanelsE:
                Touch.ShowPopup('Video_Executive')
            print('Touch Executive: Video')

    elif IDButton == 112:
        if Room['Mode'] == 'Open':
            for TxtBox in LabelsF:
                TxtBox.SetText('Control de Audio')
            for Touch in PanelsF:
                Touch.ShowPopup('Audio_Full')
            print('Touch Full: Audio')
        elif Room['Mode'] == 'Executive':
            for TxtBox in LabelsE:
                TxtBox.SetText('Control de Audio')
            for Touch in PanelsE:
                Touch.ShowPopup('Audio_Full')
            print('Touch Executive: Audio')

    elif IDButton == 113:
        if Room['Mode'] == 'Open':
            for TxtBox in LabelsF:
                TxtBox.SetText('Control de Luces')
            for Touch in PanelsF:
                Touch.ShowPopup('Lights_Full')
            print('Touch Full: Luces')
        elif Room['Mode'] == 'Executive':
            for TxtBox in LabelsE:
                TxtBox.SetText('Control de Luces')
            for Touch in PanelsE:
                Touch.ShowPopup('Lights_Executive')
            print('Touch Executive: Luces')

    elif IDButton == 114:
        for TxtBox in LabelsF:
            TxtBox.SetText('Control de Voz por IP')
        for Touch in PanelsF:
            Touch.ShowPopup('VoIP')
        print('Touch: VoIP')

    elif IDButton == 115:
        for TxtBox in LabelsF:
            TxtBox.SetText('Control de Apagado')
        for Touch in PanelsF:
            Touch.ShowPopup('x_PowerOff_Full')
        print('Touch: PowerOff')

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullMain + B_FullMain + C_FullMain + M_FullMain, ButtonEventList)
def room_master_events(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        MainFullEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video Mode --------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProj, B_FullProj, C_FullProj, M_FullProj
A_FullProj = []
B_FullProj = []
C_FullProj = []
M_FullProj = []
#
for ID in range(141, 146):
    A_FullProj.append(Button(TLP1, ID))
for ID in range(141, 146):
    B_FullProj.append(Button(TLP2, ID))
for ID in range(141, 146):
    C_FullProj.append(Button(TLP3, ID))
for ID in range(141, 146):
    M_FullProj.append(Button(TLPM, ID))

def FullVideoEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global Touch, Panels, Labels, TxtBox
    Panels = [TLP1, TLP2, TLP3, TLPM]
    Labels = [Label(TLP1, 121), Label(TLP2, 121), Label(TLP3, 121), Label(TLPM, 121), ]

    if IDButton == 141:
        for TxtBox in Labels:
            TxtBox.SetText('Proyección Sala A')
        for Touch in Panels:
            Touch.ShowPopup('Video_Full_A')
        print('Touch: Projector A')

    elif IDButton == 142:
        for TxtBox in Labels:
            TxtBox.SetText('Proyección Sala B')
        for Touch in Panels:
            Touch.ShowPopup('Video_Full_B')
        print('Touch: Audio')

    elif IDButton == 143:
        for TxtBox in Labels:
            TxtBox.SetText('Proyección Sala C')
        for Touch in Panels:
            Touch.ShowPopup('Video_Full_C')
        print('Touch Lights')

    elif IDButton == 144:
        for TxtBox in Labels:
            TxtBox.SetText('Proyección Sala D')
        for Touch in Panels:
            Touch.ShowPopup('Video_Full_D')
        print('Touch Lights')

    elif IDButton == 145:
        for TxtBox in Labels:
            TxtBox.SetText('Proyección Global')
        for Touch in Panels:
            Touch.ShowPopup('Video_Full_M')
        print('Touch Lights')

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProj + B_FullProj + C_FullProj + M_FullProj, ButtonEventList)
def full_video_events(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video A ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProjA, B_FullProjA, C_FullProjA, M_FullProjA
A_FullProjA = []
B_FullProjA = []
C_FullProjA = []
M_FullProjA = []
#
for ID in range(151, 161):
    A_FullProjA.append(Button(TLP1, ID))
for ID in range(151, 161):
    B_FullProjA.append(Button(TLP2, ID))
for ID in range(151, 161):
    C_FullProjA.append(Button(TLP3, ID))
for ID in range(151, 161):
    M_FullProjA.append(Button(TLPM, ID))

def FullVideoEventsA(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 151:
        print('Touch Full: Proj A HDMI')

    elif IDButton == 152:
        print('Touch Full: Proj A ShareLink')

    elif IDButton == 155:
        print('Touch Full: Proj A PowerOn')

    elif IDButton == 156:
        print('Touch Full: Proj A PowerOff')

    elif IDButton == 157:
        print('Touch Full: Proj A Screen Up')

    elif IDButton == 158:
        print('Touch Full: Proj A Screen Stop')

    elif IDButton == 159:
        print('Touch Full: Proj A Screen Down')

    elif IDButton == 160:
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch Full: Proj A Back')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProjA + B_FullProjA + C_FullProjA + M_FullProjA, ButtonEventList)
def full_video_events_a(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEventsA(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video B ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProjB, B_FullProjB, C_FullProjB, M_FullProjB
A_FullProjB = []
B_FullProjB = []
C_FullProjB = []
M_FullProjB = []
#
for ID in range(161, 171):
    A_FullProjB.append(Button(TLP1, ID))
for ID in range(161, 171):
    B_FullProjB.append(Button(TLP2, ID))
for ID in range(161, 171):
    C_FullProjB.append(Button(TLP3, ID))
for ID in range(161, 171):
    M_FullProjB.append(Button(TLPM, ID))

def FullVideoEventsB(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 161:
        print('Touch Full: Proj B HDMI')

    elif IDButton == 162:
        print('Touch Full: Proj B ShareLink')

    elif IDButton == 165:
        print('Touch Full: Proj B PowerOn')

    elif IDButton == 166:
        print('Touch Full: Proj B PowerOff')

    elif IDButton == 167:
        print('Touch Full: Proj B Screen Up')

    elif IDButton == 168:
        print('Touch Full: Proj B Screen Stop')

    elif IDButton == 169:
        print('Touch Full: Proj B Screen Down')

    elif IDButton == 170:
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch Full: B Back')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProjB + B_FullProjB + C_FullProjB + M_FullProjB, ButtonEventList)
def full_video_events_b(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEventsB(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video C ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProjC, B_FullProjC, C_FullProjC, M_FullProjC
A_FullProjC = []
B_FullProjC = []
C_FullProjC = []
M_FullProjC = []
#
for ID in range(171, 181):
    A_FullProjC.append(Button(TLP1, ID))
for ID in range(171, 181):
    B_FullProjC.append(Button(TLP2, ID))
for ID in range(171, 181):
    C_FullProjC.append(Button(TLP3, ID))
for ID in range(171, 181):
    M_FullProjC.append(Button(TLPM, ID))

def FullVideoEventsC(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 171:
        print('Touch Full: Proj C HDMI')

    elif IDButton == 172:
        print('Touch Full: Proj C ShareLink')

    elif IDButton == 175:
        print('Touch Full: Proj C PowerOn')

    elif IDButton == 176:
        print('Touch Full: Proj C PowerOff')

    elif IDButton == 177:
        print('Touch Full: Proj C Screen Up')

    elif IDButton == 178:
        print('Touch Full: Proj C Screen Stop')

    elif IDButton == 179:
        print('Touch Full: Proj C Screen Down')

    elif IDButton == 180:
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch Full: C Back')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProjC + B_FullProjC + C_FullProjC + M_FullProjC, ButtonEventList)
def full_video_events_c(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEventsC(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video D ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProjD, B_FullProjD, C_FullProjD, M_FullProjD
A_FullProjD = []
B_FullProjD = []
C_FullProjD = []
M_FullProjD = []
#
for ID in range(181, 191):
    A_FullProjD.append(Button(TLP1, ID))
for ID in range(181, 191):
    B_FullProjD.append(Button(TLP2, ID))
for ID in range(181, 191):
    C_FullProjD.append(Button(TLP3, ID))
for ID in range(181, 191):
    M_FullProjD.append(Button(TLPM, ID))

def FullVideoEventsD(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 181:
        print('Touch Full: Proj D HDMI')

    elif IDButton == 182:
        print('Touch Full: Proj D ShareLink')

    elif IDButton == 185:
        print('Touch Full: Proj D PowerOn')

    elif IDButton == 186:
        print('Touch Full: Proj D PowerOff')

    elif IDButton == 187:
        print('Touch Full: Proj D Screen Up')

    elif IDButton == 188:
        print('Touch Full: Proj D Screen Stop')

    elif IDButton == 189:
        print('Touch Full: Proj D Screen Down')

    elif IDButton == 190:
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch Full: D Back')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProjD + B_FullProjD + C_FullProjD + M_FullProjD, ButtonEventList)
def full_video_events_c(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEventsD(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Video Global  -----------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullProjG, B_FullProjG, C_FullProjG, M_FullProjG
A_FullProjG = []
B_FullProjG = []
C_FullProjG = []
M_FullProjG = []
#
for ID in range(191, 199):
    A_FullProjG.append(Button(TLP1, ID))
for ID in range(191, 199):
    B_FullProjG.append(Button(TLP2, ID))
for ID in range(191, 199):
    C_FullProjG.append(Button(TLP3, ID))
for ID in range(191, 199):
    M_FullProjG.append(Button(TLPM, ID))

def FullVideoEventsG(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 191:
        print('Touch Full: Proj Global HDMI')

    elif IDButton == 193:
        print('Touch Full: Proj Global ShareLink')

    elif IDButton == 195:
        print('Touch Full: Proj D Screen Up')

    elif IDButton == 196:
        print('Touch Full: Proj D Screen Stop')

    elif IDButton == 197:
        print('Touch Full: Proj D Screen Down')

    elif IDButton == 198:
        for Touch in Panels:
            Touch.ShowPopup('Video_Full')
        print('Touch Full: D Back')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullProjG + B_FullProjG + C_FullProjG + M_FullProjG, ButtonEventList)
def full_video_events_g(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullVideoEventsG(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Audio --------------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullAudio, B_FullAudio, C_FullAudio, M_FullAudio
A_FullAudio = []
B_FullAudio = []
C_FullAudio = []
M_FullAudio = []
#
for ID in range(201, 211):
    A_FullAudio.append(Button(TLP1, ID))
for ID in range(201, 211):
    B_FullAudio.append(Button(TLP2, ID))
for ID in range(201, 211):
    C_FullAudio.append(Button(TLP3, ID))
for ID in range(201, 211):
    M_FullAudio.append(Button(TLPM, ID))

def FullAudioEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 201:
        print('Touch Full: HDMI')

    elif IDButton == 203:
        print('Touch Full: ShareLink')

    elif IDButton == 205:
        print('Touch Full: Vol -')

    elif IDButton == 206:
        print('Touch Full: Vol +')

    elif IDButton == 208:
        print('Touch Full: Mute Spk')

    elif IDButton == 209:
        print('Touch Full: Mute Hand Mic')

    elif IDButton == 210:
        print('Touch Full: Mute Cielling Mic')
    pass

@event(A_FullAudio + B_FullAudio + C_FullAudio + M_FullAudio, ButtonEventList)
def full_video_events(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullAudioEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Lights Mode --------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullLights, B_FullLights, C_FullLights, M_FullLights
A_FullLights = [Button(TLP1, 291), Button(TLP1, 292)]
B_FullLights = [Button(TLP2, 291), Button(TLP2, 292)]
C_FullLights = [Button(TLP3, 291), Button(TLP3, 292)]
M_FullLights = [Button(TLPM, 291), Button(TLPM, 292)]
#
for ID in range(211, 215):
    A_FullLights.append(Button(TLP1, ID))
for ID in range(211, 215):
    B_FullLights.append(Button(TLP2, ID))
for ID in range(211, 215):
    C_FullLights.append(Button(TLP3, ID))
for ID in range(211, 215):
    M_FullLights.append(Button(TLPM, ID))

def FullLightEvents(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    global Touch, Panels, Labels, TxtBox
    Panels = [TLP1, TLP2, TLP3, TLPM]
    Labels = [Label(TLP1, 121), Label(TLP2, 121), Label(TLP3, 121), Label(TLPM, 121), ]

    if IDButton == 211 or IDButton == 291:
        for TxtBox in Labels:
            TxtBox.SetText('Luces Sala A')
        for Touch in Panels:
            Touch.ShowPopup('Lights_FullA')
        print('Touch Full: Lights A')

    elif IDButton == 212 or IDButton == 292:
        for TxtBox in Labels:
            TxtBox.SetText('Luces Sala B')
        for Touch in Panels:
            Touch.ShowPopup('Lights_FullB')
        print('Touch Full: Lights B')

    elif IDButton == 213:
        for TxtBox in Labels:
            TxtBox.SetText('Luces Sala C')
        for Touch in Panels:
            Touch.ShowPopup('Lights_FullC')
        print('Touch Full: Lights C')

    elif IDButton == 214:
        for TxtBox in Labels:
            TxtBox.SetText('Luces Global')
        for Touch in Panels:
            Touch.ShowPopup('Lights_FullM')
        print('Touch Full: Lights Global')

    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullLights + B_FullLights + C_FullLights + M_FullLights, ButtonEventList)
def full_video_events(button, state):
    """User Actions: Touch Full Main Page"""
    if state == 'Pressed':
        FullLightEvents(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Lights A ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullLightsA, B_FullLightsA, C_FullLightsA, M_FullLightsA
A_FullLightsA = []
B_FullLightsA = []
C_FullLightsA = []
M_FullLightsA = []
#
for ID in range(221, 228):
    A_FullLightsA.append(Button(TLP1, ID))
for ID in range(221, 228):
    B_FullLightsA.append(Button(TLP2, ID))
for ID in range(221, 228):
    C_FullLightsA.append(Button(TLP3, ID))
for ID in range(221, 228):
    M_FullLightsA.append(Button(TLPM, ID))

def FullLightsEventsA(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 221:
        print('Touch Full: Lights A Escene 1')

    elif IDButton == 222:
        print('Touch Full: Lights A Escene 2')

    elif IDButton == 223:
        print('Touch Full: Lights A Escene 3')

    elif IDButton == 224:
        print('Touch Full: Lights A Escene 4')

    elif IDButton == 225:
        print('Touch Full: Lights A Blinds Up')

    elif IDButton == 226:
        print('Touch Full: Lights A Blinds Stop')

    elif IDButton == 227:
        print('Touch Full: Lights A Blinds Down')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullLightsA + B_FullLightsA + C_FullLightsA + M_FullLightsA, ButtonEventList)
def full_lights_events_a(button, state):
    """User Actions: Touch Full Lights A Page"""
    if state == 'Pressed':
        FullLightsEventsA(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Lights B ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullLightsB, B_FullLightsB, C_FullLightsB, M_FullLightsB
A_FullLightsB = []
B_FullLightsB = []
C_FullLightsB = []
M_FullLightsB = []
#
for ID in range(231, 238):
    A_FullLightsB.append(Button(TLP1, ID))
for ID in range(231, 238):
    B_FullLightsB.append(Button(TLP2, ID))
for ID in range(231, 238):
    C_FullLightsB.append(Button(TLP3, ID))
for ID in range(231, 238):
    M_FullLightsB.append(Button(TLPM, ID))

def FullLightsEventsB(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 231:
        print('Touch Full: Lights B Escene 1')

    elif IDButton == 232:
        print('Touch Full: Lights B Escene 2')

    elif IDButton == 233:
        print('Touch Full: Lights B Escene 3')

    elif IDButton == 234:
        print('Touch Full: Lights B Escene 4')

    elif IDButton == 235:
        print('Touch Full: Lights B Blinds Up')

    elif IDButton == 236:
        print('Touch Full: Lights B Blinds Stop')

    elif IDButton == 237:
        print('Touch Full: Lights B Blinds Down')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullLightsB + B_FullLightsB + C_FullLightsB + M_FullLightsB, ButtonEventList)
def full_lights_events_b(button, state):
    """User Actions: Touch Full Lights A Page"""
    if state == 'Pressed':
        FullLightsEventsB(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Lights C ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullLightsC, B_FullLightsC, C_FullLightsC, M_FullLightsC
A_FullLightsC = []
B_FullLightsC = []
C_FullLightsC = []
M_FullLightsC = []
#
for ID in range(241, 248):
    A_FullLightsC.append(Button(TLP1, ID))
for ID in range(241, 248):
    B_FullLightsC.append(Button(TLP2, ID))
for ID in range(241, 248):
    C_FullLightsC.append(Button(TLP3, ID))
for ID in range(241, 248):
    M_FullLightsC.append(Button(TLPM, ID))

def FullLightsEventsC(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 241:
        print('Touch Full: Lights C Escene 1')

    elif IDButton == 242:
        print('Touch Full: Lights C Escene 2')

    elif IDButton == 243:
        print('Touch Full: Lights C Escene 3')

    elif IDButton == 244:
        print('Touch Full: Lights C Escene 4')

    elif IDButton == 245:
        print('Touch Full: Lights C Blinds Up')

    elif IDButton == 246:
        print('Touch Full: Lights C Blinds Stop')

    elif IDButton == 247:
        print('Touch Full: Lights C Blinds Down')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullLightsC + B_FullLightsC + C_FullLightsC + M_FullLightsC, ButtonEventList)
def full_lights_events_c(button, state):
    """User Actions: Touch Full Lights A Page"""
    if state == 'Pressed':
        FullLightsEventsC(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full Lights Global ----------------------------------------------------------
## Dynamic Buttons Assignement
global ID, A_FullLightsG, B_FullLightsG, C_FullLightsG, M_FullLightsG
A_FullLightsG = []
B_FullLightsG = []
C_FullLightsG = []
M_FullLightsG = []
#
for ID in range(251, 258):
    A_FullLightsG.append(Button(TLP1, ID))
for ID in range(251, 258):
    B_FullLightsG.append(Button(TLP2, ID))
for ID in range(251, 258):
    C_FullLightsG.append(Button(TLP3, ID))
for ID in range(251, 258):
    M_FullLightsG.append(Button(TLPM, ID))

def FullLightsEventsG(DeviceAlias, IDButton):
    """This avoid to type too much code in Main Page"""
    if IDButton == 251:
        print('Touch Full: Lights Global Escene 1')

    elif IDButton == 252:
        print('Touch Full: Lights Global Escene 2')

    elif IDButton == 253:
        print('Touch Full: Lights Global Escene 3')

    elif IDButton == 254:
        print('Touch Full: Lights Global Escene 4')

    elif IDButton == 255:
        print('Touch Full: Lights Global Blinds Up')

    elif IDButton == 256:
        print('Touch Full: Lights Global Blinds Stop')

    elif IDButton == 257:
        print('Touch Full: Lights Global Blinds Down')
    ## Turn On Mutually Exclusive
    ## Group.SetCurrent(Button(DeviceAlias, (IDButton)))
    pass

@event(A_FullLightsG + B_FullLightsG + C_FullLightsG + M_FullLightsG, ButtonEventList)
def full_lights_events_c(button, state):
    """User Actions: Touch Full Lights A Page"""
    if state == 'Pressed':
        FullLightsEventsG(button.Host.DeviceAlias, button.ID) #Recall a Function
    pass

## Main Full PowerOff ----------------------------------------------------------
## Dynamic Buttons Assignement
A_FullPwr = Button(TLP1, 301, repeatTime=1)
B_FullPwr = Button(TLP2, 301, repeatTime=1)
C_FullPwr = Button(TLP3, 301, repeatTime=1)
M_FullPwr = Button(TLPM, 301, repeatTime=1)
FullPwr = [A_FullPwr, B_FullPwr, C_FullPwr, M_FullPwr]

@event(FullPwr, ButtonEventList)
def full_video_events(button, state):
    """User Actions: Touch Full PowerOff Page"""
    global PWRCOUNT, ID

    ## POWER GLOBAL
    if Room['Mode'] == 'Open':
        print('Touch Full: PowerOff')
        Panels = [TLP1, TLP2, TLP3, TLPM]
        Labels = [Label(TLP1, 303), Label(TLP2, 303), Label(TLP3, 303), Label(TLPM, 303)]
        FullPwr = [A_FullPwr, B_FullPwr, C_FullPwr, M_FullPwr]
        #
        if state == 'Pressed':
            for ID in FullPwr:
                ID.SetState(3)
            for TxtBox in Labels:
                TxtBox.SetText('3')
            print('Touch A: Pressed PowerOff')
        elif state == 'Repeated':
            print(PWRCOUNT)
            PWRCOUNT = PWRCOUNT - 1
            button.SetState(PWRCOUNT)
            for TxtBox in Labels:
                TxtBox.SetText(str(PWRCOUNT))
            print('Touch A: Repeated PowerOff')
            if PWRCOUNT == 0:
                #ShutDown All Devices
                for Touch in Panels:
                    Touch.ShowPage('Index')
        elif state == 'Released':
            PWRCOUNT = 4
            for ID in FullPwr:
                ID.SetState(0)
            for TxtBox in Labels:
                TxtBox.SetText('')
            print('Touch A: Released PowerOff')

    ## POWER EXECUTIVE
    elif Room['Mode'] == 'Executive':
        print('Touch Executive: PowerOff')
        Panels = [TLP1, TLP2, TLPM]
        Labels = [Label(TLP1, 303), Label(TLP2, 303), Label(TLPM, 303)]
        FullPwr = [A_FullPwr, B_FullPwr, M_FullPwr]
        #
        if state == 'Pressed':
            for ID in FullPwr:
                ID.SetState(3)
            for TxtBox in Labels:
                TxtBox.SetText('3')
            print('Touch A: Pressed PowerOff')
        elif state == 'Repeated':
            print(PWRCOUNT)
            PWRCOUNT = PWRCOUNT - 1
            button.SetState(PWRCOUNT)
            for TxtBox in Labels:
                TxtBox.SetText(str(PWRCOUNT))
            print('Touch A: Repeated PowerOff')
            if PWRCOUNT == 0:
                #ShutDown All Devices
                for Touch in Panels:
                    Touch.ShowPage('Index')
        elif state == 'Released':
            PWRCOUNT = 4
            for ID in FullPwr:
                ID.SetState(0)
            for TxtBox in Labels:
                TxtBox.SetText('')
            print('Touch A: Released PowerOff')
    pass

## End Events Definitions-------------------------------------------------------
## End Events Definitions-------------------------------------------------------
## End Events Definitions-------------------------------------------------------

Initialize()

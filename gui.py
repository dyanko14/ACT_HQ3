""" --------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | Mixed Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT ------------------------------------------------------
from extronlib.device import UIDevice
from extronlib.ui import Button, Label, Level
from extronlib.system import MESet

# UI Device
TLPM = UIDevice('TouchPanelM')
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
TLP3 = UIDevice('TouchPanelC')

# UI Buttons
BTN = {
    ## PANEL M ----------------------------------------
    ## Page Master Index
    'M_Index'   : Button(TLPM, 1),
    ## Page Master PIN
    'M_Pin0'    : Button(TLPM, 1000),
    'M_Pin1'    : Button(TLPM, 1001),
    'M_Pin2'    : Button(TLPM, 1002),
    'M_Pin3'    : Button(TLPM, 1003),
    'M_Pin4'    : Button(TLPM, 1004),
    'M_Pin5'    : Button(TLPM, 1005),
    'M_Pin6'    : Button(TLPM, 1006),
    'M_Pin7'    : Button(TLPM, 1007),
    'M_Pin8'    : Button(TLPM, 1008),
    'M_Pin9'    : Button(TLPM, 1009),
    'M_PinD'    : Button(TLPM, 1010, repeatTime=0.1),
    'M_PinX'    : Button(TLPM, 1011),
    ## Page Master Main
    'M_Room1'   : Button(TLPM, 2001),
    'M_Room2'   : Button(TLPM, 2002),
    'M_Room3'   : Button(TLPM, 2003),
    'M_Room4'   : Button(TLPM, 2004),
    ## Page Master Main
    'M_Video'   : Button(TLPM, 11),
    'M_Audio'   : Button(TLPM, 12),
    'M_Blinds'  : Button(TLPM, 13),
    'M_Lights'  : Button(TLPM, 14),
    'M_Status'  : Button(TLPM, 15),
    'M_PwrOff'  : Button(TLPM, 16),
    ## Page Master Video
    'M_VHDMI'   : Button(TLPM, 21),
    'M_VShare'  : Button(TLPM, 22),
    'M_VPwrOn'  : Button(TLPM, 23),
    'M_VPwrOff' : Button(TLPM, 24),
    'M_Up'      : Button(TLPM, 25),
    'M_Stop'    : Button(TLPM, 26),
    'M_Down'    : Button(TLPM, 27),
    ## Page Master Audio
    'M_VolLess' : Button(TLPM, 31, repeatTime=0.1),
    'M_VolPlus' : Button(TLPM, 32, repeatTime=0.1),
    'M_Mute'    : Button(TLPM, 33),
    ## Page Master Persianas
    'M_BUp'     : Button(TLPM, 41),
    'M_BStop'   : Button(TLPM, 42),
    'M_BDown'   : Button(TLPM, 43),
    ## Page Master Luces
    'M_LightOn' : Button(TLPM, 51),
    'M_LightOf' : Button(TLPM, 52),
    ## Page Master Status
    'M_232LCD1' : Button(TLPM, 61),
    'M_232LCD2' : Button(TLPM, 62),
    'M_232DXP'  : Button(TLPM, 63),
    'M_232Bimp' : Button(TLPM, 64),
    'M_232PTZ'  : Button(TLPM, 65),
    'M_232Cisc' : Button(TLPM, 66),
    'M_LANSMP'  : Button(TLPM, 67),
    'M_LANVadd' : Button(TLPM, 68),
    ## Page Master PowerOff
    'M_PwrAll'  : Button(TLPM, 101, holdTime=3),

    ## PANEL A ----------------------------------------
    ## Page RoomA Index
    'A_Index'   : Button(TLP1, 1),
    ## Page RoomA PIN
    'A_Pin0'    : Button(TLP1, 1000),
    'A_Pin1'    : Button(TLP1, 1001),
    'A_Pin2'    : Button(TLP1, 1002),
    'A_Pin3'    : Button(TLP1, 1003),
    'A_Pin4'    : Button(TLP1, 1004),
    'A_Pin5'    : Button(TLP1, 1005),
    'A_Pin6'    : Button(TLP1, 1006),
    'A_Pin7'    : Button(TLP1, 1007),
    'A_Pin8'    : Button(TLP1, 1008),
    'A_Pin9'    : Button(TLP1, 1009),
    'A_PinD'    : Button(TLP1, 1010, repeatTime=0.1),
    'A_PinX'    : Button(TLP1, 1011),
    ## Page RoomA Main
    'A_Video'   : Button(TLP1, 11),
    'A_Audio'   : Button(TLP1, 12),
    'A_Blinds'  : Button(TLP1, 13),
    'A_Lights'  : Button(TLP1, 14),
    'A_Status'  : Button(TLP1, 15),
    'A_PwrOff'  : Button(TLP1, 16),
    ## Page RoomA Video
    'A_VHDMI'   : Button(TLP1, 21),
    'A_VShare'  : Button(TLP1, 22),
    'A_VPwrOn'  : Button(TLP1, 23),
    'A_VPwrOff' : Button(TLP1, 24),
    'A_Up'      : Button(TLP1, 25),
    'A_Stop'    : Button(TLP1, 26),
    'A_Down'    : Button(TLP1, 27),
    ## Page RoomA Audio
    'A_VolLess' : Button(TLP1, 31, repeatTime=0.1),
    'A_VolPlus' : Button(TLP1, 32, repeatTime=0.1),
    'A_Mute'    : Button(TLP1, 33),
    ## Page RoomA Persianas
    'A_BUp'     : Button(TLP1, 41),
    'A_BStop'   : Button(TLP1, 42),
    'A_BDown'   : Button(TLP1, 43),
    ## Page RoomA Luces
    'A_LightOn' : Button(TLP1, 51),
    'A_LightOf' : Button(TLP1, 52),
    ## Page RoomA Status
    'A_232LCD1' : Button(TLP1, 61),
    'A_232LCD2' : Button(TLP1, 62),
    'A_232DXP'  : Button(TLP1, 63),
    'A_232Bimp' : Button(TLP1, 64),
    'A_232PTZ'  : Button(TLP1, 65),
    'A_232Cisc' : Button(TLP1, 66),
    'A_LANSMP'  : Button(TLP1, 67),
    'A_LANVadd' : Button(TLP1, 68),
    ## Page RoomA PowerOff
    'A_PwrAll'  : Button(TLP1, 101, holdTime=3),

    ## PANEL B ----------------------------------------
    ## Page RoomB Index
    'B_Index'   : Button(TLP2, 1),
    ## Page RoomB PIN
    'B_Pin0'    : Button(TLP2, 1000),
    'B_Pin1'    : Button(TLP2, 1001),
    'B_Pin2'    : Button(TLP2, 1002),
    'B_Pin3'    : Button(TLP2, 1003),
    'B_Pin4'    : Button(TLP2, 1004),
    'B_Pin5'    : Button(TLP2, 1005),
    'B_Pin6'    : Button(TLP2, 1006),
    'B_Pin7'    : Button(TLP2, 1007),
    'B_Pin8'    : Button(TLP2, 1008),
    'B_Pin9'    : Button(TLP2, 1009),
    'B_PinD'    : Button(TLP2, 1010, repeatTime=0.1),
    'B_PinX'    : Button(TLP2, 1011),
    ## Page RoomB Main
    'B_Video'   : Button(TLP2, 11),
    'B_Audio'   : Button(TLP2, 12),
    'B_Blinds'  : Button(TLP2, 13),
    'B_Lights'  : Button(TLP2, 14),
    'B_Status'  : Button(TLP2, 15),
    'B_PwrOff'  : Button(TLP2, 16),
    ## Page RoomB Video
    'B_VHDMI'   : Button(TLP2, 21),
    'B_VShare'  : Button(TLP2, 22),
    'B_VPwrOn'  : Button(TLP2, 23),
    'B_VPwrOff' : Button(TLP2, 24),
    'B_Up'      : Button(TLP2, 25),
    'B_Stop'    : Button(TLP2, 26),
    'B_Down'    : Button(TLP2, 27),
    ## Page RoomB Audio
    'B_VolLess' : Button(TLP2, 31, repeatTime=0.1),
    'B_VolPlus' : Button(TLP2, 32, repeatTime=0.1),
    'B_Mute'    : Button(TLP2, 33),
    ## Page RoomB Persianas
    'B_BUp'     : Button(TLP2, 41),
    'B_BStop'   : Button(TLP2, 42),
    'B_BDown'   : Button(TLP2, 43),
    ## Page RoomB Luces
    'B_LightOn' : Button(TLP2, 51),
    'B_LightOf' : Button(TLP2, 52),
    ## Page RoomB Status
    'B_232LCD1' : Button(TLP2, 61),
    'B_232LCD2' : Button(TLP2, 62),
    'B_232DXP'  : Button(TLP2, 63),
    'B_232Bimp' : Button(TLP2, 64),
    'B_232PTZ'  : Button(TLP2, 65),
    'B_232Cisc' : Button(TLP2, 66),
    'B_LANSMP'  : Button(TLP2, 67),
    'B_LANVadd' : Button(TLP2, 68),
    ## Page RoomB PowerOff
    'B_PwrAll'  : Button(TLP2, 101, holdTime=3),

    ## PANEL C ----------------------------------------
    ## Page RoomC Index
    'C_Index'   : Button(TLP3, 1),
    ## Page RoomC PIN
    'C_Pin0'    : Button(TLP3, 1000),
    'C_Pin1'    : Button(TLP3, 1001),
    'C_Pin2'    : Button(TLP3, 1002),
    'C_Pin3'    : Button(TLP3, 1003),
    'C_Pin4'    : Button(TLP3, 1004),
    'C_Pin5'    : Button(TLP3, 1005),
    'C_Pin6'    : Button(TLP3, 1006),
    'C_Pin7'    : Button(TLP3, 1007),
    'C_Pin8'    : Button(TLP3, 1008),
    'C_Pin9'    : Button(TLP3, 1009),
    'C_PinD'    : Button(TLP3, 1010, repeatTime=0.1),
    'C_PinX'    : Button(TLP3, 1011),
    ## Page RoomC Main
    'C_Video'   : Button(TLP3, 11),
    'C_Audio'   : Button(TLP3, 12),
    'C_Blinds'  : Button(TLP3, 13),
    'C_Lights'  : Button(TLP3, 14),
    'C_Status'  : Button(TLP3, 15),
    'C_PwrOff'  : Button(TLP3, 16),
    ## Page RoomC Video
    'C_VHDMI'   : Button(TLP3, 21),
    'C_VShare'  : Button(TLP3, 22),
    'C_VPwrOn'  : Button(TLP3, 23),
    'C_VPwrOff' : Button(TLP3, 24),
    'C_Up'      : Button(TLP3, 25),
    'C_Stop'    : Button(TLP3, 26),
    'C_Down'    : Button(TLP3, 27),
    ## Page RoomC Audio
    'C_VolLess' : Button(TLP3, 31, repeatTime=0.1),
    'C_VolPlus' : Button(TLP3, 32, repeatTime=0.1),
    'C_Mute'    : Button(TLP3, 33),
    ## Page RoomC Persianas
    'C_BUp'     : Button(TLP3, 41),
    'C_BStop'   : Button(TLP3, 42),
    'C_BDown'   : Button(TLP3, 43),
    ## Page RoomC Luces
    'C_LightOn' : Button(TLP3, 51),
    'C_LightOf' : Button(TLP3, 52),
    ## Page RoomC Status
    'C_232LCD1' : Button(TLP3, 61),
    'C_232LCD2' : Button(TLP3, 62),
    'C_232DXP'  : Button(TLP3, 63),
    'C_232Bimp' : Button(TLP3, 64),
    'C_232PTZ'  : Button(TLP3, 65),
    'C_232Cisc' : Button(TLP3, 66),
    'C_LANSMP'  : Button(TLP3, 67),
    'C_LANVadd' : Button(TLP3, 68),
    ## Page RoomC PowerOff
    'C_PwrAll'  : Button(TLP3, 101, holdTime=3),
}

# UI Page Buttons
BTNPAGE = {
    'Index' : [BTN['A_Index'], BTN['B_Index'], BTN['C_Index'], BTN['M_Index']],
    'Room'  : [BTN['M_Room1'], BTN['M_Room2'], BTN['M_Room3'], BTN['M_Room4']],

    'PIN'   : [BTN['M_Pin0'], BTN['M_Pin1'], BTN['M_Pin2'], BTN['M_Pin3'], BTN['M_Pin4'], BTN['M_Pin5'],
               BTN['M_Pin6'], BTN['M_Pin7'], BTN['M_Pin8'], BTN['M_Pin9'], BTN['M_PinD'], BTN['M_PinX'],
               BTN['A_Pin0'], BTN['A_Pin1'], BTN['A_Pin2'], BTN['A_Pin3'], BTN['A_Pin4'], BTN['A_Pin5'],
               BTN['A_Pin6'], BTN['A_Pin7'], BTN['A_Pin8'], BTN['A_Pin9'], BTN['A_PinD'], BTN['A_PinX'],
               BTN['B_Pin0'], BTN['B_Pin1'], BTN['B_Pin2'], BTN['B_Pin3'], BTN['B_Pin4'], BTN['B_Pin5'],
               BTN['B_Pin6'], BTN['B_Pin7'], BTN['B_Pin8'], BTN['B_Pin9'], BTN['B_PinD'], BTN['B_PinX'],
               BTN['C_Pin0'], BTN['C_Pin1'], BTN['C_Pin2'], BTN['C_Pin3'], BTN['C_Pin4'], BTN['C_Pin5'],
               BTN['C_Pin6'], BTN['C_Pin7'], BTN['C_Pin8'], BTN['C_Pin9'], BTN['C_PinD'], BTN['C_PinX']],

    'Main'  : [BTN['A_Video'], BTN['A_Audio'], BTN['A_Blinds'], BTN['A_Lights'], BTN['A_Status'], BTN['A_PwrOff'],
               BTN['B_Video'], BTN['B_Audio'], BTN['B_Blinds'], BTN['B_Lights'], BTN['B_Status'], BTN['B_PwrOff'],
               BTN['C_Video'], BTN['C_Audio'], BTN['C_Blinds'], BTN['C_Lights'], BTN['C_Status'], BTN['C_PwrOff']],

    'Video' : [BTN['A_VHDMI'], BTN['A_VShare'], BTN['A_VPwrOn'], BTN['A_VPwrOff'], BTN['A_Up'], BTN['A_Stop'], BTN['A_Down'],
               BTN['B_VHDMI'], BTN['B_VShare'], BTN['B_VPwrOn'], BTN['B_VPwrOff'], BTN['B_Up'], BTN['B_Stop'], BTN['B_Down'],
               BTN['C_VHDMI'], BTN['C_VShare'], BTN['C_VPwrOn'], BTN['C_VPwrOff'], BTN['C_Up'], BTN['C_Stop'], BTN['C_Down']],

    'Audio' : [BTN['A_VolLess'], BTN['A_VolPlus'], BTN['A_Mute'],
               BTN['B_VolLess'], BTN['B_VolPlus'], BTN['B_Mute'],
               BTN['C_VolLess'], BTN['C_VolPlus'], BTN['C_Mute']],

    'Blinds': [BTN['A_BUp'], BTN['A_BStop'], BTN['A_BDown'],
               BTN['B_BUp'], BTN['B_BStop'], BTN['B_BDown'],
               BTN['C_BUp'], BTN['C_BStop'], BTN['C_BDown']],

    'Lights': [BTN['A_LightOn'], BTN['A_LightOf'],
               BTN['B_LightOn'], BTN['B_LightOf'],
               BTN['C_LightOn'], BTN['C_LightOf']],

    'PowerAll' : [BTN['A_PwrAll'], BTN['B_PwrAll'], BTN['C_PwrAll']],
}

# UI Group Page Buttons
BTNGROUP = {
    'Room'     : MESet(BTNPAGE['Room']),

    'MainA'    : MESet([BTN['A_Video'], BTN['A_Audio'], BTN['A_Blinds'], BTN['A_Lights'], BTN['A_Status'], BTN['A_PwrOff']]),
    'MainB'    : MESet([BTN['B_Video'], BTN['B_Audio'], BTN['B_Blinds'], BTN['B_Lights'], BTN['B_Status'], BTN['B_PwrOff']]),
    'MainC'    : MESet([BTN['C_Video'], BTN['C_Audio'], BTN['C_Blinds'], BTN['C_Lights'], BTN['C_Status'], BTN['C_PwrOff']]),

    'VideoA'   : MESet([BTN['A_Up'], BTN['A_Stop'], BTN['A_Down']]),
    'VideoB'   : MESet([BTN['B_Up'], BTN['B_Stop'], BTN['B_Down']]),
    'VideoC'   : MESet([BTN['C_Up'], BTN['C_Stop'], BTN['C_Down']]),

    'BlindsA'  : MESet([BTN['A_BUp'], BTN['A_BStop'], BTN['A_BDown']]),
    'BlindsB'  : MESet([BTN['B_BUp'], BTN['B_BStop'], BTN['B_BDown']]),
    'BlindsC'  : MESet([BTN['C_BUp'], BTN['C_BStop'], BTN['C_BDown']]),

    'LightsA'  : MESet([BTN['A_LightOn'], BTN['A_LightOf']]),
    'LightsB'  : MESet([BTN['B_LightOn'], BTN['B_LightOf']]),
    'LightsC'  : MESet([BTN['C_LightOn'], BTN['C_LightOf']]),
}

# UI Button states
BTNSTATE = {
    'List' : ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
}

# UI Labels
LBL = {
    ## PANEL M ----------------------------------------
    'M_Index'    : Label(TLPM, 2),
    'M_LblPwrAll': Label(TLPM, 102),
    'M_Master'   : Label(TLPM, 300),
    'M_Room'     : Label(TLPM, 301),
    'M_PIN'      : Label(TLPM, 1012),

    ## PANEL A ----------------------------------------
    'A_Index'    : Label(TLP1, 2),
    'A_PwrAll'   : Label(TLP1, 102),
    'A_Master'   : Label(TLP1, 300),
    'A_Room'     : Label(TLP1, 301),
    'A_PIN'      : Label(TLP1, 1012),

    ## PANEL B ----------------------------------------
    'B_Index'    : Label(TLP2, 2),
    'B_PwrAll'   : Label(TLP2, 102),
    'B_Master'   : Label(TLP2, 300),
    'B_Room'     : Label(TLP2, 301),
    'B_PIN'      : Label(TLP2, 1012),

    ## PANEL C ----------------------------------------
    'C_Index'    : Label(TLP3, 2),
    'C_PwrAll'   : Label(TLP3, 102),
    'C_Master'   : Label(TLP3, 300),
    'C_Room'     : Label(TLP3, 301),
    'C_PIN'      : Label(TLP3, 1012),
}

# UI Levels
LVL = {
    ## PANEL M ----------------------------------------
    'M_Room' : Level(TLPM, 34),

    ## PANEL A ----------------------------------------
    'A_Room' : Level(TLP1, 34),

    ## PANEL B ----------------------------------------
    'B_Room' : Level(TLP2, 34),

    ## PANEL C ----------------------------------------
    'C_Room' : Level(TLP3, 34),
}

POPUP = {
}

PAGE = {
}

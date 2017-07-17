# How to use the Module in Main script
#
# import module by name of the py file
# import module
#
# Declare controller
# dvPro350 = ProcessorDevice('dvPro350')
#
# Specify communication settings if Serial
# SerialPort1 = module.SerialClass(dvPro350, 'COM1', Baud=19200, Model='SMX 200')
#
# Specify communication settings if Ethernet (for TCP)
# EthernetPort1 = module.EthernetClass('10.10.10.10', 23, Model='SMX 200')
#
# When using Ethernet Class:
# EthernetPort1.Connect() must be coded,
# Module does NOT connect to
# the device automatically.
#
# How to send a control command
# without qualifiers
# SerialPort1.Set('AudioMute', 'On')
#
# with qualifiers
# The 3rd argument (qualifier) must be specified as the example {'Input': 1}
# SerialPort1.Set('AudioMute', 'On',{'Input': 1})
#
# How  to send a control command with qualifier, but no value
# This example also show how to send multiple qualifier arguments
# SerialPort1.Set('MatrixTieCommand', None, {'Input': 1,'Ouput': 2,'TieType': 'Video'})
#
# How to send a update command
# Without qualifier
# SerialPort1.Update('AudioMute')
#
# How to send a update command
# With qualifier
# SerialPort1.Update('AudioMute',{'Input': 1})
#
# To avoid using delay after an Update command is called, it is recommended to use
# SubscribeStatus for commands that are query often, for logic or one time check
# use the example below
# How to subscribe to a command
# module.SubscribeStatus('Power',None, MethodToCall)
# any time we get status back for power from the device the Subscribed command
# 'Power' will call the Method defined 'MethodToCall'
# 'MethodToCall' must take 3 parameters (command, value, qualifier)
#
# def MethodToCall(command, value, qualifier)
#     if value == 'On':
#        Logic here
#     else:
#        Logic here
#
# All statuses of the Device will be store into a dictionary,
#
# Get Current Status of Audio Mute w/o qualifier.
# value will be equals to one of the states for the command requested
# value = SerialPort1.ReadStatus('AudioMute')
#
# Get Current Status of Audio Mute with qualifier
# value = SerialPort1.ReadStatus('AudioMute', {'Input': 1})
#
#####################################################################
# List of Models Supported by module
#####################################################################
# SW2 HDMI,SW4 HDMI,SW6 HDMI,SW8 HDMI,
#
#####################################################################
# REQUIRED VARIABLE SETTINGS
#####################################################################
# Unidirectional variable must be set to 'True' if status is not required
# Default value is 'False'
# Example: ModuleName.Unidirectional = 'True'

# ConnectionCounter variable must be set the number of queries that will be sent to the device
# before displaying 'Disconnected' if no response is received. Default value is 15.
# Example: ModuleName.ConnectionCounter = 5

# If login credentials are required, devicePassword and deviceUsername
# must be set accordingly.
# Example: ModuleName.devicePassword = 'extron'


from extronlib.interface import EthernetClientInterface, EthernetServerInterface, SerialInterface, IRInterface, RelayInterface
from struct import pack
import re


class DeviceClass():

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 5

        # Do not change this the variables values below
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Models = {
            'SW2 HDMI': self.extr_2_70_sw2,
            'SW4 HDMI': self.extr_2_70_sw4,
            'SW6 HDMI': self.extr_2_70_sw6,
            'SW8 HDMI': self.extr_2_70_sw8,
            }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AudioMute': {'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'Input': {'Status': {}},
            'IRSensor': {'Status': {}},
            'SignalStatus': {'Parameters': ['Input'], 'Status': {}},
            'VideoMute': {'Status': {}},
            }

    def SetAudioMute(self, value, qualifier):
        AudioMuteStateValues = {
            'On': '1Z',
            'Off': '0Z',
            }
        AudioMuteCmdString = AudioMuteStateValues[value]
        self.__SetHelper('AudioMute', AudioMuteCmdString, value, qualifier)

    def UpdateAudioMute(self, value, qualifier):

        AudioMuteStateNames = {
            b'0': 'Off',
            b'1': 'On',
            }
        AudioMuteCmdString = b'Z'

        res = self.__UpdateHelper('AudioMute', AudioMuteCmdString, value, qualifier)

        if res:
            try:
                value = AudioMuteStateNames[res[0:1]]
                self.WriteStatus('AudioMute', value, qualifier)
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateAudioMute')

    def SetExecutiveMode(self, value, qualifier):
        ExecutiveModeStateValues = {
            'On': '1X',
            'Off': '0X'
            }
        ExecutiveModeCmdString = ExecutiveModeStateValues[value]
        self.__SetHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):
        ExecutiveModeStateNames = {
            b'1': 'On',
            b'0': 'Off',
            }

        ExecutiveModeCmdString = b'X'
        res = self.__UpdateHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)
        if res:
            try:
                value = ExecutiveModeStateNames[res[0:1]]
                self.WriteStatus('ExecutiveMode', value, qualifier)
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateExecutiveMode')

    def SetInput(self, value, qualifier):
        InputStateValues = {
            '1': '1!',
            '2': '2!',
            '3': '3!',
            '4': '4!',
            '5': '5!',
            '6': '6!',
            '7': '7!',
            '8': '8!',
            'No Input': '0!'
            }
        InputCmdString = InputStateValues[value]
        self.__SetHelper('Input', InputCmdString, value, qualifier)

    def UpdateInput(self, value, qualifier):
        InputStateNames = {
            b'V1': '1',
            b'V2': '2',
            b'V3': '3',
            b'V4': '4',
            b'V5': '5',
            b'V6': '6',
            b'V7': '7',
            b'V8': '8',
            b'V0': 'No Input'
            }
        InputCmdString = b'I'
        res = self.__UpdateHelper('Input', InputCmdString, value, qualifier)
        if res:
            try:
                value = InputStateNames[res[0:2]]
                self.WriteStatus('Input', value, qualifier)
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateInput')

    def SetIRSensor(self, value, qualifier):
        IRSensorStateValues = {
            'Off': '0*65#',
            'On': '1*65#',
            }

        IRSensorCmdString = IRSensorStateValues[value]
        self.__SetHelper('IRSensor', IRSensorCmdString, value, qualifier)

    def UpdateIRSensor(self, value, qualifier):
        IRSensorStateNames = {
            b'0': 'Off',
            b'1': 'On',
            }

        IRSensorCmdString = b'65#'
        res = self.__UpdateHelper('IRSensor', IRSensorCmdString, value, qualifier)
        if res:
            try:
                value = IRSensorStateNames[res[0:1]]
                self.WriteStatus('IRSensor', value, qualifier)
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateIRSensor')

    def UpdateSignalStatus(self, value, qualifier):

        SignalStatusStateNames = {
            b'0': 'No Signal Present',
            b'1': 'Signal Present',
            }

        SignalStatusCmdString = b'\x1BLS\x0D'
        res = self.__UpdateHelper('SignalStatus', SignalStatusCmdString, value, qualifier)
       
        if res:
            try:                
                if self.InputSize == 2:
                    Input1 = SignalStatusStateNames[res[3:4]]
                    Input2 = SignalStatusStateNames[res[5:6]]
                    self.WriteStatus('SignalStatus', Input1, {'Input': 'Input 1'})
                    self.WriteStatus('SignalStatus', Input2, {'Input': 'Input 2'})
                elif self.InputSize == 4:
                    Input1 = SignalStatusStateNames[res[3:4]]                    
                    Input2 = SignalStatusStateNames[res[5:6]]
                    Input3 = SignalStatusStateNames[res[7:8]]
                    Input4 = SignalStatusStateNames[res[9:10]]
                    self.WriteStatus('SignalStatus', Input1, {'Input': 'Input 1'})
                    self.WriteStatus('SignalStatus', Input2, {'Input': 'Input 2'})
                    self.WriteStatus('SignalStatus', Input3, {'Input': 'Input 3'})
                    self.WriteStatus('SignalStatus', Input4, {'Input': 'Input 4'})
                elif self.InputSize == 6:
                    Input1 = SignalStatusStateNames[res[3:4]]
                    Input2 = SignalStatusStateNames[res[5:6]]
                    Input3 = SignalStatusStateNames[res[7:8]]
                    Input4 = SignalStatusStateNames[res[9:10]]
                    Input5 = SignalStatusStateNames[res[11:12]]
                    Input6 = SignalStatusStateNames[res[13:14]]
                    self.WriteStatus('SignalStatus', Input1, {'Input': 'Input 1'})
                    self.WriteStatus('SignalStatus', Input2, {'Input': 'Input 2'})
                    self.WriteStatus('SignalStatus', Input3, {'Input': 'Input 3'})
                    self.WriteStatus('SignalStatus', Input4, {'Input': 'Input 4'})
                    self.WriteStatus('SignalStatus', Input5, {'Input': 'Input 5'})
                    self.WriteStatus('SignalStatus', Input6, {'Input': 'Input 6'})
                elif self.InputSize == 8:
                    Input1 = SignalStatusStateNames[res[3:4]]
                    Input2 = SignalStatusStateNames[res[5:6]]
                    Input3 = SignalStatusStateNames[res[7:8]]
                    Input4 = SignalStatusStateNames[res[9:10]]
                    Input5 = SignalStatusStateNames[res[11:12]]
                    Input6 = SignalStatusStateNames[res[13:14]]
                    Input7 = SignalStatusStateNames[res[15:16]]
                    Input8 = SignalStatusStateNames[res[17:18]]
                    self.WriteStatus('SignalStatus', Input1, {'Input': 'Input 1'})
                    self.WriteStatus('SignalStatus', Input2, {'Input': 'Input 2'})
                    self.WriteStatus('SignalStatus', Input3, {'Input': 'Input 3'})
                    self.WriteStatus('SignalStatus', Input4, {'Input': 'Input 4'})
                    self.WriteStatus('SignalStatus', Input5, {'Input': 'Input 5'})
                    self.WriteStatus('SignalStatus', Input6, {'Input': 'Input 6'})
                    self.WriteStatus('SignalStatus', Input7, {'Input': 'Input 7'})
                    self.WriteStatus('SignalStatus', Input8, {'Input': 'Input 8'})
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateSignalStatus')

    def SetVideoMute(self, value, qualifier):
        VideoMuteStateValues = {
            'On': '1B',
            'Off': '0B',
            }
        VideoMuteCmdString = VideoMuteStateValues[value]
        self.__SetHelper('VideoMute', VideoMuteCmdString, value, qualifier)

    def UpdateVideoMute(self, value, qualifier):
        print('Here')
        VideoMuteStateNames = {
            b'0': 'Off',
            b'1': 'On',
            }

        VideoMuteCmdString = b'B'
        res = self.__UpdateHelper('VideoMute', VideoMuteCmdString, value, qualifier)
        if res:
            try:
                value = VideoMuteStateNames[res[0:1]]
                self.WriteStatus('VideoMute', value, qualifier)
            except (KeyError, IndexError):
                print('Invalid/unexpected response for UpdateVideoMute')

    def __CheckResponseForErrors(self, sourceCmdName, response):
        
        DEVICE_ERROR_CODES = {
            b'E01': 'Invalid input channel number',
            b'E06': 'Invalid input selection during auto-input switching',
            b'E10': 'Invalid Command',
            b'E13': 'Invalid value(out of range)'
            }
        
        if response:
            if response[0:3] in DEVICE_ERROR_CODES:
                ErrorString = sourceCmdName + DEVICE_ERROR_CODES[response[0:3]]
                print(ErrorString)
                response = ''
        return response

    def __SetHelper(self, command, commandstring, value, qualifier, queryDisallowTime=0):

        if self.Unidirectional == 'True':
            self.Send(commandstring)
        else:
            res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliTag='\r\n')
            if not res:
                print('Invalid/unexpected response')
            else:
                res = self.__CheckResponseForErrors(command + ':' + str(commandstring.strip()), res)
            
    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.Unidirectional == 'True':
            print('Inapproprite command ', command)
            return ''
        else:
            res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliTag='\r\n')
            if not res:
                return ''
            else:
                if self.initializationChk:
                    self.OnConnected()
                    self.initializationChk = False

                self.counter = self.counter + 1
                if self.counter > self.connectionCounter and self.connectionFlag:
                    self.OnDisconnected()
                    
                return self.__CheckResponseForErrors(command + ':' + str(commandstring.strip()), res)    

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        pass

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        

    def extr_2_70_sw2(self):

        self.InputSize = 2

    def extr_2_70_sw4(self):

        self.InputSize = 4

    def extr_2_70_sw6(self):

        self.InputSize = 6

    def extr_2_70_sw8(self):

        self.InputSize = 8
        
    ######################################################    
    # RECOMMENDED not to modify the code below this point
    ######################################################

    # Send  Control Commands
    def Set(self, command, value, qualifier=None):
        try:
            getattr(self, 'Set%s' % command)(value, qualifier)
        except AttributeError:
            print(command, 'does not support Set.')
        
    # Send Update Commands
    def Update(self, command, qualifier=None):
        try:
            getattr(self, 'Update%s' % command)(None, qualifier)    
        except AttributeError:
            print(command, 'does not support Update.')    

    def __ReceiveData(self, interface, data):
    # handling incoming unsolicited data
        self._ReceiveBuffer += data
        compile_list = self._compile_list
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para':arg}
                

    # Check incoming unsolicited data to see if it matched with device expectancy. 
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = search(regexString, self._ReceiveBuffer)                
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True      

    # This method is to tie a specific command with specific parameter to a call back method
    # when it value is updated. It all setup how often the command to be query, if the command
    # have the update method.
    # interval 0 is for query once, any other integer is used as the query interval.
    # If command doesn't have the update feature then that command is only used for feedback 
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method':{}}
        
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
        
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return
        
            Method['callback'] = callback
            Method['qualifier'] = qualifier    
        else:
            print(command, 'does not exist in the module')
        
    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription :
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)                
                
    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if self.connectionFlag == False:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return  
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)            

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

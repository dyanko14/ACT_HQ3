from extronlib.interface import EthernetClientInterface, EthernetServerInterface, SerialInterface, IRInterface, RelayInterface
from re import compile, findall, match, search
from extronlib.system import Wait


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
            'DXP 44 DVI Pro': self.extr_15_49_DVI44,
            'DXP 44 HDMI': self.extr_15_49_HDMI44,
            'DXP 48 DVI Pro': self.extr_15_49_DVI48,
            'DXP 48 HDMI': self.extr_15_49_HDMI48,
            'DXP 84 HDMI': self.extr_15_49_HDMI84,
            'DXP 84 DVI Pro': self.extr_15_49_DVI84,
            'DXP 88 DVI Pro': self.extr_15_49_DVI88,
            'DXP 88 HDMI': self.extr_15_49_HDMI88,
            }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AudioMute': {'Parameters': ['Output'], 'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'GlobalAudioMute': {'Status': {}},
            'GlobalVideoMute': {'Status': {}},
            'InputTieStatus': {'Parameters': ['Input', 'Output'], 'Status': {}},
            'MatrixTieCommand': {'Parameters': ['Input', 'Output', 'Tie Type'], 'Status': {}},
            'OutputTieStatus': {'Parameters': ['Output', 'Tie Type'], 'Status': {}},
            'RecallPreset': {'Status': {}},
            'SavePreset': {'Status': {}},
            'SignalStatus': {'Parameters': ['Input'], 'Status': {}},
            'Temperature': {'Status': {}},
            'VideoMute': {'Parameters': ['Output'], 'Status': {}},
        }

        self.lastInputSignalUpdate = 0
        
        self.OutputSize = 8
        self.OutputStatus = {'Video': [], 'Audio': []}
        self.OutputStatus['Video'] = [('0') for i in range(0, self.OutputSize)]
        self.OutputStatus['Audio'] = [('0') for i in range(0, self.OutputSize)]

        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'Amt([1-8])\*([0-1])\r\n'), self.__MatchAudioMute, None)
            self.AddMatchString(compile(b'Out(\d+) In(\d+) (\w{3})\r\n'), self.__MatchOutputTieStatus, None)
            self.AddMatchString(compile(b'Exe(0|1|2)\r\n'), self.__MatchExecutiveMode, None)
            self.AddMatchString(compile(b'Rpr[\d]{2}\r\n'), self.__MatchPreset, None)
            self.AddMatchString(compile(b'Vcu01 ([0-9 -]*)Vid\r\n'), self.__MatchAllMatrixTie, 'Video')
            self.AddMatchString(compile(b'Vcu01 ([0-9 -]*)Aud\r\n'), self.__MatchAllMatrixTie, 'Audio')
            self.AddMatchString(compile(b'Vmt([1-8])\*([0-1])\r\n'), self.__MatchVideoMute, None)
            self.AddMatchString(compile(b'In\d (\d+)\r\n'), self.__MatchSignalStatus, None)
            self.AddMatchString(compile(b'Sts00\*(\d{1,2}\.\d{2}) (\d{1,2}\.\d{2}) (\-|\+)(\d{3}\.\d{2}) (\d{5}) ([01])\r\n'), self.__MatchTemperature, None)

            self.AddMatchString(compile(b'E(\d+)\r\n'), self.__MatchErrors, None)
            self.AddMatchString(compile(b'Qik\r\n'), self.__MatchQik, None)

            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)

            if 'Serial' not in self.ConnectionType:
                self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 1:
            print('Log in failed. Please supply proper Admin password')
        else:
            self.Send(self.devicePassword + '\r\n')
        self.Authenticated = 'None'

    def __MatchLoginAdmin(self, match, tag):
        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):
        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def SetVerbose(self, value, qualifier):
        self.Send('w3cv\r\n')

    def __MatchVerboseMode(self, match, qualifier):

        self.VerboseDisabled = False
        self.UpdateAllMatrixTie(None, None)

        self.OnConnected()

    def __MatchPreset(self, match, tag):
        self.UpdateAllMatrixTie(None, None)

    def __MatchQik(self, match, tag):
        self.UpdateAllMatrixTie(None, None)

    def UpdateAllMatrixTie(self, value, qualifier):
        self.Send('w0*1*2vc\r')
        self.Send('w0*1*1vc\r')

    def __MatchAllMatrixTie(self, match, qualifier):
        inputList = findall(b'\d', match.group(1))
        Counter = 1
        for value in inputList:
            newInVal = str(int(value))
            self.__SetMatrixStatus(str(Counter), newInVal, qualifier)
            Counter += 1

    def __SetMatrixStatus(self, output, newInput, tag):
        print('output: ' , output, " newInput: ", newInput, " tag: ", tag)
        print(self.OutputStatus['Audio'])
        oldInput = self.OutputStatus[tag][int(output)-1]
        opTag = 'Audio' if tag == 'Video' else 'Video'
        if oldInput != newInput:
            self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': tag})
            opInVal = self.ReadStatus('OutputTieStatus', {'Output': output, 'Tie Type': opTag})
            prevInputTieStatus = self.ReadStatus('InputTieStatus', {'Input': oldInput, 'Output': output})
            if prevInputTieStatus == 'Audio/Video':
                self.WriteStatus('InputTieStatus', opTag, {'Input': oldInput, 'Output': output})
            else:
                self.WriteStatus('InputTieStatus', 'Untied', {'Input': oldInput, 'Output': output})

            if opInVal == newInput:
                self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', 'Audio/Video', {'Input': newInput, 'Output': output})
            else:
                self.WriteStatus('OutputTieStatus', '0', {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', tag, {'Input': newInput, 'Output': output})

            self.OutputStatus[tag][int(output)-1] = newInput

    def SetAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0',
            'On': '1',
        }
        channel = int(qualifier['Output'])
        if channel < 0 or channel > self.OutputSize:
            print('Invalid Command for SetAudioMute')
        else:
            self.__SetHelper('AudioMute', '{0}*{1}Z'.format(channel, AudioMuteState[value]), value, qualifier)

    def UpdateAudioMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 0 or channel > self.OutputSize:
            print('Invalid Command for UpdateAudioMute')
        else:
            self.__UpdateHelper('AudioMute', '{0}Z'.format(channel), value, qualifier)

    def __MatchAudioMute(self, match, qualifier):
        AudioMuteName = {
            b'0': 'Off',
            b'1': 'On',
        }
        self.WriteStatus('AudioMute', AudioMuteName[match.group(2)], {'Output': str(match.group(1).decode())})

    def SetExecutiveMode(self, value, qualifier):
        ExecutiveModeState = {
            'Off': '0',
            'Mode 1': '1',
            'Mode 2': '2',
        }
        self.__SetHelper('ExecutiveMode', '{0}X'.format(ExecutiveModeState[value]), value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):
        self.__UpdateHelper('ExecutiveMode', 'X', value, qualifier)

    def __MatchExecutiveMode(self, match, qualifier):
        ExecutiveModeName = {
            b'0': 'Off',
            b'1': 'Mode 1',
            b'2': 'Mode 2',
        }
        self.WriteStatus('ExecutiveMode', ExecutiveModeName[match.group(1)], None)

    def SetMatrixTieCommand(self, value, qualifier):

        TieTypeValues = {
            'Audio/Video': '!',
            'Video': '%',
            'Audio': '$',
        }

        Input = int(qualifier['Input'])
        tieType = qualifier['Tie Type']
        Output = int(qualifier['Output'])
        if Output < 0 or Output > self.OutputSize:
            print('Invalid Command for SetMatrixTieCommand')
        elif Input < 0 or Input > self.InputSize:
            print('Invalid Command for SetMatrixTieCommand')
        else:
            if Output == 0:
                MatrixTieCmdString = '{0}*{1}'.format(Input, TieTypeValues[tieType])
                self.__SetHelper('MatrixTieCommand', MatrixTieCmdString, value, qualifier)
            else:
                MatrixTieCmdString = '{0}*{1}{2}'.format(Input, Output, TieTypeValues[tieType])
                self.__SetHelper('MatrixTieCommand', MatrixTieCmdString, Output, qualifier)

    def __MatchOutputTieStatus(self, match, qualifier):
        TieTypeStates = {
            'Aud': 'Audio',  
            'Vid': 'Video', 
            'RGB': 'Video', 
            'All': 'Audio/Video',
        }
        output, input = str(int(match.group(1))), str(int(match.group(2)))
        tieType = TieTypeStates[match.group(3).decode()]
        if tieType != 'Audio/Video':
            self.__SetMatrixStatus(output, input, tieType)
        else:
            self.__SetMatrixStatus(output, input, 'Audio')
            self.__SetMatrixStatus(output, input, 'Video')        

    def SetGlobalAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0*Z',
            'On': '1*Z',
        }
        GlobalAudioString = AudioMuteState[value]
        self.__SetHelper('AudioMuteState', GlobalAudioString, value, qualifier)

    def SetGlobalVideoMute(self, value, qualifier):
        VideoMuteState = {
            'Off': '0*B',
            'On': '1*B',
        }
        GlobalVideoString = VideoMuteState[value]
        self.__SetHelper('VideoMuteState', GlobalVideoString, value, qualifier)

    def SetVideoMute(self, value, qualifier):
        VideoMuteState = {
            'Off': '0',
            'On': '1',
        }
        channel = qualifier['Output']
        if int(channel) < 0 or int(channel) > self.OutputSize:
            print('Invalid Command for SetVideoMute')
        else:
            self.__SetHelper('VideoMute', '{0}*{1}B'.format(channel, VideoMuteState[value]), value, qualifier)

    def UpdateVideoMute(self, value, qualifier):
        channel = qualifier['Output']
        if int(channel) < 0 or int(channel) > self.OutputSize:
            print('Invalid Command for UpdateVideoMute')
        else:
            VideoMuteCmdString = '{0}B'.format(channel)
            self.__UpdateHelper('VideoMute', VideoMuteCmdString, value, {'Output': channel})

    def __MatchVideoMute(self, match, qualifier):
        VideoMuteName = {
            b'0': 'Off',
            b'1': 'On',
        }
        self.WriteStatus('VideoMute', VideoMuteName[match.group(2)], {'Output': str(match.group(1).decode())})

    def SetSavePreset(self, value, qualifier):
        if 0 < int(value) <= 32:
            SavePresetCmdString = '{0},'.format(value)   
            self.__SetHelper('SavePreset', SavePresetCmdString, value, qualifier)
        else:
            print('Invalid Command for SetSavePreset')

    def SetRecallPreset(self, value, qualifier):
        if 0 < int(value) <= 32:
            RecallPresetCmdString = '{0}.'.format(value) 
            self.__SetHelper('RecallPreset', RecallPresetCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRecallPreset')

    def UpdateSignalStatus(self, value, qualifier):
        self.__UpdateHelper('SignalStatus', '0LS', value, qualifier)

    def __MatchSignalStatus(self, match, qualifier):

        InputList = match.group(1).decode()
        input = 1
        for stat in InputList:
            value = 'No Signal Detected' if stat == '0' else 'Signal Detected'
            self.WriteStatus('SignalStatus', value, {'Input': str(input)})
            input += 1

    def UpdateTemperature(self, value, qualifier):
        self.__UpdateHelper('Temperature', 'S', value, qualifier)

    def __MatchTemperature(self, match, qualifier):
        value = float(match.group(4))
        self.WriteStatus('Temperature', '%.2f' % value+'F', None)

    def __SetHelper(self, command, commandstring, value, qualifier, queryDisallowTime=0):
        self.Send(commandstring)
                 
    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter += 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()
        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)                    
        else:
            print('Inappropriate Command ', command)

    def __MatchErrors(self, match, tag):
        DEVICE_ERROR_CODES = {
            '01': 'Invalid input number (too large)',
            '10': 'Invalid command',
            '11': 'Invalid preset number',
            '12': 'Invalid output number or port number',
            '13': 'Invalid parameter (out of range)',
            '14': 'Command not available for this configuration',
            '17': 'System timed out (caused by direct write of global presets)',
            '21': 'Invalid room number',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device not present',
            '26': 'Maximum number of connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '30': 'Hardware failure (followed by a colon [:] and a descriptor number)',
            '31': 'Attempt to break port pass-through when it has not been set',
        }
        value = match.group(1).decode()
        if value in DEVICE_ERROR_CODES:
            print(DEVICE_ERROR_CODES[value])
        else:
            print('Unrecognized error code: ' + match.group(0).decode())

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        self.OutputStatus['Video'] = [('0') for i in range(0, self.OutputSize)]
        self.OutputStatus['Audio'] = [('0') for i in range(0, self.OutputSize)]

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        if 'Serial' not in self.ConnectionType:
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0
        self.VerboseDisabled = True

    def extr_15_49_DVI44(self):

        self.InputSize = 4
        self.OutputSize = 4

    def extr_15_49_DVI48(self):

        self.InputSize = 4
        self.OutputSize = 8

    def extr_15_49_DVI84(self):

        self.InputSize = 8
        self.OutputSize = 4

    def extr_15_49_DVI88(self):

        self.InputSize = 8
        self.OutputSize = 8

    def extr_15_49_HDMI44(self):

        self.InputSize = 4
        self.OutputSize = 4

    def extr_15_49_HDMI48(self):

        self.InputSize = 4
        self.OutputSize = 8

    def extr_15_49_HDMI84(self):

        self.InputSize = 8
        self.OutputSize = 4

    def extr_15_49_HDMI88(self):

        self.InputSize = 8
        self.OutputSize = 8

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
        if not self.connectionFlag:
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

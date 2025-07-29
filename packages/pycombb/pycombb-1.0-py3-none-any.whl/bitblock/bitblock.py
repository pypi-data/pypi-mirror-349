import serial
import time
from .constants import *
from .utils import * 
from termcolor import cprint

__all__ = [
    "Bitblock",
]

class Bitblock():
    def __init__(self, port, timeout=5, baud=57600, verbose=False):
        self.__verbose = verbose
        self.__port = port
        self.__timeout = timeout
        self.__baud = baud
        self.__client = None
        self._packetIndex = 1;
        self.display = self.Display(self)
        self.pin = self.PIN()

        self.__sensors = {
            'switch': [0, 0],
            'mic': 0,
            'lightSensor': [0, 0],
            'touchSensor': [0, 0, 0],
            'mpuSensor': [0, 0, 0, 0], # left, right, top, bottom
        };

    def connect(self):
        if self.__port and not self.__client:
            cprint(f'👽 Connect {self.__port}', "green")
            
            self.__client = serial.Serial(self.__port, self.__baud, timeout=self.__timeout)
            self.__client.flush()
        
            return True
        return False
    
    def disconnect(self):
        print("💧💧💧")
        print(self.__client)
        print(self.__client)

        
        if self.__client and self.__client.isOpen():
            try:
                cprint(f'🔥 Disconnect {self.__port}', 'red')
                # return asyncio.run(self.__client.disconnect())
                #  에러가 발생해서 호출 안하는 것으로 수정 2024.11.05
                # self._run_async(self.__client.disconnect())

                self.__client.flush()
                self.__client.close()

            except Exception as e:
                pass
   
    def send_command(self, data):
        if self.__client :
            try:
                self.__client.write(bytes(bytearray(data)))
                self.__client.flush()
            except Exception as e:
                print('An Exception occurred!', e)

    def read_data(self):
        data = []
        while len(data) < 20:
            if self.__client.inWaiting():
                c = self.__client.read()
                data.append(ord(c))
            else:
                time.sleep(.1)
        # print('return data length {0}'.format(len(data)))
        if len(data) == 20:
            return data
        else:
            print('Return data error!') 
            return []
        
    # def __process_return(self):
    #     data = []
    #     while len(data) < 20:
    #         if self.__client.inWaiting():
    #             c = self.__client.read()
    #             data.append(ord(c))
    #         else:
    #             time.sleep(.1)
    #     # print('return data length {0}'.format(len(data)))
    #     if len(data) == 20:
    #         return data
    #     else:
    #         print('Return data error!') 
    #         return []

    def __send(self, command):
        if self.__client :
            try:
                self.__client.write(bytes(bytearray(command)))
                self.__client.flush()
            except Exception as e:
                print('An Exception occurred!', e)
    
    def __get_index(self):
        self._packetIndex = (self._packetIndex + 1) % 256  # 0~255 사이에서 순환
        return self._packetIndex
    
    class PIN:
        def __init__(self):
            self.P0 = 10 
            self.P1 = 4
            self.P2 = 8
            self.P3 = 2
            self.P4 = 9
            self.P7 = 39
            self.P11 = 7
            self.P12 = 18
            self.SERVO = 16
            self.DCMOTOR = 46

    # -------------------------------------------------------
    #   DISPLAY (LED MATRIX)
    # -------------------------------------------------------
    class Display():
        def __init__(self, controler=None):
            self.__controller = controler

        def __color(self, color):
            if isinstance(color, str):
                r, g, b = (0, 0, 0)
                # Hex 색상 코드인 경우
                if color.startswith("#") and len(color) == 7:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                else:
                    raise ValueError("Invalid color string format. Expected format: '#RRGGBB'")
            elif (isinstance(color, list) or isinstance(color, tuple)) and len(color) == 3:
                # RGB 리스트인 경우
                r, g, b = color
                if not all(0 <= val <= 255 for val in (r, g, b)):
                    raise ValueError("RGB values must be between 0 and 255.")
            else:
                raise TypeError("Color must be a string in '#RRGGBB' format or a list [R, G, B].")
            return r, g, b

        def color(self, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_COLOR
            command[BBPACKET.DATA1] = r
            command[BBPACKET.DATA2] = g
            command[BBPACKET.DATA3] = b
            self.__controller._Bitblock__send(command)

        def symbol(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_SYMBOL
            command[BBPACKET.DATA1] = symbol[0]
            command[BBPACKET.DATA2] = symbol[1]
            command[BBPACKET.DATA3] = symbol[2]
            command[BBPACKET.DATA4] = symbol[3]
            command[BBPACKET.DATA5] = symbol[4]
            command[BBPACKET.DATA6] = r
            command[BBPACKET.DATA7] = g
            command[BBPACKET.DATA8] = b
            self.__controller._Bitblock__send(command)

        def row(self, row, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_ROW
            command[BBPACKET.DATA1] = symbol
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            command[BBPACKET.DATA5] = row
            self.__controller._Bitblock__send(command)

        def bright(self, bright):
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_BRIGHT
            command[BBPACKET.DATA1] = bright
            self.__controller._Bitblock__send(command)

        def char(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_CHAR
            command[BBPACKET.DATA1] = ord(symbol)
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            self.__controller._Bitblock__send(command)


        def num(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_NUM;
            command[BBPACKET.DATA1] = int(symbol);
            command[BBPACKET.DATA2] = r;
            command[BBPACKET.DATA3] = g;
            command[BBPACKET.DATA4] = b;
            self.__controller._Bitblock__send(command)

        def xy(self, coordX, coordY, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_XY;
            command[BBPACKET.DATA1] = r;
            command[BBPACKET.DATA2] = g;
            command[BBPACKET.DATA3] = b;
            command[BBPACKET.DATA4] = coordX;
            command[BBPACKET.DATA5] = coordY;
            self.__controller._Bitblock__send(command)

        def effect(self, no):
            """
            정해진 효과를 표시한다.
            
            Parameters:
                no (int): 효과 번호 (e.g., 0, 1, 2).
            Returns:
                0: 무지개 효과 
                1: 폭포 효과
                2: 와이퍼 효과 

            Example:
                None
            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_EFFECT
            command[BBPACKET.DATA1] = no
            command[BBPACKET.DATA2] = 1     # 아두이노에서 사용하는 값
            self.__controller._Bitblock__send(command)

        def clear(self):
            self.color("#000000")
    # --- END OF DIAPLAY ----------------------------------------------
    # -------------------------------------------------------
    # BUZZER
    # -------------------------------------------------------
    def note(self, note, time):
        # time 은 미리초 단위로 넘어온다.
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_NOTE;
        command[BBPACKET.DATA1] = note;

        ah = (time >> 8) & 0xff; # 상위 바이트
        al = time & 0xff;
        command[BBPACKET.DATA2] = ah;
        command[BBPACKET.DATA3] = al;
        self.__send(command)

    def melody(self, melody):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_MELODY;
        command[BBPACKET.DATA1] = melody;
        self.__send(command)

    def beep(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_BEEP;
        self.__send(command)

    # -------------------------------------------------------
    # BUTTON
    # -------------------------------------------------------    
    def button(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUTTON
        self.__send(command)
        packet = self.read_data()

        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # print(self._packetIndex, ' ## ', packet[BBRETURN.INDEX])
        # print(split_and_join(packet))
        # A, B 버튼 동시 리턴 
        return packet[BBRETURN.DATA1]==1, packet[BBRETURN.DATA2]==1
       

    # -------------------------------------------------------
    # TOUCH SENSOR
    # -------------------------------------------------------    
    # def touch_init(self):
    #     '''사용하지 않음'''
    #     command = NULL_COMMAND_PACKET[:]
    #     command[BBPACKET.INDEX] = self.__get_index()
    #     command[BBPACKET.ACTION] = ACTION_CODE.TOUCH;
    #     command[BBPACKET.DATA0] = ACTION_MODE.TOUCH_INIT;
    #     self.__send(command)

    
    def touch(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.TOUCH;
        command[BBPACKET.DATA0] = ACTION_MODE.TOUCH_VALUES;
        self.__send(command)
        packet = self.read_data()

        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return

        # 5, 6
        al = packet[5]
        ah = packet[6]
        p0 = (ah << 8) | al;

        # 7, 8
        al = packet[7]
        ah = packet[8]
        p1 = (ah << 8) | al;

        # 9, 10
        al = packet[9]
        ah = packet[10]
        p2 = (ah << 8) | al;

        return p0==1, p1==1, p2==1

    # -------------------------------------------------------
    # MPU
    # -------------------------------------------------------    
    def tilt(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.MPU_ACTION;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        return packet[13]==1,packet[14]==1,packet[15]==1,packet[16]==1
    # -------------------------------------------------------
    # 밝기 센서
    # -------------------------------------------------------   
    def light(self):
        # 0 ~ 1023
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.LIGHT_SENSOR;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # 5, 6
        al = packet[5]
        ah = packet[6]
        l1 = (ah << 8) | al;

        # 7, 8
        al = packet[7]
        ah = packet[8]
        l2 = (ah << 8) | al;
        return l1, l2
    
    # -------------------------------------------------------
    # 소리 센서
    # -------------------------------------------------------   
    def mic(self):
       # 0 ~ 1023
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.MIC_SENSOR;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # 5, 6
        al = packet[5]
        ah = packet[6]
        val = (ah << 8) | al;
        return val

    # -------------------------------------------------------
    # 디지털 입출력
    # -------------------------------------------------------   
    def digital_write(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.DIGITAL
        command[BBPACKET.DATA0] = ACTION_MODE.DIGITAL_OUTPUT
        command[BBPACKET.DATA1] = pin
        command[BBPACKET.DATA2] = val
        self.__send(command)
    

    def digital_read(self, pin):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.DIGITAL
        command[BBPACKET.DATA0] = ACTION_MODE.DIGITAL_PULLUP    #디지털 풀업
        command[BBPACKET.DATA1] = pin
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        val = packet[5]
        return val

    # -------------------------------------------------------
    # 아날로그 입출력
    # -------------------------------------------------------   
    def analog_write(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ANALOG;
        command[BBPACKET.DATA0] = ACTION_MODE.ANALOG_OUTPUT;
        command[BBPACKET.DATA1] = pin;

        # 0 ~ 1023
        # val 값을 상위 바이트와 하위 바이트로 분리
        ah = (val >> 8) & 0xff  # 상위 바이트
        al = val & 0xff         # 하위 바이트

        command[BBPACKET.DATA2] = al; # 펌웨어에서 readShort 함수를 사용할려면 상위와 하위를 조심
        command[BBPACKET.DATA3] = ah;
        self.__send(command)

    def analog_read(self, pin):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ANALOG;
        command[BBPACKET.DATA0] = ACTION_MODE.ANALOG_INPUT;
        command[BBPACKET.DATA1] = pin;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        
        # 5, 6
        al = packet[5]
        ah = packet[6]
        val = (ah << 8) | al;
        return val


    def dcmotor(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ANALOG
        command[BBPACKET.DATA0] = ACTION_MODE.ANALOG_OUTPUT
        command[BBPACKET.DATA1] = pin
        # 0 ~ 1023
        ah = (val >> 8) & 0xff      # 상위 바이트
        al = val & 0xff
        command[BBPACKET.DATA2] = al    # 펌웨어에서 readShort 함수를 사용할려면 상위와 하위를 조심
        command[BBPACKET.DATA3] = ah
        self.__send(command)

    # 메인보드의 서버도 핀번호로 동작시키자 
    def servo(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        if pin == self.pin.SERVO:
            command[BBPACKET.ACTION] = ACTION_CODE.MAIN_SERVO
        else:
            command[BBPACKET.ACTION] = ACTION_CODE.SERVO
        command[BBPACKET.DATA0] = pin;
        command[BBPACKET.DATA1] = val;
        self.__send(command)

    
    def ultrasonic(self, trig, echo):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ULTRASONIC
        command[BBPACKET.DATA0] = trig
        command[BBPACKET.DATA1] = echo
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        return packet[5]
    
    def dht11(self, pin):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.TMPHUM
        command[BBPACKET.DATA0] = pin
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        temp = packet[5]
        humi = packet[6]
        return temp, humi
    # -----------------------------------------------------------------
    # 🔥 UTIL 함수
    # -----------------------------------------------------------------
    def delay(self, sec):
        """기다리기

        Args:
            sec (float): 초
        Returns:
            None
        """
        time.sleep(sec)

    def delayms(self,ms):
            """기다리기

            Args:
                ms (float): 밀리초
            Returns:
                None
            """
            self.delay(ms/1000)


    def wait(self, ms):
            """기다리기

            Args:
                ms (float): 밀리초
            Returns:
                None
            """
            self.delay(ms/1000)

    # -----------------------------------------------------------------
    # 🔥 Bitblock 내부 클래스로 정의
    # -----------------------------------------------------------------
    def rccar_init(self):
        return self.RCCar(self)

    class RCCar():
        def __init__(self, controler=None):
            self.__controller = controler
            # print(dir(self.__controller))
            self.__init()

        def __init(self):
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.RCCAR
            command[BBPACKET.DATA0] = ACTION_MODE.RCCAR_INITIALIZE
            self.__controller._Bitblock__send(command)

        def __rlspeed(self, dir_l, speed_l, dir_r, speed_r):
            """
            RCCar의 왼쪽 오른쪽 바퀴의 회전 속도와 방향을 설정해서 동작시킨다.
            
            Parameters:
                dir_l (int): 왼쪽 바퀴의 방향 (e.g., forward(0), or reverse(1)).
                speed_l (int): 왼쪽 바퀴의 속도 (e.g., 0 ~ 255).
                dir_r (int): 오른쪽 바퀴의 방향 (e.g., forward(0), or reverse(1)). 
                speed_r (int): 오른쪽 바퀴의 방향 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                    self.rlspeed(dir_l=1, speed_l=50, dir_r=1, speed_r=50)
            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.RCCAR
            command[BBPACKET.DATA0] = ACTION_MODE.RCCAR_RLSPEED
            command[BBPACKET.DATA1] = dir_l;
            command[BBPACKET.DATA2] = speed_l;
            command[BBPACKET.DATA3] = dir_r;
            command[BBPACKET.DATA4] = speed_r;
            self.__controller._Bitblock__send(command)

        def move_forward(self, speed=100):
            """
            주어진 속도(speed)로 앞으로 이동한다.
            
            Parameters:
                speed (int): 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(0, int(abs(speed)), 0, int(abs(speed)))
        
        def move_backward(self, speed=100):
            """
            주어진 속도(speed)로 뒤로 이동한다.
            
            Parameters:
                speed (int): 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(1, int(abs(speed)), 1, int(abs(speed)))
        
        def turn_left(self, speed=100):
            """
            주어진 속도(speed)로 왼쪽으로 회전한다. 왼쪽 바퀴의 속도는 speed * 0.5로 설정된다.
            
            Parameters:
                speed (int): 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(0, int(abs(speed)/2), 0, int(abs(speed)))

        def turn_right(self, speed=100):
            """
            주어진 속도(speed)로 오른으로 회전한다. 오른쪽 바퀴의 속도는 speed * 0.5로 설정된다.
            
            Parameters:
                speed (int): 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(0, int(abs(speed)), 0, int(abs(speed)/2))

        def pivot_left(self, speed=100):
            """
            왼쪽으로 제자리 돌기
            
            Parameters:
                speed (int): 회전 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(1, int(abs(speed)), 0, int(abs(speed)))
        
        def pivot_right(self, speed=100):
            """
            오른쪽으로 제자리 돌기
            
            Parameters:
                speed (int): 회전 속도 (e.g., 0 ~ 255).

            Returns:
                None

            Example:
                None
            """
            self.__rlspeed(0, int(abs(speed)), 1, int(abs(speed)))
        
        
        def wheels(self, lspeed=100, rspeed=100):
            """
            RCCar의 왼쪽 오른쪽 바퀴의 회전 속도와 방향을 설정해서 동작시킨다.
            
            Parameters:
                lspeed (int): 왼쪽 바퀴의 속도. 음수값이면 역회전 (e.g., -255 ~ 255).
                rspeed (int): 오른쪽 바퀴의 속도. 음수값이면 역회전 (e.g., -255 ~ 255).

            Returns:
                None

            Example:
                    self.wheels(50, -50)
            """
            ldir = 0 if lspeed >= 0 else 1
            rdir = 0 if rspeed >= 0 else 1
            self.__rlspeed(ldir , int(abs(lspeed)), rdir, int(abs(rspeed)))

        def stop(self):
            """
            RCCar 바퀴의 동작을 멈춥니다.
            
            Parameters:
                None

            Returns:
                None

            Example:
                    self.stop()
            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.RCCAR
            command[BBPACKET.DATA0] = ACTION_MODE.RCCAR_STOP
            self.__controller._Bitblock__send(command)


        def distance(self):
            """
            RCCar의 거리센서(초음파센서)값을 반환한다.

            Returns:
                int: 앞의 장애물과의 거리 (cm)

            Example:
                val = self.distance()

            Note:
                None

            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.RCCAR
            command[BBPACKET.DATA0] = ACTION_MODE.RCCAR_DISTANCE
            command[BBPACKET.DATA1] = 39 #P7
            command[BBPACKET.DATA2] = 5  #P9
            self.__controller._Bitblock__send(command)
            packet = self.__controller.read_data()
            if self.__controller._packetIndex != packet[BBRETURN.INDEX]:
                print(ERROR.WRONG_PACKET_INDEX)
                return
            return packet[6]
        

        def line(self):
            """
            RCCar의 라인 센서값을 반환한다.

            Returns:
                tuple: 3개의 라인센서 값을 포함한다. (왼쪽, 중간, 오른쪽)값을 나타낸다.

            Example:
                l1, l2, l3 = self.line()
                print(f"Sensor values: {l1}, {l2}, {l3}")

            Note:
                None

            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.RCCAR
            command[BBPACKET.DATA0] = ACTION_MODE.RCCAR_LINESENSOR
            self.__controller._Bitblock__send(command)
            packet = self.__controller.read_data()
            if self.__controller._packetIndex != packet[BBRETURN.INDEX]:
                print(ERROR.WRONG_PACKET_INDEX)
                return
            # 6, 7
            al = packet[6]
            ah = packet[7]
            l1 = (ah << 8) | al;

            # 8, 9
            al = packet[8]
            ah = packet[9]
            l2 = (ah << 8) | al;

            # 10, 11
            al = packet[10]
            ah = packet[11]
            l3 = (ah << 8) | al;
            return l1, l2, l3

        # 메인보드의 서버도 핀번호로 동작시키자 
        def servo(self, pin, val):
            """
            RCCar의 뒷쪽 커넥터에 연결된 서보모터를 동작시킨다.

            Returns:
                pin (int): P3, P4 3개의 핀 중 하나.

            Example:
                l1, l2, l3 = self.linesensor()
                print(f"Sensor values: {l1}, {l2}, {l3}")

            Note:
                비트블록 1.x 버전은 P3 사용 가능 
                비트블록 2.x 이상은 P3, P4 사용 가능 

            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Bitblock__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.SERVO
            command[BBPACKET.DATA0] = pin
            command[BBPACKET.DATA1] = clamp(val)
            self.__controller._Bitblock__send(command)

# END CLASS




# microbit-module: haizen@1.0.0
from microbit import *
"""
SWITCH EDUCATION
ロボットベースを配膳ロボットとして使うためのモジュール
"""

motorStatus = "move"
motorPin = {'p13':[False,0], 'p14':[False,0], 'p15':[False,0], 'p16':[False,0]}
optionPin = {'p8':[True,0,1], 'p9':[True,0,2], 'p10':[False,0,0], 'p12':[False,0,0]}

'''
write_analog()をまとめて扱うための関数
'''
def analogOut(pin,data=0):
    
    if pin == pin8:
        if optionPin['p8'][2] == 0:
            for i in optionPin:
                if optionPin[i][2] == 1:
                    optionPin[i][2] = 0
                    optionPin[i][0] = False
                elif optionPin[i][2] == 2:
                    optionPin[i][2] = 1
            optionPin['p8'][2] = 2
            optionPin['p8'][0] = True
        optionPin['p8'][1] = data
    elif pin == pin9:
        if optionPin['p9'][2] == 0:
            for i in optionPin:
                if optionPin[i][2] == 1:
                    optionPin[i][2] = 0
                    optionPin[i][0] = False
                elif optionPin[i][2] == 2:
                    optionPin[i][2] = 1
            optionPin['p9'][2] = 2
            optionPin['p9'][0] = True
        optionPin['p9'][1] = data
    elif pin == pin10:
        if optionPin['p10'][2] == 0:
            for i in optionPin:
                if optionPin[i][2] == 1:
                    optionPin[i][2] = 0
                    optionPin[i][0] = False
                elif optionPin[i][2] == 2:
                    optionPin[i][2] = 1
            optionPin['p10'][2] = 2
            optionPin['p10'][0] = True
        optionPin['p10'][1] = data
    elif pin == pin12:
        if optionPin['p12'][2] == 0:
            for i in optionPin:
                if optionPin[i][2] == 1:
                    optionPin[i][2] = 0
                    optionPin[i][0] = False
                elif optionPin[i][2] == 2:
                    optionPin[i][2] = 1
            optionPin['p12'][2] = 2
            optionPin['p12'][0] = True
        optionPin['p12'][1] = data  
        
    if pin == pin13:
        motorPin['p13'][0] = True
        motorPin['p13'][1] = data
        motorPin['p15'][0] = False
    elif pin == pin14:
        motorPin['p14'][0] = True
        motorPin['p14'][1] = data
        motorPin['p16'][0] = False
    elif pin == pin15:
        motorPin['p15'][0] = True
        motorPin['p15'][1] = data
        motorPin['p13'][0] = False
    elif pin == pin16:
        motorPin['p16'][0] = True
        motorPin['p16'][1] = data
        motorPin['p14'][0] = False
    
    if motorStatus == "stop":
        if motorPin['p13'][0] == False:
            pin13.write_digital(1)
        if motorPin['p14'][0] == False:
            pin14.write_digital(1)
        if motorPin['p15'][0] == False:
            pin15.write_digital(1)
        if motorPin['p16'][0] == False:
            pin16.write_digital(1)
    else:
    
        if motorPin['p13'][0] == False:
            pin13.write_digital(0)
        if motorPin['p14'][0] == False:
            pin14.write_digital(0)
        if motorPin['p15'][0] == False:
            pin15.write_digital(0)
        if motorPin['p16'][0] == False:
            pin16.write_digital(0)
            
    if optionPin['p8'][0] == False:
        pin8.write_digital(0)
    if optionPin['p9'][0] == False:
        pin9.write_digital(0)
    if optionPin['p10'][0] == False:
        if pin10.get_mode() != "display":
            pin10.write_digital(0)
    if optionPin['p12'][0] == False:
        pin12.write_digital(0)


    count= 0
    for i in motorPin:
        if motorPin[i][0] == True:
            count += 1
    for i in optionPin:
        if optionPin[i][0] == True:
            count += 1
    
    if count <= 4:    
        if optionPin['p8'][0] == True:
            pin8.write_analog(optionPin['p8'][1])
        if optionPin['p9'][0] == True:
            pin9.write_analog(optionPin['p9'][1])
        if optionPin['p10'][0] == True:
            if pin10.get_mode() != "display":
                pin10.write_analog(optionPin['p10'][1])
        if optionPin['p12'][0] == True:
            pin12.write_analog(optionPin['p12'][1])
        
        if motorPin['p13'][0] == True:
            pin13.write_analog(motorPin['p13'][1])
        if motorPin['p14'][0] == True:
            pin14.write_analog(motorPin['p14'][1])
        if motorPin['p15'][0] == True:
            pin15.write_analog(motorPin['p15'][1])
        if motorPin['p16'][0] == True:
            pin16.write_analog(motorPin['p16'][1])




class Lcd():
    """
    I2C接続のキャラクター液晶を制御します。
    """
    def __init__(self):
        try:
            self.address = 0x3E
            i2c.init()
            self.lcd_init()
        except:
            pass

    def lcd_init(self):
        """
        LCDを初期化するための命令です。
        """

        try:
            buf = bytearray(2)
            buf[0] = 0x00
            buf[1] = 0x38
            sleep(100)
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x39
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x14
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x73
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x56
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x6C
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x38
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x01
            i2c.write(self.address, buf)
            sleep(20)
            buf[1] = 0x0C
            i2c.write(self.address, buf)
        except:
            pass

    def write_data(self, data):
        """
        LCDに文字を表示させる命令です。
        :param data : 文字列
        """
        try:
            # i2c.write(address,b'\x40')
            buf0 = bytearray([0x40])
            buf1 = bytearray(data)
            buf = buf0 + buf1
            i2c.write(self.address, buf)
            sleep(1)
        except OSError:
            display.scroll('ENODEV')

    def clear(self):
        """
        LCD画面の表示をすべて消す命令です。
        """
        self.write_command(0x01)
        sleep(10)

    def write_command(self, com):
        """
        LCD操作用のコマンドを送信するための命令です。
        """
        try:
            buf = bytearray([0x00,com])
            i2c.write(self.address,buf)
            sleep(10)
        except OSError:
            display.scroll('ENODEV')

    def move_cursor(self, line = 0, col = 0):
        """
        カーソルの位置を動かすための命令です。
        行（line)と列（col）で位置を指定します。
        lineとcolそれぞれ０から始まります。
        :param int line : 行
        :param int col : 列
        """
        if line < 0:
            line = 0
        if col < 0:
            col = 0
        ddram_address = line * 0x40 + col
        self.write_command(0x80 + ddram_address)
        sleep(1)

class Servo180:
    """
    サーボモーターを使用するピン番号を指定します。
    ピン番号はpin8,pin9,pin10,pin12から選択可能です。
    pin10はmicro:bitのLEDと共用です。使用する場合は事前にdisplay.off()が必要です。
    デフォルトでpin9が割り当てられます。
    """

    def __init__(self, pin = pin9):
        self.PWM_PERIOD = 20
        self.pwm_angle = 76
        self.pin_num = pin
        self.pin_num.set_analog_period(self.PWM_PERIOD)

    def set_angle(self, angle):
        """
        角度を0～180の範囲で指定します。
        :param int angle : 角度
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        self.pwm_angle = (100/180)*angle + 26
        analogOut(self.pin_num,int(self.pwm_angle))

class Servo360:
    """
    連続回転サーボモーターを制御します。
    ピン番号はpin8,pin9,pin10,pin12から選択可能です。
    pin10はmicro:bitのLEDと共用です。使用する場合は事前にdisplay.off()が必要です。
    デフォルトでpin12が割り当てられます。
    """
    def __init__(self, pin = pin12):
        self.PWM_PERIOD = 20
        self.pin_num = pin
        self.STOP_SIGNAL = 76
        self.pin_num.set_analog_period(self.PWM_PERIOD)

    def set_speed(self, speed):
        """
        speedを-100～100の範囲で指定します。
        0にすると停止、符号によって回転の向きが変わります。
        0で停止しない場合は回転サーボモーターのトリマーを調整するか、
        1,2等の0付近の小さい値を入れてください。
        :param int speed : 回転速さと向き
        """
        if speed < -100:
            speed = -100
        elif speed > 100:
            speed = 100
        self.servo_signal = (8 / 100) * speed + self.STOP_SIGNAL
        analogOut(self.pin_num,int(self.servo_signal))


class WheelMotor:
    """
    走行するためのモーター2個を制御します。
    pin13,pin14,pin15,pin16を使用します。
    """
    

    def __init__(self,lm_in1 = pin13, lm_in2 = pin15, rm_in1 = pin14, rm_in2 = pin16):
        self.lm_in1 = lm_in1
        self.lm_in2 = lm_in2
        self.rm_in1 = rm_in1
        self.rm_in2 = rm_in2

    def set_speed_l(self, speed_l):
        """
        左モーターの速さを-100～100の範囲で指定します。
        ０にすると停止します。符号によって回転の向きが変わります。
        :param int speed_l :左モーター速さ
        """
        global motorStatus
        motorStatus = "move"
        
        if speed_l < -100:
            speed_l = -100
        elif speed_l > 100:
            speed_l = 100
        

        if speed_l >= 0:
            analogOut(self.lm_in2, int((1023 / 100) * speed_l))
        else:
            analogOut(self.lm_in1, int((1023 / 100) * (-speed_l)))

    def set_speed_r(self, speed_r):
        """
        右モーターの速さを-100～100の範囲で指定します。
        ０にすると停止します。符号によって回転の向きが変わります。
        :param int speed_r : 右モーターの速さ
        """
        global motorStatus
        motorStatus = "move"
        
        if speed_r < -100:
            speed_r = -100
        elif speed_r > 100:
            speed_r = 100

        if speed_r >= 0:
            analogOut(self.rm_in2,int((1023 / 100) * speed_r))
        else:
            analogOut(self.rm_in1,int((1023 / 100) * (-speed_r)))

    def set_speed(self, speed_l, speed_r):
        """モーターの速さ設定
        左右のモーターの速さを-100～100の範囲で指定します。
        0にすると停止します。符号によって回転の向きが変わります。
        :param int speed_l: 左モーターの速さ -100～100
        :param int speed_r: 右モーターの速さ -100～100
        """
        self.set_speed_l(speed_l)
        self.set_speed_r(speed_r)
    
    def stop(self):
        """
        ブレーキをかけて停止します。
        """
        
        self.lm_in1.write_digital(1)
        self.lm_in2.write_digital(1)
        self.rm_in1.write_digital(1)
        self.rm_in2.write_digital(1)

        for i in motorPin:
            motorPin[i][0] = False
            motorPin[i][1] = 1023
            
        
        global motorStatus
        motorStatus = "stop"


start_time_of_find_marker = 0
state_of_find_marker = False

def find_marker(pin = pin0,threshold = 200,timeout = 2000):
    """
    テーブルのマーカーを見つけるための関数です。
    センサーの状態が白ー＞黒ー＞白に変化する時間を返します。
    :param pin: センサーのピン番号　デフォルトPin0
    :param int threshold: センサーの閾値 デフォルト200
    :param int timeout: この値より長い時間(ms)は無視します。デフォルト2000ms
    """

    global state_of_find_marker
    global start_time_of_find_marker

    sensor0 = pin.read_analog()
    if state_of_find_marker == False:
        if sensor0 < threshold:
            start_time_of_find_marker = running_time()
        else:
            state_of_find_marker = True
    else:
        if sensor0 < threshold:
            state_of_find_marker = False
            time = running_time() - start_time_of_find_marker
            if time >= 2000:
                return 0
            else:
                return time
    return 0
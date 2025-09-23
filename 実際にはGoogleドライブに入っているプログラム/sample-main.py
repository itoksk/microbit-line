# Imports go at the top
from microbit import *
from haizen import *
import music

motor = WheelMotor()


table_counter = 0
target_table = 1

display.show(table_counter)

def trace_line():
    sensor1 = pin1.read_analog()
    sensor2 = pin2.read_analog()
    th = 200                               #白と黒の閾値

    if sensor1 < th and sensor2 < th:      #白　白
        motor.set_speed(50,50)
    elif sensor1 >= th and sensor2 < th:   #黒　白  
        motor.set_speed(0,50)
    elif sensor1 < th and sensor2 >= th:   #白　黒
        motor.set_speed(50,0)
    else:                                  #黒　黒（ゴールライン）
        motor.stop()
        
while True:
    #線に沿って進む
    trace_line()
    #テーブルマーカーを探す
    if find_marker() > 10:
        music.play(music.BA_DING, pin=None, wait=False)
        table_counter = table_counter + 1
        display.show(table_counter)
        
        #目標のテーブルに到達したら
        if table_counter == target_table:
            motor.stop()
            sleep(2000)
            #配膳動作を記述






import network,usocket,time
from machine import I2C,Pin,Timer,PWM
from somewhere_you_dont_see import ssid, pwd

LED = Pin(2, Pin.OUT)    # 初始化WIFI指示灯


def Beep_twice():
    Beep = PWM(Pin(25), freq=800, duty=512)
    Beep.freq(800)
    time.sleep_ms(50)
    Beep.freq(600)
    time.sleep_ms(30)
    Beep.freq(800)
    time.sleep_ms(50)
    Beep.deinit()
    del Beep
    
def Long_Beep_Once():
    Beep = PWM(Pin(25), freq=800, duty=512)
    Beep.freq(800)
    time.sleep_ms(250)
    Beep.deinit()
    del Beep

def WIFI_Connect():
    
    wlan = network.WLAN(network.STA_IF)    # STA模式
    wlan.active(True)
    
    #激活接口
    start_time = time.time()    #记录时间做超时判断 
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, pwd)   # 输入WIFI账号密码 
        while not wlan.isconnected():
            #超时判断,15秒没连接成功判定为超时 
            if time.time()-start_time > 15 :
                Long_Beep_Once()
                print('WIFI Connected Timeout!')
                break
            
    if wlan.isconnected():
        #串口打印信息
        Beep_twice()
        print('network information:', wlan.ifconfig())
        return wlan
    else:
        return False

def main():
    wlan = WIFI_Connect()
    if wlan is not False:
        #创建socket连接，连接成功后发送“Hello”给服务器。 
        s = usocket.socket()
        addr = ('192.168.1.102', 10000)    #服务器IP和端口 
        s.connect(addr)
        s.send('Your ESP32 is online \r\n')
        time.sleep_ms(100)
        s.send('Send "ON" to turn the light on \r\n')
        time.sleep_ms(100)
        s.send('Send "OFF" to turn the light off \r\n')
        
        while True:
            text = s.recv(128)
            if text == '':
                pass
            elif text.decode('utf-8') == 'ON':
                LED.value(1)
                s.send('Light has been turned on.\n')
            elif text.decode('utf-8') == 'OFF':
                LED.value(0)
                s.send('Light has been turned off.\n')
            elif text.decode('utf-8') == 'BLINK':
                s.send('Light is now going to blink.\n')
                LED.value(1)
                time.sleep(0.5)
                LED.value(0)
                time.sleep(0.5)
                LED.value(1)
                time.sleep(0.5)
                LED.value(0)
                time.sleep(0.5)
                LED.value(1)
                time.sleep(0.5)
                LED.value(0)
                time.sleep(0.5)
            else:
                s.send('Please send a proper command. Wake me up later, bye~\n')
                break

if __name__ == '__main__':
    main()

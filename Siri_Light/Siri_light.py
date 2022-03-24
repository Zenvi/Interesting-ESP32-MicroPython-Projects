import network,time
import usocket as socket
from machine import I2C,Pin,Timer,PWM
from re import search
from somewhere_you_dont_see import ssid, pwd

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

led = Pin(2, Pin.OUT)

wlan = WIFI_Connect()

ip = wlan.ifconfig()[0]
port = 80
webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
webserver.bind([ip, port])
webserver.listen(5)
print('Server Address: {}:{}'.format(ip, port))

while True:
    conn, addr = webserver.accept()
    request = conn.recv(1824)
    if len(request) > 0:
        request = request.decode()
        result = search("(.*?)(.*?) HTTP/1.1", request)

        if result:
            method = result.group(1)
            url = result.group(2)
            conn.send("HTTP/1.1 0K\r\n")
            conn.send("Server: Esp32\r\n")
            conn.send("Content-Type: text/html; charset=UTF-8\r\n")
            conn.send("Connection: close\r\n")
            conn.send("\r\n")
            conn.close()
            if url.endswith("/led1"):
                led.value(1)
                print("Lights on")
            elif url.endswith("/led2"):
                led.value(0)
                print("Lights off")
            elif url.endswith("/led3"):
                print("Led is going to blink")
                state = 1
                for i in range(5):
                    led.value(state)
                    time.sleep(0.5)
                    if state == 1:
                        state = 0
                    elif state == 0:
                        state = 1
            else:
                pass
        else:
            print("not found url")
    else:
        print("no request")
        conn.close()
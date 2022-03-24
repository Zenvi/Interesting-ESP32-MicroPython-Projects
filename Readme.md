# Interesting ESP32 Projects based on MicroPython

## 1. Contents
+ How to make MicroPython working in your ESP32
+ What tools should I prepare
+ What projects we currently have

## 2. How to Make MicroPython Working in Your ESP32
+ EN Version: http://docs.micropython.org/en/latest/esp32/tutorial/intro.html#esp32-intro
+ CN Version: https://docs.01studio.cc/esp32/tutorial/intro.html#esp32-intro

## 3. What Tools Should I Prepare
### 3.1 Hardware
+ ESP32 Board (The board I use is a Devkit-C, official website: https://www.espressif.com/zh-hans/products/devkits/esp32-devkitc)
+ A led light which can be connected to ESP32's GPIO pins
+ A PWM buzzer
### 3.2 Software
+ Thonny: https://thonny.org/
+ CP2102 Driver: Download it wherever you can
+ MicroPython Firmware for ESP32: https://micropython.org/download/?port=esp32

## 4. What Projects We Currently Have
+ BLE_Light: Use your smartphone to light the LED connected to the board through Bluetooth Low-Energy.
+ TCP_Light: Use a Socket assistant on PC to light the LED.
+ Siri_Light: Say "Light up" to Siri in your APPLE devices and let Siri do the lighting job for you
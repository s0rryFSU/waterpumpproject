def playSound(choice: number):
    global startPlayed, endPlayed
    if choice == 1 and startPlayed == 0:
        music.start_melody(music.built_in_melody(Melodies.POWER_UP),
            MelodyOptions.ONCE_IN_BACKGROUND)
        startPlayed = 1
    if choice == 0 and endPlayed == 0:
        music.start_melody(music.built_in_melody(Melodies.POWER_DOWN),
            MelodyOptions.ONCE_IN_BACKGROUND)
        endPlayed = 1
def setRGB(red: number, green: number, blue: number):
    global r, g, b
    r = red
    g = green
    b = blue
    pins.analog_write_pin(AnalogPin.P13, b)
    pins.analog_write_pin(AnalogPin.P7, g)
    pins.analog_write_pin(AnalogPin.P6, r)

def on_button_pressed_a():
    bottleCalibrate()
input.on_button_pressed(Button.A, on_button_pressed_a)

def bottleCalibrate():
    global weight_2, min_weight, _2lightweight, _3lightWeight, _4lightWeight, _5lightWeight, maxweight
    weight_2 = pins.analog_read_pin(AnalogPin.P2)
    min_weight = weight_2 - 25
    _2lightweight = weight_2 + 90
    _3lightWeight = _2lightweight + 90
    _4lightWeight = _3lightWeight + 90
    _5lightWeight = _4lightWeight + 90
    maxweight = _5lightWeight + 40
    basic.show_string("Calibrate Complete!")

def on_button_pressed_b():
    WaterLevelLights()
input.on_button_pressed(Button.B, on_button_pressed_b)

def WaterLevelLights():
    global motor
    if weight >= _5lightWeight:
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.ONE), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.TWO), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.THREE), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.FOUR), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.FIVE), 0x007fff)
        playSound(0)
        setRGB(0, 0, 255)
        motor = 0
    elif weight >= _4lightWeight:
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.FOUR), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.THREE), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.TWO), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.ONE), 0x007fff)
        motor = 1
    elif weight >= _3lightWeight:
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.ONE), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.TWO), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.THREE), 0x007fff)
        motor = 1
    elif weight >= _2lightweight:
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.ONE), 0x007fff)
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.TWO), 0x007fff)
        motor = 1
    elif weight >= min_weight:
        BLiXel.set_pixel_colour(BLiXel.blixel_index(BLiXelIndex.ONE), 0x007fff)
        playSound(1)
        setRGB(255, 0, 0)
        motor = 1
    else:
        setRGB(255, 0, 0)
        motor = 0
def SystemRestart():
    global startPlayed, endPlayed, motor
    bBoard_Motor.motor_right_duty(0)
    startPlayed = 0
    endPlayed = 0
    motor = 1
    control.wait_micros(6000)
    control.wait_micros(6000)
    BLiXel.blixels_off()
    setRGB(0, 0, 0)
def setMotor():
    if motor == 1:
        bBoard_Motor.motor_right_duty(80)
    else:
        bBoard_Motor.motor_right_duty(0)
        control.wait_micros(6000)
        control.wait_micros(6000)
def WaterBottleCheck():
    if weight <= maxweight and weight > min_weight and Reed2.get_switch() == 1:
        WaterLevelLights()
        setMotor()
    else:
        SystemRestart()
Reed2: Reed.Reed = None
weight = 0
weight_2 = 0
b = 0
g = 0
r = 0
endPlayed = 0
startPlayed = 0
motor = 0
_5lightWeight = 0
_4lightWeight = 0
_3lightWeight = 0
_2lightweight = 0
min_weight = 0
maxweight = 0
setRGB(0, 0, 0)
music.set_volume(25)
maxweight = 800
min_weight = 400
_2lightweight = 490
_3lightWeight = 580
_4lightWeight = 670
_5lightWeight = 760
motor = 1

def on_forever():
    global weight_2
    weight_2 = pins.analog_read_pin(AnalogPin.P2)
    basic.show_string("" + str(weight))
    WaterBottleCheck()
basic.forever(on_forever)

def on_every_interval():
    global weight, Reed2
    weight = pins.analog_read_pin(AnalogPin.P2)
    Reed2 = Reed.create_reed(BoardID.ZERO, ClickID.B)
loops.every_interval(100, on_every_interval)
 

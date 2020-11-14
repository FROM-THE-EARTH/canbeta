
# component name
NAME_MOTOR_L = "motor_l"
NAME_MOTOR_R = "motor_r"
NAME_WHEELS = "wheels"

NAME_BME280 = "bme280"
NAME_BNO055 = "bno055"
NAME_GPS = "gps"
NAME_IM920 = "im920"

NAME_BNO055_RESET = "bno055_reset"
NAME_BNO055_INT = "bno055_int"
NAME_MOSFET_PARA = "mosfet_para"
NAME_MOSFET_CHILD = "mosfet_child"

NAME_SENSOR_CONTROLLER = "sensor_controller"
NAME_LOGQUEUE = "logqueue"
NAME_DATA_LOGGER = "dlogger"
NAME_SYSTEM_LOGGER = "slogger"
NAME_MANAGER = "manager"
NAME_LED = "led"

# device setting
GPIO_MOTOR_L_FIN = 12
GPIO_MOTOR_L_RIN = 18
GPIO_MOTOR_R_FIN = 13
GPIO_MOTOR_R_RIN = 19
GPIO_BNO055_RESET = 17
GPIO_BNO055_INT = 22
GPIO_MOSFET_PARA = 5
GPIO_MOSFET_CHILD = 6
GPIO_SONIC_TRIG = 20
GPIO_SONIC_ECHO = 21
GPIO_LED = 25

MOTOR_PWM_FREQ = 40_0000
MOTOR_PWM_RANGE = 255

I2C_ADDRESS_BNO055 = 0x28
I2C_ADDRESS_BME280 = 0x76
I2C_ADDRESS_OPT3002 = 0x68
SERIAL_PORT_GPS = "/dev/serial0"
SERIAL_PORT_IM920 = "/dev/ttyUSB0"

# threshold setting
THRESHOLD_LANDING_DETECT = 10.
THRESHOLD_CHILD_RELEASE = 0.5
THRESHOLD_CAMERA_DETECTION = 1.

# pid control setting
KP = 1.
KI = 1.
KD = 1.
MAX_DUTY = 100.
MIN_DUTY = 0.
ACCEPTABLE_MOE = 0.1
THRESHOLD_I_CTRLR = 10
DUTY_BASE = 50.
SAMPLE_TIME = 1.

# other
POSITION_GOAL = (0., 0.)
POSITION_CHILD = (0., 0.)

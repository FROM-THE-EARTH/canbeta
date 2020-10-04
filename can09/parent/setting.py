
from pisat.handler import UART_SERIAL_PORT


# component name
NAME_MOTOR_L = "motor_l"
NAME_MOTOR_R = "motor_r"
NAME_WHEELS = "wheels"
NAME_MPU9250 = "mpu9250"
NAME_GPS_MODULE = "gps_module"
NAME_GPS_ADAPTER = "gps_adapter"
NAME_SENSOR_CONTROLLER = "sensor_controller"
NAME_LOGQUEUE = "logqueue"
NAME_DATA_LOGGER = "dlogger"
NAME_SYSTEM_LOGGER = "slogger"
NAME_MANAGER = "manager"

# device setting
PIN_MOTOR_L_FIN = 0
PIN_MOTOR_L_RIN = 0
PIN_MOTOR_R_FIN = 0
PIN_MOTOR_R_RIN = 0

I2C_ADDRESS_MPU9250 = 0x58
SERIAL_PORT_GPS = UART_SERIAL_PORT

# threshold setting
THRESHOLD_LANDING_DETECT = 10.
THRESHOOD_PID_START = 30.
THRESHOLD_PID_FINISH = 5.

# pid control setting
KP = 1
KI = 1
KD = 1
MAX_I_TERM = 20
DEFAULT_DUTY_RATIO = 60

# other
POSITION_GOAL = (0., 0.)

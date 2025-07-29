# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# THIS HEADER FILE CONTAINS THE FUNCTION IMPORTS AND CONSTANTS FOR THE
# FUNCTIONS EXPORTED BY THE CANdo API DLL - CANdo.dll v4.1
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
#  TITLE :- CANdo.dll header file - CANdoImport.py
#  AUTHOR(s) :- Martyn Brown, Riccardo Belli
#  DATE :- 22/01/21
#
#  DESCRIPTION :- Python import module for interfacing with the CANdo.dll.
#
#  UPDATES :-
#  22/01/21 Created (Martyn Brown)
#  05/11/24 Modified for python-can compatibility, type
#           hinting and error codes (Riccardo Belli). Found on:
#           github.com/belliriccardo/python-can-cando
#
#  LICENSE :-
#  The SDK (Software Development Kit) provided for use with the CANdo device
#  is issued as FREE software, meaning that it is free for personal,
#  educational & commercial use, without restriction or time limit. The
#  software is supplied "as is", with no implied warranties or guarantees.
#
#  (c) 2021 Netronics Ltd. All rights reserved.
# ------------------------------------------------------------------------------
import ctypes
import sys
from dataclasses import dataclass
from enum import IntEnum
from queue import Queue
from typing import TYPE_CHECKING, Dict, Optional, Tuple

from can.exceptions import CanInitializationError, CanOperationError

# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
# CANdoOpen function constants
CANDO_CLOSED = 0  # USB channel closed
CANDO_OPEN = 1  # USB channel open

# CANdoSetState function constants
CANDO_STOP = 0  # Stop Rx/Tx of CAN messages
CANDO_RUN = 1  # Start Rx/Tx of CAN messages

# CANdo status message constants
CANDO_CLEAR = 0  # Status message flag clear
CANDO_SET = 1  # Status message flag set


class CANdoMode(IntEnum):
    # CANdoSetMode function constants
    CANDO_NORMAL_MODE = 0  # Rx/Tx CAN mode
    CANDO_LISTEN_ONLY_MODE = 1  # Rx only mode, no ACKs
    CANDO_LOOPBACK_MODE = 2  # Tx internally looped back to Rx


# CANdo baud rate & bus load constants
# CANdo clk. freq. in kHz for baud rate calc.
CANDO_CLK_FREQ = 20000

# CANdoISO & CANdo AUTO clk. freq. in kHz for baud rate calc.
CANDO_CLK_FREQ_HIGH = 40000

# CANdoISO clock frequency in Hz
CANDOISO_F_CLOCK = CANDO_CLK_FREQ_HIGH * 1000

# CANdo clock frequency in Hz
CANDO_F_CLOCK = CANDO_CLK_FREQ * 1000

CAN_MSG_TIMESTAMP_RESOLUTION = 25.6e-6  # Timestamp resolution is 25.6us per bit

# BRP enhanced baud rate setting offset (CANdoISO & CANdo AUTO only)
CANDO_BRP_ENHANCED_OFFSET = 63

# CANdo AUTO Module constants
CANDO_AUTO_V1_INPUT = 1  # V1 analogue I/P
CANDO_AUTO_V2_INPUT = 2  # V2 analogue I/P
CANDO_AUTO_MAX_NO_OF_TX_ITEMS = 10  # Max. no. of items in CAN Transmit store
CANDO_AUTO_ANALOG_INPUT_RESOLUTION = 0.0315  # Analogue I/P resolution 31.5mV

# CAN message constants
CANDO_ID_11_BIT = 0  # Standard 11 bit ID
CANDO_ID_29_BIT = 1  # Extended 29 bit ID
CANDO_DATA_FRAME = 0  # CAN data frame
CANDO_REMOTE_FRAME = 1  # CAN remote frame

# CANdo buffer lengths
CANDO_CAN_BUFFER_LENGTH = 2048  # Size of CAN message receive cyclic buffer
CANDO_MAX_STRING_SIZE = 256  # Max. no. of bytes in a string returned by the device

# Maximum number of filters masks
CANDO_MAX_FILTERS = 2


class CANdoHWType(IntEnum):
    # CANdo H/W types
    CANDO_TYPE_ANY = 0x0000  # Any H/W type
    CANDO_TYPE_CANDO = 0x0001  # CANdo H/W type
    CANDO_TYPE_CANDOISO = 0x0002  # CANdoISO H/W type
    CANDO_TYPE_CANDO_AUTO = 0x0003  # CANdo AUTO H/W type
    CANDO_TYPE_UNKNOWN = 0x8000  # Unknown H/W type


# CANdo status types
CANDO_NO_STATUS = 0  # No new status received
CANDO_DEVICE_STATUS = 1  # Device status received
CANDO_DATE_STATUS = 2  # Date status received
CANDO_BUS_LOAD_STATUS = 3  # Bus load status received
CANDO_SETUP_STATUS = 4  # CAN setup status received
CANDO_ANALOG_INPUT_STATUS = 5  # Analogue I/P status received

# CANdo USB PIDs
CANDO_PID = b"8095"  # CANdo PID
CANDOISO_PID = b"8660"  # CANdoISO PID
CANDO_AUTO_PID = b"889B"  # CANdo AUTO PID


class CANdoFuncRetCode(IntEnum):
    # CANdo function return codes
    CANDO_SUCCESS = 0x0000  # All OK
    CANDO_USB_DLL_ERROR = 0x0001  # WinUSB DLL error
    CANDO_USB_DRIVER_ERROR = 0x0002  # WinUSB driver error
    CANDO_NOT_FOUND = 0x0004  # CANdo not found
    CANDO_IO_FAILED = 0x0008  # Failed to initialise USB I/O
    CANDO_CONNECTION_CLOSED = 0x0010  # No CANdo channel open
    CANDO_READ_ERROR = 0x0020  # USB read error
    CANDO_WRITE_ERROR = 0x0040  # USB write error
    CANDO_WRITE_INCOMPLETE = 0x0080  # Not all requested bytes written to CANdo
    CANDO_BUFFER_OVERFLOW = 0x0100  # Overflow in cyclic buffer
    CANDO_RX_OVERRUN = 0x0200  # Message received greater than max. message size
    CANDO_RX_TYPE_UNKNOWN = 0x0400  # Unknown message type received
    CANDO_RX_CRC_ERROR = 0x0800  # CRC mismatch
    CANDO_RX_DECODE_ERROR = 0x1000  # Error decoding message
    CANDO_INVALID_HANDLE = 0x2000  # Invalid device handle
    CANDO_ERROR = 0x8000  # Non specific error


class CANdoRepeatTime(IntEnum):
    # CANdo CAN transmit repeat times
    CANDO_REPEAT_TIME_OFF = 0  # Off
    CANDO_REPEAT_TIME_10MS = 1  # 10ms
    CANDO_REPEAT_TIME_20MS = 2  # 20ms
    CANDO_REPEAT_TIME_50MS = 3  # 50ms
    CANDO_REPEAT_TIME_100MS = 4  # 100ms
    CANDO_REPEAT_TIME_200MS = 5  # 200ms
    CANDO_REPEAT_TIME_500MS = 6  # 500ms
    CANDO_REPEAT_TIME_1S = 7  # 1s
    CANDO_REPEAT_TIME_2S = 8  # 2s
    CANDO_REPEAT_TIME_5S = 9  # 5s
    CANDO_REPEAT_TIME_10S = 10  # 10s


# From Canalyzer's website; will need to be updated
CANDO_LATEST_SW = {
    60: 31,
    70: 42,
    80: 51,
}


CANDOISO_LATEST_SW = {
    20: 34,
    30: 41,
}

# ------------------------------------------------------------------------------
# TYPEDEFS
# ------------------------------------------------------------------------------
TCANdoDeviceString = ctypes.c_char * CANDO_MAX_STRING_SIZE  # CANdo string type
PCANdoDeviceString = ctypes.POINTER(TCANdoDeviceString)  # Pointer type to CANdo string


# Type used to store device H/W type & S/N for connected CANdo
class TCANdoDevice(ctypes.Structure):
    _fields_ = [
        ("HardwareType", ctypes.c_int),
        ("SerialNo", TCANdoDeviceString),
    ]


PCANdoDevice = ctypes.POINTER(TCANdoDevice)  # Pointer type to TCANdoDevice


# Type used to store USB info. for connected CANdo
class TCANdoUSB(ctypes.Structure):
    _fields_ = [
        ("TotalNo", ctypes.c_int),
        ("No", ctypes.c_int),
        ("OpenFlag", ctypes.c_bool),
        ("Description", TCANdoDeviceString),
        ("SerialNo", TCANdoDeviceString),
        ("Handle", ctypes.c_int),
    ]


PCANdoUSB = ctypes.POINTER(TCANdoUSB)  # Pointer type to TCANdoUSB


# Type used to store a CAN message
class TCANdoCAN(ctypes.Structure):
    _fields_ = [
        ("IDE", ctypes.c_ubyte),
        ("RTR", ctypes.c_ubyte),
        ("ID", ctypes.c_uint),
        ("DLC", ctypes.c_ubyte),
        ("Data", ctypes.c_ubyte * 8),
        ("BusState", ctypes.c_ubyte),
        ("TimeStamp", ctypes.c_uint),
    ]


# Type used as a cyclic buffer to store decoded CAN messages received from CANdo
class TCANdoCANBuffer(ctypes.Structure):
    _fields_ = [
        ("CANMessage", TCANdoCAN * CANDO_CAN_BUFFER_LENGTH),
        ("WriteIndex", ctypes.c_int),
        ("ReadIndex", ctypes.c_int),
        ("FullFlag", ctypes.c_bool),
    ]


PCANdoCANBuffer = ctypes.POINTER(TCANdoCANBuffer)  # Pointer type to TCANdoCANBuffer


# Type used to store status information received from CANdo
class TCANdoStatus(ctypes.Structure):
    _fields_ = [
        ("HardwareVersion", ctypes.c_ubyte),
        ("SoftwareVersion", ctypes.c_ubyte),
        ("Status", ctypes.c_ubyte),
        ("BusState", ctypes.c_ubyte),
        ("TimeStamp", ctypes.c_uint),
        ("NewFlag", ctypes.c_ubyte),
    ]


PCANdoStatus = ctypes.POINTER(TCANdoStatus)  # Pointer type to TCANdoStatus

# ------------------------------------------------------------------------------
# Import CANdo library
lib = ctypes.windll.LoadLibrary("CANdo")
# ------------------------------------------------------------------------------
# FUNCTION HANDLES & PROTOTYPES
# ------------------------------------------------------------------------------
# Note : All functions return a ctypes.c_int containing a CANdo function return code
CANdoGetVersion = lib.CANdoGetVersion
CANdoGetVersion.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
]
CANdoGetPID = lib.CANdoGetPID
CANdoGetPID.argtypes = [ctypes.c_int, PCANdoDeviceString]
CANdoGetDevices = lib.CANdoGetDevices
CANdoGetDevices.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]

# The CANdoOpen(...) function returns a connection to the first free CANdo device found, regardless
# of hardware type or serial number.The CANdoOpenDevice(...) function allows a particular CANdo
# device to be selected based on hardware type, serial number or both.
CANdoOpen = lib.CANdoOpen
CANdoOpen.argtypes = [PCANdoUSB]
CANdoOpenDevice = lib.CANdoOpenDevice
CANdoOpenDevice.argtypes = [PCANdoUSB, PCANdoDevice]
CANdoClose = lib.CANdoClose
CANdoClose.argtypes = [PCANdoUSB]
CANdoFlushBuffers = lib.CANdoFlushBuffers
CANdoFlushBuffers.argtypes = [PCANdoUSB]
CANdoSetBaudRate = lib.CANdoSetBaudRate
CANdoSetBaudRate.argtypes = [
    PCANdoUSB,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
]
CANdoSetMode = lib.CANdoSetMode
CANdoSetMode.argtypes = [PCANdoUSB, ctypes.c_ubyte]
CANdoSetFilters = lib.CANdoSetFilters
CANdoSetFilters.argtypes = [
    PCANdoUSB,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_uint,
]
CANdoSetState = lib.CANdoSetState
CANdoSetState.argtypes = [PCANdoUSB, ctypes.c_ubyte]
CANdoClearStatus = lib.CANdoClearStatus
CANdoClearStatus.argtypes = [PCANdoUSB]
CANdoRequestStatus = lib.CANdoRequestStatus
CANdoRequestStatus.argtypes = [PCANdoUSB]
CANdoRequestDateStatus = lib.CANdoRequestDateStatus
CANdoRequestDateStatus.argtypes = [PCANdoUSB]
CANdoRequestBusLoadStatus = lib.CANdoRequestBusLoadStatus
CANdoRequestBusLoadStatus.argtypes = [PCANdoUSB]
CANdoTransmit = lib.CANdoTransmit
CANdoTransmit.argtypes = [
    PCANdoUSB,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_ubyte,
    ctypes.c_ubyte,
]
CANdoReceive = lib.CANdoReceive
CANdoReceive.argtypes = [PCANdoUSB, PCANdoCANBuffer, PCANdoStatus]

# ------------------------------------------------------------------------------
# CANdo AUTO DEVICE FUNCTIONS (UNUSED IN THIS MODULE)
# ------------------------------------------------------------------------------
CANdoRequestSetupStatus = lib.CANdoRequestSetupStatus
CANdoRequestSetupStatus.argtypes = [PCANdoUSB]
CANdoRequestAnalogInputStatus = lib.CANdoRequestAnalogInputStatus
CANdoRequestAnalogInputStatus.argtypes = [PCANdoUSB]
CANdoAnalogStoreRead = lib.CANdoAnalogStoreRead
CANdoAnalogStoreRead.argtypes = [PCANdoUSB]
CANdoAnalogStoreWrite = lib.CANdoAnalogStoreWrite
CANdoAnalogStoreWrite.argtypes = [
    PCANdoUSB,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
]
CANdoAnalogStoreClear = lib.CANdoAnalogStoreClear
CANdoAnalogStoreClear.argtypes = [PCANdoUSB]
CANdoTransmitStoreRead = lib.CANdoTransmitStoreRead
CANdoTransmitStoreRead.argtypes = [PCANdoUSB]
CANdoTransmitStoreWrite = lib.CANdoTransmitStoreWrite
CANdoTransmitStoreWrite.argtypes = [
    PCANdoUSB,
    ctypes.c_ubyte,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_ubyte,
]
CANdoTransmitStoreClear = lib.CANdoTransmitStoreClear
CANdoTransmitStoreClear.argtypes = [PCANdoUSB]
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TYPE CHECKING AND TYPE ALIASES
# ------------------------------------------------------------------------------
TCanDoMsg = Tuple[float, int, bool, bool, int, bytearray]

if TYPE_CHECKING:
    CANdoUSBPtrType = ctypes._Pointer[TCANdoUSB]  # type: ignore
    CANdoCANBufferPtrType = ctypes._Pointer[TCANdoCANBuffer]  # type: ignore
    CANdoStatusPtrType = ctypes._Pointer[TCANdoStatus]  # type: ignore
else:
    CANdoUSBPtrType = ctypes.POINTER(TCANdoUSB)
    CANdoCANBufferPtrType = ctypes.POINTER(TCANdoCANBuffer)
    CANdoStatusPtrType = ctypes.POINTER(TCANdoStatus)

if sys.version_info >= (3, 9):
    CANdoPIDType = ctypes.Array[ctypes.c_char]  # novermin
    MsgQueueType = Queue[TCanDoMsg]  # novermin
    MsgDataType = ctypes.Array[ctypes.c_ubyte]  # novermin
else:
    CANdoPIDType = ctypes.Array
    MsgQueueType = Queue
    MsgDataType = ctypes.Array


class CANdoOperationError(CanOperationError):
    """Indicates an error in the CANdo ISO API."""


class CANdoInitializationError(CanInitializationError):
    """Indicates an error during the initialization of the CANdo ISO API."""


# ------------------------------------------------------------------------------
# BIT TIMINGS UTILITIES
# ------------------------------------------------------------------------------


@dataclass
class CANdoBusTiming:
    """CANdo ISO bus timing settings.

    NOTE: All these CAN register values are 0 based, so that 0 actually equals 1 (in the CANdo v5.4 application, for example).
    So, for example, a PHSEG1 value of 3 equates to a 4 PHSEG1 segments in the CAN bit timing (CANdo v5.4 application).
    """

    brp: int
    propseg: int
    phseg1: int
    phseg2: int
    sjw: int
    sam: int

    def f_clock(self, is_candoiso: bool = True) -> int:
        return CANDOISO_F_CLOCK if is_candoiso else CANDO_F_CLOCK

    def baud(self, is_candoiso: bool = True) -> float:
        return self.f_clock(is_candoiso) / (2 * (self.brp + 1) * (4 + self.propseg + self.phseg1 + self.phseg2))


CANDO_REPEAT_TIME_MAP = {
    0: CANdoRepeatTime.CANDO_REPEAT_TIME_OFF,
    10: CANdoRepeatTime.CANDO_REPEAT_TIME_10MS,
    20: CANdoRepeatTime.CANDO_REPEAT_TIME_20MS,
    50: CANdoRepeatTime.CANDO_REPEAT_TIME_50MS,
    100: CANdoRepeatTime.CANDO_REPEAT_TIME_100MS,
    200: CANdoRepeatTime.CANDO_REPEAT_TIME_200MS,
    500: CANdoRepeatTime.CANDO_REPEAT_TIME_500MS,
    1000: CANdoRepeatTime.CANDO_REPEAT_TIME_1S,
    2000: CANdoRepeatTime.CANDO_REPEAT_TIME_2S,
    5000: CANdoRepeatTime.CANDO_REPEAT_TIME_5S,
    10000: CANdoRepeatTime.CANDO_REPEAT_TIME_10S,
}

# These values have been calculated using the CANdo v5.4 application;
# the values with a single sample point are the default values used by the application.
# Register's values start at 0 for these timings, see programmer's guide
CANDO_COMMON_TIMINGS: Dict[int, Dict[Optional[int], CANdoBusTiming]] = {
    12500: {68: CANdoBusTiming(31, 7, 7, 7, 0, 0)},
    20000: {70: CANdoBusTiming(24, 4, 7, 5, 0, 0)},
    50000: {70: CANdoBusTiming(9, 4, 7, 5, 0, 0)},
    100000: {70: CANdoBusTiming(4, 4, 7, 5, 0, 0)},
    125000: {70: CANdoBusTiming(3, 4, 7, 5, 0, 0)},
    250000: {70: CANdoBusTiming(1, 4, 7, 5, 0, 0)},
    500000: {
        # Most used baud, different sample points options
        70: CANdoBusTiming(0, 4, 7, 5, 0, 0),
        80: CANdoBusTiming(1, 2, 3, 1, 0, 0),
        85: CANdoBusTiming(0, 7, 7, 2, 0, 0),
    },
    625000: {75: CANdoBusTiming(0, 4, 5, 3, 0, 0)},
    1000000: {80: CANdoBusTiming(0, 2, 3, 1, 0, 0)},
}


def cando_get_timing(bitrate: int, sample_point: Optional[int] = None) -> CANdoBusTiming:
    if bitrate not in CANDO_COMMON_TIMINGS:
        raise ValueError(f"Bitrate {bitrate} not supported")

    avail_bitrates = CANDO_COMMON_TIMINGS[bitrate]

    if sample_point is None:
        # if len(avail_bitrates) == 1:
        #     raise ValueError(f"Sample point must be specified for bitrate {bitrate}")

        return next(iter(avail_bitrates.values()))
    if sample_point not in avail_bitrates:
        raise ValueError(f"Sample point {sample_point} not supported for bitrate {bitrate}")
    return avail_bitrates[sample_point]


# ------------------------------------------------------------------------------
# ERROR CODES
# ------------------------------------------------------------------------------


class CANdoErrCodes(IntEnum):
    # CANdo Status Error (may be logical ORed together)
    CANDO_OK = 0x00  # "All OK"
    CANDO_USB_RX_OVERRUN = 0x01  # "USB port receive message overrun"
    CANDO_USB_RX_CORRUPTED = 0x02  # "USB port receive message invalid"
    CANDO_USB_RX_CRC_ERROR = 0x04  # "USB port receive message CRC error"
    CANDO_CAN_RX_NO_DATA = 0x08  # "CAN receive message no data"
    CANDO_CAN_RX_OVERRUN = 0x10  # "CAN receive message overrun"
    CANDO_CAN_RX_INVALID = 0x20  # "CAN receive message invalid"
    CANDO_CAN_TX_OVERRUN = 0x40  # "CAN transmit message overrun"
    CANDO_CAN_BUS_ERROR = 0x80  # "CAN bus error"


class CANdoBusSts(IntEnum):
    # CANdo BusState (may be logical ORed together)
    CAN_OK = 0x00  # "All OK"
    CAN_WARN = 0x01  # "Rx/Tx warning (>95 errors)"
    CAN_RX_WARN = 0x02  # "Receiver warning (>95 errors)"
    CAN_TX_WARN = 0x04  # "Transmitter warning (>95 errors)"
    CAN_RX_PASSIVE = 0x08  # "Receiver bus passive (>127 errors)"
    CAN_TX_PASSIVE = 0x10  # "Transmitter bus passive (>127 errors)"
    CAN_TX_OFF = 0x20  # "Transmitter bus off (>255 errors)"
    CAN_RX1_OVERFLOW = 0x40  # "Receive buffer 1 overflow"
    CAN_RX2_OVERFLOW = 0x80  # "Receive buffer 2 overflow"


def CANdoStsErr(value: int) -> str:
    # CANdo Status Error (may be logical ORed together)
    sts_err = ""

    if value & CANdoErrCodes.CANDO_USB_RX_OVERRUN.value:
        sts_err += "USB port receive message overrun, "
    if value & CANdoErrCodes.CANDO_USB_RX_CORRUPTED.value:
        sts_err += "USB port receive message invalid, "
    if value & CANdoErrCodes.CANDO_USB_RX_CRC_ERROR.value:
        sts_err += "USB port receive message CRC error, "
    if value & CANdoErrCodes.CANDO_CAN_RX_NO_DATA.value:
        sts_err += "CAN receive message no data, "
    if value & CANdoErrCodes.CANDO_CAN_RX_OVERRUN.value:
        sts_err += "CAN receive message overrun, "
    if value & CANdoErrCodes.CANDO_CAN_RX_INVALID.value:
        sts_err += "CAN receive message invalid, "
    if value & CANdoErrCodes.CANDO_CAN_TX_OVERRUN.value:
        sts_err += "CAN transmit message overrun, "
    if value & CANdoErrCodes.CANDO_CAN_BUS_ERROR.value:
        sts_err += "CAN bus error, "

    if sts_err == "":
        sts_err = "All OK"
    return sts_err.rstrip(", ")


def CANdoBusStsErr(value: int) -> str:
    # CANdo Bus State Error (may be logical ORed together)
    sts_err = ""

    if value & CANdoBusSts.CAN_WARN.value:
        sts_err += "Rx/Tx warning (>95 errors), "
    if value & CANdoBusSts.CAN_RX_WARN.value:
        sts_err += "Receiver warning (>95 errors), "
    if value & CANdoBusSts.CAN_TX_WARN.value:
        sts_err += "Transmitter warning (>95 errors), "
    if value & CANdoBusSts.CAN_RX_PASSIVE.value:
        sts_err += "Receiver bus passive (>127 errors), "
    if value & CANdoBusSts.CAN_TX_PASSIVE.value:
        sts_err += "Transmitter bus passive (>127 errors), "
    if value & CANdoBusSts.CAN_TX_OFF.value:
        sts_err += "Transmitter bus off (>255 errors), "
    if value & CANdoBusSts.CAN_RX1_OVERFLOW.value:
        sts_err += "Receive buffer 1 overflow, "
    if value & CANdoBusSts.CAN_RX2_OVERFLOW.value:
        sts_err += "Receive buffer 2 overflow, "

    if sts_err == "":
        sts_err = "All OK"
    return sts_err.rstrip(", ")


def CANdoFuncRetCodeErr(value: int) -> str:
    # CANdo function return codes (may be logical ORed together)
    sts_err = ""

    if value & CANdoFuncRetCode.CANDO_USB_DLL_ERROR.value:
        sts_err += "WinUSB DLL error, "
    if value & CANdoFuncRetCode.CANDO_USB_DRIVER_ERROR.value:
        sts_err += "WinUSB driver error, "
    if value & CANdoFuncRetCode.CANDO_NOT_FOUND.value:
        sts_err += "CANdo not found, "
    if value & CANdoFuncRetCode.CANDO_IO_FAILED.value:
        sts_err += "Failed to initialise USB I/O, "
    if value & CANdoFuncRetCode.CANDO_CONNECTION_CLOSED.value:
        sts_err += "No CANdo channel open, "
    if value & CANdoFuncRetCode.CANDO_READ_ERROR.value:
        sts_err += "USB read error, "
    if value & CANdoFuncRetCode.CANDO_WRITE_ERROR.value:
        sts_err += "USB write error, "
    if value & CANdoFuncRetCode.CANDO_WRITE_INCOMPLETE.value:
        sts_err += "Not all requested bytes written to CANdo, "
    if value & CANdoFuncRetCode.CANDO_BUFFER_OVERFLOW.value:
        sts_err += "Overflow in cyclic buffer, "
    if value & CANdoFuncRetCode.CANDO_RX_OVERRUN.value:
        sts_err += "Message received greater than max. message size, "
    if value & CANdoFuncRetCode.CANDO_RX_TYPE_UNKNOWN.value:
        sts_err += "Unknown message type received, "
    if value & CANdoFuncRetCode.CANDO_RX_CRC_ERROR.value:
        sts_err += "CRC mismatch, "
    if value & CANdoFuncRetCode.CANDO_RX_DECODE_ERROR.value:
        sts_err += "Error decoding message, "
    if value & CANdoFuncRetCode.CANDO_INVALID_HANDLE.value:
        sts_err += "Invalid device handle, "
    if value & CANdoFuncRetCode.CANDO_ERROR.value:
        sts_err += "Non specific error, "

    if sts_err == "":
        sts_err = "All OK"
    return sts_err.rstrip(", ")

from enum import IntEnum


class FTUcMode(IntEnum):
    Reset = 0x0
    AsynchronousBitBang = 0x1
    MPSSE = 0x2
    SynchronousBitBang = 0x4
    MCUHostBusEmulationMode = 0x8
    FastOptoIsolatedSerialMode = 0x10
    CBUSBitBangMode = 0x20
    SingleChannelSynchronous245FIFOMode = 0x40

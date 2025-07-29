from ftd2xx import FTD2XX, ftd2xx
from ._ft_define import FTUcMode


class FTIODevice:
    mask: int
    ftd: FTD2XX

    def __init__(self, serial_number: str, mask: int = 0xFF):
        """创建FTD_IO对象

        Args:
            serial_number (str): 设备序列号
            mask (int): 0x00~0xFF 位模式掩码的，这设置了哪些位是输入和输出。
                一个位值为0将相应的引脚设置为输入，一个位值为1将相应的引脚设置为输出。

        Raises:
            Exception: 创建错误
        """
        devices = ftd2xx.listDevices()
        if devices is None or serial_number.encode() not in devices:
            raise Exception(
                f"未找到{serial_number}设备,请检查序列号是否正确或确认设备是否连接"
            )

        self.mask = mask
        self.ftd = ftd2xx.openEx(serial_number.encode())

        try:
            self.ftd.setBitMode(mask, FTUcMode.SynchronousBitBang)
        except Exception as e:
            raise Exception(f"配置通道D为GPIO模式失败: {e}")

    def __del__(self):
        self.ftd.close()

    def set_all(self, value: int):
        """设置所有引脚的值

        Args:
            value (int): 所有引脚的值 0x00~0xFF

        Raises:
            Exception: 设置失败
        """
        try:
            self.ftd.write(bytes([value]))
        except Exception as e:
            raise Exception(f"设置所有引脚失败: {e}")

    def get_all(self) -> int:
        """获取所有引脚的值

        Raises:
            Exception: 获取失败

        Returns:
            int: 所有引脚的值 0x00~0xFF
        """
        try:
            current_value = self.ftd.getBitMode()
            return current_value
        except Exception as e:
            raise Exception(f"获取引脚状态失败: {e}")

    def set_pin(self, gpio: int, state: bool):
        """设置引脚输出状态

        Args:
            gpio (int): 引脚编号 0~7
            state (bool): 想设置引脚输出状态 True为高 False为低

        Raises:
            Exception: 设置失败
        """
        try:
            current_value = self.ftd.getBitMode()

            if state:
                new_value = current_value | (1 << gpio)
            else:
                new_value = current_value & ~(1 << gpio)

            self.ftd.write(bytes([new_value]))

        except Exception as e:
            raise Exception(f"设置引脚{gpio}失败: {e}")

    def toggle_pin(self, gpio: int):
        """翻转引脚输出状态

        Args:
            gpio (int): 引脚编号
        """
        try:
            current_value = self.ftd.getBitMode()
            new_value = current_value ^ (1 << gpio)
            self.ftd.write(bytes([new_value]))
        except Exception as e:
            raise Exception(f"翻转引脚{gpio}失败: {e}")

    def get_pin(self, gpio: int) -> bool:
        try:
            current_value = self.ftd.getBitMode()
            state = bool((current_value >> gpio) & 0x01)
            return state
        except Exception as e:
            raise Exception(f"获取引脚{gpio}状态失败: {e}")


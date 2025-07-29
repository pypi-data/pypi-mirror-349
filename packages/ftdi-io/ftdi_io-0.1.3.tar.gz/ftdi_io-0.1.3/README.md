# FTDI CHIPS IO CTRL

This is a simple program to control the FTDI chips IO pins.

To ctrl the FTD IO pins, you need to install the FTD2XX library.

Github: https://github.com/DreamerDK/ftdi_io

It is written in Python 3.

Use [ftd2xx](https://pypi.org/project/ftd2xx/) to communicate with the FTD IO pins.

Test with "FT4232HQ" in windows 11, other models may have different usage methods, please modify according to the actual situation.

---

简单的 FTDI  IO控制程序。

用于控制 FTDI 芯片 IO 引脚的简单程序，需要安装 FTD2XX 库。

Github: https://github.com/DreamerDK/ftdi_io

本程序使用 Python 3 编写。

使用 [ftd2xx](https://pypi.org/project/ftd2xx/) 与 FTDI 芯片 IO 引脚进行通信。

在 windows 11 上使用 "FT4232HQ" 进行测试，其他型号或设备可能会有不同的使用方法，请根据实际情况进行修改。

## Usage

1. Install ftio package by pip: `pip install ftdi-io`
2. use it by python:
```python
from ftio import FTIODevice # import

device_number = "FTAO1NUQD"

ftio = FTIODevice(device_number)
ftio.set_pin(0, true)

```

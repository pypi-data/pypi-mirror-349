# coding=utf-8
import serial
import time
from typing import List, Optional


READ_MODEL_H = 0xFF
READ_MODEL_L = 0x01
READ_VERSION_H = 0XFF
READ_VERSION_L = 0X02
READ_FACTORY_H = 0XFF
READ_FACTORY_L = 0X03
READ_HW_ID_H = 0XFF
READ_HW_ID_L = 0X04
READ_NAME_H = 0XFF
READ_NAME_L = 0X05
WRITE_NAME_H = 0XFF
WRITE_NAME_L = 0X06
READ_CONNECT_H = 0XFF
READ_CONNECT_L = 0X07

UPDATE_REQUEST_H = 0XFF
UPDATE_REQUEST_L = 0X10
UPDATE_REQUEST_H = 0XFF
UPDATE_REQUEST_L = 0X10
MAX_COM_LEN_H = 0XFF
MAX_COM_LEN_L = 0X11
DOWNLOAD_H = 0XFF
DOWNLOAD_L = 0X12
READ_STATUS_H = 0XFF
READ_STATUS_L = 0X13
PAGE_CHECK_H = 0XFF
PAGE_CHECK_L = 0X14
PAGE_SEND_H = 0XFF
PAGE_SEND_L = 0X15

READ_PERIPH_H = 0X01
READ_PERIPH_L = 0X01



# 串口配置参数
SERIAL_PORT = "/dev/ttyS3"  # 串口设备路径
BAUD_RATE = 115200          # 波特率
TIMEOUT = 3                # 读取超时时间（秒）





def calculate_pro_check(command_h: int, command_l: int, data: List[bytes] = None) -> int:
    """计算校验值（原C代码中的pro_check逻辑）"""
    base_sum = 0x86 + 0xAB + 0x00 + 0x09 + command_h + command_l + 0x01 + 0xCF
    if data:
        base_sum += sum(data)
    return base_sum % 256  # 确保结果为单字节（原C代码未取模，需根据实际协议调整）


def read_operation(ser, command_h, command_l, read_len):
    send_data = [
        0x86, 0xAB, 0x00, 0x09,
        command_h, command_l,
        0x01,
        calculate_pro_check(command_h, command_l),
        0xCF
    ]
    send_bytes = bytes(send_data)
    
    try:
        ser.write(send_bytes)
        time.sleep(0.1)
        
        response = b""
        start_time = time.time()  # 关键修复点：初始化开始时间
        while len(response) < read_len:
            chunk = ser.read(read_len - len(response))
            if not chunk:
                time.sleep(0.01)
                if time.time() - start_time > 5:
                    print("读取超时")  # 中文正常显示的前提是编码正确
                    return None
            else:
                response += chunk
        
        if check_geted_buffer(response, read_len):
            return response
        else:
            print("校验失败")
            return None
            
    except Exception as e:
        print(f"读取错误: {e}")  # 如果使用Python 3.6+，f-string可用
        return None


def write_operation(ser: serial.Serial, command_h: int, command_l: int, send_data: bytes) -> Optional[bytes]:
    """写入操作（对应C代码中的Write_operation）"""
    len_data = len(send_data)
    pro_check = calculate_pro_check(command_h, command_l, list(send_data))
    
    # 构造发送数据
    send_packet = [
        0x86, 0xAB,
        (0x09 + len_data) // 256,  # 高8位
        (0x09 + len_data) % 256,   # 低8位
        command_h, command_l,
        *send_data,
        0x01, pro_check, 0xCF
    ]
    send_bytes = bytes(send_packet)
    
    try:
        ser.write(send_bytes)
        time.sleep(0.1)  # 等待数据发送
        
        response = ser.read(0x0B)  # 读取固定长度响应
        if check_geted_buffer(response, 0x0B):
            return response
        else:
            print("校验失败")
            return None
            
    except Exception as e:
        print(f"Write error: {e}")
        return None


def check_geted_buffer(buf: bytes, expected_len: int) -> bool:
    """校验接收数据（对应C代码中的check_geted_buffer）"""
    if len(buf) < expected_len:
        print("数据长度不足")
        return False
    
    # 帧头检查
    if buf[0] != 0x86 or buf[1] != 0xAB:
        print("Header byte error")
        return False
    
    # 帧尾检查（假设最后一个字节为0xCF）
    if buf[-1] != 0xCF:
        print("End byte error")
        return False
    
    # 校验和计算（假设校验位为倒数第二个字节）
    total = sum(buf[:-2]) + buf[-1]
    if total % 256 != buf[-2]:
        print("Check byte error")
        return False
    
    return True


# --------------------- 功能函数 ---------------------

class Uart3_funtions:

    def uart3_init() -> Optional[serial.Serial]:
        """初始化串口"""
        try:
            ser = serial.Serial
            (
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                bytesize=serial.EIGHTBITS,  # 8位数据位
                parity=serial.PARITY_NONE,  # 无校验位
                stopbits=serial.STOPBITS_ONE,  # 1位停止位
                timeout=TIMEOUT,
                xonxoff=False,  # 关闭软件流控
                rtscts=False,   # 关闭硬件流控
            )
            if ser.is_open:
                print("UART3初始化成功")
                return ser
            else:
                print("Error opening UART3")
                return None
        except Exception as e:
            print(f"Error opening UART3: {e}")
            return None

    def read_device_model(ser: serial.Serial) -> None:
        """读取设备型号"""
        response = read_operation(ser, READ_MODEL_H, READ_MODEL_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")  # 截取有效数据并转换为字符串
            print(f"设备型号: {display_data}")
    
    def read_version(ser: serial.Serial) -> None:
        """读取版本号"""
        response = read_operation(ser, READ_VERSION_H, READ_VERSION_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"版本号: {display_data}")       
    
    def read_factory_data(ser: serial.Serial) -> None:
        """读取工厂信息"""
        response = read_operation(ser, READ_FACTORY_H, READ_FACTORY_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"厂家信息: {display_data}")
            
    
    def read_hardware_ID(ser: serial.Serial) -> None:
        """读取硬件ID"""
        response = read_operation(ser, READ_HW_ID_H, READ_HW_ID_L, 0x15)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"硬件ID: {display_data}")
                  
    def read_device_name(ser: serial.Serial) -> None:
        """读取设备名称"""
        response = read_operation(ser, READ_NAME_H, READ_NAME_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"设备名称: {display_data}")        
            
    def write_device_name(ser: serial.Serial, send_data: bytes) -> None:
        """设置设备名称"""
        data_bytes = send_data.encode('utf-8')
        response = write_operation(ser, READ_NAME_H, READ_NAME_L, data_bytes)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"设置状态: {display_data}")
            
    def read_connected(ser: serial.Serial) -> None:
        """读取连接方式"""
        response = read_operation(ser, READ_CONNECT_H, READ_CONNECT_L, 0x0C)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"连接方式: {display_data}") 
             
        
        
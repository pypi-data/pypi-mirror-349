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



# �������ò���
SERIAL_PORT = "/dev/ttyS3"  # �����豸·��
BAUD_RATE = 115200          # ������
TIMEOUT = 3                # ��ȡ��ʱʱ�䣨�룩





def calculate_pro_check(command_h: int, command_l: int, data: List[bytes] = None) -> int:
    """����У��ֵ��ԭC�����е�pro_check�߼���"""
    base_sum = 0x86 + 0xAB + 0x00 + 0x09 + command_h + command_l + 0x01 + 0xCF
    if data:
        base_sum += sum(data)
    return base_sum % 256  # ȷ�����Ϊ���ֽڣ�ԭC����δȡģ�������ʵ��Э�������


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
        start_time = time.time()  # �ؼ��޸��㣺��ʼ����ʼʱ��
        while len(response) < read_len:
            chunk = ser.read(read_len - len(response))
            if not chunk:
                time.sleep(0.01)
                if time.time() - start_time > 5:
                    print("��ȡ��ʱ")  # ����������ʾ��ǰ���Ǳ�����ȷ
                    return None
            else:
                response += chunk
        
        if check_geted_buffer(response, read_len):
            return response
        else:
            print("У��ʧ��")
            return None
            
    except Exception as e:
        print(f"��ȡ����: {e}")  # ���ʹ��Python 3.6+��f-string����
        return None


def write_operation(ser: serial.Serial, command_h: int, command_l: int, send_data: bytes) -> Optional[bytes]:
    """д���������ӦC�����е�Write_operation��"""
    len_data = len(send_data)
    pro_check = calculate_pro_check(command_h, command_l, list(send_data))
    
    # ���췢������
    send_packet = [
        0x86, 0xAB,
        (0x09 + len_data) // 256,  # ��8λ
        (0x09 + len_data) % 256,   # ��8λ
        command_h, command_l,
        *send_data,
        0x01, pro_check, 0xCF
    ]
    send_bytes = bytes(send_packet)
    
    try:
        ser.write(send_bytes)
        time.sleep(0.1)  # �ȴ����ݷ���
        
        response = ser.read(0x0B)  # ��ȡ�̶�������Ӧ
        if check_geted_buffer(response, 0x0B):
            return response
        else:
            print("У��ʧ��")
            return None
            
    except Exception as e:
        print(f"Write error: {e}")
        return None


def check_geted_buffer(buf: bytes, expected_len: int) -> bool:
    """У��������ݣ���ӦC�����е�check_geted_buffer��"""
    if len(buf) < expected_len:
        print("���ݳ��Ȳ���")
        return False
    
    # ֡ͷ���
    if buf[0] != 0x86 or buf[1] != 0xAB:
        print("Header byte error")
        return False
    
    # ֡β��飨�������һ���ֽ�Ϊ0xCF��
    if buf[-1] != 0xCF:
        print("End byte error")
        return False
    
    # У��ͼ��㣨����У��λΪ�����ڶ����ֽڣ�
    total = sum(buf[:-2]) + buf[-1]
    if total % 256 != buf[-2]:
        print("Check byte error")
        return False
    
    return True


# --------------------- ���ܺ��� ---------------------

class Uart3_funtions:

    def uart3_init() -> Optional[serial.Serial]:
        """��ʼ������"""
        try:
            ser = serial.Serial
            (
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                bytesize=serial.EIGHTBITS,  # 8λ����λ
                parity=serial.PARITY_NONE,  # ��У��λ
                stopbits=serial.STOPBITS_ONE,  # 1λֹͣλ
                timeout=TIMEOUT,
                xonxoff=False,  # �ر��������
                rtscts=False,   # �ر�Ӳ������
            )
            if ser.is_open:
                print("UART3��ʼ���ɹ�")
                return ser
            else:
                print("Error opening UART3")
                return None
        except Exception as e:
            print(f"Error opening UART3: {e}")
            return None

    def read_device_model(ser: serial.Serial) -> None:
        """��ȡ�豸�ͺ�"""
        response = read_operation(ser, READ_MODEL_H, READ_MODEL_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")  # ��ȡ��Ч���ݲ�ת��Ϊ�ַ���
            print(f"�豸�ͺ�: {display_data}")
    
    def read_version(ser: serial.Serial) -> None:
        """��ȡ�汾��"""
        response = read_operation(ser, READ_VERSION_H, READ_VERSION_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"�汾��: {display_data}")       
    
    def read_factory_data(ser: serial.Serial) -> None:
        """��ȡ������Ϣ"""
        response = read_operation(ser, READ_FACTORY_H, READ_FACTORY_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"������Ϣ: {display_data}")
            
    
    def read_hardware_ID(ser: serial.Serial) -> None:
        """��ȡӲ��ID"""
        response = read_operation(ser, READ_HW_ID_H, READ_HW_ID_L, 0x15)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"Ӳ��ID: {display_data}")
                  
    def read_device_name(ser: serial.Serial) -> None:
        """��ȡ�豸����"""
        response = read_operation(ser, READ_NAME_H, READ_NAME_L, 0x0F)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"�豸����: {display_data}")        
            
    def write_device_name(ser: serial.Serial, send_data: bytes) -> None:
        """�����豸����"""
        data_bytes = send_data.encode('utf-8')
        response = write_operation(ser, READ_NAME_H, READ_NAME_L, data_bytes)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"����״̬: {display_data}")
            
    def read_connected(ser: serial.Serial) -> None:
        """��ȡ���ӷ�ʽ"""
        response = read_operation(ser, READ_CONNECT_H, READ_CONNECT_L, 0x0C)
        if response:
            display_data = response[6:-3].decode(errors="ignore")
            print(f"���ӷ�ʽ: {display_data}") 
             
        
        
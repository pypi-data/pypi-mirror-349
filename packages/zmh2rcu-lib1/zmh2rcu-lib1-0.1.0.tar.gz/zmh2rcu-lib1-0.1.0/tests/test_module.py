from mylibrary.module1 import Uart3_funtions




if __name__ == "__main__":
    ser = uart3_init()
    if ser:
        try:
            write_device_name(ser,"H2-RCU")
            # �����������ܺ���
        except KeyboardInterrupt:
            print("\n������ֹ")
        finally:
            ser.close()
            print("���ڹر�")



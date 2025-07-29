from mylibrary.module1 import Uart3_funtions




if __name__ == "__main__":
    ser = uart3_init()
    if ser:
        try:
            write_device_name(ser,"H2-RCU")
            # 调用其他功能函数
        except KeyboardInterrupt:
            print("\n程序终止")
        finally:
            ser.close()
            print("串口关闭")



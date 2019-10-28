from src import serialinterface as ser

BAUDRATE = 192500


def get_online_control_units():
    ports = ser.get_com_ports()

    for port, name in ports:
        print(port, name)
        with ser.connect(port, baudrate=BAUDRATE, timeout=5) as conn:
            print("write data..")
            conn.write("PING")
            print("read data..")
            data = conn.readline()
            print(data)
            print("end")


if __name__ == "__main__":
    get_online_control_units()

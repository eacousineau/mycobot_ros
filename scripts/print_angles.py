import numpy as np
import time

from pymycobot.mycobot import MyCobot


def main():
    port = "/dev/ttyUSB0"
    mycobot = MyCobot(port)
    np.set_printoptions(formatter={"float_kind": lambda x: "{:.2f}".format(x)})

    while True:
        degrees = np.asarray(mycobot.get_angles())
        print(degrees * 6)
        time.sleep(0.5)


if __name__ == "__main__":
    main()

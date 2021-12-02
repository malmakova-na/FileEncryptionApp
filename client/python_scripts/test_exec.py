import time
import sys

if __name__ == "__main__":
    for i in range(10):
        print('i =', i, end="\r")
        sys.stdout.flush()
        time.sleep(0.5)
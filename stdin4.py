import sys
import time
import numpy as np
import datetime


if __name__ == "__main__":
    filename = 'output/'+ str(datetime.datetime.now()).replace(' ','_').replace('.','_').replace(':','')+'.txt'
    with open(filename,'w') as f:
        for line in sys.stdin:
            if "module_captouch.c(933)" in line:
                slider_list = line.replace(',','').split()
                pos = int(slider_list[17])
                # print(line,end='')
                if pos < 65535:
                    f.write(line)
                    print(line,end='')

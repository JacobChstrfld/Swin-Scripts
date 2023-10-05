import os
from datetime import datetime

if __name__ == '__main__':
    now = str(datetime.now())
    echo = r'echo+ >> "C:\T31Copy\output.txt"'
    echo = r'echo ' + str(now) + r' >> "C:\T31Copy\output.txt"'
    print(echo)
    os.system(echo)
    os.system(r'xcopy "\\Argus\Compliance\t31 2023\" "D:\t31 2023\" /E /H /C /I /Y /Q >> "C:\T31Copy\output.txt"')

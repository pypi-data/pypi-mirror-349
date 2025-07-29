#Uses bundled libs in Lib folder, from a default installation. This means it has no dependencies needed when installing
import sys,time

def printslow(string,TimeIntervalPerChar=None):
    if TimeIntervalPerChar == None:
        TimeIntervalPerChar = 0.01
    for carrier in string:
        sys.stdout.write(carrier)
        time.sleep(TimeIntervalPerChar)
    sys.stdout.write("\n")
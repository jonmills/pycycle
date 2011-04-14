#!/usr/bin/env python

import os
import sys
import subprocess
import time
from threading import Thread
import argparse

sleeptime = 10
runthread = True
pause = False

if sys.platform == "win32":
    import msvcrt
else:
#    import sys, tty, termios
    pass

def kbfunc():
    """ Poller function
    """
    if sys.platform == "win32":
        x = msvcrt.kbhit()
        if x:
            ret = ord(msvcrt.getch())
        else:
            ret = 0
        return ret
    else:
        fd = sys.stdin.fileno()
#        old_settings = termios.tcgetattr(fd)
#        try:
#            tty.setraw(sys.stdin.fileno())
#            ch = sys.stdin.read(1)
#        finally:
#            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#        print ch
        return 0

class KBPoller(Thread):
    def run(self):
        """ Poller thread
        """
        global sleeptime
        global runthread
        global pause
        while(runthread):
            key = kbfunc()
            if key == 0:
                pass
            elif key == 113:
                # q
                sleeptime -= 5
                if sleeptime < 0:
                    sleeptime = 0
                print "SLEEP TIME =", sleeptime
            elif key == 119:
                # w
                sleeptime += 5
                if sleeptime > 60:
                    sleeptime = 60
                print "SLEEP TIME =", sleeptime
            elif key == 32:
                # spacebar
                if pause:
                    pause = False
                    print "Resumed"
                else:
                    pause = True
                    print "Paused"
            elif key == 27:
                # escape
                print "Quitting"
                runthread = False
            else:
                print "Key =", key
            time.sleep(0.5)

def main():
    KBPoller().start()
    
    runthread = True

    try:
        while(runthread):
            if not pause:
                if sys.platform == "win32":
                    filename = os.getcwd() + os.sep + "make_and_run_tests.bat"
                else:
                    filename = os.getcwd() + os.sep + "make_and_run_tests.sh"
                print
                print "*** Running command ***"
                print
                subprocess.call([args.command])
                if runthread:
                    if not pause:
                        print
                        print "*** Waiting %d seconds ***" % (sleeptime)
                        print
                        start_time = time.time()
                        while ((start_time + sleeptime) > time.time()):
                            time.sleep(5)
                    else:
                        print
                        print "*** PAUSED ***"
                        print
                else:
                    print "*** Quitting ***"
                    exit()
                    
    except KeyboardInterrupt:
        print "Keyboard interrupt"
        runthread = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', help = "command to execute")
    args = parser.parse_args()
    if args.command != None:
        main()
    else:
        print "No -c attribute passed on command line."

import os
from multiprocessing import Process

def run_pro(name):
    print('child process %s (%s) Running...' % (name, os.getpid()))

if __name__ == '__main__':
    print('Parent processor %s.' % (os.getpid()));
    for i in range(5):
        p = Process(target=run_pro,args=(str(i)))
        print('Process will start')
        p.start()
    p.join()
    print('Process end')

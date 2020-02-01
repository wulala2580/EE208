# -*- coding: gbk -*-
from Queue import Queue
from threading import Thread
import time
#q���������
#NUM�ǲ����߳�����
#JOBS���ж�������
q = Queue()
NUM = 2
JOBS = 10
#����Ĵ�������������������
def do_something_using(arguments):
    time.sleep(1)
    print arguments
    
#����ǹ������̣����𲻶ϴӶ���ȡ���ݲ�����
def working():
    while True:
        arguments = q.get()
        do_something_using(arguments)
        q.task_done()


#fork NUM���̵߳ȴ�����
for i in range(NUM):
    t = Thread(target=working)
    t.setDaemon(True)
    t.start()
#��JOBS�������
for i in range(JOBS):
    q.put(i)
#�������ȴ�����JOBS���
q.join()

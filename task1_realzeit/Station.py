from collections import deque
import threading
import time

lock = threading.Lock()


class Station(threading.Thread):

    start_time = 0

    def __init__(self, name, duration):
        threading.Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.queue = deque([])
        self.isOperate = False
        self.arrEv = threading.Event()

    def run(self):
        while True:
            self.arrEv.wait()
            if len(self.queue) != 0:
                task = self.leave()
                time.sleep(task[0] * self.duration)
                print(f"{time.time() - self.start_time:.2f}: " + task[2].name + " Finished at " + self.name)
                task[1].set()
            else:
                self.arrEv.clear()

    def arrival(self, task):
        lock.acquire()
        self.queue.append(task)
        lock.release()

    def leave(self):
        lock.acquire()
        task = self.queue.pop()
        lock.release()
        return task

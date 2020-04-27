import subprocess
import queue
import threading
from collections import namedtuple

num_worker_threads = 2

def conv_audio(from_file, to_file):
    r = subprocess.run(args=['ffmpeg.exe', '-y', '-i', from_file,
                        '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', to_file])

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        conv_audio(item.from_file, item.to_file)
        q.task_done()

def init_tasks():
    global q, threads
    q = queue.Queue()
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

def join():
    # block until all tasks are done
    q.join()

    # stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()

WorkItem = namedtuple('WorkItem', 'from_file, to_file')
if __name__ == '__main__':
    init_tasks()
    q.put(WorkItem(r'C:\record\20180305234046.wav', r'C:\record\20180305234046.mp3'))
    q.put(WorkItem(r'C:\record\20180306011655.wav', r'C:\record\20180306011655.mp3'))
    20180306011655
    join()
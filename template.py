# Multithreaded template for brute/checker automation
# Personal use only, Threading concept required to use properly
import requests
import sys
import threading
import Queue
import socket
import time

#set the thread count below
threads_count = 40
socket.setdefaulttimeout(5)

class StartThread(threading.Thread):
    def __init__(self, queue, *args):
        self.queue = queue
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        while True:
            server = None
            username = ""
            passwd = ""
            try:
                server = self.queue.get(timeout=1)
            except Queue.Empty:
                return
            try:
                source_passlist = sys.argv[2]
                with open(source_passlist) as passlist:
                    for pairs in passlist:
                        pairs= pairs.replace('\n', '')
                        target_url = "LOGIN PATH HERE" # login path here
                        username = pairs.split(':')[0]
                        passwd = pairs.split(':')[1]
                        # work here for more login path works
                        data = {
                            # payloads here
                            }
                        headers = {
                            # headers content here if required
                            }
                        ret_code = requests.post(target_url, data= data, timeout=5).text
                        if "condition to check" in ret_code: # place checking condition
                            print 'Good: ' + username + ":" + passwd + ":" + server
                            open('good.txt', 'a+').write(username + ":" + passwd + ":" + server + "\n")
                            #break
                        else:
                            print 'Bad: ' + username + ":" + passwd + ":" + server
            except:
                print 'Bad: ' + username + ":" + passwd + ":" + server
                
            self.queue.task_done()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: ' + sys.argv[0] + ' server_list.txt userpass_list.txt'
    else:
        queue = Queue.Queue()
        threads = []
        for i in range(threads_count):
            worker = StartThread(queue, i)
            worker.setDaemon(True)
            worker.start()
            threads.append(worker)
        source_servers = sys.argv[1]
        with open(source_servers) as servs:
            for a_server in servs:
                a_server = a_server.replace('\n', '')
                queue.put(a_server)
            #queue.join()
            for item in threads:
                item.join()
    print 'DONE Scanning!'

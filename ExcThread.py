import threading
import sys
 
class ExcThread(threading.Thread):

    def __init__(self, target = None, args = ()):
        super(ExcThread, self).__init__()
        self.exc = None
        self.target = target
        self.args = args
    
    def run(self):
        try:
            if self.target is not None:
                self.target(*self.args)
        except SystemExit as e:
            self.exc = e
        finally:
            del self.target, self.args
    def join(self):
        threading.Thread.join(self)
        if self.exc:
            raise self.exc
import threading


class IDSBackgroundThread(threading.Thread):
    def __init__(self, target=None):
        super().__init__(target=target)

    def run(self):
        # Implement the thread's run logic here
        super().run()

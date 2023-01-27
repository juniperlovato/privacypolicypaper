import time

class Timer():
    def __init__(self, step_name, log=True):
        self.step_name = step_name
        self.log = log

    def __enter__(self):
        if self.log:
            print(f"{self.step_name}...")
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        end_time = time.time()
        if self.log:
            print(f"{self.step_name} took {end_time - self.start_time:.2f} seconds")

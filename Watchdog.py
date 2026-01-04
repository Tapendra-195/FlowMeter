'''
Author: Tapendra BC
Date: Dec 2025
Description: Watchdog timer class to handle the circulation system program crash.
'''


class Watchdog:
    def __init__(self, device='/dev/watchdog'):
        self.device = device
        self._running = False
        self._wdt = None #watch dog timer

    #This dog gets mad if you don't pet it. Give it some belly rub
    def pet_dog(self):
        if not self._running or self._wdt is None:
            print("Watchdog isn't started")
            return
        #meow, I assume the dog says meow when you pet it :0
        try:
            self._wdt.write(b'1')
            self._wdt.flush()
        except Exception as e:
            print(f"petting the dog failed: {e}")

    def _start(self):
        try:
            self._wdt = open(self.device, 'wb')
        except PermissionError:
            raise PermissionError("can\'t open device. Need root previlage or device busy")
        self._running = True
        
    def _stop(self):
        if not self._running:
            return

        self._running = False
        try:
            self._wdt.write(b'V')
            self._wdt.flush()
        except Exception as e:
            print(f"Error disabling watchdog: {e}")
        finally:
            self._wdt.close()
            print("watchdog stopped safely")

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop()

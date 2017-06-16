from random import *

class AlarmManager:
    def __init__(self, hour, minutes, am, selDays):
        self.on = False
        self.set(hour, minutes, am, selDays)

    def set(self, hour, minutes, am, selDays):
        self.hour = hour
        self.min = minutes
        self.am = am
        self.selectedDays = selDays
        self.writeConfig()

    def getBanner(self):
        pass

    def writeConfig(self):
        with open('alarm.config', 'w') as f:
            f.write(":".join(map(str, [self.on, self.hour, self.min, self.am, ",".join(self.selectedDays.keys())])))

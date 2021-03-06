import os
import gc
import subprocess
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import pyglet
from pyglet.gl import *

WHITE = (255, 255, 255, 255)
PINK = (200, 0, 100, 255)
DPINK = (99, 75, 101, 255)

class SettingsDisplay:
    def __init__(self):
        self.hour = 1
        self.min = 0
        self.am = True
        self.selectedTime = None
        cronOut = None
        try:
            if os.path.exists('crontab.bak'):
                subprocess.check_output("crontab -u pi crontab.bak", shell=True)
            cronOut = subprocess.check_output("crontab -l", shell=True).split()
            inTime = datetime.strptime(cronOut[0]+' '+cronOut[1], "%M %H")
            outTime = datetime.strftime(inTime, "%I %M %p").split()
            self.hour = int(outTime[0])
            self.min = int(outTime[1])
            self.am = True if outTime[2] == 'AM' else False
        except subprocess.CalledProcessError:
            pass

        self.batchUI = pyglet.graphics.Batch()
        self.bgOff = pyglet.image.load('data/img/bgoff.png')
        self.bgOn = pyglet.image.load('data/img/bgon.png')
        self.bg = self.bgOff
        self.inc = Icon('data/img/inc.png', x=394, y=145, batch=self.batchUI)
        self.dec = Icon('data/img/dec.png', x=394, y=70, batch=self.batchUI)
        self.done = Icon('data/img/done.png', x=402, y=15, batch=self.batchUI)
        self.off = Icon('data/img/off.png', x=405, y=240, batch=self.batchUI)
        self.on = Icon('data/img/on.png', x=405, y=240, batch=self.batchUI, visible=False)
        self.hourLabel = pyglet.text.Label(str(self.hour), font_name='Cat Font',
            font_size=85, x=50-27, y=210, color=WHITE, width=120, height=100,
            multiline=True, align='right', batch=self.batchUI)
        self.minLabel = pyglet.text.Label("{:02}".format(self.min), font_name='Cat Font',
            font_size=85, x=195-27, y=210, color=WHITE, width=130, height=100,
            batch=self.batchUI)
        self.amLabel = pyglet.text.Label('AM' if self.am else 'PM', font_name='Cat Font', font_size=25, x=315,
            y=235, color=WHITE, width=50, height=50, batch=self.batchUI)
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=85,
            x=165-27, y=215, color=WHITE, batch=self.batchUI)
        self.dayLabels = [
            pyglet.text.Label('S', font_name='Cat Font', font_size=35, x=58,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('M', font_name='Cat Font', font_size=35, x=94,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('T', font_name='Cat Font', font_size=35, x=139,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('W', font_name='Cat Font', font_size=35, x=174,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('T', font_name='Cat Font', font_size=35, x=234,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('F', font_name='Cat Font', font_size=35, x=271,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI),
            pyglet.text.Label('S', font_name='Cat Font', font_size=35, x=308,
                y=150, color=DPINK, width=40, height=50, batch=self.batchUI)]
        self.banner = pyglet.text.Label('', font_name='Helvetica', font_size=13.5, 
            x=10, y=58, color=WHITE, width=375, multiline=True, align='center')
        self.setBanner()

        def off_func():
            self.bg = self.bgOn
            def f(dt):
                self.off.visible = False
                self.on.visible = True
                self.setBanner()
            pyglet.clock.schedule_once(f, 0.21)

        def on_func():
            self.bg = self.bgOff
            def f(dt):
                self.off.visible = True
                self.on.visible = False
            pyglet.clock.schedule_once(f, 0.21)

        def inc_func():
            if self.selectedTime == self.hourLabel:
                self.hour = 1 if self.hour == 12 else self.hour+1
                self.hourLabel.text = str(self.hour)
            elif self.selectedTime == self.minLabel:
                self.min = 0 if self.min == 55 else self.min+5
                self.minLabel.text = "{:02}".format(self.min)
            self.setBanner()

        def dec_func():
            if self.selectedTime == self.hourLabel:
                self.hour = 12 if self.hour == 1 else self.hour-1
                self.hourLabel.text = str(self.hour)
            elif self.selectedTime == self.minLabel:
                self.min = 55 if self.min == 0 else self.min-5
                self.minLabel.text = "{:02}".format(self.min)
            self.setBanner()

        def done_func():
            self.saveCronTab()
            return True

        if cronOut:
            off_func()
            for i in cronOut[4].split(','):
                self.dayLabels[int(i)].color = PINK
        self.icons = {self.off:off_func, self.on:on_func, self.inc:inc_func, self.dec:dec_func, self.done:done_func}

    def saveCronTab(self):
        if os.path.exists('crontab.bak'):
            os.remove('crontab.bak')
        os.system("crontab -r") # clear crontab first
        if self.on.visible:
            os.system("echo '{} pigs w 16 1' | crontab -u pi -".format(self.getCronTime()))
            os.system("crontab -l > crontab.bak")
            gc.collect()

    def getCronTime(self):
        inTime = datetime.strptime("{}:{} {}".format(self.hour, self.min, 'AM' if self.am else 'PM'), "%I:%M %p")
        days = ",".join(map(str, [i for i, l in enumerate(self.dayLabels) if l.color == PINK]))
        return "{} * * {}".format(datetime.strftime(inTime, "%M %H"), days)

    def setBanner(self):
        if not self.on.visible or len([e for e in self.dayLabels if e.color == PINK]) < 1:
            return
        nowTime = datetime.now()
        nextTime = croniter(self.getCronTime(), nowTime).get_next(datetime)
        diff = nextTime-nowTime
        minutes = (diff.seconds//60)%60
        hours = diff.seconds//60**2

        txt = 'Alarm set for '
        if diff.days > 0:
            txt += "{} days, ".format(diff.days)
        self.banner.text = txt + "{} hours\nand {} minutes from now".format(hours, minutes)

    def isPressed(self, icon, x, y):
        x2 = icon.x
        y2 = icon.y
        w = icon.width
        h = icon.height
        if x >= x2 and y >= y2 and x <= x2+w and y <= y2+h:
            return True
        return False

    def setSelectedTime(self, label):
        if self.selectedTime:
            self.selectedTime.color = WHITE
        label.color = PINK
        self.selectedTime = label

    def press(self, x, y):
        if x > 390:
            for i in self.icons:
                if i.visible and self.isPressed(i, x, y):
                    i.act()
                    return self.icons[i]()
        elif y > 190:
            if self.isPressed(self.hourLabel, x, y):
                self.setSelectedTime(self.hourLabel)
            elif self.isPressed(self.minLabel, x, y):
                self.setSelectedTime(self.minLabel)
            elif self.isPressed(self.amLabel, x, y):
                self.am = not self.am
                self.amLabel.text = 'AM' if self.am else 'PM'
                self.setBanner()
        elif y < 85:
            return self.icons[self.done]()
        else:
            for l in self.dayLabels:
                if self.isPressed(l, x, y):
                    if l.color == DPINK: # not selected
                        l.color = PINK
                    else: # selected
                        l.color = DPINK
                    self.setBanner()

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.bg.blit(0, 0)
        self.batchUI.draw()
        if self.on.visible:
            self.banner.draw()


class Icon(pyglet.sprite.Sprite):
    def __init__(self, path, x, y, batch=None, visible=True):
        pyglet.sprite.Sprite.__init__(self, pyglet.image.load(path), x, y, batch=batch)
        self.visible = visible
        self.waiting = False # avoid double click abuse

    def act(self):
        if self.waiting:
            return
        self.waiting = True
        self.x -= self.width/6
        self.y -= self.height/6
        self.scale = 1.25
        pyglet.clock.schedule_once(self.restoreScale, 0.2)

    def restoreScale(self, dt=0):
        self.waiting = False
        self.scale = 1.0
        self.x += self.width/6
        self.y += self.height/6

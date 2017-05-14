import pyglet

# TODO
# add day, month, date text
class TimeDisplay:
    def __init__(self, winWidth, winHeight):
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.dayText = None
        self.timeText = None
        self.colon = pyglet.text.Label(':', font_name='Cat Font', font_size=125,
            y=winHeight/2, color=(200, 0, 100, 255),
            anchor_x='center', anchor_y='center')
        self._showColon = True
        self._bound1 = 0
        self._bound2 = 0
        self.day = ''
        self.hour = ''
        self.minute = ''

    def colonSwitch(self, dt):
        self._showColon = not self._showColon

    def update(self, day, hour, minute):
        if self.day != day: # update day text label
            self.day = day
        if self.hour != hour: # update hour colon bound
            self._bound1 = pyglet.text.Label(hour, font_name='Cat Font', font_size=125).content_width
            self.hour = hour
        if self.minute != minute: # update time text label
            self.timeText = pyglet.text.Label("{} {}".format(hour, minute),
                font_name='Cat Font', font_size=125, x=self.winWidth/2,
                y=self.winHeight/2, color=(200, 0, 100, 255),
                anchor_x='center', anchor_y='center')
            self._bound2 = pyglet.text.Label(minute, font_name='Cat Font', font_size=125).content_width
            self.colon.x = self.winWidth/2-(self._bound2-self._bound1)/2.0
            self.minute = minute

    def draw(self):
        self.timeText.draw()
        if self._showColon:
            self.colon.draw()


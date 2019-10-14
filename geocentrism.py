#! /usr/bin/env python

import matplotlib;
import matplotlib.pyplot as pyplot;
import numpy;
import matplotlib.animation as animation;


class SolarSystem:

    def __init__(self):
        self.au = 100;
        self.alpha = None;
        self.earth = pyplot.Circle((0, 0), 3, color = "#101080");
        self.sun = pyplot.Circle((0, 0), 5, color = "#808010");

    @staticmethod
    def transform0(sun_position, earth_position):
        return;

    @staticmethod
    def transform1(sun_position, earth_position):
        sun_position[0] = -earth_position[0];
        sun_position[1] = -earth_position[1];
        earth_position[0] = 0;
        earth_position[1] = 0;

    @staticmethod
    def transform2(sun_position, earth_position):
        sun_position[0] = -earth_position[0] / 2.;
        sun_position[1] = -earth_position[1] / 2.;
        earth_position[0] /= 2.;
        earth_position[1] /= 2.;

    def draw(self, transform_func = None):
        angular = self.alpha * numpy.pi / 180.;
        x = self.au * numpy.cos(angular);
        y = self.au * numpy.sin(angular);
        sun_position = [0, 0];
        earth_position = [x, y];
        if transform_func:
            transform_func(sun_position, earth_position);
        self.sun.set_center((sun_position[0], sun_position[1]));
        self.earth.set_center((earth_position[0], earth_position[1]));

    def add_to_axes(self, axes):
        axes.add_artist(self.sun);
        axes.add_artist(self.earth);

    def shift(self, delta_degrees, transform_func = None):
        if self.alpha is None:
            self.alpha = 0;
        else:
            self.alpha += delta_degrees;
        self.alpha %= 360;
        self.draw(transform_func);

    def get_artists(self):
        return [self.sun, self.earth];


def shift_solar_system(value, ss, transform_func):
    ss.shift(10, transform_func);


def init_rotation():
    return solar.get_artists();


pyplot.style.use("dark_background");
ax = pyplot.axes(label="123");
pyplot.axis([-160, 160, -120, 120]);
pyplot.axis(False);
pyplot.grid(True);
figure = pyplot.gcf();
solar = SolarSystem();
solar.add_to_axes(ax);
rot_animation = animation.FuncAnimation(fig = figure,
                                        init_func = init_rotation,
                                        func = shift_solar_system,
                                        fargs = (solar, SolarSystem.transform2),
                                        frames = 36,
                                        repeat = False,
                                        interval = 100);

rot_animation.save("transform2.gif", dpi = 96, writer = matplotlib.animation.PillowWriter(96));

pyplot.show();

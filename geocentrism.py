#! /usr/bin/env python

import matplotlib;
import matplotlib.pyplot as pyplot;
import numpy;
import matplotlib.animation as animation;


class Planet:

    def __init__(self, radius, orbit_radius, angular_step, color, initial_angular):
        self.radius = radius;
        self.orbit_radius = orbit_radius;
        self.angular_step = angular_step;
        self.color = color;
        self.angular = initial_angular;

    def step(self):
        self.angular += self.angular_step;
        if self.angular >= 360:
            self.angular %= 360;


class SolarSystem:

    def __init__(self):
        self.au = 100;
        self.sun = Planet(7, 0, 0, "#808010", 0);
        self.mercury = Planet(2, 30, 40, "#505000", 0);
        self.venus = Planet(4, 70, 12, "#505000", 0);
        self.earth = Planet(4, 100, 10, "#101080", 0);
        self.mars = Planet(3, 120, 6, "#801010", 0);
        self.jupiter = Planet(5, 150, 1, "#505050", 0);

    def step(self):
        for attr in self.__dict__:
            planet = self.__dict__[attr];
            if type(planet) == Planet:
                planet.step();


class Projection:

    def __init__(self):



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

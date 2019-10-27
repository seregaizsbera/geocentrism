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
        self.venus = Planet(4, 70, 12, "#AF3410", 0);
        self.earth = Planet(4, 100, 10, "#101080", 0);
        self.mars = Planet(3, 120, 6, "#801010", 0);
        self.jupiter = Planet(5, 140, 1, "#505050", 0);

    def foreach(self, f, *args, **kwargs):
        for attr in self.__dict__:
            planet = self.__dict__[attr];
            if type(planet) == Planet:
                f(planet, *args, **kwargs);

    def step(self):
        self.foreach(Planet.step);


class Projection:

    def __init__(self, axes, ss):
        self.figures = [];
        ss.foreach(Projection.init_planet, self, axes);

    @staticmethod
    def init_planet(planet, *args, **kwargs):
        a = list(args);
        projection = a.pop(0);
        args2 = tuple(a)
        projection.init_planet_internal(planet, *args2, **kwargs);

    def init_planet_internal(self, planet, *args, **kwargs):
        fig = pyplot.Circle(self.calculate_xy(planet), planet.radius, color=planet.color);
        self.figures.append((fig, planet));
        args[0].add_artist(fig);

    # noinspection PyMethodMayBeStatic
    def calculate_xy(self, planet):
        x = planet.orbit_radius * numpy.cos(planet.angular * numpy.pi / 180.);
        y = planet.orbit_radius * numpy.sin(planet.angular * numpy.pi / 180.);
        return x, y;

    def draw(self):
        for (fig, planet) in self.figures:
            fig.set_center(self.calculate_xy(planet));


def animate(value):
    solar.step();
    projection1.draw();


solar = SolarSystem();

pyplot.style.use("dark_background");
ax = pyplot.axes(label="123");
pyplot.axis([-200, 199, -150, 149]);
pyplot.axis("equal");
pyplot.axis(False);
pyplot.grid(True);

projection1 = Projection(ax, solar);

rot_animation = animation.FuncAnimation(fig=pyplot.gcf(),
                                        func=animate,
                                        frames=359,
                                        repeat=False,
                                        interval=100);

rot_animation.save("transform.gif", dpi=96, writer=matplotlib.animation.PillowWriter(96));

pyplot.show();

'''
figure = pyplot.gcf();
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
'''

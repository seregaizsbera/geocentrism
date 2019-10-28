#! /usr/bin/env python

import matplotlib;
import matplotlib.pyplot as pyplot;
import numpy;
import matplotlib.animation as animation;


class Planet:

    def __init__(self, name, radius, orbit_radius, angular_step, color, initial_angular):
        self.name = name;
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
        self.planets = {};
        self.au = 100;
        self.add_planet(Planet("sun", 7, 0, 0, "#808010", 0));
        # self.add_planet(Planet("mercury", 2, 20, 40, "#505000", 0));
        self.add_planet(Planet("venus", 4, 40, 12, "#AF3410", 0));
        self.add_planet(Planet("earth", 4, 60, 10, "#101080", 0));
        # self.add_planet(Planet("mars", 3, 80, 6, "#801010", 0));
        # self.add_planet(Planet("jupiter", 5, 100, 1, "#505050", 0));

    def add_planet(self, planet):
        self.planets[planet.name] = planet;

    def foreach(self, f, *args, **kwargs):
        for p, planet in self.planets.items():
            f(planet, *args, **kwargs);

    def step(self):
        self.foreach(Planet.step);


class Projection:
    """
    Вид модели в системе отсчета, связанной с Солнцем
    """

    def __init__(self, axes, ss, window_shift):
        self.figures = [];
        self.ss = ss;
        self.window_shift = window_shift;
        ss.foreach(Projection.init_planet, self, axes);

    # noinspection PyMethodMayBeStatic
    def calculate_shift_vec(self):
        return [0, 0];

    @staticmethod
    def init_planet(planet, *args, **kwargs):
        a = list(args);
        projection = a.pop(0);
        args2 = tuple(a)
        projection.init_planet_internal(planet, *args2, **kwargs);

    def init_planet_internal(self, planet, *args, **kwargs):
        shift_vec = self.calculate_shift_vec();
        fig = pyplot.Circle(self.calculate_xy(shift_vec, planet), planet.radius, color=planet.color);
        self.figures.append((fig, planet));
        args[0].add_artist(fig);

    # noinspection PyMethodMayBeStatic
    def calculate_xy(self, shift_vec, planet):
        x = self.window_shift[0] + shift_vec[0] + planet.orbit_radius * numpy.cos(planet.angular * numpy.pi / 180.);
        y = self.window_shift[1] + shift_vec[1] + planet.orbit_radius * numpy.sin(planet.angular * numpy.pi / 180.);
        return x, y;

    def draw(self):
        shift_vec = self.calculate_shift_vec();
        for (fig, planet) in self.figures:
            fig.set_center(self.calculate_xy(shift_vec, planet));


class Projection2(Projection):
    """
    Вид модели в системе отсчета, связанной с центром отрезка между Солнцем и Землей
    """

    def __init__(self, axes, ss, window_shift):
        super().__init__(axes, ss, window_shift);

    def calculate_shift_vec(self):
        sun = self.ss.planets["sun"];
        earth = self.ss.planets["earth"];
        sun_x = sun.orbit_radius * numpy.cos(sun.angular * numpy.pi / 180.);
        sun_y = sun.orbit_radius * numpy.sin(sun.angular * numpy.pi / 180.);
        earth_x = earth.orbit_radius * numpy.cos(earth.angular * numpy.pi / 180.);
        earth_y = earth.orbit_radius * numpy.sin(earth.angular * numpy.pi / 180.);
        return [(sun_x - earth_x) / 2., (sun_y - earth_y) / 2.];


class Projection3(Projection):
    """
    Вид модели в системе отсчета, связанной с Землей
    """

    def __init__(self, axes, ss, window_shift):
        super().__init__(axes, ss, window_shift);

    def calculate_shift_vec(self):
        sun = self.ss.planets["sun"];
        earth = self.ss.planets["earth"];
        sun_x = sun.orbit_radius * numpy.cos(sun.angular * numpy.pi / 180.);
        sun_y = sun.orbit_radius * numpy.sin(sun.angular * numpy.pi / 180.);
        earth_x = earth.orbit_radius * numpy.cos(earth.angular * numpy.pi / 180.);
        earth_y = earth.orbit_radius * numpy.sin(earth.angular * numpy.pi / 180.);
        return [sun_x - earth_x, sun_y - earth_y];


def animate(value):
    solar.step();
    projection1.draw();
    projection2.draw();
    projection3.draw();


solar = SolarSystem();

pyplot.style.use("dark_background");
ax = pyplot.axes(label="123");
pyplot.axis([0, 800, 0, 480]);
pyplot.gca().set_aspect("equal", adjustable="box");
pyplot.axis(False);
pyplot.grid(False);

projection1 = Projection(ax, solar, [110, 180]);
projection2 = Projection2(ax, solar, [370, 180]);
projection3 = Projection3(ax, solar, [630, 180]);

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

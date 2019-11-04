#! /usr/bin/env python

from datetime import datetime;

import matplotlib
import matplotlib.pyplot as pyplot;
import numpy;
import matplotlib.animation as animation;

# выводить анимацию в файл или в окно
output_to_gif = False;
# Cколько кадров в итоговой анимации. Больше кадров, лучше качество, но больше весит итоговый gif.
number_of_steps = 720;
# Cколько оборотов вокруг Солнца должен сделать Юпитер, самый медленный объект
jupiter_rounds = 2;
# Время анимации, за которое Юпитер делает 1 полный оборот вокруг Солнца
jupiter_year_ms = 30000;
# Угол поворота Юпитера в градусах относительно Солнца за 1 шаг (угловая скорость).
# Скорость всех планет рассчитывается от скорости Юпитера, так как он самый медленный.
# Он должен за один цикл анимации сделать jupiter_rounds оборотов.
# Остальные планеты движутся со скоростями пропорционально указанным коэффициентам.
jupiter_step = jupiter_rounds * 360 / number_of_steps;
# задержка между кадрами
frame_delay_ms = (jupiter_year_ms * jupiter_rounds) / number_of_steps;


class Planet:

    def __init__(self, name, radius, orbit_radius, angular_step, color, initial_angular, trace):
        self.name = name;
        self.radius = radius;
        self.orbit_radius = orbit_radius;
        self.angular_step = angular_step;
        self.color = color;
        self.angular = initial_angular;
        self.trace = trace;

    def step(self):
        self.angular += self.angular_step;
        if self.angular >= 360:
            self.angular %= 360;


class SolarSystem:

    def __init__(self):
        self.planets = {};
        self.au = 100;
        traces = True;
        self.add_planet(Planet("sun", 7, 0, jupiter_step * 0, "#909020", 0, traces));
        self.add_planet(Planet("mercury", 3, 24, jupiter_step * 24, "#404000", 0, traces));
        self.add_planet(Planet("venus", 4, 48, jupiter_step * 12, "#A0A0A0", 0, traces));
        self.add_planet(Planet("earth", 4, 72, jupiter_step * 10, "#101080", 0, traces));
        self.add_planet(Planet("mars", 3, 96, jupiter_step * 6, "#801010", 0, traces));
        self.add_planet(Planet("jupiter", 5, 120, jupiter_step, "#505050", 0, traces));
        self.has_traces = False;
        for planet in self.planets:
            if self.planets[planet].trace:
                self.has_traces = True;
                break;

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
        self.axes = axes;
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
        fig.set_zorder(10);
        if planet.trace:
            line = pyplot.Line2D([fig.center[0]], [fig.center[1]], color=planet.color, linewidth=1);
            line.set_zorder(1);
            line.stop = False;
            args[0].add_artist(line);
        else:
            line = None;
        self.figures.append((fig, planet, line));
        args[0].add_artist(fig);

    # noinspection PyMethodMayBeStatic
    def calculate_xy(self, shift_vec, planet):
        x = self.window_shift[0] + shift_vec[0] + planet.orbit_radius * numpy.cos(planet.angular * numpy.pi / 180.);
        y = self.window_shift[1] + shift_vec[1] + planet.orbit_radius * numpy.sin(planet.angular * numpy.pi / 180.);
        return x, y;

    def draw(self):
        shift_vec = self.calculate_shift_vec();
        for (fig, planet, line) in self.figures:
            x, y = self.calculate_xy(shift_vec, planet);
            fig.set_center((x, y));
            if line:
                if not line.stop:
                    (xdata, ydata) = line.get_data();
                    if len(xdata) > 3:
                        dx1 = x - xdata[1];
                        dy1 = y - ydata[1];
                        dx2 = xdata[-1] - xdata[0];
                        dy2 = ydata[-1] - ydata[0];
                        dd = numpy.sqrt(numpy.abs(dx1 * dx2) + numpy.abs(dy1 * dy2));
                        if dd < 0.00001:
                            # если траектория замкнулась, то начало линии сохраняется в конец,
                            # и дальнейшее рисование прекращается
                            line.stop = True;
                            xdata.pop();
                            ydata.pop();
                            x = xdata[0];
                            y = ydata[0];
                    xdata.append(x);
                    ydata.append(y);
                    line.set_data((xdata, ydata));


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
    if value == 0:
        # Не двигать модель в 0-м кадре
        return;
    solar.step();
    projection1.draw();
    projection2.draw();
    projection3.draw();


solar = SolarSystem();

pyplot.style.use("dark_background");
ax = pyplot.axes(label="123");
pyplot.gcf().set_figheight(6);
pyplot.gcf().set_figwidth(12);
pyplot.axis([0, 1000, 0, 400]);
pyplot.gca().set_aspect("equal", adjustable=None, anchor="SW");
pyplot.axis(False);
pyplot.grid(False);

projection1 = Projection(ax, solar, [135, 200]);
projection2 = Projection2(ax, solar, [425, 200]);
projection3 = Projection3(ax, solar, [780, 200]);

if output_to_gif:
    # В gif выдается количество кадров, на 1 меньше количества шагов
    # Последний шаг не нужен, поскольку он будет сделан в следующем цикле анимации
    number_of_frames = number_of_steps - 1;
else:
    # В окне, почему-то на один кадр получается меньше
    number_of_frames = number_of_steps + 1;

rot_animation = animation.FuncAnimation(fig=pyplot.gcf(),
                                        blit=False,
                                        func=animate,
                                        frames=number_of_frames,
                                        repeat=False,
                                        interval=frame_delay_ms);

if output_to_gif:
    rot_animation.save("transform-{0:%Y-%m-%d-%H-%M-%S}.gif".format(datetime.now()),
                       dpi=96,
                       writer=matplotlib.animation.PillowWriter(96));
else:
    pyplot.show();

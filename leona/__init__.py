import math
import random
import asyncio

from atlasbuggy.serial import SerialStream

from leona.actuators import Actuators
from atlasbuggy.plotters.liveplotter import LivePlotter
from atlasbuggy.plotters.plot import RobotPlot
from atlasbuggy.plotters.collection import RobotPlotCollection
from atlasbuggy.plotters.staticplotter import StaticPlotter


class Leona(SerialStream):
    def __init__(self, enabled=True, log_level=None, plot=False):
        self.actuators = Actuators()
        super(Leona, self).__init__(self.actuators, enabled=enabled, log_level=log_level)

    def serial_start(self):
        self.actuators.stop()

    def take(self):
        pass

    async def update(self):
        pass

    def receive_actuators(self, timestamp, packet):
        pass

    def received_log(self, timestamp, whoiam, packet, packet_type):
        pass
        # if whoiam == self.actuators.whoiam:
        #     if packet == "h":
        #         print("%0.4fs:" % self.dt(), "stop")
        #     elif packet[0] == "r":
        #         print("%0.4fs:" % self.dt(), "spinning %s" % "right" if bool(int(packet[1:3])) else "left")
        #     elif packet[0] == "p":
        #         print(
        #             "%0.4fs:" % self.dt(), "driving at %sº at speed %s" % (
        #                 (1 if packet[1] == "0" else -1) * int(packet[2:5]), int(packet[5:8]))
        #         )
        #     elif packet[0] == "c":
        #         yaw = int(packet[1:4])
        #         azimuth = int(packet[4:7])
        #         print("%0.4fs:" % self.dt(), end="looking ")
        #         if yaw == 90 and azimuth == 90:
        #             print("straight")
        #         else:
        #             if yaw > 90:
        #                 print("left and ", end="")
        #             elif yaw < 90:
        #                 print("right and ", end="")
        #
        #             if azimuth == 90:
        #                 print("straight")
        #             elif azimuth > 90:
        #                 print("up", end="")
        #             else:
        #                 print("down", end="")
        #
        #             if yaw == 90:
        #                 print(" and straight", end="")
        #             print()
        #
        #     elif packet[0] == "o":
        #         if self.plotter is not None and self.led_plot.enabled:
        #             start_led = int(packet[1:4])
        #             r = int(packet[4:7])
        #             g = int(packet[7:10])
        #             b = int(packet[10:13])
        #             if len(packet) > 13:
        #                 end_led = int(packet[13:16])
        #                 for led_num in range(start_led, end_led):
        #                     self.led_plot[led_num].set_properties(color=(r / 255, g / 255, b / 255))
        #             else:
        #                 self.led_plot[start_led].set_properties(color=(r / 255, g / 255, b / 255))
        #             self.plotter.draw_text(
        #                 self.led_plot,
        #                 "Hi I'm naboris!\nThese are the LEDs states at t=%0.2fs" % (self.dt()),
        #                 0, 0, verticalalignment='center',  horizontalalignment='center', text_name="welcome text",
        #                 fontsize='small'
        #             )

    def serial_close(self):
        self.actuators.stop()
        self.actuators.release()

        if self.plotter is not None:
            if isinstance(self.plotter, StaticPlotter):
                self.exit()
                self.plotter.plot()
            elif isinstance(self.plotter, LivePlotter):
                self.plotter.plot()

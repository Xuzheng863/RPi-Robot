import math
import time
import random
import numpy as np

from atlasbuggy.serial import SerialStream
from atlasbuggy.plotters import LivePlotter, RobotPlot, RobotPlotCollection, StaticPlotter
from atlasbuggy.subscriptions import *

from leona.actuators import Actuators


class Leona(SerialStream):
    def __init__(self, enabled=True, log_level=None, demo=False):
        self.actuators = Actuators()
        super(Leona, self).__init__(self.actuators, enabled=enabled, log_level=log_level)

        self.link_callback(self.actuators, self.receive_actuators)
        self.demo = demo

        self.autonomous = False

        self.pipeline_results = None
        self.pipeline_feed = None
        self.pipeline_tag = "pipeline"
        self.results_service_tag = "results"
        self.require_subscription(self.pipeline_tag, Feed, service_tag=self.results_service_tag, is_suggestion=True)


    def take(self, subscriptions):
        if self.pipeline_tag in subscriptions:
            self.pipeline_feed = subscriptions[self.pipeline_tag].get_feed()

    def serial_start(self):
        self.actuators.stop()
        self.actuators.lower()

    def serial_update(self):
        safe_w = (220, 420)
        safe_h = (140, 340)
        default_size = 5000
        size_scale = 0.8
        while self.is_running():
            if self.pipeline_results is not None:
                # print(self.pipeline_results)
                (face, face_size) = self.pipeline_results
                if self.autonomous:
                    if face is None:
                        status = "search"
                        self.actuators.spin(200)
                    else:
                        status = "adjusting"
                        (x, y, w, h) = face
                        c = (x + w / 2, y + h / 2)
                        if c[0] < safe_w[0]:
                            self.actuators.spin(-200)
                        elif c[0] > safe_w[1]:
                            self.actuators.spin(200)
                        elif c[1] < safe_h[0]:
                            self.actuators.lift()
                        elif c[1] > safe_h[1]:
                            self.actuators.lower()
                        elif face_size < default_size * size_scale:
                            self.actuators.drive(-200, 0, 0)
                        elif face_size > default_size / size_scale:
                            self.actuators.drive(200, 0, 0)
                        else:
                            self.status = "steady"
                            self.actuators.stop()
                            self.actuators.stop_LA()
                    # print(face, face_size)
            time.sleep(0.1)

        self.logger.debug("Serial update exited")

    async def update(self):
        if self.is_subscribed(self.pipeline_tag):
            while not self.pipeline_feed.empty():
                self.pipeline_results = await self.pipeline_feed.get()
                self.pipeline_feed.task_done()

        await asyncio.sleep(0.0)
    def receive_actuators(self, timestamp, packet):
        pass

    def receive_serial_log(self, timestamp, whoiam, packet, packet_type):
        if whoiam == self.actuators.whoiam:
            if packet == "h":
                print("%0.4fs:" % self.dt(), "stop")
            elif packet[0] == "r":
                print("%0.4fs:" % self.dt(), "spinning %s" % "right" if bool(int(packet[1:3])) else "left")
            elif packet[0] == "p":
                print(
                    "%0.4fs:" % self.dt(), "driving at %sº at speed %s" % (
                        (1 if packet[1] == "0" else -1) * int(packet[2:5]), int(packet[5:8]))
                )

    def serial_close(self):
        self.actuators.stop()
        self.actuators.release()
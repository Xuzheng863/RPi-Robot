from atlasbuggy.serial.object import SerialObject


class Actuators(SerialObject):
    def __init__(self, enabled=True):
        self.speed_increment = 10
        self.speed_delay = 1

        super(Actuators, self).__init__("actuators", enabled)

    def receive_first(self, packet):
        data = packet.split("\t")
        assert len(data) == 2

        self.speed_increment = int(data[0])
        self.speed_delay = int(data[1])

    def receive(self, timestamp, packet):
        pass

    def drive(self, speed, angle, rotational_speed=0):
        direction_flag = 0
        if speed > 0:
            direction_flag = 1
        if rotational_speed > 0:
            if direction_flag == 1:
                direction_flag = 3
            else:
                direction_flag = 2
        command = "p%d%03d%03d%03d" % (direction_flag, angle, abs(speed), abs(rotational_speed))

        self.send(command)

    def spin(self, speed):
        command = "r%d%03d" % (int(-speed > 0), abs(speed))
        self.send(command)

    def stop(self):
        self.send("h")

    def release(self):
        self.send("d")

    def lift(self):
        self.send("u")

    def lower(self):
        self.send("l")

    def stop_LA(self):
        self.send("s")

    # @staticmethod
    # def constrain_value(value):
    #     if value < 0:
    #         value = 0
    #     if value > 255:
    #         value = 255
    #     return value

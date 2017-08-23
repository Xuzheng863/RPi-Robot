import re
import os
from atlasbuggy.extras.cmdline import CommandLine


class CMDline(CommandLine):
    def __init__(self, enabled=True, log_level=None):
        super(CMDline, self).__init__(enabled, log_level)
        self.leona = None
        self.actuators = None
        self.capture = None

        self.leona_tag = "leona"
        self.capture_tag = "capture"

        self.video_num_counter_regex = r"([\s\S]*)-([0-9]*)\.([\S]*)"
        self.video_name_regex = r"([\s\S]*)\.([\S]*)"

        self.require_subscription(self.leona_tag)
        self.require_subscription(self.capture_tag)

    def take(self, subscriptions):
        self.leona = subscriptions[self.leona_tag].get_stream()
        self.capture = subscriptions[self.capture_tag].get_stream()
        self.actuators = self.leona.actuators

    def spin_left(self, params):
        value = int(params) if len(params) > 0 else 75
        self.actuators.spin(value)

    def spin_right(self, params):
        value = int(params) if len(params) > 0 else 75
        self.actuators.spin(-value)

    def drive(self, params):
        angle = 0
        speed = 200
        angular = 0
        if len(params) > 1:
            values = params.split(" ")

            try:
                if len(values) >= 1:
                    angle = int(values[0])

                if len(values) >= 2:
                    speed = int(values[1])

                if len(values) >= 3:
                    angular = int(values[2])
            except ValueError:
                print("Failed to parse input:", repr(values))
        self.actuators.drive(speed, angle, angular)

    def set_autonomous(self, params=None):
        self.logger.debug("Enabling autonomous mode")
        self.leona.autonomous = True
        self.actuators.stop()

    def set_manual(self, params=None):
        self.logger.debug("Enabling manual mode")
        self.leona.autonomous = False
        self.actuators.stop()

    def my_exit(self, params):
        self.exit()

    def my_stop(self, params):
        self.actuators.stop()

    def start_new_video(self, params):
        if not self.capture.is_recording:
            matches = re.findall(self.video_num_counter_regex, self.capture.file_name)
            if len(matches) == 0:
                name_matches = re.findall(self.video_name_regex, self.capture.file_name)
                file_name_no_ext, extension = name_matches[0]
                new_file_name = "%s-1.%s" % (file_name_no_ext, extension)
            else:
                file_name_no_ext, counter, extension = matches[0]
                counter = int(counter) + 1
                new_file_name = "%s-%s.%s" % (file_name_no_ext, counter, extension)

            self.capture.start_recording(new_file_name, self.capture.directory)
        else:
            print("PiCamera already recording")

    def stop_recording(self, params):
        if self.capture.is_recording:
            self.capture.stop_recording()
        else:
            print("PiCamera already stopped recording")

    def check_commands(self, line, **commands):
        function = None
        current_command = ""
        for command, fn in commands.items():
            if line.startswith(command) and len(command) > len(current_command):
                function = fn
                current_command = command
        if function is not None:
            function(line[len(current_command):].strip(" "))

    def handle_input(self, line):
        if type(line) == str:
            self.check_commands(
                line,
                q=self.my_exit,
                l=self.spin_left,
                r=self.spin_right,
                d=self.drive,
                s=self.my_stop,
                start_video=self.start_new_video,
                stop_video=self.stop_recording,
                manual=self.set_manual,
                auton=self.set_autonomous
            )

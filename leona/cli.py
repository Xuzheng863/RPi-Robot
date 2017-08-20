from atlasbuggy.cmdline import CommandLine


class CMDline(CommandLine):
    def __init__(self, enabled=True):
        super(CMDline, self).__init__(enabled)
        self.leona = None
        self.actuators = None

    def take(self):
        self.leona = self.streams["robot"]
        self.actuators = self.leona.actuators

    def spin_left(self, params):
        value = int(params) if len(params) > 0 else 75
        self.actuators.spin(value)

    def spin_right(self, params):
        value = int(params) if len(params) > 0 else 75
        self.actuators.spin(-value)

    def drive(self, params):
        angle = 0
        speed = 75
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

    def my_exit(self, params):
        self.exit_all()

    def my_stop(self, params):
        self.actuators.stop()

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
            )

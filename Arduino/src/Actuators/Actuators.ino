/*
This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM
control
p0
For use with the Adafruit Motor Shield v2
---->	http://www.adafruit.com/products/1438

This sketch creates a fun motor party on your desk *whiirrr*
Connect a unipolar/bipolar stepper to M3/M4
Connect a DC motor to M1
Connect a hobby servo to SERVO1
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Atlasbuggy.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

Atlasbuggy robot("actuators");

struct MotorStruct {
    Adafruit_DCMotor* af_motor;
    int speed;
    int goal_speed;
    byte run_state;
};

MotorStruct init_motor(int motor_num) {
    MotorStruct new_motor;
    new_motor.af_motor = AFMS.getMotor(motor_num);
    new_motor.speed = 0;
    new_motor.goal_speed = 0;
    return new_motor;
}

#define NUM_MOTORS 4
#define TOPLEFT_OFFSET 5
#define BOTLEFT_OFFSET 5
#define TOPRIGHT_OFFSET 0
#define BOTRIGHT_OFFSET 0

int speed_increment = 10;
int speed_delay = 1;
MotorStruct* motors = new MotorStruct[NUM_MOTORS];

bool attached = false;
bool goal_available = false;

uint32_t ping_timer = millis();

void setup() {
    robot.begin();
    AFMS.begin();

    for (int motor_num = 1; motor_num <= NUM_MOTORS; motor_num++) {
        motors[motor_num - 1] = init_motor(motor_num);
    }

    String speedIncreStr = String(speed_increment);
    String speedDelayStr = String(speed_delay);

    robot.setInitData(
        speedIncreStr + "\t" +
        speedDelayStr
    );
}

void set_motor_speed(int motor_num)
{
    if (motors[motor_num].speed > 0) {
        motors[motor_num].af_motor->run(FORWARD);
    }
    else if (motors[motor_num].speed == 0) {
        motors[motor_num].af_motor->run(BRAKE);
    }
    else {
        motors[motor_num].af_motor->run(BACKWARD);
    }
    motors[motor_num].af_motor->setSpeed(abs(motors[motor_num].speed));
}

void set_motor_goal(int motor_num, int speed, int offset) {
    motors[motor_num].goal_speed = speed;
    if (abs(motors[motor_num].goal_speed) > offset) {
        if (motors[motor_num].goal_speed > 0) {
            motors[motor_num].goal_speed -= offset;

            if (motors[motor_num].goal_speed < 0) {
                motors[motor_num].goal_speed = 0;
            }
            if (motors[motor_num].goal_speed > 255) {
                motors[motor_num].goal_speed = 255;
            }
        }
        else {
            motors[motor_num].goal_speed += offset;
            if (motors[motor_num].goal_speed > 0) {
                motors[motor_num].goal_speed = 0;
            }
            if (motors[motor_num].goal_speed < -255) {
                motors[motor_num].goal_speed = -255;
            }
        }
    }
}

// top left, top right, bottom left, bottom right
void set_motor_goals(int speed2, int speed3, int speed1, int speed4)
{
    set_motor_goal(0, speed1, BOTLEFT_OFFSET);  // top left
    set_motor_goal(1, speed2, TOPLEFT_OFFSET);  // top right
    set_motor_goal(2, speed3, TOPRIGHT_OFFSET);  // bottom left
    set_motor_goal(3, speed4, BOTRIGHT_OFFSET);  // bottom right
}

void drive(int angle, int speed, int angular)
{
    angle %= 360;

    if (0 <= angle && angle < 90) {
        int fraction_speed = -2 * speed / 90 * angle + speed;
        set_motor_goals(speed + angular, fraction_speed - angular, fraction_speed + angular, speed - angular);
    }
    else if (90 <= angle && angle < 180) {
        int fraction_speed = -2 * speed / 90 * (angle - 90) + speed;
        set_motor_goals(fraction_speed + angular, -speed - angular, -speed + angular, fraction_speed - angular);
    }
    else if (180 <= angle && angle < 270) {
        int fraction_speed = 2 * speed / 90 * (angle - 180) - speed;
        set_motor_goals(-speed + angular, fraction_speed - angular, fraction_speed + angular, -speed - angular);
    }
    else if (270 <= angle && angle < 360) {
        int fraction_speed = 2 * speed / 90 * (angle - 270) - speed;
        set_motor_goals(fraction_speed + angular, speed - angular, speed + angular, fraction_speed - angular);
    }
}

void ping() {
    ping_timer = millis();
}

void spin(int speed) {
    set_motor_goals(speed, -speed, speed, -speed);
}

void stop_motors() {
    set_motor_goals(0, 0, 0, 0);
}

void release_motors()
{
    for (int motor_num = 0; motor_num < NUM_MOTORS; motor_num++)
    {
        motors[motor_num].goal_speed = 0;
        motors[motor_num].speed = 0;
        motors[motor_num].af_motor->run(RELEASE);
    }
}

void update_motors()
{
    for (int motor_num = 0; motor_num < NUM_MOTORS; motor_num++)
    {
        set_motor_speed(motor_num);

        if (motors[motor_num].speed < motors[motor_num].goal_speed) {
            motors[motor_num].speed += speed_increment;
        }
        else {
            motors[motor_num].speed -= speed_increment;
        }

        if (abs(motors[motor_num].speed - motors[motor_num].goal_speed) < 2 * speed_increment) {
            motors[motor_num].speed = motors[motor_num].goal_speed;
        }
    }
    delay(speed_delay);
}

void loop()
{
    while (robot.available())
    {
        int status = robot.readSerial();
        if (status == 0) {  // user command
            String command = robot.getCommand();
            if (command.charAt(0) == 'p') {  // drive command
                int angle = 360 - command.substring(2, 5).toInt();
                int speed = command.substring(5, 8).toInt();
                int angular = command.substring(8, 11).toInt();
                if (command.charAt(1) == '1') {
                    speed *= -1;
                }
                else if (command.charAt(1) == '2') {
                    angular *= -1;
                }
                else if (command.charAt(1) == '3') {
                    speed *= -1;
                    angular *= -1;
                }
                Serial.print("run");
                drive(angle, speed, angular * 2);
                ping();
            }
            else if (command.charAt(0) == 'r') {  // spin command
                int speed = command.substring(2, 5).toInt();
                if (command.charAt(1) == '1') {
                    speed *= -1;
                }
                spin(speed);
                ping();
            }

            else if (command.charAt(0) == 'h') {  // stop command
                stop_motors();
            }
            else if (command.charAt(0) == 'r') {  // release command
                release_motors();
            }
        }
        else if (status == 1) {  // stop event
            stop_motors();
            release_motors();
        }
        else if (status == 2) {  // start event
            stop_motors();
        }
    }

    if (!robot.isPaused()) {
        update_motors();
        if (ping_timer > millis())  ping_timer = millis();
        if ((millis() - ping_timer) > 750) {
            stop_motors();
            ping_timer = millis();
        }
    }
}

import argparse
from leona.camera import RPiCam
from leona.cli import CMDline
from leona.pipeline import Pipeline
from leona import Leona

# from atlasbuggy.cameras.picamera.pivideo import PiVideoRecorder as Recorder
# from atlasbuggy.cameras.cvcamera.cvvideo import CvVideoRecorder as Recorder
from atlasbuggy.robot import Robot

parser = argparse.ArgumentParser()
parser.add_argument("-pipe", "--pipeline", help="enable pipeline", action="store_true")
args = parser.parse_args()

log = args.log

robot = Robot(write=log)

camera = RPiCam()
leona = Leona()
pipeline = Pipeline(args.pipeline)
cmdline = CMDline()

camera.give()
pipeline.give(actuators=leona.actuators, capture=camera)
cmdline.give(leona=leona)

robot.run(camera, leona, pipeline, cmdline)

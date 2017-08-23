import matplotlib
matplotlib.use('Agg')

import argparse

from atlasbuggy import Robot
from atlasbuggy.subscriptions import *

from leona import Leona
from leona.picamera import PiCamera
from leona.cli import CMDline
from leona.pipeline import LeonaPipeline
# from naboris.inception.pipeline import InceptionPipeline

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", help="disable logging", action="store_false")
parser.add_argument("-d", "--debug", help="enable debug prints", action="store_true")
args = parser.parse_args()

log = args.log

robot = Robot(write=log)

video_file_name = robot.log_info["file_name"].replace(";", "_")[:-3] + "mp4"
video_directory = "videos/" + robot.log_info["directory"].split("/")[-1]

camera = PiCamera(file_name=video_file_name, directory=video_directory)
leona = Leona()
pipeline = LeonaPipeline(enabled=True)
cmdline = CMDline()

leona.subscribe(Feed(leona.pipeline_tag, pipeline, leona.results_service_tag))

cmdline.subscribe(Subscription(cmdline.leona_tag, leona))
cmdline.subscribe(Subscription(cmdline.capture_tag, camera))
pipeline.subscribe(Update(pipeline.capture_tag, camera))

robot.run(camera, leona, pipeline, cmdline)

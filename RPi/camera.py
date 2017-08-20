from atlasbuggy.cameras.picamera import PiCamera


class RPiCam(PiCamera):
    def __init__(self, enabled=True):
        super(RPiCam, self).__init__(enabled)

    def init_cam(self, cam):
        cam.resolution = (cam.resolution[0] // 2, cam.resolution[1] // 2)
        cam.framerate = 30
        cam.hflip = True
        cam.vflip = True

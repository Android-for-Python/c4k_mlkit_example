from kivy.clock import mainthread
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from camera4kivy import Preview
from jnius import PythonJavaClass, java_method, autoclass

ImageProxy = autoclass('androidx.camera.core.ImageProxy')
InputImage = autoclass('com.google.mlkit.vision.common.InputImage')
FaceContour = autoclass('com.google.mlkit.vision.face.FaceContour')
FaceDetector = autoclass('com.google.mlkit.vision.face.FaceDetector')
FaceDetection = autoclass('com.google.mlkit.vision.face.FaceDetection')
FaceDetectorOptions =\
    autoclass('com.google.mlkit.vision.face.FaceDetectorOptions')
FaceDetectorOptionsBuilder =\
    autoclass('com.google.mlkit.vision.face.FaceDetectorOptions$Builder')

FailureListener = autoclass('org.kivy.mlkit.FailureListener')
SuccessListenerFace = autoclass('org.kivy.mlkit.SuccessListenerFace')
CompleteListener = autoclass('org.kivy.mlkit.CompleteListener')
CallbackWrapper = autoclass('org.kivy.mlkit.CallbackWrapper')


class CallbackWrapper(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ['org/kivy/mlkit/CallbackWrapper']

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method('(Ljava/util/List;)V')        
    def callback_faces_list(self, faces):
        if self.callback:
            self.callback(faces)
        
    @java_method('(Ljava/lang/String;)V')        
    def callback_string(self, e):
        if self.callback:
            self.callback(e)
        
class FaceDetect(Preview):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contours = []
        self.fdob = FaceDetectorOptionsBuilder()
        self.fdob.setContourMode(FaceDetectorOptions.CONTOUR_MODE_ALL)
        self.fdo = self.fdob.build()
        self.detector = FaceDetection.getClient(self.fdo)  ##init????
        self.success_wrapper = CallbackWrapper(self.got_result)
        self.failure_wrapper = CallbackWrapper(self.report_failure)
        self.complete_wrapper = CallbackWrapper(self.completed)
        self.success = SuccessListenerFace(self.success_wrapper)
        self.failure = FailureListener(self.failure_wrapper)
        self.complete = CompleteListener(self.complete_wrapper)


    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################        

    def analyze_imageproxy_callback(self, image_proxy, image_pos, image_scale,
                                    mirror, degrees):
        self.image_proxy = image_proxy
        self.image_scale = image_scale # scale image to screen
        self.mirror = mirror
        self.image_pos = image_pos
        if degrees in [0, 180]:
            self.image_size = [image_proxy.getWidth(), image_proxy.getHeight()]
        else:
            self.image_size = [image_proxy.getHeight(), image_proxy.getWidth()]

        mediaImage = image_proxy.getImage()
        if mediaImage:
            try:
                self.image = InputImage.fromMediaImage(mediaImage, degrees)
                self.task = self.detector.process(self.image)
                self.task.addOnSuccessListener(self.success)
                self.task.addOnFailureListener(self.failure)
                self.task.addOnCompleteListener(self.complete)
            except Exception as e:
                print('ImageProxy error: ' + str(e))
        else:
            self.completed("")

    def completed(self, e):
        self.image_proxy.close()

    def report_failure(self,e):
        pass

    def got_result(self, faces):
        analyze_contours = []
        for face in faces:
            for fc in [FaceContour.FACE, # FACE is first, see below
                       FaceContour.LEFT_EYE,
                       FaceContour.RIGHT_EYE,
                       FaceContour.LEFT_EYEBROW_BOTTOM,
                       FaceContour.LEFT_EYEBROW_TOP, 
                       FaceContour.RIGHT_EYEBROW_BOTTOM,
                       FaceContour.RIGHT_EYEBROW_TOP,
                       FaceContour.LOWER_LIP_BOTTOM,
                       FaceContour.LOWER_LIP_TOP,
                       FaceContour.UPPER_LIP_BOTTOM,
                       FaceContour.UPPER_LIP_TOP,
                       FaceContour.NOSE_BRIDGE,
                       FaceContour.NOSE_BOTTOM]:
                analyze_contours.append(face.getContour(fc).getPoints())

        screen_contours = []
        for contour in analyze_contours:
            sc = [] 
            for c in contour:
                # Map MLKit coordinates to Kivy screen coordinates
                y = self.image_size[1] - c.y 
                if self.mirror:
                    x = self.image_size[0] -c.x 
                else:
                    x = c.x
                # Map MKKit analysis coordinates to Preview screen coordinates
                # Preview coordinates include the letterbox size given by tpos
                sc.append(round(x * self.image_scale + self.image_pos[0]))
                sc.append(round(y * self.image_scale + self.image_pos[1]))
            screen_contours.append(list(sc))
        self.make_thread_safe(list(screen_contours)) 

    @mainthread
    def make_thread_safe(self, contours):
        self.contours = contours

    ################################
    # Canvas Update  - on UI Thread
    ################################
        
    def canvas_instructions_callback(self, texture, size, pos):
        # Add the preview image 
        Color(1,1,1,1)
        Rectangle(texture= texture, size = size, pos = pos)
        # Add the analysis annotations
        Color(1,0,0,1)
        face = True # FACE is first in the list above, and is a closed line
        for contour in self.contours:
            Line(points = contour, width = dp(1), close = face)
            face = False










import jetson.inference
import jetson.utils
import cv2
import numpy as np

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
# camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
camera = jetson.utils.videoSource("/dev/video0", ["--input-width=640","--input-height=320"])
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	img = jetson.utils.cudaToNumpy(img, 640, 320, 4)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB).astype(np.uint8)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	if len(detections) > 0:	
		cx, cy = detections[0].Center
		cx = int(cx)
		cy = int(cy)	
		img = cv2.circle(img,(cx, cy), 10, (0, 255, 0), -1, cv2.LINE_AA)
	cv2.imshow("Detection",img)
	if cv2.waitKey(1) & 0xFF == ord('c'):
		break
	#display.Render(img)
	#display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

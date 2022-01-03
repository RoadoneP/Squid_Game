import jetson.inference
import jetson.utils
import cv2
import numpy as np

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
# camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
camera = jetson.utils.videoSource("/dev/video0", ["--input-width=640","--input-height=320"])
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
sub = cv2.createBackgroundSubtractorKNN(history=1, dist2Threshold=500, detectShadows=False)

while display.IsStreaming():
	img = camera.Capture()
	frame = camera.Capture()
	detections = net.Detect(img)
	img = jetson.utils.cudaToNumpy(img, 640, 320, 4)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB).astype(np.uint8)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

	frame = jetson.utils.cudaToNumpy(frame, 640, 320, 4)
	frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB).astype(np.uint8)
	frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
	# bounding box complete
	mask = sub.apply(frame)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	if len(detections) > 0:
		xidx = [int(detections[0].Left),int(detections[0].Right)]
		yidx = [int(detections[0].Top),int(detections[0].Bottom)]
		cx, cy = detections[0].Center
		bbox = np.zeros_like(img)
		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
		bbox[yidx[0]+1:yidx[1]-1,xidx[0]+1:xidx[1]-1] = mask[yidx[0]+1:yidx[1]-1,xidx[0]+1:xidx[1]-1]		
		cx = int(cx)
		cy = int(cy)	
		img = cv2.circle(img,(cx, cy), 10, (0, 255, 0), -1, cv2.LINE_AA)
	cv2.imshow("Detection",img)
	cv2.imshow("mask", bbox)
	if cv2.waitKey(1) & 0xFF == ord('c'):
		break
	#display.Render(img)
	#display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

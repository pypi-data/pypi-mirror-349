import cv2
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput
import io
import socketserver
from http import server
from threading import Condition, Thread
import time

class Camera:
    FOCAL_LENGTH_PX = 548.8
    REAL_HEIGHT_CM_OBSTACLE = 3.7
    REAL_HEIGHT_CM_ARUCO = 10.0  # <-- ArUco marker real height in cm
    HORIZONTAL_FOV = 48.4
    DISTANCE_CALIBRATION_FACTOR = 2.01
    ANGLE_CALIBRATION_FACTOR = 1
    MIN_AREA_THRESHOLD = 2500

    lower_blue = np.array([10, 130, 10])
    upper_blue = np.array([20, 255, 255])
    lower_red = np.array([100, 100, 50])
    upper_red = np.array([130, 255, 255])

    PAGE_TEMPLATE = """
        <html>
        <head><title>Picamera2 MJPEG Streaming</title></head>
        <body>
        <h1>Camera Feed</h1>
        <div style="display: flex;">
            <img src="stream.mjpg" width="640" height="480" />
            <pre id="info" style="padding-left: 20px; font-size: 16px;"></pre>
        </div>
        <script>
        async function fetchInfo() {
            const res = await fetch('/info');
            const data = await res.text();
            document.getElementById('info').textContent = data;
            setTimeout(fetchInfo, 1000);
        }
        fetchInfo();
        </script>
        </body>
        </html>
        """

    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}))
        self.picam2.start()
        self.output = self.StreamingOutput(self.picam2)
        self.streaming_server = None
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()

    class StreamingOutput(io.BufferedIOBase):
        def __init__(self, picam2):
            self.picam2 = picam2
            self.frame = None
            self.condition = Condition()

        def write(self, buf):
            frame = self.picam2.capture_array()
            if frame is not None:
                _, jpeg = cv2.imencode('.jpg', frame)
                buf = jpeg.tobytes()
            with self.condition:
                self.frame = buf
                self.condition.notify_all()

    def annotate_frame(self, frame, objects):
        for obj in objects:
            if 'distance' in obj and isinstance(obj['distance'], (float, int)):
                text = f"{obj['id']} ({obj.get('type', '-')}) | {obj['distance']:.1f} cm"
            else:
                text = f"{obj['id']} ({obj.get('type', '-')}) | {obj['distance']}"

            left_angle = obj.get('left_angle', 0)
            right_angle = obj.get('right_angle', 0)

            # Estimate center and width of object in image
            width = self.picam2.camera_config()['main']['size'][0]
            pixel_per_degree = width / self.HORIZONTAL_FOV
            center_x = int((left_angle + right_angle) / 2 * pixel_per_degree + width / 2)
            box_width = int(abs(right_angle - left_angle) * pixel_per_degree)
            x1 = max(center_x - box_width // 2, 0)
            y1 = 100
            x2 = min(center_x + box_width // 2, width)
            y2 = 300
            color = (255, 0, 0) if obj.get('type') == 'front' else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return frame

    class StreamingHandler(server.BaseHTTPRequestHandler):
        def do_GET(self):
            cam = self.server.camera_ref
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = cam.PAGE_TEMPLATE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/info':
                objects = cam.get_objects()
                text = '\n'.join(str(obj) for obj in objects)
                content = text.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        frame = cam.get_camera_frame()
                        objects = cam.get_objects()
                        frame = cam.annotate_frame(frame, objects)
                        _, jpeg = cv2.imencode('.jpg', frame)
                        buf = jpeg.tobytes()

                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(buf))
                        self.end_headers()
                        self.wfile.write(buf)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    print(f"Streaming client removed: {e}")
            else:
                self.send_error(404)
                self.end_headers()
                
        def do_GET(self):
            cam = self.server.camera_ref
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = cam.PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with cam.output.condition:
                            cam.output.condition.wait()
                            frame = cam.output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    print(f"Streaming client removed: {e}")
            else:
                self.send_error(404)
                self.end_headers()

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    def get_camera_frame(self):
        return self.picam2.capture_array()

    def get_objects(self):
        frame = self.get_camera_frame()
        height, width = frame.shape[:2]
        center_x = width // 2

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        blue_mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        red_mask = cv2.inRange(hsv, self.lower_red, self.upper_red)
        combined_mask = red_mask | blue_mask
        combined_mask[:height // 3, :] = 0  # Ignore top part of the image

        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.dilate(combined_mask, kernel, iterations=1)
        combined_mask = cv2.erode(combined_mask, np.ones((3, 3), np.uint8), iterations=3)

        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects = []

        for contour in contours:
            if cv2.contourArea(contour) > self.MIN_AREA_THRESHOLD:
                x, y, w, h = cv2.boundingRect(contour)
                bottom_y = y + h

                if bottom_y >= height:
                    distance = "too close"
                else:
                    distance = (self.FOCAL_LENGTH_PX * self.REAL_HEIGHT_CM_OBSTACLE / h) * self.DISTANCE_CALIBRATION_FACTOR

                # Determine type based on which mask dominates
                roi_red = red_mask[y:y+h, x:x+w]
                red_pixels = cv2.countNonZero(roi_red)
                roi_blue = blue_mask[y:y+h, x:x+w]
                blue_pixels = cv2.countNonZero(roi_blue)

                obj_type = "back" if red_pixels > blue_pixels else "front"

                left_offset = x - center_x
                right_offset = (x + w) - center_x
                pixel_per_degree = width / self.HORIZONTAL_FOV
                left_angle = (left_offset / pixel_per_degree) * self.ANGLE_CALIBRATION_FACTOR
                right_angle = (right_offset / pixel_per_degree) * self.ANGLE_CALIBRATION_FACTOR

                objects.append({
                    "id": "obstacle",
                    "type": obj_type, # "back" for red plate or "front" for blue plate
                    "distance": distance,
                    "left_angle": round(left_angle, 2),
                    "right_angle": round(right_angle, 2)
                })

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)
        if ids is not None:
            for marker_corners in corners:
                x, y, w, h = cv2.boundingRect(marker_corners[0])
                distance = (self.FOCAL_LENGTH_PX * self.REAL_HEIGHT_CM_ARUCO / h) * self.DISTANCE_CALIBRATION_FACTOR
                left_offset = x - center_x
                right_offset = (x + w) - center_x
                pixel_per_degree = width / self.HORIZONTAL_FOV
                left_angle = (left_offset / pixel_per_degree) * self.ANGLE_CALIBRATION_FACTOR
                right_angle = (right_offset / pixel_per_degree) * self.ANGLE_CALIBRATION_FACTOR
                objects.append({
                    "id": "target",
                    "distance": round(distance, 2),
                    "left_angle": round(left_angle, 2),
                    "right_angle": round(right_angle, 2)
                })

        return objects

    def get_object_from_id(self, target_id):
        return [obj for obj in self.get_objects() if obj['id'] == target_id]

    def get_closest_object(self):
        objects = self.get_objects()
        return min(objects, key=lambda o: float('inf') if o['distance'] == "too close" else o['distance']) if objects else None

    def broadcast_camera_feed(self, on=True, port=8080):
        if on:
            address = ('', port)
            self.streaming_server = self.StreamingServer(address, self.StreamingHandler)
            self.streaming_server.camera_ref = self
            Thread(target=self.streaming_server.serve_forever, daemon=True).start()
            self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        else:
            if self.streaming_server:
                self.streaming_server.shutdown()
                self.streaming_server = None
            self.picam2.stop_recording()

    def take_picture(self, file_path):
        frame = self.get_camera_frame()
        cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def record_video(self, duration_sec, file_path):
        encoder = H264Encoder()
        self.picam2.start_recording(encoder, FileOutput(file_path))
        time.sleep(duration_sec)
        self.picam2.stop_recording()
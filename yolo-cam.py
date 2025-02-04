import cv2
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.datasets import letterbox


GST_PIPELINE = "qtiqmmfsrc name=qmmf ! video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = attempt_load("yolov7.pt", map_location=device)  # Ensure you have the correct model path
model.eval()


cap = cv2.VideoCapture(GST_PIPELINE, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    
    img = letterbox(frame, new_shape=640)[0]  # Resize with padding
    img = img[:, :, ::-1].transpose(2, 0, 1)  # Convert BGR to RGB and transpose
    img = torch.from_numpy(img).float().to(device) / 255.0  # Normalize
    img = img.unsqueeze(0) if img.ndimension() == 3 else img  # Add batch dimension

    
    with torch.no_grad():
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)  # Apply NMS

    
    for det in pred:
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
            for *xyxy, conf, cls in det:
                label = f"{conf:.2f}"
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    
    cv2.imshow("YOLOv7 Camera", frame)    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

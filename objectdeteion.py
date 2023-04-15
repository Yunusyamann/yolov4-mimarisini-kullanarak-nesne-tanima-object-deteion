import cv2
import numpy as np
import time

# eğitimden sonra indirdiğimiz dosyaları burada tanımlıyoruz.
net = cv2.dnn.readNet("yenideneme.weights", "yeni.cfg")


cap = cv2.VideoCapture(0)

# FPS sayacı
fps_start_time = None
fps_counter = 0

while True:
    _, img = cap.read()
    height, width, channels = img.shape

  
    input_blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), swapRB=True, crop=False)

    
    net.setInput(input_blob)
    layer_outputs = net.forward(net.getUnconnectedOutLayersNames())

    bitki_confidences = []
    bitki_boxes = []

    
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                bitki_boxes.append([x, y, w, h])
                bitki_confidences.append(float(confidence))

    
    if len(bitki_boxes) > 0:
        max_bitki_index = np.argmax(bitki_confidences)
        bitki_box = bitki_boxes[max_bitki_index]
        x, y, w, h = bitki_box
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
        print("1")
        
    else:
        print("0")
       

  
    if fps_start_time is None:
        fps_start_time = time.time()
    else:
        fps_counter += 1
        elapsed_time = time.time() - fps_start_time
        if elapsed_time > 1:
            fps = fps_counter / elapsed_time
            print("FPS: {:.2f}".format(fps))
            fps_start_time = None
            fps_counter = 0

   
    cv2.imshow("Bitki Tespiti", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

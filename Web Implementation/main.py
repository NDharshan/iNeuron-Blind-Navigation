# sri
from flask import Flask, render_template, request
# import yolo_opencv
app = Flask(__name__)

@app.route('/dist')
def distance_det():
    import cv2
    import os, winsound
    import winsound

    # variables
    # distance from camera to object(face) measured
    KNOWN_DISTANCE = 76.2  # centimeter
    # width of face in the real world or Object Plane
    KNOWN_WIDTH = 14.3  # centimeter
    # Colors
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    WHITE = (255, 255, 255)
    fonts = cv2.FONT_HERSHEY_COMPLEX
    cap = cv2.VideoCapture(0)

    # face detector object
    # cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
    # face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_detector = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))

    # focal length finder function
    def focal_length(measured_distance, real_width, width_in_rf_image):

        focal_length_value = (width_in_rf_image * measured_distance) / real_width
        return focal_length_value

    # distance estimation function
    def distance_finder(focal_length, real_face_width, face_width_in_frame):
        distance = (real_face_width * focal_length) / face_width_in_frame
        return distance

    # face detector function
    def face_data(image):

        face_width = 0
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
        for (x, y, h, w) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
            face_width = w

        return face_width

    # reading reference image from directory
    ref_image = cv2.imread("person distance\\ref.jpg")

    ref_image_face_width = face_data(ref_image)
    focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)
    print(focal_length_found)
    # cv2.imshow("ref_image", ref_image)

    while True:
        _, frame = cap.read()

        # calling face_data function
        face_width_in_frame = face_data(frame)
        # finding the distance by calling function Distance
        if face_width_in_frame != 0:
            Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
            # Drwaing Text on the screen
            # if Distance < 100:
            #     winsound.Beep(500,1000)

            cv2.putText(
                frame, f"Distance = {round(Distance, 2)} CM", (50, 50), fonts, 1, (WHITE), 2
            )
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/yolo')
def yolo_full():
    import cv2
    import argparse
    import numpy as np

    def get_output_layers(net):

        layer_names = net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        except:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    image = cv2.imread('object classification\\ref.jpg')

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open('object classification\yolov3.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet('object classification\yolov3.weights', 'object classification\yolov3.cfg')

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]

        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

    cv2.imshow("object detection", image)
    cv2.waitKey()

    # cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()
    college_photo = "static/Global college.jpg"
    return render_template('landingpage.html', college_photo=college_photo)

@app.route('/cab')
def cab():
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    def book_a_cab():
        chrome_options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 1,
                 "profile.default_content_setting_values.geolocation": 1}

        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://book.olacabs.com/?pickup_name=Current%20Location&lat=13.0540663&lng=77.7614751")
        time.sleep(2)

        # location_button=driver.find_element('xpath','/html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button')
        # location_button=driver.find_element(By.XPATH, "/html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button")
        # location_button=driver.find_elements("xpath","//*[contains(text(), 'Continue to next step')]")
        # print(location_button[0].text())
        # locatoin_button[0].click()
        # /html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button

        # element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "/div/div/div[3]"))
        #     )
        # drop_location=driver.find_element('xpath','/div/div/div[3]')
        # time.sleep(5)
        driver.quit()
        # /div/div/div[3]
        # driver.quit()
        college_photo = "static/Global college.jpg"
        return render_template('landingpage.html', college_photo=college_photo)

    college_photo = "static/Global college.jpg"
    return render_template('landingpage.html', college_photo=college_photo)

@app.route('/')
def hello_world():
    college_photo = "static/Global college.jpg"
    return render_template('landingpage.html', college_photo=college_photo)


app.run(debug=True, host='0.0.0.0')

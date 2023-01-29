# sri
from flask import Flask, render_template, request

app = Flask(__name__)

def object_classification():
    import cv2
    import argparse
    import numpy as np

    from yolo_opencv import classes, COLORS

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

    def call_me(frame):
        image = frame

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        classes = None

        with open(args.classes, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

        net = cv2.dnn.readNet(args.weights, args.config)

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
        cv2.imwrite("object-detection.jpg", image)
        # cv2.destroyAllWindows()

    # define a video capture object
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        call_me(frame)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


@app.route('/')
def hello_world():
    college_photo = "static/Global college.jpg"
    return render_template('landingpage.html', college_photo=college_photo)


@app.route("/call_to_run")
def delete_student():
    college_photo = "static/Global college.jpg"
    object_classification()
    return render_template('landingpage.html', college_photo=college_photo)

"""
@app.route("/saverecord", methods=["POST", "GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            # all attributes
            name = request.form.get("name")
            gender = request.form.get("gender")
            email = request.form.get("email")
            usn = request.form.get("usn")
            phone = request.form.get("phone")
            branch = request.form.get("branch")
            semester = request.form.get("semester")
            floor_number = request.form.get("floor_number")
            room_number = request.form.get("room_number")
            city = request.form.get("city")

            # creating connection
            connection = mysql.connector.connect(
                host="localhost", user="root",
                password="", database="hayavadana")
            # cursor object
            cursor = connection.cursor()

            # inserting values
            room_id = "GH-" + str(floor_number) + str(room_number)
            queries = [
                f'INSERT INTO College_details(USN, branch, semester) values ("{usn}", "{branch}", "{semester}")',
                f'INSERT INTO Personal_details(USN, name, city) values ("{usn}", "{name}", "{city}")',
                f'INSERT INTO Room(room_id, floor_no, room_no) values ("{usn}", "{floor_number}", "{room_number}")'
            ]
            for query in queries:
                cursor.execute(query)
            connection.commit()
            msg = "Student details successfully Added"
        except:
            connection.rollback()
            msg = "We can not add Student details to the database"
        finally:
            return render_template("success_record.html", msg=msg)
            connection.close()


@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")


@app.route("/student_info")
def student_info():
    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object

    cursor = connection.cursor()
    cursor.execute("select usn, name, floor_no, room_no from Personal_details p, Room r where r.room_id=p.usn")
    rows = list(cursor.fetchall())
    # cursor.execute("select usn, name from Personal_details")
    # row1 = list(cursor.fetchall())
    # cursor.execute("select floor_no, room_no from Room")
    # row2 = cursor.fetchall()
    # rows = list_merge(row1, row2)
    print(rows)
    cursor.close()
    connection.close()
    return render_template("student_info.html", rows=rows)


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    usn = request.form["usn"]
    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object
    cursor = connection.cursor()
    cursor.execute(f"select * from college_details where usn = ('{usn}')")
    rows = cursor.fetchall()
    print(rows)
    if not rows == []:
        cursor.execute(f"DELETE FROM `college_details` WHERE `USN` = ('{usn}')")
        cursor.close()
        connection.commit()
        connection.close()
        msg = "Student detail successfully deleted"
        return render_template("delete_record.html", msg=msg)
    else:
        msg = "Could not be deleted"
        cursor.close()
        connection.close()
        return render_template("delete_record.html", msg=msg)


@app.route("/log_in")
def log_entry():
    import cv2
    import datetime
    from pyzbar import pyzbar
    usn = ''
    log_time_in = ''
    log_time_out = ''

    def write_to_sql(usn, log_time_in):
        connection = mysql.connector.connect(
            host="localhost", user="root",
            password="", database="hayavadana")
        # cursor object
        cursor = connection.cursor()

        try:
            cursor.execute(f'select * from Log_details where usn = ("{usn}")')
            rows = cursor.fetchall()
            if rows == []:
                query = f'INSERT INTO Log_details(USN, log_time_in) values ("{usn}", "{log_time_in}")'
                cursor.execute(query)
            else:
                print("Not unique")
                connection.commit()
        except mysql.connector.IntegrityError as err:
            print("Entry already exists")
        finally:
            connection.commit()
            connection.close()

    def read_barcodes(frame):

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect  # 1
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)  # 3
            log_time_in = str(datetime.datetime.now())

            print(barcode_info)
            write_to_sql(barcode_info.strip(), log_time_in)
            # with open("barcode_result.txt", mode='w') as file:
            #     log_time_in = str(datetime.datetime.now())
            #     file.write("Recognized Barcode:" + barcode_info)
            #     usn = (barcode_info)
        return frame

    # define a video capture object
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame = read_barcodes(frame)
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object

    cursor = connection.cursor()
    cursor.execute("select usn, log_time_in, log_time_out from log_details")
    rows = list(cursor.fetchall())
    cursor.close()
    connection.close()
    return render_template("log_view.html", rows=rows)


@app.route("/log_out")
def log_entry_out():
    import mysql.connector
    import cv2
    import datetime
    from pyzbar import pyzbar

    def write_to_sql(usn, log_time_out):
        connection = mysql.connector.connect(
            host="localhost", user="root",
            password="", database="hayavadana")
        # cursor object
        cursor = connection.cursor()

        try:
            #             usn = usn[:9]
            cursor.execute(f'select * from Log_details where usn = "{usn}" ')
            rows = cursor.fetchall()
            #             check =
            print('Rows:', rows)
            if len(rows) != 0 and rows[0][-1] == None:
                query = f"UPDATE Log_details SET log_time_out = '{log_time_out}' WHERE usn = '{usn}'"
                #     query = f'INSERT INTO Log_details(log_time_out) values ("{log_time_out}" where usn = "1GA20CS085")'
                cursor.execute(query)
            else:
                print("Not Entered earlier")
                connection.commit()

        except mysql.connector.IntegrityError as err:
            print("Entry already exists")
        finally:
            connection.commit()

    def read_barcodes(frame):

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect  # 1
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)  # 3
            log_time_in = str(datetime.datetime.now())

            print(barcode_info)
            write_to_sql(barcode_info.strip(), log_time_in)
            # with open("barcode_result.txt", mode='w') as file:
            #     log_time_in = str(datetime.datetime.now())
            #     file.write("Recognized Barcode:" + barcode_info)
            #     usn = (barcode_info)
        return frame

    # define a video capture object
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame = read_barcodes(frame)
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="hayavadana")
    # cursor object

    cursor = connection.cursor()
    cursor.execute("select usn, log_time_in, log_time_out from log_details")
    rows = list(cursor.fetchall())
    cursor.close()
    connection.close()
    return render_template("log_view.html", rows=rows)


@app.route("/update")
def update():
    if request.method == "POST":
        try:
            # all attributes
            print("check -1")
            usn = request.form.get("usn")
            floor = request.form.get("floor")
            room = request.form.get("room")
            print(usn, floor, room)
            # creating connection
            connection = mysql.connector.connect(
                host="localhost", user="root",
                password="", database="hayavadana")
            # cursor object
            cursor = connection.cursor()
            # query = "select * from room"
            # cursor.execute(query)
            connection.commit()
            msg = "Student details successfully Updated"
        except:
            connection.rollback()
            msg = "We can not update Student details in the database"
        finally:
            return render_template("success_record.html", msg=msg)
            connection.close()
"""

app.run(debug=True)

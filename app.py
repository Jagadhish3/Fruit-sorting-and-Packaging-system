from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from flask import Response
import cv2
import mediapipe as mp
import time 



camera = cv2.VideoCapture(0)

app = Flask(__name__)

# Load your trained model
model = load_model('C:\\Users\\K.JAGADHISH\\Desktop\\CVbackup\\CVfinal\\fruit_predictor.h5')

# Define your fruit labels
class_labels = [
    'apple fruit', 'banana fruit', 'cherry fruit', 'chickoo fruit', 'grapes fruit',
    'kiwi fruit', 'mango fruit', 'orange fruit', 'strawberry fruit'
]

IMG_HEIGHT = 224  # As per model requirement
IMG_WIDTH = 224


@app.route('/')
def home():
    with open("C:\\Users\\K.JAGADHISH\\Desktop\\CVbackup\\CVfinal\\static\\stop_reason.txt", "w") as f:
        f.write("")
    return render_template('index.html')


@app.route('/camera')
def camera_page():
    return render_template('live.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected.'})

    if file:
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize

        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        result = class_labels[predicted_class]

        return jsonify({'prediction': result})

    return jsonify({'error': 'Prediction failed'})


def generate_frames():
    camera = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    threshold = 0.8
    stop_detecting = False
    stop_reason = ""
    last_prediction = "Detecting..."
    prob_display = ""

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                if thumb_tip.y < index_tip.y:
                    stop_reason = "Thumbs up detected. Closing the camera..."
                    cv2.putText(frame, stop_reason, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    stop_detecting = True
                    break

        img = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)[0]
        predicted_class = np.argmax(prediction)
        confidence = prediction[predicted_class]

        if confidence > threshold:
            last_prediction = class_labels[predicted_class]
            prob_display = f"{last_prediction} ({confidence*100:.2f}%)"
        else:
            prob_display = "Detecting..."

        cv2.putText(frame, prob_display, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        if stop_detecting:
            break

    camera.release()
    cv2.destroyAllWindows()

    with open("static/stop_reason.txt", "w") as f:
        f.write(stop_reason or "Camera Closed!")




@app.route('/stop-camera')
def stop_camera():
    global camera
    if camera.isOpened():
        camera.release()
        cv2.destroyAllWindows()
    return "Camera stopped"


@app.route('/live-detection')
def live_detection():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

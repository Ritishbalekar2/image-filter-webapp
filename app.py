import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"
PROCESSED_FOLDER = "static/processed/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# --- Helper function ---
def apply_filter(image_path, filter_type):
    img = cv2.imread(image_path)

    if filter_type == "gray":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    elif filter_type == "blur":
        result = cv2.GaussianBlur(img, (15, 15), 0)

    elif filter_type == "edge":
        result = cv2.Canny(img, 100, 200)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    elif filter_type == "sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        result = cv2.filter2D(img, -1, kernel)

    elif filter_type == "invert":
        result = cv2.bitwise_not(img)

    elif filter_type == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        result = cv2.transform(img, kernel)
        result = np.clip(result, 0, 255)

    else:
        result = img

    # Save to processed folder
    output_filename = f"{filter_type}_output.jpg"
    output_path = os.path.join(app.config["PROCESSED_FOLDER"], output_filename)
    cv2.imwrite(output_path, result)
    return output_filename  # return only filename


# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            return render_template("index.html", uploaded_image=filename)

    return render_template("index.html")


@app.route("/filter/<filter_type>/<filename>")
def filter_image(filter_type, filename):
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    processed_filename = apply_filter(image_path, filter_type)
    return render_template("index.html",
                           uploaded_image=filename,
                           processed_image=processed_filename,
                           filename=filename)


# NEW: Download processed image
@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config["PROCESSED_FOLDER"], filename)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template
from pymongo import MongoClient
from bson import ObjectId
import base64

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["image_db"]
collection = db["images"]

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files["image"]
        if image:
            image_data = image.read()
            image_id = collection.insert_one({"image_data": image_data}).inserted_id
            return f"Image uploaded successfully! <a href='/view/{image_id}'>View Image</a>"
    return render_template("upload.html")

@app.route("/view/<image_id>")
def view_image(image_id):
    image = collection.find_one({"_id": ObjectId(image_id)})
    if image:
        image_data = image["image_data"]
        image_url = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
        return render_template("view.html", image_url=image_url)
    else:
        return "Image not found"

@app.route("/view/all")
def view_all_images():
    images = collection.find()  # Retrieve all images from the collection
    image_data_list = []
    for image in images:
        image_data = image["image_data"]
        image_url = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
        image_data_list.append({"id": str(image["_id"]), "url": image_url})

    return render_template("view_all.html", image_data_list=image_data_list)

if __name__ == "__main__":
    app.run(debug=True)
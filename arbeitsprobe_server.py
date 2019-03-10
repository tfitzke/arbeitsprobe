#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import string
import json
from flask import Flask, redirect, jsonify, abort, url_for
from flask import request
from flask import send_from_directory
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import urllib.request
import sqlite3

# Initialisierung des Servers
app = Flask(__name__)
# Initialisierung der DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
db = SQLAlchemy(app)

# # SQL Table definition
from models import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Aktives Bild für ImageView
global activeImageName
activeImageName = None


def images_in_db():
    img_in_db = []
    for photo in db.session.query(Photo.photoPath).distinct():
        img_in_db.append(photo[0])
    return img_in_db


def tags_in_db():
    tag_in_db = []
    for tag in db.session.query(Tag.tagName).distinct():
        tag_in_db.append(tag[0])
    return tag_in_db


def getImageByName(imageName):
    image = db.session.query(Photo).filter(Photo.photoPath == imageName).one()
    return image


def getImageById(imageId):
    image = db.session.query(Photo).filter(Photo.photo_id == imageId).one()
    return image


def getTagByName(tagName):
    tag = db.session.query(Tag).filter(Tag.tagName == tagName).one()
    return tag


def tags_of_image(photoPath):
    print(photoPath)
    activeImage = getImageByName(photoPath)
    tmp_tags = activeImage.photoTags.all()
    active_tags = []
    for row in tmp_tags:
        active_tags.append(row.tagName)
    return active_tags


def images_of_tag(tagName):
    activeTag = db.session.query(Tag).filter(
        Tag.tagName == tagName).first()
    tmp_images = activeTag.taggedImages
    print(tmp_images)
    return tmp_images


# Redirect zu Gallerie
@app.route("/")
def index():
    return redirect("gallery", code=302)


@app.route("/upload", methods=['POST'])
def upload():
    # Images Ordner finden/ erstellen
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
        print("Ordner {} wurde erstellt".format(target))
        img_in_images = os.listdir('./images')
    else:
        print("Ordner {} existiert bereits".format(target))
        img_in_images = os.listdir('./images')
        # images aus Ordner in DB laden
        for upload in img_in_images:
            print("Existierende Images sind:" + upload)
            if upload not in images_in_db():
                print(upload + "wird zur DB hinzugefügt")
                db.session.add(Photo(upload))
        db.session.commit()

        # Redirect wenn ein leeres Form abgeschickt wird
    if not request.files.getlist("file"):
        print("No new files added")
        return redirect("gallery", code=302)
    else:
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            # iteriert durch ausgewählte Fotos und lädt den filename
            filename = upload.filename
            if filename not in img_in_images and filename:
                # Solange filename  nicht in Ordner Images ist,
                # wird Datei dort abgelegt.
                # Danach Abfrage, ob filename auch in DB ist
                img_in_images.append(filename)
                if filename not in images_in_db():
                    print("File: " + filename +
                          " wird zu Ordner und DB hinzugefuegt")
                    db.session.add(Photo(filename))
                else:
                    print("File: " + filename +
                          " wird nur zum Ordner hinzugefuegt, ist bereits in DB")
                destination = "/".join([target, filename])
                print(destination)
                upload.save(destination)
            else:
                print("File bereits im Ordner")
                if filename in images_in_db():
                    print("Und in der DB")
                else:
                    print("Und jetzt auch in der DB")
        db.session.commit()
        return redirect("gallery", code=302)


@app.route("/upload/<filename>")
def send_image(filename):
    return send_from_directory("images", filename)


@app.route("/gallery")
def gallery():
    image_names = []
    for photo in db.session.query(Photo):
        image_names.append(photo.photoPath)
    return render_template('gallery.html', image_names=image_names)


@app.route('/imageView')
@app.route("/imageView/<filename>", methods=['GET', 'POST'])
def imageView(filename=None):
    global activeImageName
    activeImage = None
    activeTags = []
    if activeImageName is None and filename is None:
        print("Exception: Kein aktives Bild ausgewählt")
        return redirect('gallery')
    else:
        if filename is None:
            filename = activeImageName
        else:
            activeImage = getImageByName(filename)
            activeImageName = filename
        activeTags = tags_of_image(activeImageName)

        prev_img = ""
        next_img = ""
        prev_img = prev_image(activeImage.photo_id)
        next_img = next_image(activeImage.photo_id)

        data_container = {
            'imageName': activeImageName,
            'imageTags': activeTags
        }
        return render_template('imageView.html', data_container=data_container, prev_img=prev_img, next_img=next_img)


def prev_image(photo_id):
    photo_id -= 1
    if (photo_id <= 0):
        photo_id = len(images_in_db())
        print("prev_image")
        print(photo_id)
    return getImageById(photo_id).photoPath


def next_image(photo_id):
    print("drin")
    print(photo_id)
    photo_id += 1
    if (photo_id > len(images_in_db())):
        photo_id = 1
        print("next_image")
        print(photo_id)
    return getImageById(photo_id).photoPath


@app.route("/addTag", methods=['GET', 'POST'])
def addTag():
    print("addTag")
    data = request.get_json()
    tagName = data['newTag']
    photoName = data['photoName'].replace('%20', ' ')
    activeImage = getImageByName(photoName)
    activeImageName = activeImage.photoPath
    if (tagName not in tags_of_image(activeImageName) and tagName):
        # if tag does not even exist in db
        if (tagName not in tags_in_db()):
            # füg Tag hinzu
            tag = Tag(tagName)
            db.session.add(tag)
        # füg Tag an Photo an
        activeTag = getTagByName(tagName)
        activeTag.taggedImages.append(activeImage)
        db.session.commit()
    else:
        print("Tag existiert bereits")
    return redirect('imageView')


@app.route("/deleteTag", methods=['POST'])
def deleteTag():
    data = request.get_json()
    tagName = data['tagName']
    imageName = data['photoName'].replace('%20', ' ')
    tagToBeDeleted = getTagByName(tagName)
    activeImage = getImageByName(imageName)
    countImages = tagToBeDeleted.taggedImages
    tagToBeDeleted.taggedImages.remove(activeImage)
    if (len(countImages) < 1):
        db.session.delete(tagToBeDeleted)
    db.session.commit()
    return redirect('imageView')


if __name__ == '__main__':
    app.run(port=4000, debug=True)

import os
import random
import string
from datetime import datetime
import cv2
import imutils
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from flask import render_template, request, redirect, url_for, session
from keras import backend as k
from werkzeug.utils import secure_filename
from project import app
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropNameDAO import CropNameDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.dao.DetectionDAO import DetectionDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.DetectionVO import DetectionVO
UPLOAD_IMAGE_FOLDER = "project/static/adminResources/uploadImage/"
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER



# admin
@app.route('/admin/viewImage', methods=['GET'])
def adminViewImage():
    try:
        if adminLoginSession() == "admin":
            print("a")
            imageDAO = ImageDAO()
            imageVOList = imageDAO.adminViewImage()

            return render_template('admin/viewImage.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# user
@app.route('/user/loadImage', methods=['GET'])
def userLoadImage():
    try:
        if adminLoginSession() == 'user':
            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()

            cropNameDAO = CropNameDAO()
            cropNameVOList = cropNameDAO.viewCropName()

            return render_template('user/addImage.html', cropTypeVOList=cropTypeVOList,
                                   cropNameVOList=cropNameVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertUploadImage', methods=['POST'])
def userInsertUploadImage():
    try:
        if adminLoginSession() == 'user':
            image_CropTypeId = request.form['image_CropTypeId']
            image_CropNameId = request.form['image_CropNameId']

            file = request.files['file']

            imageFileName = secure_filename(file.filename)
            imageFilePath = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'])

            file.save(os.path.join(imageFilePath, imageFileName))

            imageUploadDate = str(datetime.date(datetime.now()))

            imageUploadTime = str(datetime.time(datetime.now()))
            image_LoginId = session['session_loginId']
            imageDAO = ImageDAO()
            imageVO = ImageVO()


            path = imageFilePath + imageFileName
            k.clear_session()
            image = cv2.imread(path)
            print(image)
            orig = image.copy()

            # pre-process the image for classification
            image = cv2.resize(image, (28, 28))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)

            # load the trained convolutional neural network
            print("[INFO] loading network.  ..")
            print("1")
            model = load_model(r"D:\projectworkspace\cropdiseasepredictipn\project\static\adminResources\model\croptype_not_croptype1.model")
            print("2")

            # classify the input image
            (croptype, notcroptype) = model.predict(image)[0]

            # build the label
            label1 = "Croptype" if croptype > notcroptype else "Notcroptype"
            print(label1)
            proba = croptype if croptype > notcroptype else notcroptype
            label = "{}: {:.2f}%".format(label1, proba * 100)

            # draw the label on the image
            output = imutils.resize(orig, width=400)
            cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
            cv2.imshow("Output", output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if label1 == "Croptype":
                imageVO.image_CropTypeId = image_CropTypeId
                imageVO.image_CropNameId = image_CropNameId
                imageVO.imageFileName = imageFileName
                imageVO.imageFilePath = imageFilePath.replace("project", "..")
                imageVO.imageUploadDate = imageUploadDate
                imageVO.imageUploadTime = imageUploadTime
                imageVO.image_LoginId = image_LoginId
                imageDAO.userInsertImage(imageVO)


                image = cv2.imread(path)
                B, G, R = cv2.split(image)
                mask = np.zeros(image.shape, np.uint8)
                zeros = np.zeros(image.shape[:2], dtype="uint8")
                #yellow = cv2.imshow("y", cv2.merge([zeros, G, R]))

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edged = cv2.Canny(cv2.merge([zeros, G, R]), 15, 235)
                cv2.waitKey(0)

                contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

               # cv2.imshow('Canny Edges After Contouring', edged)
                cv2.waitKey(0)

                print("Number of Contours found = " + str(len(contours)))
                a = int(len(contours))
                print(a)
                # check1=35
                # b=int(check1)
                # print(b)

                if a <= int(35):
                    check = "healthy"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image, check, (20, 30), font, 1, (0, 255, 0), 3)


                else:
                    check = "unhealthy"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image, check, (50, 90), font, 1, (0, 255, 0), 3)

                # cv2.drawContours(image, contours, -1, (0, 255, 0), 3
                print(check)
                cv2.imshow('Contours', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                session['session_detectionPrediction']=check
                print(check)
                print(session['session_loginUsername'])
                detectionImagePath = "project/static/adminResources/detectionImage/"
                detectionImageName = ''.join((random.choice(string.digits)) for x in range(8))
                cv2.imwrite(detectionImagePath + detectionImageName + ".jpg",image)




                detectionDate = datetime.today().strftime("%d/%m/%Y")
                detectionTime = datetime.now().strftime("%H:%M:%S")

                detectionVO = DetectionVO()
                detection_LoginId = session['session_loginId']
                print(detection_LoginId)
                detectionVO.detectionImageName=detectionImageName  + ".jpg"
                detectionVO.detectionImagePath=detectionImagePath.replace("project", "..")
                detectionVO.detectionDate=detectionDate
                detectionVO.detectionTime =detectionTime
                detectionVO.detection_LoginId = detection_LoginId
                detectionVO.detectionPrediction=check

                print("ert")
                imageDAO.UserInsertDetection(detectionVO)

                return redirect(url_for('userViewImage'))

            elif label1 == "Notcroptype":
                path = imageFilePath + imageFileName
                os.remove(path)
                msg="sorry! you upload image was in a wrong category "
                return render_template('user/addImage.html', error=msg)
            # show the output image

            k.clear_session()


        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewImage', methods=['GET'])
def userViewImage():
    try:

        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            imageVO.image_LoginId = session['session_loginId']
            imageVOList = imageDAO.userViewImage(imageVO)

            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteImage', methods=['GET'])
def userDeleteImage():
    try:
        if adminLoginSession() == 'user':

            imageDAO = ImageDAO()
            imageVO = ImageVO()

            imageId = request.args.get('imageId')
            imageFileName = request.args.get('imageFileName')

            imageVO.imageId = imageId
            imageVO.imageFileName = imageFileName

            imageList = imageDAO.userDeleteImage(imageVO)

            print(imageList)

            imageFileName = imageList.imageFileName
            imageFilePath = imageList.imageFilePath.replace("..", "project")
            imageFullPath = imageFilePath + imageFileName
            os.remove(imageFullPath)
            return redirect(url_for('userViewImage'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)



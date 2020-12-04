from project import  app
from flask import request, render_template, redirect, url_for,session
import os
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DetectionDAO import DetectionDAO
from project.com.vo.DetectionVO import DetectionVO


@app.route('/user/viewDetection', methods=['GET'])
def userviewDetection():
    try:

        if adminLoginSession() == 'user':
            detectionVO = DetectionVO()
            detectionDAO = DetectionDAO()
            detection_LoginId  = session['session_loginId']
            detectionVO.detection_LoginId=detection_LoginId
            print(session['session_loginId'])
            detectionVOList = detectionDAO.userViewDetection(detectionVO)

            return render_template('user/viewDetection.html', detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteDetection', methods=['GET'])
def userDeleteDetection():
    try:
        if adminLoginSession() == 'user':

            detectionDAO = DetectionDAO()
            detectionVO = DetectionVO()

            detectionId = request.args.get('detectionId')
            detectionImageName = request.args.get('detectionList')

            detectionVO.detectionId = detectionId
            detectionVO.detectionFileName = detectionImageName

            detectionList = detectionDAO.userDeleteDetection(detectionVO)

            print(detectionList)

            detectionImageName = detectionList.detectionImageName
            detectionImagePath = detectionList.detectionImagePath.replace("..", "project")
            detectionFullPath = detectionImagePath + detectionImageName
            os.remove(detectionFullPath)
            return redirect(url_for('userviewDetection'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

@app.route('/admin/viewDetection', methods=['GET'])
def adminViewDetection():
    try:

        if adminLoginSession() == 'admin':
            print("a")
            detectionDAO = DetectionDAO()
            detectionVOList = detectionDAO.adminViewDetection()

            return render_template('admin/viewDetection.html', detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
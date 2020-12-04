import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO



COMPLAIN_UPLOAD_FOLDER = "project/static/adminResources/complain/"
app.config['COMPLAIN_UPLOAD_FOLDER'] = COMPLAIN_UPLOAD_FOLDER
REPLY_UPLOAD_FOLDER = "project/static/adminResources/reply/"
app.config['REPLY_UPLOAD_FOLDER'] = REPLY_UPLOAD_FOLDER

# admin
@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainStatus = 'Pending'
            complainVO.complainStatus = complainStatus
            complainVOList = complainDAO.adminViewComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReplay():
    try:
        if adminLoginSession() == "admin":
            complainId = request.args.get('complainId')
            return render_template('admin/complainReply.html', complainId=complainId)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            replyDate = str(datetime.date(datetime.now()))

            replyTime = str(datetime.time(datetime.now()))

            complainStatus = 'Replied'

            complainTo_LoginId = session['session_loginId']

            file = request.files['file']

            replyFileName = secure_filename(file.filename)

            replyFilePath = os.path.join(app.config['REPLY_UPLOAD_FOLDER'])

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = complainTo_LoginId
            complainVO.complainStatus = complainStatus

            complainDAO.adminInsertComplainReply(complainVO)
            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
# user
@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            complainDate = datetime.today().strftime("%d/%m/%Y")

            complainTime = datetime.now().strftime("%H:%M:%S")

            complainStatus = 'Pending'

            file = request.files['file']

            complainFileName = secure_filename(file.filename)

            complainFilePath = os.path.join(app.config['COMPLAIN_UPLOAD_FOLDER'])

            file.save(os.path.join(complainFilePath, complainFileName))

            complainFrom_LoginId = session['session_loginId']

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace('project', '..')
            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainDAO.userInsertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
@app.route('/user/viewComplain')
def userViewComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVOList = complainDAO.userViewComplain(complainVO)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()

            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainList = complainDAO.userDeleteComplain(complainVO)

            if complainList.complainStatus == 'Replied':
                replyPath = complainList.replyFilePath.replace("..", "project") + complainList.replyFileName

                os.remove(replyPath)

            complainPath = complainList.complainFilePath.replace("..", "project") + complainList.complainFileName

            os.remove(complainPath)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
@app.route("/user/viewComplainReply", methods=['GET'])
def userViewComplainReplay():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.userViewComplainReply(complainVO)
            print(complainVOList)
            return render_template("user/viewComplainReply.html", complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

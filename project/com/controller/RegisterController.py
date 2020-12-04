import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route("/user/loadRegister")
def userLoadRegister():
    try:
        return render_template('user/register.html')
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']
        print(loginUsername)

        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "cropdiseaseprediction30@gmail.com"
        print("+", sender)
        receiver = loginUsername
        print("++", receiver)
        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"
        print('form')
        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()
        print("few")

        server.login(sender, "your password")
        print("send")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)
        print("email sent")

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"
        loginVO.loginRole = "user"

        loginDAO.insertLogin(loginVO)

        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerContact = registerContact
        registerVO.registerAddress = registerAddress
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser')
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister()
            print("___________________", registerVOList)
            status = 'active'
            return render_template('admin/viewUser.html', registerVOList=registerVOList, status=status)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            loginVO = LoginVO()

            loginId = request.args.get('loginId')
            loginStatus = 'inactive'

            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus

            loginDAO.blockUser(loginVO)

            return adminViewUser()

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            loginVO = LoginVO()

            loginId = request.args.get('loginId')
            loginStatus = 'active'

            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus

            loginDAO.UnblockUser(loginVO)

            return adminViewUser()

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

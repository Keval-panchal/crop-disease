from flask import request, render_template, redirect, url_for, session
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO


@app.route('/', methods=['GET'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:
            msg = 'Username Or Password is Incorrect !'
            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == 'inactive':
            msg = 'you are temporary block by admin!'
            return render_template('admin/login.html', error=msg)

        else:
            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:

        if adminLoginSession() == 'admin':

            return render_template('admin/index.html')
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/index.html')
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:

        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'user':

                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False

    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)

@app.route("/admin/forgotPassword")
def adminForgotPassword():
    try:
        return render_template("admin/forgotPassword.html")
    except Exception as ex:
        print(ex)


@app.route("/admin/insertUsername",methods=['POST'])
def adminInsertUsername():
    try:
        loginDAO=LoginDAO()
        loginVO=LoginVO()

        loginUsername=request.form['loginUsername']
        loginVO.loginUsername=loginUsername
        loginVOList=loginDAO.validateLoginUsername(loginVO)
        loginDictList = [i.as_dict() for i in loginVOList]
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            error="E - mail is not exist !"
            return render_template("admin/forgotPassword.html", error=error)
        else:
            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername


            otp = ''.join((random.choice(string.digits)) for x in range(6))

            sender = "cropdiseaseprediction30@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "keval12345")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            session["otp"]=otp
            return render_template("admin/addOtp.html")


    except Exception as ex:
        print(ex)

@app.route("/admin/insertOtp",methods=['POST'])
def adminInsertOtp():
    try:

        loginOtp=request.form["loginOtp"]
        if session["otp"] == loginOtp:
            return render_template("admin/addNewPassword.html")
        else:
            err="Otp is not Match!"
            return render_template("admin/addOTP.html",err=err)
    except Exception as ex:
        print(ex)

@app.route("/admin/insertNewPassword",methods=['POST'])
def adminInsertNewPassword():
    try:
        loginDAO=LoginDAO()
        loginVO=LoginVO()
        loginPassword=request.form["loginPassword"]

        sender = "cropdiseaseprediction30@gmail.com"

        receiver = session["session_loginUsername"]

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "New Password"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "keval12345")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        server.quit()

        loginVO.loginId=session['session_loginId']
        loginVO.loginPassword=loginPassword
        loginDAO.loginUpdateUser(loginVO)
        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)
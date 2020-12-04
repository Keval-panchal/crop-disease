from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO():

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)

        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def blockUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def UnblockUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def loginUpdateUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()
        return loginList
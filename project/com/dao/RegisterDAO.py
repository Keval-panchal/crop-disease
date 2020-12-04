from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class RegisterDAO():

    def insertRegister(self, registerVO):
        db.session.add(registerVO)

        db.session.commit()

    def viewRegister(self):
        registerList = db.session.query(RegisterVO, LoginVO).join(LoginVO,
                                                                  RegisterVO.register_LoginId == LoginVO.loginId).all()

        return registerList

    def editRegister(self, registerVO):
        registerList = db.query.filter_by(registerId=registerVO.registerId)

        return registerList

    def deleteRegister(self, registerId):
        registerList = db.get(registerId)

        db.session.delete(registerList)

        db.session.commit()

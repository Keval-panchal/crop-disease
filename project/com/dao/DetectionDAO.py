from project import db
from project.com.vo.DetectionVO import DetectionVO
from project .com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO

class DetectionDAO:
    def userViewDetection(self,detectionVO):
      detectionList = DetectionVO.query.filter_by(detection_LoginId=detectionVO.detection_LoginId).all()

      return detectionList

    def userDeleteDetection(self, detectionVO):
        detectionList = DetectionVO.query.get(detectionVO.detectionId)

        db.session.delete(detectionList)

        db.session.commit()
        return detectionList


    def adminViewDetection(self):
        detectionList=db.session.query(DetectionVO,LoginVO)\
        .join(LoginVO,DetectionVO.detection_LoginId == LoginVO.loginId).all()

        return detectionList





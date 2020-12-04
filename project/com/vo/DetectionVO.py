from project import db
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO


class DetectionVO(db.Model):
    __tablename__ = 'detectionmaster'
    detectionId = db.Column('detectionId', db.INTEGER, autoincrement=True, primary_key=True)
    detectionImageName = db.Column('detectionImageName', db.VARCHAR(100))
    detectionImagePath = db.Column('detectionFilePath', db.VARCHAR(200))
    detectionDate = db.Column('detectionUploadDate', db.VARCHAR(100), nullable=False)
    detectionTime = db.Column('detectionUploadTime', db.VARCHAR(100), nullable=False)
    detection_LoginId = db.Column('detection_LoginId', db.INTEGER, db.ForeignKey(LoginVO.loginId), nullable=False)
    detectionPrediction = db.Column('detectionPrediction', db.VARCHAR(200), nullable=False)
    def as_disct(self):
        return {
            'detectionId': self.detectionId,
            'detectionImageName': self.detectionImageName,
            'detectionFilePath': self.detectionFilePath,
            'detectionUploadDate': self.detectionUploadDate,
            'detectionUploadTime': self.detectionUploadTime,
            'detection_LoginId': self.detection_LoginId,
            'detectionImage':self.detectionImage,
            'detectionPrediction':self.detectionPrediction,
            'detection_image': self.detection_image

        }


db.create_all()

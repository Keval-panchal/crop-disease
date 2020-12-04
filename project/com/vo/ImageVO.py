from project import db
from project.com.vo.CropNameVO import CropNameVO
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.LoginVO import LoginVO


class ImageVO(db.Model):
    __tablename__ = 'Imagemaster'
    imageId = db.Column('imageId', db.INTEGER, primary_key=True, autoincrement=True)
    imageFileName = db.Column('imageFileName', db.String(100))
    imageFilePath = db.Column('imageFilePath', db.VARCHAR(200))
    imageUploadDate = db.Column('imageUploadDate', db.String(100))
    imageUploadTime = db.Column('imageUploadTime', db.String(100))
    image_CropTypeId = db.Column('image_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))
    image_CropNameId = db.Column('image_CropNameId', db.Integer, db.ForeignKey(CropNameVO.cropNameId))
    image_LoginId = db.Column('image_LoginId', db.INTEGER, db.ForeignKey(LoginVO.loginId), nullable=False)

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageFileName': self.imageFileName,
            'imageFilePath': self.imageFilePath,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime,
            'image_CropTypeId': self.image_CropTypeId,
            'image_CropNameId': self.image_CropNameId,
            'video_LoginId': self.video_LoginId

        }


db.create_all()

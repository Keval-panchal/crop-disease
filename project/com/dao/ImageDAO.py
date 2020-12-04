from project import db
from project.com.vo.CropNameVO import CropNameVO
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.DetectionVO import DetectionVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO


class ImageDAO:

    def adminViewImage(self):
        imageList = db.session.query(ImageVO, CropNameVO, CropTypeVO, LoginVO).join(CropTypeVO,
                                                                                    ImageVO.image_CropTypeId == CropTypeVO.cropTypeId).join(
            CropNameVO, ImageVO.image_CropNameId == CropNameVO.cropNameId).join(LoginVO,
                                                                                ImageVO.image_LoginId == LoginVO.loginId).all()
        return imageList

    def userInsertImage(self, imageVO):
        db.session.add(imageVO)
        db.session.commit()

    def userViewImage(self, imageVO):
        imageList = db.session.query(ImageVO, CropNameVO, CropTypeVO) \
            .filter_by(image_LoginId=imageVO.image_LoginId) \
            .join(CropTypeVO, ImageVO.image_CropTypeId == CropTypeVO.cropTypeId) \
            .join(CropNameVO, ImageVO.image_CropNameId == CropNameVO.cropNameId) \
            .all()

        return imageList

    def userDeleteImage(self, imageVO):
        imageList = ImageVO.query.get(imageVO.imageId)

        db.session.delete(imageList)

        db.session.commit()
        return imageList

    def UserInsertDetection(self,detectionVO):
        db.session.add(detectionVO)
        db.session.commit()




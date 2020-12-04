from project import db
from project.com.vo.CropNameVO import CropNameVO
from project.com.vo.CropTypeVO import CropTypeVO


class CropNameDAO:
    def insertCropName(self, cropNameVO):
        db.session.add(cropNameVO)

        db.session.commit()

    def viewCropName(self):
        cropNameList = db.session.query(CropNameVO, CropTypeVO).join(CropTypeVO,
                                                                     CropNameVO.cropName_CropTypeId == CropTypeVO.cropTypeId).all()

        return cropNameList

    def deleteCropName(self, cropNameId):
        cropNameList = CropNameVO.query.get(cropNameId)

        db.session.delete(cropNameList)

        db.session.commit()

    def editCropName(self, cropNameVO):
        cropNameList = CropNameVO.query.filter_by(cropNameId=cropNameVO.cropNameId)

        return cropNameList

    def updateCropName(self, cropNameVO):
        db.session.merge(cropNameVO)

        db.session.commit()

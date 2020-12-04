from project import db
from project.com.vo.CropMedicineVO import CropMedicineVO
from project.com.vo.CropNameVO import CropNameVO
from project.com.vo.CropTypeVO import CropTypeVO


class CropMedicineDAO:
    def insertCropMedicine(self, cropMedicineVO):
        db.session.add(cropMedicineVO)

        db.session.commit()

    def viewCropMedicine(self):
        cropMedicineList = db.session.query(CropMedicineVO, CropNameVO, CropTypeVO).join(CropTypeVO,
                                                                                         CropMedicineVO.cropMedicine_CropTypeId == CropTypeVO.cropTypeId).join(
            CropNameVO, CropMedicineVO.cropMedicine_CropNameId == CropNameVO.cropNameId).all()

        return cropMedicineList

    def deleteCropMedicine(self, cropMedicineId):
        cropMedicineList = CropMedicineVO.query.get(cropMedicineId)

        db.session.delete(cropMedicineList)

        db.session.commit()

    def editCropMedicine(self, cropMedicineVO):
        cropMedicineList = CropMedicineVO.query.filter_by(cropMedicineId=cropMedicineVO.cropMedicineId).all()

        return cropMedicineList

    def updateCropMedicine(self, cropMedicineVO):
        db.session.merge(cropMedicineVO)

        db.session.commit()

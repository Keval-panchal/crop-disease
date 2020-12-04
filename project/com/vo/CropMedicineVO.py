from project import db
from project.com.vo.CropNameVO import CropNameVO
from project.com.vo.CropTypeVO import CropTypeVO


class CropMedicineVO(db.Model):
    __tablename__ = 'cropmedicinemaster'
    cropMedicineId = db.Column(' cropMedicineId', db.Integer, primary_key=True, autoincrement=True)
    cropMedicineName = db.Column('cropMedicineName', db.String(100), nullable=False)
    cropMedicinePower = db.Column('medicinePower', db.String(100), nullable=False)
    cropMedicineDescription = db.Column('medicineDescription', db.String(100), nullable=False)
    cropMedicine_CropTypeId = db.Column('cropMedicine_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))
    cropMedicine_CropNameId = db.Column('cropMedicine_CropNameId', db.Integer, db.ForeignKey(CropNameVO.cropNameId))

    def as_dict(self):
        return {

            'cropMedicineId': self.cropMedicineId,
            'cropMedicineName': self.cropMedicineName,
            'cropMedicinePower': self.cropMedicinePower,
            'cropMedicineDescription': self.cropMedicineDescription,
            'cropMedicine_CropTypeId': self.cropMedicine_CropTypeId,
            'cropMedicine_CropNameId': self.cropMedicine_CropNameId

        }


db.create_all()

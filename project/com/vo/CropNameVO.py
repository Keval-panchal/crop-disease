from project import db
from project.com.vo.CropTypeVO import CropTypeVO


class CropNameVO(db.Model):
    __tablename__ = 'cropnamemaster'
    cropNameId = db.Column('cropNameId', db.Integer, primary_key=True, autoincrement=True)
    cropName = db.Column('cropName', db.String(100))
    cropNameDescription = db.Column('cropNameDescription', db.String(100))
    cropName_CropTypeId = db.Column('cropName_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))

    def as_dict(self):
        return {
            'cropNameId': self.cropNameId,
            'cropName': self.cropName,
            'cropNameDescription': self.cropNameDescription,
            ' cropName_CropTypeId': self.cropName_CropTypeId

        }


db.create_all()

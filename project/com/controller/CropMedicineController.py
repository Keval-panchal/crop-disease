from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropMedicineDAO import CropMedicineDAO
from project.com.dao.CropNameDAO import CropNameDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.vo.CropMedicineVO import CropMedicineVO


@app.route('/admin/loadCropMedicine', methods=['GET'])
def adminLoadCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()

            cropNameDAO = CropNameDAO()
            cropNameVOList = cropNameDAO.viewCropName()

            return render_template('admin/addCropMedicine.html', cropTypeVOList=cropTypeVOList,
                                   cropNameVOList=cropNameVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCropMedicine', methods=['POST'])
def adminInsertCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropMedicineName = request.form['cropMedicineName']
            cropMedicinePower = request.form['cropMedicinePower']
            cropMedicineDescription = request.form['cropMedicineDescription']
            cropMedicine_CropTypeId = request.form['cropMedicine_CropTypeId']
            cropMedicine_CropNameId = request.form['cropMedicine_CropNameId']

            cropMedicineVO = CropMedicineVO()
            cropMedicineDAO = CropMedicineDAO()

            cropMedicineVO.cropMedicineName = cropMedicineName
            cropMedicineVO.cropMedicinePower = cropMedicinePower
            cropMedicineVO.cropMedicineDescription = cropMedicineDescription
            cropMedicineVO.cropMedicine_CropTypeId = cropMedicine_CropTypeId
            cropMedicineVO.cropMedicine_CropNameId = cropMedicine_CropNameId

            cropMedicineDAO.insertCropMedicine(cropMedicineVO)

            return redirect(url_for('adminViewCropMedicine'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewCropMedicine', methods=['GET'])
def adminViewCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropMedicineDAO = CropMedicineDAO()
            cropMedicineVOList = cropMedicineDAO.viewCropMedicine()
            print(cropMedicineVOList)
            return render_template('admin/viewCropMedicine.html', cropMedicineVOList=cropMedicineVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCropMedicine', methods=['GET'])
def adminDeleteCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropMedicineDAO = CropMedicineDAO()

            cropMedicineId = request.args.get('cropMedicineId')

            cropMedicineDAO.deleteCropMedicine(cropMedicineId)

            return redirect(url_for('adminViewCropMedicine'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editCropMedicine', methods=['GET'])
def adminEditCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            print("in edit")

            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()

            cropNameDAO = CropNameDAO()
            cropNameVOList = cropNameDAO.viewCropName()
            cropMedicineVO = CropMedicineVO()

            cropMedicineDAO = CropMedicineDAO()

            cropMedicineId = request.args.get('cropMedicineId')

            print(cropMedicineId)

            cropMedicineVO.cropMedicineId = cropMedicineId

            cropMedicineVOList = cropMedicineDAO.editCropMedicine(cropMedicineVO)

            print(cropMedicineVOList)

            return render_template('admin/editCropMedicine.html', cropMedicineVOList=cropMedicineVOList,
                                   cropTypeVOList=cropTypeVOList, cropNameVOList=cropNameVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updateCropMedicine', methods=['POST'])
def adminUpdateCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropMedicineId = request.form['cropMedicineId']
            cropMedicineName = request.form['cropMedicineName']
            cropMedicinePower = request.form['cropMedicinePower']
            cropMedicineDescription = request.form['cropMedicineDescription']

            cropMedicine_CropTypeId = request.form['cropMedicine_CropTypeId']
            cropMedicine_CropNameId = request.form['cropMedicine_CropNameId']

            cropMedicineVO = CropMedicineVO()
            cropMedicineDAO = CropMedicineDAO()

            cropMedicineVO.cropMedicineId = cropMedicineId
            cropMedicineVO.cropMedicineName = cropMedicineName
            cropMedicineVO.cropMedicinePower = cropMedicinePower
            cropMedicineVO.cropMedicineDescription = cropMedicineDescription
            cropMedicineVO.cropMedicine_CropTypeId = cropMedicine_CropTypeId
            cropMedicineVO.cropMedicine_CropNameId = cropMedicine_CropNameId

            cropMedicineDAO.updateCropMedicine(cropMedicineVO)

            return redirect(url_for('adminViewCropMedicine'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

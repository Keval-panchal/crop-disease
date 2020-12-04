from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropNameDAO import CropNameDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.vo.CropNameVO import CropNameVO


@app.route('/admin/loadCropName', methods=['GET'])
def adminLoadCropName():
    try:
        if adminLoginSession() == 'admin':
            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()

            return render_template('admin/addCropName.html', cropTypeVOList=cropTypeVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertCropName', methods=['POST'])
def adminInsertCropName():
    try:
        if adminLoginSession() == 'admin':
            cropName = request.form['cropName']
            cropNameDescription = request.form['cropNameDescription']
            cropName_CropTypeId = request.form['cropName_CropTypeId']

            cropNameVO = CropNameVO()
            cropNameDAO = CropNameDAO()

            cropNameVO.cropName = cropName
            cropNameVO.cropNameDescription = cropNameDescription
            cropNameVO.cropName_CropTypeId = cropName_CropTypeId

            cropNameDAO.insertCropName(cropNameVO)

            return redirect(url_for('adminViewCropName'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewCropName')
def adminViewCropName():
    try:
        if adminLoginSession() == 'admin':
            cropNameDAO = CropNameDAO()
            cropNameVOList = cropNameDAO.viewCropName()
            print(cropNameVOList)

            return render_template('admin/viewCropName.html', cropNameVOList=cropNameVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCropName', methods=['GET'])
def adminDeleteCropName():
    try:
        if adminLoginSession() == 'admin':
            cropNameDAO = CropNameDAO()

            cropNameId = request.args.get('cropNameId')

            cropNameDAO.deleteCropName(cropNameId)

            return redirect(url_for('adminViewCropName'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editCropName', methods=['GET'])
def adminEditCropName():
    try:
        if adminLoginSession() == 'admin':
            cropNameVO = CropNameVO()
            cropTypeDAO = CropTypeDAO()
            cropNameDAO = CropNameDAO()
            cropNameId = request.args.get('cropNameId')

            cropNameVO.cropNameId = cropNameId

            cropNameVOList = cropNameDAO.editCropName(cropNameVO)

            cropTypeVOList = cropTypeDAO.viewCropType()

            return render_template('admin/editCropName.html', cropNameVOlist=cropNameVOList,
                                   cropTypeVOList=cropTypeVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updateCropName', methods=['POST'])
def adminUpdateCropName():
    try:
        if adminLoginSession() == 'admin':
            cropNameId = request.form['cropNameId']
            cropName_CropTypeId = request.form['cropName_CropTypeId']
            cropName = request.form['cropName']
            cropNameDescription = request.form['cropNameDescription']

            cropNameVO = CropNameVO()
            cropNameDAO = CropNameDAO()

            cropNameVO.cropNameId = cropNameId
            cropNameVO.cropName_CropTypeId = cropName_CropTypeId
            cropNameVO.cropName = cropName
            cropNameVO.cropNameDescription = cropNameDescription

            cropNameDAO.updateCropName(cropNameVO)

            return redirect(url_for('adminViewCropName'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

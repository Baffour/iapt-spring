# IAPT Spring Assessment - Group 13

from gluon.contrib.appconfig import AppConfig
import os

APP_NAME = 'Shortboxes'

myconf = AppConfig(reload=True) # see private/appconfig.ini for settings

# Set up the database
db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])

# Set the response style for forms
response.formstyle = myconf.take('forms.formstyle')
response.form_label_separator = myconf.take('forms.separator')

uploadfolder = os.path.join(request.folder,'uploads')

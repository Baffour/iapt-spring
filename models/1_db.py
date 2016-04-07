# IAPT Spring Assessment - Group 13

from gluon.contrib.appconfig import AppConfig
import re
import os

APP_NAME = 'Shortboxes'

myconf = AppConfig(reload=True) # see private/appconfig.ini for settings

# Set up the database
db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])

# Set the response style for forms
response.formstyle = myconf.take('forms.formstyle')
response.form_label_separator = myconf.take('forms.separator')

uploadfolder = os.path.join(request.folder,'uploads')

# Define a custom validator for currency values
class IS_CURRENCY_VALUE(object):
    def __call__(self, value):
        error_str = 'Enter a currency value, e.g. "2.50"'
        if value is None or type(value) != str:
            return None, error_str

        regex = re.compile(r"^([0-9]+)(\.[0-9]{1,2})?$")
        match = regex.match(value)
        if not match:
            return None, error_str

        pounds, pence = match.groups()
        pounds, pence = int(pounds) if pounds else 0, int(pence.lstrip('.')) if pence else 0
        return (pounds * 100) + pence, None

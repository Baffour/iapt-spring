# IAPT Spring Assessment - Group 13

from gluon.admin import apath
from gluon.fileutils import read_file
from gluon.restricted import restricted

def erase_db():
    def onconfirm():
        for table in db.tables():
            try: db[table].drop()
            except: pass
        db.commit()
        session.clear()
        return "Database wiped successfully. Refresh the page and you will have been logged out."
    return sudo_screen("Wipe the database", onconfirm)

def verify_admin_password(password):
    _config = {}
    port = int(request.env.server_port or 0)
    restricted(read_file(apath('../parameters_%i.py' % port, request)), _config)
    return _config['password'] == CRYPT()(password)[0]

def sudo_screen(button_text, onconfirm):
    form = SQLFORM.factory(Field('password', type='password'), submit_button=button_text)

    if form.process().accepted:
        if verify_admin_password(form.vars['password']):
            response.flash = onconfirm()
            response.flash_type = 'success'
        else:
            response.flash = "Please re-enter the admin password (not your account password) and retry."
            response.flash_type = 'danger'

    return dict(form=form)

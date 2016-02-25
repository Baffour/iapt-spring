# IAPT Spring Assessment - Group 13

@auth.requires_login()
def list():
    pass

@auth.requires_login()
def new():
    form = SQLFORM(db.itm, submit_button="Add item")
    form.custom.widget.name['_autofocus'] = True

    if form.process().accepted:
        redirect(URL('object', 'view', args=form.vars['id']))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(form=form)

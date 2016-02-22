# IAPT Spring Assessment - Group 13

@auth.requires_login()
def add():
    form = SQLFORM(db.obj, submit_button="Create")

    if form.process().accepted:
        redirect(URL('object', 'view', args=form.vars['id']))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(form=form)

# IAPT Spring Assessment - Group 13

@auth.requires_login()
def list():
    pass

def view():
    box = load_box(request.args(0))
    guest = not auth.user or auth.user.id != box.auth_user
    return dict(box=box, guest=guest, objects=None)

@auth.requires_login()
def new():
    form = SQLFORM(db.box, submit_button="Create box")

    if form.process().accepted:
        redirect(URL('box', 'view', args=form.vars['id']))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(form=form)

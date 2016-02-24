# IAPT Spring Assessment - Group 13

@auth.requires_login()
def list():
    boxes = db(db.box.auth_user==auth.user).select(orderby=db.box.name)
    return dict(boxes=boxes)

@auth.requires_login()
def new():
    form = SQLFORM(db.box, submit_button="Create box")
    form.custom.widget.name['_autofocus'] = True

    if form.process().accepted:
        redirect(URL('view', args=form.vars['id']))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(form=form)

def view():
    box = load_box(request.args(0))
    guest = not auth.user or auth.user.id != box.auth_user
    return dict(box=box, guest=guest, objects=None)

@auth.requires_login()
def edit():
    box = load_box(request.args(0), editing=True)

    form = SQLFORM(db.box, box, submit_button='Save', showid=False)

    if form.process().accepted:
        session.flash = 'Box changes saved successfully'
        session.flash_type = 'success'
        redirect(URL('view', args=box.id))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(name=box.name, form=form)

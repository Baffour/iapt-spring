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
    return dict(box=box, guest=guest, items=items_in(box))

@auth.requires_login()
def edit():
    box = load_box(request.args(0), editing=True)

    # The unfiled box cannot be renamed
    if box.unfiled:
        db.box.name.readable = False
        db.box.name.writable = False

    form = SQLFORM(db.box, box, submit_button='Save', showid=False)

    if form.process().accepted:
        session.flash = 'Box changes saved successfully'
        session.flash_type = 'success'
        redirect(URL('view', args=box.id))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(name=box.name, form=form)

@auth.requires_login()
def delete():
    box = load_box(request.args(0), editing=True)
    box_name = box.name

    if box.unfiled:
        raise HTTP(403)

    form = FORM.confirm('Delete', {'Cancel': URL('view/' + str(box.id))})
    form['_class'] = 'confirmation-form'
    form[0]['_class'] = 'btn btn-danger'
    form[1]['_class'] = 'btn btn-default'

    if form.accepted:
        items = items_in(box)
        del db.box[box.id]

        unfiled = load_unfiled_box()
        for item in items:
            if db(db.itm2box.itm==item.id).isempty():
                db.itm2box.insert(itm=item.id, box=unfiled.id)

        session.flash = 'Box "' + box_name + '" successfully deleted.'
        session.flash_type = 'success'
        redirect(URL('list'))

    return dict(name=box_name, form=form)

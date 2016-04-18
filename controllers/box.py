# IAPT Spring Assessment - Group 13

@auth.requires_login()
def list():
    query = db(db.box.auth_user==auth.user)
    boxes = query.select().sort(lambda b: (not b.unfiled, b.name.lower()))
    return dict(boxes=boxes)

@auth.requires_login()
def new():
    form = SQLFORM(db.box, submit_button="Create box",_role="form")
    form.custom.widget.name['_autofocus'] = True

    if 'public' in request.vars:
        if request.vars['public'] == 'True':
            form.element('input[name=private]')['_checked'] = False

    if form.process().accepted:
        redirect(URL('view', args=form.vars['id']))

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    return dict(form=form)

def view():
    box = load_box(request.args(0))
    guest = not auth.user or auth.user.id != box.auth_user
    items = items_in(box)
    full = not guest and len(items) == db(db.itm.auth_user==auth.user).count()
    items.explore_info=[Tag.item_type, Tag.monetary_value]
    return dict(box=box, guest=guest, items=items, full=full)

@auth.requires_login()
def edit():
    box = load_box(request.args(0), editing=True)

    # The unfiled box cannot be renamed
    if box.unfiled:
        db.box.name.readable = False
        db.box.name.writable = False

    form = SQLFORM(db.box, box, submit_button='Save', showid=False, _role="form")

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
    form['_role'] = 'form'
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

@auth.requires_login()
def insert_item():
    box = load_box(request.args(0), editing=True)
    item_ids_in_box = [i.id for i in items_in(box)]

    constraint = db(~db.itm.id.belongs(item_ids_in_box) & (db.itm.auth_user == auth.user.id))
    validator = IS_IN_DB(constraint, 'itm.id', 'itm.name', zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Add to this box', _role="form")

    if form.process().accepted:
        itm = load_item(form.vars['itm'], editing=True)
        db.itm2box.insert(itm=itm.id, box=box.id)

        session.flash = 'Item "' + itm.name + '" added to "' + box.name + '" box successfully.'
        session.flash_type = 'success'
        redirect(URL('view', args=box.id))

    return dict(box=box, form=form)

@auth.requires_login()
def remove_item():
    box = load_box(request.args(0), editing=True)
    constraint = box.itm2box(db.itm2box.itm==db.itm.id)
    validator = IS_IN_DB(constraint, 'itm.id', 'itm.name', zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Remove from this box', _role="form")

    if form.process().accepted:
        item = load_item(form.vars['itm'], editing=True)

        # TODO: Would be better not to show boxes fitting this criteria at all
        if box.unfiled and item.itm2box.count() == 1:
            response.flash = 'Cannot remove this item: This is the Unfiled box, and the item is not part of any other boxes.'
            response.flash_type = 'danger'
            return dict(box=box, form=form)

        box.itm2box(db.itm2box.itm==item.id).delete()

        if item.itm2box.isempty():
            unfiled = load_unfiled_box()
            db.itm2box.insert(itm=item.id, box=unfiled.id)
            session.flash = 'Item "' + item.name + '" removed successfully and added to the "' + unfiled.name + '" box.'

        else:
            session.flash = 'Item "' + item.name + '" removed successfully.'

        session.flash_type = 'success'
        redirect(URL('view', args=box.id))

    return dict(box=box, form=form)

# IAPT Spring Assessment - Group 13

def view():
    item = load_item(request.args(0))
    guest = not auth.user or auth.user.id != item.auth_user
    boxes = item.itm2box(db.itm2box.box==db.box.id).select(db.box.id, db.box.name, db.box.unfiled)
    return dict(item=item, guest=guest, boxes=boxes.sort(lambda b: (not b.unfiled, b.name.lower())))

@auth.requires_login()
def new():
    # There's no actual logic needed here, the page is just a list of links
    return dict()

@auth.requires_login()
def new_of_type():
    type = request.args(0)
    if not type or type not in ITEM_TYPES:
        raise HTTP(400)

    form = SQLFORM.factory(
        db.itm.name,
        db.itm.itm_condition,
        db.itm.monetary_value,
        Field('box', 'reference box', requires=IS_IN_DB(db(db.box.auth_user==auth.user), 'box.id', 'box.name', zero=None, orderby='box.name'), required=True, notnull=True, comment='You can add this item to additional boxes after creating it'),
        db.itm.description,
        db.itm.thumbnail,
        submit_button='Add item'
    )

    if form.process().accepted:
        name = form.vars['name']
        item_id = db.itm.insert(
            name=name,
            itm_type=type,
            itm_condition=form.vars['itm_condition'],
            monetary_value=form.vars['monetary_value'],
            description=form.vars['description'],
            thumbnail=form.vars['thumbnail']
        )

        db.itm2box.insert(itm=item_id, box=form.vars['box'])

        session.flash = 'New item "'+ name + '" created successfully.'
        session.flash_type = 'success'

        redirect(URL('item', 'view', args=item_id))
        return

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    form.custom.widget.name['_autofocus'] = True

    # Move the unfiled box to the top of the list of boxes
    unfiled = load_unfiled_box()
    box_picker = form.element('#no_table_box')
    box_picker.element('option[value=' + str(unfiled.id) + ']', replace=None)
    box_picker.insert(0, OPTION(unfiled.name, _value=unfiled.id))

    # If we're creating this comic within a specified box (e.g. from a box's "New comic here" link)
    # then that box will be selected by default
    if 'box' in request.vars:
        in_box_id = request.vars['box']
        in_box = load_box(in_box_id, editing=True) # we already have the id, but load the box to check permissions
        box_picker.element('option[value=' + str(in_box.id) + ']')['_selected'] = 'selected'

    return dict(type=type, form=form)

def image():
    file = request.args(0)
    return response.stream(os.path.join(uploadfolder, file))

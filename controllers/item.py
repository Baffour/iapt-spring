# IAPT Spring Assessment - Group 13

def view():
    item = load_item(request.args(0))
    guest = not auth.user or auth.user.id != item.auth_user
    boxes = item.itm2box(db.itm2box.box==db.box.id).select(db.box.id, db.box.name, db.box.unfiled)
    return dict(item=item, guest=guest, boxes=boxes.sort(lambda b: (not b.unfiled, b.name.lower())))

@auth.requires_login()
def edit():
    item = load_item(request.args(0), editing=True)

    fields = [db.itm.name]
    extra_fields = _extra_fields_for(item.itm_type)
    fields += extra_fields
    fields += [
        db.itm.name,
        db.itm.itm_condition,
        Field('monetary_value', requires=IS_CURRENCY_VALUE(), notnull=True, required=True),
        db.itm.description,
        Field('thumbnail', type='upload', uploadfolder=uploadfolder, label="Thumbnail (uploaded file will replace existing image)")
    ]

    form = SQLFORM.factory(*fields, submit_button='Save item')

    if form.process().accepted:
        newvals = dict(
            name=form.vars['name'],
            itm_condition=form.vars['itm_condition'],
            monetary_value=form.vars['monetary_value'],
            description=form.vars['description']
        )

        extra_field_names = [f.name for f in extra_fields]
        extra_field_vals = dict((k, v) for k, v in form.vars.items() if k in extra_field_names)
        newvals.update(extra_field_vals)

        uploaded_image = form.vars['thumbnail']
        if uploaded_image:
            newvals['thumbnail'] = uploaded_image

        item.update(**newvals)
        item.update_record()

        session.flash = 'Item changes saved successfully'
        session.flash_type = 'success'
        redirect(URL('view', args=item.id))


    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    # Fill form with the item's current attributes
    form.element('input[name=name]')['_value'] = item.name
    form.element('select[name=itm_condition] option')['_selected'] = False # Deselects first option
    form.element('select[name=itm_condition] option[value={}]'.format(item.itm_condition))['_selected'] = True
    form.element('input[name=monetary_value]')['_value'] = format_pence_as_pounds(item.monetary_value)
    form.element('textarea[name=description]').append(item.description)

    for field in extra_fields:
        form.element('input[name={}]'.format(field.name))['_value'] = item[field.name]

    return dict(item=item, form=form)

@auth.requires_login()
def delete():
    item = load_item(request.args(0), editing=True)

    form = FORM.confirm('Delete', {'Cancel': URL('view', args=item.id)})
    form['_class'] = 'confirmation-form'
    form[0]['_class'] = 'btn btn-danger'
    form[1]['_class'] = 'btn btn-default'

    if form.accepted:
        item_name = item.name
        del db.itm[item.id]

        session.flash = 'Item "' + item_name + '" successfully deleted.'
        session.flash_type = 'success'
        redirect(URL('box', 'list')) # TODO: Is there a better destination possible?

    return dict(name=item.name, form=form)

@auth.requires_login()
def new():
    # There's no actual logic needed here, the page is just a list of links
    return dict()

@auth.requires_login()
def new_of_type():
    type = request.args(0)
    if not type or type not in ITEM_TYPES:
        raise HTTP(400)

    fields = [db.itm.name]
    extra_fields = _extra_fields_for(type)
    fields += extra_fields
    fields += [
        db.itm.name,
        db.itm.itm_condition,
        Field('monetary_value', requires=IS_CURRENCY_VALUE(), notnull=True, required=True),
        Field('box', 'reference box', requires=IS_IN_DB(db(db.box.auth_user==auth.user), 'box.id', 'box.name', zero=None, orderby='box.name'), required=True, notnull=True, comment='You can add this item to additional boxes after creating it'),
        db.itm.description,
        db.itm.thumbnail,
    ]

    form = SQLFORM.factory(*fields, submit_button='Add item')

    if form.process().accepted:
        name = form.vars['name']
        extra_field_names = [f.name for f in extra_fields]
        extra_field_vals = dict((k, v) for k, v in form.vars.items() if k in extra_field_names)
        item_id = db.itm.insert(
            name=name,
            itm_type=type,
            itm_condition=form.vars['itm_condition'],
            monetary_value=form.vars['monetary_value'],
            description=form.vars['description'],
            thumbnail=form.vars['thumbnail'],
            **extra_field_vals
        )

        compress_image(form.vars['thumbnail'])
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
        if in_box.id != unfiled.id:
            box_picker.element('option[value=' + str(in_box.id) + ']')['_selected'] = 'selected'

    return dict(type=type, form=form)

def image():
    file = request.args(0)
    return response.stream(os.path.join(uploadfolder, file))

@auth.requires_login()
def remove_from_box():
    item = load_item(request.args(0), editing=False)
    box = load_box(request.args(1), editing=False)

    itm2box = item.itm2box(db.itm2box.box==box.id)
    if itm2box.isempty() or (box.unfiled and item.itm2box.count() == 1): raise HTTP(400)
    itm2box.delete()

    if item.itm2box.isempty():
        unfiled = load_unfiled_box()
        db.itm2box.insert(itm=item.id, box=unfiled.id)
        session.flash = 'Item removed from box "' + box.name + '" successfully and moved to the "' + unfiled.name + '" box.'

    else:
        session.flash = 'Item removed from box "' + box.name + '" successfully.'

    session.flash_type = 'success'
    redirect(URL('view', args=item.id))

@auth.requires_login()
def add_to_box():
    item = load_item(request.args(0), editing=True)
    boxes = db((db.box.id==db.itm2box.box) & (db.itm2box.itm==item.id)).select(db.box.id)

    constraint = db((db.box.auth_user == auth.user) & (~db.box.id.belongs(list(boxes))))

    validator = IS_IN_DB(constraint, 'box.id', 'box.name', zero=None, orderby='box.name')
    form = SQLFORM.factory(Field('box', 'reference box', requires=validator, label="Box"),
                           submit_button='Add to this box')

    if form.process().accepted:
        box = load_box(form.vars['box'], editing=True)
        db.itm2box.insert(itm=item.id, box=box.id)

        session.flash = 'Item "' + item.name + '" added to "' + box.name + '" box successfully.'
        session.flash_type = 'success'
        redirect(URL('item', 'view', args=item.id))

    return dict(item=item, form=form, constraint=constraint)

def _extra_fields_for(typ):
    return [f for f in EXTRA_FIELDS[typ]] if typ in EXTRA_FIELDS else []

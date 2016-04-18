# IAPT Spring Assessment - Group 13

def view():
    user = user_from_request(request)
    guest = not auth.user or user.id != auth.user.id
    witems = db(db.want_item.auth_user==user.id).select().sort(lambda i: i.name.lower())
    witems.explore_info=[Tag.item_type]
    return dict(user=user, guest=guest, items=witems)

def view_item():
    item = db.want_item(request.args(0))
    guest = not auth.user or auth.user.id != item.auth_user
    return dict(item=item, guest=guest)

@auth.requires_login()
def new_item():
    # There's no actual logic needed here, the page is just a list of links
    return dict()

@auth.requires_login()
def new_item_of_type():
    type = request.args(0)
    if not type or type not in ITEM_TYPES:
        raise HTTP(400)

    fields = [db.want_item.name]
    extra_fields = _extra_fields_for(type)
    fields += extra_fields
    fields += [db.want_item.description, db.want_item.thumbnail]

    db.want_item.description.label=SPAN(db.want_item.description.label, SPAN(_class="optional-field"))
    form = SQLFORM.factory(*fields, submit_button='Add want item')

    if form.process().accepted:
        name = form.vars['name']
        extra_field_names = [f.name for f in extra_fields]
        extra_field_vals = dict((k, v) for k, v in form.vars.items() if k in extra_field_names)

        item_id = db.want_item.insert(
            name=name,
            itm_type=type,
            description=form.vars['description'],
            thumbnail=form.vars['thumbnail'],
            **extra_field_vals
        )

        compress_image(form.vars['thumbnail'])

        add_another = A("Add another", _href=URL('new_item'), _class="btn btn-primary add-another")
        session.flash = SPAN('New item "'+ name + '" created successfully.', add_another)
        session.flash_type = 'success'

        redirect(URL('view', args=auth.user.id))
        return

    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    form.custom.widget.name['_autofocus'] = True

    return dict(type=type, form=form)

@auth.requires_login()
def remove_item():
    constraint = db(db.want_item.auth_user==auth.user.id)
    validator = IS_IN_DB(constraint, 'want_item.id', 'want_item.name', zero=None, orderby='want_item.name')
    form = SQLFORM.factory(Field('want_item', 'reference want_item', requires=validator, label="Want Item"), submit_button='Delete want item')

    if form.process().accepted:
        want_item = load_want_item(form.vars['want_item'], editing=True)
        name = want_item.name
        del db.want_item[want_item.id]

        session.flash = 'Item "' + name + '" removed successfully.'
        session.flash_type = 'success'
        redirect(URL('view', args=auth.user.id))

    return dict(form=form)

@auth.requires_login()
def edit_item():
    item = db.want_item(request.args(0))
    if not item:
        raise HTTP(404)
    if item.auth_user != auth.user.id:
        raise HTTP(403)

    fields = [db.itm.name]
    extra_fields = _extra_fields_for(item.itm_type)
    fields += extra_fields
    fields += [
        db.itm.name,
        db.itm.description,
        Field('thumbnail', type='upload', uploadfolder=uploadfolder, label="Thumbnail (uploaded file will replace existing image)")
    ]

    db.itm.description.label=SPAN(db.itm.description.label, SPAN(_class="optional-field"))
    form = SQLFORM.factory(*fields, submit_button='Save want item')

    if form.process().accepted:
        newvals = dict(
            name=form.vars['name'],
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

        session.flash = 'Want item changes saved successfully'
        session.flash_type = 'success'
        redirect(URL('view_item', args=item.id))


    elif form.errors:
        response.flash = 'Invalid details entered. See the annotations below and try again.'
        response.flash_type = 'danger'

    # Fill form with the item's current attributes
    form.element('input[name=name]')['_value'] = item.name
    if len(form.element('textarea[name=description]')) == 0:
        form.element('textarea[name=description]').append(item.description)
    else:
        form.element('textarea[name=description]')[0]=item.description

    for field in extra_fields:
        form.element('input[name={}]'.format(field.name))['_value'] = item[field.name]

    return dict(item=item, form=form)

@auth.requires_login()
def delete_item():
    item = db.want_item(request.args(0))
    if not item:
        raise HTTP(404)
    if item.auth_user != auth.user.id:
        raise HTTP(403)

    form = FORM.confirm('Delete', {'Cancel': URL('view', args=item.id)})
    form['_class'] = 'confirmation-form'
    form[0]['_class'] = 'btn btn-danger'
    form[1]['_class'] = 'btn btn-default'

    if form.accepted:
        item_name = item.name
        del db.want_item[item.id]

        session.flash = 'Want item "' + item_name + '" successfully deleted.'
        session.flash_type = 'success'
        redirect(URL('want', 'view', args=auth.user.id))

    return dict(name=item.name, form=form)

def user_from_request(r):
    user = db.auth_user(r.args(0))
    if not user:
        raise HTTP(404)
    return user

def _extra_fields_for(typ):
    return [f for f in EXTRA_FIELDS[typ]] if typ in EXTRA_FIELDS else []

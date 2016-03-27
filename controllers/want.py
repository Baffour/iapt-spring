# IAPT Spring Assessment - Group 13

def view():
    user = user_from_request(request)
    guest = not auth.user or user.id != auth.user.id
    witems = db(db.want_item.auth_user==user.id).select().sort(lambda i: i.name.lower())
    return dict(user=user, guest=guest, items=witems)

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

        session.flash = 'New want item "'+ name + '" created successfully.'
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
    pass

def user_from_request(r):
    user = db.auth_user(r.args(0))
    if not user:
        raise HTTP(404)
    return user

def _extra_fields_for(typ):
    return [f for f in EXTRA_FIELDS[typ]] if typ in EXTRA_FIELDS else []

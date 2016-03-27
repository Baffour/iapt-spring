# IAPT Spring Assessment - Group 13

def view():
    user = user_from_request(request)
    guest = auth.user is None or user.id != auth.user.id

    iquery = db((db.itm.auth_user==user.id) & (db.itm.in_have_list==True))
    items = iquery.select().sort(lambda i: i.name.lower())

    full = not guest and len(items) == db(db.itm.auth_user==auth.user).count()
    return dict(user=user, guest=guest, items=items, full=full)

@auth.requires_login()
def insert_item():
    items = db((db.itm.auth_user==auth.user.id) & (db.itm.in_have_list==True)).select()
    item_ids_in_list = [i.id for i in items]

    constraint = db(~db.itm.id.belongs(item_ids_in_list) & (db.itm.auth_user == auth.user.id))
    validator = IS_IN_DB(constraint, 'itm.id', 'itm.name', zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Add to Have List')

    if form.process().accepted:
        itm = load_item(form.vars['itm'], editing=True)
        itm.in_have_list = True
        itm.update_record()

        session.flash = 'Item "' + itm.name + '" added to Have List successfully.'
        session.flash_type = 'success'
        redirect(URL('view', args=auth.user.id))

    return dict(form=form)

@auth.requires_login()
def remove_item():
    constraint = db((db.itm.auth_user==auth.user.id) & (db.itm.in_have_list==True))
    validator = IS_IN_DB(constraint, 'itm.id', 'itm.name', zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Remove from Have List')

    if form.process().accepted:
        item = load_item(form.vars['itm'], editing=True)
        item.in_have_list = False
        item.update_record()

        session.flash = 'Item "' + item.name + '" removed successfully.'
        session.flash_type = 'success'
        redirect(URL('view', args=auth.user.id))

    return dict(form=form)

def user_from_request(r):
    user = db.auth_user(r.args(0))
    if not user:
        raise HTTP(404)
    return user

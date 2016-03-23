# IAPT Spring Assessment - Group 13

@auth.requires_login()
def list():
    return dict()

@auth.requires_login()
def new():
    widget = SQLFORM.widgets.autocomplete(request, db.auth_user.username, db=db(db.auth_user.id!=auth.user.id), limitby=(0,10), min_length=1)
    form = SQLFORM.factory(Field('user', widget=widget, required=True, notnull=True, label="User to trade with", comment="Start typing above and matching users will appear"), submit_button="Propose a trade with this user")

    if form.process().accepted:
        username = form.vars['user']
        user = db.auth_user(db.auth_user.username==username)

        if not user:
            response.flash = 'User "{}" does not exist. Try entering a valid username.'.format(username)
            response.flash_type = 'danger'
        elif user.id == auth.user.id:
            raise HTTP(400) # A user cannot trade with themself
        else:
            propid = db.trade_proposal.insert(target=user)
            redirect(URL('choose_items', args=propid))
            return

    form.element('#no_table_user')['_class'] += ' form-control'
    return dict(form=form)

@auth.requires_login()
def choose_items():
    prop = load_trade_proposal(request.args(0), editing=True)
    if prop.status != 'pending':
        raise HTTP(400)
    target = db.auth_user(prop.target)

    oi_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==auth.user.id))
    offered_items = oi_query.select(db.itm.ALL)

    wi_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==target.id))
    wanted_items = wi_query.select(db.itm.ALL)

    return dict(prop=prop, target=target, offered_items=offered_items, wanted_items=wanted_items)

@auth.requires_login()
def add_offered_item():
    return dict()

@auth.requires_login()
def remove_offered_item():
    return dict()

@auth.requires_login()
def add_requested_item():
    return dict()

@auth.requires_login()
def remove_requested_item():
    return dict()

@auth.requires_login()
def view():
    pass

@auth.requires_login()
def accept():
    pass

@auth.requires_login()
def reject():
    pass

@auth.requires_login()
def delete():
    pass

@auth.requires_login()
def counter():
    pass

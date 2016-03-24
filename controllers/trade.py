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

    ri_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==target.id))
    requested_items = ri_query.select(db.itm.ALL)

    return dict(prop=prop, target=target, offered_items=offered_items, requested_items=requested_items)

@auth.requires_login()
def add_offered_item():
    prop = load_trade_proposal(request.args(0), editing=True)
    target = db.auth_user(prop.target)

    oi_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==auth.user.id))
    oi_ids = oi_query.select(db.itm.id)

    constraint = db(~db.itm.id.belongs(oi_ids) & (db.itm.auth_user == auth.user.id))
    reprfn = lambda i: "{} ({}, {} condition, {})".format(i.name, i.itm_type, i.itm_condition, format_pence_as_pounds(i.monetary_value))
    validator = IS_IN_DB(constraint, 'itm.id', reprfn, zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Add to this trade')

    if form.process().accepted:
        itm = load_item(form.vars['itm'], editing=True)
        db.itm2trade_proposal.insert(itm=itm.id, trade_proposal=prop.id)
        redirect(URL('choose_items', args=prop.id))
        return

    return dict(target=target, form=form)

@auth.requires_login()
def remove_offered_item():
    if request.env.request_method != "POST":
        raise HTTP(405)

    prop = load_trade_proposal(request.args(0), editing=True)
    item = load_item(request.args(1))

    if prop.status == 'pending':
        if prop.sender == item.auth_user:
            itm2tp = item.itm2trade_proposal(db.itm2trade_proposal.trade_proposal==prop.id)
            if itm2tp.isempty(): raise HTTP(400)
            itm2tp.delete()
            redirect(URL('choose_items', args=prop.id))
        else:
            raise HTTP(403)
    else:
        raise HTTP(400) # TODO: Handle other prop statuses if needed

@auth.requires_login()
def add_requested_item():
    prop = load_trade_proposal(request.args(0), editing=True)
    target = db.auth_user(prop.target)

    ri_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==target.id))
    ri_ids = ri_query.select(db.itm.id)

    target_user_items = db(~db.itm.id.belongs(ri_ids) & (db.itm.auth_user==target.id)).select()
    ri_selectable_ids = [item.id for item in target_user_items if is_public(item)]

    constraint = db(db.itm.id.belongs(ri_selectable_ids))
    reprfn = lambda i: "{} ({}, {} condition, {})".format(i.name, i.itm_type, i.itm_condition, format_pence_as_pounds(i.monetary_value))
    validator = IS_IN_DB(constraint, 'itm.id', reprfn, zero=None, orderby='itm.name')
    form = SQLFORM.factory(Field('itm', 'reference itm', requires=validator, label="Item"), submit_button='Add to this trade')

    if form.process().accepted:
        itm = load_item(form.vars['itm'])

        if itm.auth_user != target.id or not is_public(itm):
            raise HTTP(403)

        db.itm2trade_proposal.insert(itm=itm.id, trade_proposal=prop.id)
        redirect(URL('choose_items', args=prop.id))
        return

    return dict(target=target, form=form)

def is_public(item):
    return item.itm2box((db.itm2box.box==db.box.id) & (db.box.private==False)).count() > 0

@auth.requires_login()
def remove_requested_item():
    if request.env.request_method != "POST":
        raise HTTP(405)

    prop = load_trade_proposal(request.args(0), editing=True)
    item = load_item(request.args(1))

    if prop.status == 'pending':
        if prop.target == item.auth_user:
            itm2tp = item.itm2trade_proposal(db.itm2trade_proposal.trade_proposal==prop.id)
            if itm2tp.isempty(): raise HTTP(400)
            itm2tp.delete()
            redirect(URL('choose_items', args=prop.id))
        else:
            raise HTTP(403)
    else:
        raise HTTP(400) # TODO: Handle other prop statuses if needed

@auth.requires_login()
def confirm():
    prop = load_trade_proposal(request.args(0), editing=True)
    if prop.status != 'pending':
        raise HTTP(400)
    target = db.auth_user(prop.target)

    oi_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==auth.user.id))
    ocount = oi_query.count()
    if not ocount: raise HTTP(400)

    ri_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==target.id))
    rcount = ri_query.count()

    form = SQLFORM.factory(db.trade_proposal.msg, submit_button="Send trade proposal")

    if form.process().accepted:
        prop.msg = form.vars['msg']
        prop.status = 'sent'
        prop.created_at = request.now
        prop.update_record()

        db.notification.insert(
            auth_user=target.id,
            msg="{} proposed a trade with you.".format(auth.user.username),
            link=URL('trade', 'view', args=prop.id),
            link_text="View and respond to this proposal"
        )

        session.flash = "Trade proposal sent to {} successfully.".format(target.username)
        session.flash_type = 'success'
        redirect(URL('list'))
        return

    return dict(form=form, target=target, ocount=ocount, rcount=rcount)

@auth.requires_login()
def cancel():
    if request.env.request_method != "POST":
        raise HTTP(405)

    prop = load_trade_proposal(request.args(0), editing=True)
    if prop.status != 'pending':
        raise HTTP(400)

    del db.trade_proposal[prop.id]
    redirect(URL('new'))

@auth.requires_login()
def view():
    prop = load_trade_proposal(request.args(0))
    sender = db.auth_user(prop.sender)
    target = db.auth_user(prop.target)

    oi_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==sender.id))
    offered_items = oi_query.select(db.itm.ALL)

    ri_query = prop.itm2trade_proposal((db.itm2trade_proposal.itm==db.itm.id) & (db.itm.auth_user==target.id))
    requested_items = ri_query.select(db.itm.ALL)

    return dict(prop=prop, sender=sender, offered_items=offered_items, requested_items=requested_items)

@auth.requires_login()
def accept():
    pass

@auth.requires_login()
def reject():
    pass

@auth.requires_login()
def counter():
    pass

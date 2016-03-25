# IAPT Spring Assessment - Group 13

def index():
    if auth.user is None:
        redirect(URL('welcome'))
    no_items = db(db.itm.auth_user==auth.user.id).count() == 0


    rpquery = db((db.trade_proposal.target==auth.user.id) & (db.trade_proposal.status!='pending'))
    rec_props = rpquery.select().sort(lambda p: (p.status == 'sent', p.created_at), reverse=True)[0:10]

    return dict(no_items=no_items, received_proposals=rec_props)

def welcome():
    form = custom_register_form()
    return dict(registerform=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def profile_page():
    username = request.vars.user
    return "TODO: Create Personal Profile Page.\nUser:{0}".format(username)

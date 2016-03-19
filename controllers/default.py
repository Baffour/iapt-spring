# IAPT Spring Assessment - Group 13

def index():
    # TODO: Controller content
    if auth.user is None:
        redirect(URL('welcome'))
    return dict()

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
    user = db(db.auth_user.username == username).select().first()
    if user is None:
        return HTTP(404)
    return dict(user=user)

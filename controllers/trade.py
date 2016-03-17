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
            redirect(URL('edit', args=propid))
            return

    form.element('#no_table_user')['_class'] += ' form-control'
    return dict(form=form)

@auth.requires_login()
def edit():
    pass

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

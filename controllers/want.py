# IAPT Spring Assessment - Group 13

def view():
    user = user_from_request(request)
    guest = user.id != auth.user.id
    witems = db(db.want_item.auth_user==user.id).select().sort(lambda i: i.name.lower())
    return dict(user=user, guest=guest, items=witems)

@auth.requires_login()
def add_item():
    pass

@auth.requires_login()
def remove_item():
    pass

def user_from_request(r):
    user = db.auth_user(r.args(0))
    if not user:
        raise HTTP(404)
    return user

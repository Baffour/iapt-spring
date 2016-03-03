# IAPT Spring Assessment - Group 13

def create_unfiled_box(form):
    db.box.insert(
        name="Unfiled",
        private=True,
        unfiled=True,
        auth_user=form.vars.id
    )

auth.settings.register_onaccept.append(create_unfiled_box)

def create_email_changed_notification(form):
    if form.vars.email != auth.user.email:
        msg = """Your email address was changed from {} to {}.
        If this wasn't you, you should start to panic now!""".format(auth.user.email, form.vars.email)
        db.notification.insert(msg=msg, link_text="Check your profile now", link=URL('default', 'user/profile'))

auth.settings.profile_onvalidation.append(create_email_changed_notification)

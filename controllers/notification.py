# IAPT Spring Assessment - Group 13

@auth.requires_login()
def inbox():
    notifications = db(db.notification.auth_user==auth.user).select().sort(lambda row: row.created_at, reverse=True)
    for n in notifications:
        if n.unread:
            n.unread = False
            n.update_record()
            n.new = True
        else:
            n.new = False
    return dict(notifications=notifications)

def update_count():
    return notification_count()

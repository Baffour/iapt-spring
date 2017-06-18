# IAPT Spring Assessment - Group 13

from gluon.tools import Auth

auth = Auth(db)

# Create all tables needed by auth
auth.define_tables(username=True, signature=False)

# Disable sending emails
auth.settings.mailer.settings.server = 'logging'

# Disable actions that we don't need for the assessment
auth.settings.actions_disabled = [
    'retrieve_password',
    'bulk_register',
    'request_reset_password'
]

auth.settings.actions_disabled.append('register')

# Hide the first name and last name fields
# (apparently this is a lot less complicated than removing them altogether)
db.auth_user.first_name.readable = db.auth_user.first_name.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False

request.requires_https()

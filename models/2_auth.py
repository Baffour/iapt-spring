# IAPT Spring Assessment - Group 13

from gluon.tools import Auth

auth = Auth(db)

# Create all tables needed by auth
auth.define_tables(username=True, signature=False)

# Disable sending emails
auth.settings.mailer.settings.server = 'logging'

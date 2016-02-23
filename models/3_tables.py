# IAPT Spring Assessment - Group 13

OBJECT_TYPES = ['book', 'cd', 'dvd', 'game']
OBJECT_CONDITIONS = ['unspecified', 'poor', 'reasonable', 'good', 'mint']

db.define_table('obj',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('obj_type', type='string', notnull=True, required=True, requires=IS_IN_SET(OBJECT_TYPES), label="Object Type"),
    Field('monetary_value', type='integer', notnull=True, required=False, requires=IS_INT_IN_RANGE(1, 1000000)),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('obj_condition', type='string', notnull=True, required=True, default='unspecified', requires=IS_IN_SET(OBJECT_CONDITIONS), label="Condition"),
    Field('description', type='text', required=True, comment="Tell your object's story in your own words"),
    Field('thumbnail', type='upload', uploadfolder=uploadfolder, notnull=True),
    Field('in_have_list', type='boolean', default=False, notnull=True, writable=False, readable=False)
)

db.define_table('box',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('private', type='boolean', default=True, notnull=True, label='Private (private collections are invisible to other users)'),
    Field('created_at', type='datetime', default=request.now, writable=False, readable=False)
)

db.define_table('obj2box',
    Field('obj', 'reference obj', notnull=True, required=True),
    Field('box', 'reference box', notnull=True, required=True)
)

PROPOSAL_STATUSES = ['pending', 'sent', 'accepted', 'rejected', 'superseded']

db.define_table('trade_proposal',
    Field('sender', 'reference auth_user', notnull=True, required=True),
    Field('received', 'reference auth_user', notnull=True, required=True),
    Field('status', type='string', notnull=True, required=True, default='pending', requires=IS_IN_SET(PROPOSAL_STATUSES)),
    Field('msg', type='text', notnull=True, comment="Send a message with your proposal"),
    Field('created_at', type='datetime', default=request.now, writable=False, readable=False),
    Field('parent', 'reference trade_proposal', notnull=True, required=False)
)

db.define_table('want_item',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('thing_type', type='string', notnull=True, required=True, requires=IS_IN_SET(OBJECT_TYPES)),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('description', type='text', required=True),
    Field('source_obj', 'reference obj', notnull=True, required=False, writable=False)
)

db.define_table('notification',
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('msg', type='text', notnull=True, required=True),
    Field('link', type='string', length=256, notnull=True, required=False),
    Field('created_at', type='datetime', default=request.now, writable=False, readable=False),
    Field('unread', type='boolean', required=True, notnull=True, default=True)
)

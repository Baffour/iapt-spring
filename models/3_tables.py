# IAPT Spring Assessment - Group 13

import copy

ITEM_TYPES = {
    'book' : 'book',
    'cd' : 'album',
    'dvd' : 'movie',
    'game' : 'game'
}

ITEM_CONDITIONS = ['unspecified', 'poor', 'reasonable', 'good', 'mint']

EXTRA_FIELDS = {
    'cd' : [Field('artist', type='string', length=256, notnull=True, required=False)],
    'book': [Field('author', type='string', length=256, notnull=True, required=False)]
}

def _flatten_and_make_nullable(list):
    out = []
    for fields in EXTRA_FIELDS.values():
        for field in fields:
            copied = copy.copy(field)
            copied.notnull = False
            out.append(copied)
    return out

db.define_table('itm',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('itm_type', type='string', notnull=True, required=True, requires=IS_IN_SET(ITEM_TYPES), label="Item Type"),
    Field('monetary_value', type='integer', notnull=True, required=False, requires=IS_INT_IN_RANGE(1, 1000000)),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('itm_condition', type='string', notnull=True, required=True, default='unspecified',
        requires=IS_IN_SET(ITEM_CONDITIONS, zero=None, labels=[c.capitalize() for c in ITEM_CONDITIONS]), label="Condition"),
    Field('description', type='text', required=True, comment="Tell your item's story in your own words"),
    Field('thumbnail', type='upload', uploadfolder=uploadfolder, notnull=True,requires=IS_NOT_EMPTY("Please upload an image of your item")),
    Field('in_have_list', type='boolean', default=False, notnull=True, writable=False, readable=False),
    *_flatten_and_make_nullable(EXTRA_FIELDS)
)

db.define_table('box',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('private', type='boolean', default=True, notnull=True, label='Private (private boxes are invisible to other users)'),
    Field('created_at', type='datetime', default=request.now, writable=False, readable=False),
    Field('unfiled', type='boolean', default=False, notnull=True, writable=False, readable=False)
)

db.define_table('itm2box',
    Field('itm', 'reference itm', notnull=True, required=True),
    Field('box', 'reference box', notnull=True, required=True)
)

PROPOSAL_STATUSES = ['pending', 'sent', 'accepted', 'rejected', 'superseded']

db.define_table('trade_proposal',
    Field('sender', 'reference auth_user', notnull=True, required=True, default=auth.user),
    Field('target', 'reference auth_user', notnull=True, required=True),
    Field('status', type='string', notnull=True, required=True, default='pending', requires=IS_IN_SET(PROPOSAL_STATUSES)),
    Field('created_at', type='datetime', writable=False, readable=False),
    Field('parent', 'reference trade_proposal', notnull=False, required=False)
)

db.define_table('itm2trade_proposal',
    Field('itm', 'reference itm', notnull=True, required=True),
    Field('trade_proposal', 'reference trade_proposal', notnull=True, required=True)
)

db.define_table('want_item',
    Field('name', type='string', length=256, notnull=True, required=True),
    Field('itm_type', type='string', notnull=True, required=True, requires=IS_IN_SET(ITEM_TYPES)),
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('description', type='text', required=True),
    Field('source_itm', 'reference itm', notnull=False, required=False),
    Field('thumbnail', type='upload', uploadfolder=uploadfolder, notnull=True, requires=IS_NOT_EMPTY("Please upload an image of your item")),
    *_flatten_and_make_nullable(EXTRA_FIELDS)
)

db.define_table('notification',
    Field('auth_user', 'reference auth_user', default=auth.user, required=True, notnull=True, writable=False, readable=False),
    Field('msg', type='text', notnull=True, required=True),
    Field('link', type='string', length=256, notnull=False, required=False),
    Field('link_text', type='string', length=256, notnull=False, required=False),
    Field('created_at', type='datetime', default=request.now, writable=False, readable=False),
    Field('unread', type='boolean', required=True, notnull=True, default=True)
)

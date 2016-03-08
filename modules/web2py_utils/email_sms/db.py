#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#


from gluon.sql import Field

from carriers import CARRIERS

fields = {
    'name': Field('name', notnull=True, unique=True,),
    'gateway': Field('gateway', notnull=True,),
    
    
    'email': Field('email', requires=IS_NULL_OR(IS_EMAIL())),
    'phone': Field('phone', 
                    requires=IS_NULL_OR(IS_LENGTH(10,10))
                  ),
    'carrier': Field('carrier', 'reference carrier',)               
}

def make_carriers(db, tablename='carrier',):
    return db.define_table(tablename,
        fields['name'], fields['gateway']
    )
    
def populate_carriers(db, tablename='carrier'):
    if db(db[tablename].id > 0).count == 0:
        for c in CARRIERS:
            db[tablename].insert(
                name = c['fields']['name'],
                gateway = c['fields']['gateway'],
            )
        return True
    else:
        return False
    
def SMSVirtual(tablename, phone_field='phone', carrier_field='carrier'):
    class _SMSVirtual():
        def sms(self):
            if self[tablename].get(carrier_field):
                return self[tablename][field].gateway % dict(phone_number = self[tablename][phone_field])
            else:
                return None

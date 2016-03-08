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

from datetime import datetime

from gluon.sql import Field
from gluon.storage import Storage

class Configure():
    """
    This class implements a configurable set of options
    for use in anything that needs settings that
    are to be stored in the database.
    """
    def __init__(self, database,
                    auto_define=True,
                    migrate=True,
                    fake_migrate=False,
                    cache=None):
        """
        Initialize configure class.

        Keyword arugments:
        database -- web2py DAL instance
        auto_define -- auto define database tables (default: True)
        migrate -- migrate the database tables (default: True)
        cache -- cache object to use for pulling database settings,
                this is a tuple object consisting of cache object
                and cache timeout. Default No Cache!
                (Cache(r).ram, 1500)
        """
        self.db = database
        self.cache = cache
        if auto_define:
            self.define_tables(migrate=migrate, fake_migrate=fake_migrate)
            self._get_settings()

    def define_tables(self, migrate=True, fake_migrate=False):
        """
        Defines the database tables needed to function
        """
        self.db.define_table('settings',
            Field('kkey'),
            Field('name'),
            Field('value', 'text'),
            Field('value_type'),
            Field('description', 'text'),
            Field('created_on', 'datetime'),
            Field('modified_on', 'datetime'),
            migrate=migrate, fake_migrate=fake_migrate
        )

        self.db.settings.created_on.default = datetime.now()
        self.db.settings.modified_on.update = datetime.now()

        self.db.settings.description.writable = False
        self.db.settings.kkey.writable = False
        self.db.settings.name.writable = False
        self.db.settings.value_type.writable = False
        
        self.db.settings.created_on.writable = False
        self.db.settings.created_on.readable = False
        self.db.settings.modified_on.writable = False
        self.db.settings.modified_on.readable = False



    def _get_settings(self):
        """
        Retreives the settings from the database and
        stores them in a storage dictionary
        """
        settings = Storage()

        rows = self.db(self.db.settings.id > 0).select(cache=self.cache)

        for row in rows:
            if not settings.has_key(row.kkey):
                settings[row.kkey] = Storage()
            settings[row.kkey][row.name] = row

        self.settings = settings

    def verify(self, kkey, settings):
        """
        Adds the configuration to memory, and assures that the
        configuration exists in the database (DAL for web2py).

        If there are no database entries, it will create the table,
        and fill in the default values, otherwise it will poll
        the database for the information.

        Keyword arguments:
        kkey -- unique name for a set of configuration options
                examples include, 'blog', 'cache', 'rss'
        items -- dictionary of configs to store into the database.
                in the format of
                {'key_name': { 'value': default, 'description': 'a desc' }}

                Example:
                    {'display_count': {
                        'value': 4,
                        'description': "Number of posts to display per-page",},}
        """
        for name, info in settings.iteritems():
            row = self.db(
                  (self.db.settings.kkey == kkey)
                & (self.db.settings.name == name)
            ).select().first()

            if not row:
                value = info.get('value', None)

                if isinstance(value, bool):
                    type = "bool"
                elif isinstance(value, int):
                    type = "int"
                elif isinstance(value, long):
                    type = "long"
                elif isinstance(value, float):
                    type = "float"
                else:
                    type = "str"

                record = self.db.settings.insert(
                 kkey=kkey,
                 name=name,
                 value=value,
                 value_type=type,
                 description=info.get('description', None)
                )
                if not self.settings.has_key(kkey):
                    self.settings[kkey] = Storage()
                self.settings[kkey][name] = record

    def read(self, kkey, name):
        """
        Returns the value of a settings object

        Keyword arguments:
        kkey -- keyname
        name -- setting name
        """
        r = self.settings[kkey][name]

        if r.value_type == "str":
            return r.value
        elif r.value_type == "int":
            return int(r.value)
        elif r.value_type == "long":
            return long(r.value)
        elif r.value_type == "float":
            return float(r.value)
        elif r.value_type == "bool":
            if r.value == "True":
                return True
            else:
                return False
        else:
            return r

    def write(self, kkey, name, value):
        """
        Writes a setting to the database

        Keyword arguments:
        kkey -- keyname
        name -- setting name
        value -- value for the setting
        """
        if isinstance(value, int):
            type = "int"
        elif isinstance(value, long):
            type = "long"
        elif isinstance(value, float):
            type = "float"
        elif isinstance(value, bool):
            type = "bool"
        else:
            type = "str"
        self.settings[kkey][name].value = value
        self.settings[kkey][name].value_type = type
        self.settings[kkey][name].update_record()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


"""
    py2jquery (Python 2 jQuery)
    Developed by Thadeus Burgess <thadeusb@thadeusb.com>
    License: GPL v2
        Inspired by Nathan Freeze's Client Tools for web2py
        
    This is a set of classes and functions for managing client events 
    and resources from a python server.
"""
import urllib
import os
import string
from random import random

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *

from py2jquery import *

__all__ = ['Rating',]

"""

manager = Manager(globals())

db.define_table("image", Field("name"))

db.define_table("comments", Field("Rating", "integer")

db.comments.Rating.widget = RatingPlugin.form_widget(manager, cancel: true)

image_ratings = RatingPlugin(db, db.image, "img_ratings", manager)
image_ratings.define_tables()

def index():
    posts = db.select(ALL posts)
    
    return posts
    
record_img_rating = image_ratings.register_recorder(URL(init/default/record_rating))



{{
for each post
    print post info
    
    image_ratings.widget(post.id, value=None)
    
}}

"""


"""####################################
           WIDGETS
"""####################################

class RatingPlugin(object):
    def __init__(self, 
            db, tableref, name="ratings",
            manager=None, cancel=True,):
        pass
            
    
    def define_tables(self, db, tableref, name="ratings"):
        self._db = db
        self._tableref = tableref
        self._name = name
    
        db.define_table(name,
            Field("id_ref", tableref),
            Field("rating", "integer", widget=self.form_widget),
        )
        
        self._table = db[name]
        
    def average_rating(self, dbid=None):
        if dbid:
            ratings = self._db(self._table.id_ref == dbid).select()
        else:
            ratings = self._db().select(self._table.ALL)
        
        total = count = average = 0
        
        for r in ratings:
            total += r.rating
            count += 1
                
        try:
            average = total / count
        except:
            average = -1
            
        return average
        
    def record_rating(self, dbid, value):
        self._table.insert(id_ref=dbid, rating=value)
        return self.average_rating(dbid)

    

class Rating(object):
    """
    A class for implementing a rating widget (usually star).
    """
    def __init__(self, manager, url=None, onclick=None, cancel=False, disabled=False, _dom="div", _class='rating_widget'):
        manager.require('jquery.rating')
        
        if cancel:
            cancel = "true"
        else:
            cancel = "false"
            
        if not url:
            url = "false"
        else:
            url = '"%s"' % url

        if not disabled:
            disabled = "false"
        else:
            disabled = 'true'

        if not onclick:
        	onclick = "function() {}"
        
        manager.add(Script("""
            $(".%s").rating({cancel:%s, dom:"%s", ajax: %s, click_after: %s, disabled: %s});
        """ % (_class, cancel, _dom, url, onclick, disabled), is_function=True, uuid=_class), True)

        self._class = _class
        self._dom = _dom
        self.url = url
        self.manager = manager
    
    def widget(self, value=0, number=5, dbid=None):
        if not dbid:
            dbid = hash("%sE%sE%s_%s" % (value, number, self._class, self.manager.environment.request.now))
        if not self.url:
            dbid += hash("%s%s" % (self.manager.environment.request.now, random()))

        xml = """
        <div class="%s" id="rating_%s" dbid="%s" num="%s" val="%s">%s</div>
        """ % (self._class, dbid, dbid, number, value, value)
        
        return xml     
          
    @staticmethod
    def form_widget(field, value, **attributes):
            
        requires = field.requires
            
        if isinstance(requires, (list, tuple)):
            raise NotImplementedError
              
        cancel = attributes.get('cancel', 'true')
        manager = attributes.get('manager', None)
                
        if manager:
            manager.add(Script("""
                $("#%s").rating({cancel:%s});
            """ % (id(field), cancel)), True)
          
        return DIV(INPUT(_name=field.name, _type='hidden', _id='rating_input_%s' % (id(field))), 
                    DIV(_class='rating_widget', _val=value, _num=len(requires.theset), _dbid=id(field), _id=id(field)),
                    _class="rating")

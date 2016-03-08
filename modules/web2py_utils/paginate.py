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


from gluon.html import A, URL
from gluon.cache import Cache

class Pagination():
    def __init__(self, db, query, 
                 orderby, current=None, 
                 display_count=4, cache=None,
                 r=None, res=None):
        self.db = db
        self.query = query
        self.orderby = orderby
        if not current:
            if not r.vars.p:
                current = 0
            else:
                current = int(r.vars.p)
        elif not isinstance(current, int):
            current = int(current)
        self.current = current
        self.display_count = display_count
        self.r = r
        self.res = res
        if not cache:
            self.cache = (Cache(r).ram, 1500)
        else:
            self.cache = cache
        
    def get_set(self, set_links = True):
        self.set = self.db(self.query).select(
            orderby=self.orderby, limitby=(
                self.current, self.current+self.display_count
                ), cache=self.cache
            )
        self.num_results = len(self.set)
        self.total_results = self.db(self.query).count()
        if set_links:
            self.res.paginate_links = self.generate_links()
            
        return self.set
    
    def generate_links(self):
        self.backward = A('<< previous()', _href=URL(r=self.r, args=self.r.args, vars={'p': self.current - self.display_count})) if self.current else '<< previous(False)'
        self.forward = A('next() >>', _href=URL(r=self.r, args=self.r.args, vars={'p': self.current + self.display_count})) if self.total_results > self.current + self.display_count else 'next(False) >>'
        self.location = 'Showing %d to %d out of %d records' % (self.current + 1, self.current + self.num_results, self.total_results)
        return (self.backward, self.forward, self.location)

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

dbcategory = plugin_category.CategoryPlugin(db)()

"""

from gluon.sql import *
from gluon.sqlhtml import *
from gluon.html import *
from gluon.validators import *

class CategoryPlugin():
    title = "Categorizor"
    author = "Thadeus Burgess <thadeusb@thadeusb.com>"
    keywords = "categories, categorize, organization"
    description = "Defines database models and functions for categorization"
    copyright = "GPL v2"

    def __init__(self, db, tablename="plugin_category"):
        self._db = db
        self._tablename = tablename
        
    def __call__(self, *args, **kwargs):
        self.define_tables(*args, **kwargs)
        return self
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._db[self._tablename][key]
        elif isinstance(key, str):
            return self._db(self._db[self._tablename].name == key).select()
        else:
            raise TypeError("Key must be of type string or int")
        
    def define_tables(self, migrate_db=True):
        self._table = self._db.define_table(self._tablename,
            Field("name", "string", unique=True),
            Field("description", "text"),
            Field('lft', 'integer'),
            Field('rgt', 'integer'),
            migrate=migrate_db
        )
        
        self._table.name.requires = [
                    IS_NOT_IN_DB(self._db, '%s.name' % self._tablename), 
                    IS_NOT_EMPTY()
        ]
        self.table = self._table
        self.fid = "%s.id" % self._tablename
        self.fname = "%s.name" % self._tablename
        
        self.requires = lambda multiple: IS_IN_DB(self._db, self.fid, self.fname, multiple=multiple)
        
        def repr(sep):
            def r(value):
                s = ''
                for i in value.split('|'):
                    try:               
                        c = self[int(i)]
                        s += c.name + sep
                    except:
                        pass
                return s
            return r
                    
        self.represent = repr
        
    def add_node(self, name, parent_name=None, description=""):
        """
        add_node('Food', None)
        add_node('Meat', 'Food')
        add_node('Fruit', 'Food')
        add_node('Apple', 'Fruit')
        """
        if parent_name:
            if isinstance(parent_name, int):
                parent = self._db(self._db[self._tablename].id == parent_name).select().first()
            else:
                parent = self._db(self._db[self._tablename].name == parent_name).select().first()
            self._db(self._db[self._tablename].rgt >= parent.rgt).update(rgt=self._db[self._tablename].rgt+2)
            self._db(self._db[self._tablename].lft >= parent.rgt).update(lft=self._db[self._tablename].lft+2)
            node_id = self._db[self._tablename].insert(name=name, description=description, lft=parent.rgt, rgt=parent.rgt+1)
        else:
            top = self._db(self._db[self._tablename].lft > 0).select(orderby=self._db[self._tablename].rgt).last()
            if top:
                node_id = self._db[self._tablename].insert(name=name, description=description, lft=top.rgt+1, rgt=top.rgt+2)
            else:
                node_id = self._db[self._tablename].insert(name=name, description=description, lft=1, rgt=2)
                
        return node_id
        
    def add_node_left_of(self, name, left_of, description=""):
        """
        add_node_left_of('Toys', 'Food')
        """
        lft_of = self._db(self._db[self._tablename].name == left_of).select().first()
        if lft_of:
            self._db(self._db[self._tablename].rgt >= lft_of.rgt).update(rgt=self._db[self._tablename].rgt+2)
            self._db(self._db[self._tablename].lft >= lft_of.lft).update(lft=self._db[self._tablename].lft+2)
            node_id = self._db[self._tablename].insert(name=name, description=description, lft=lft_of.lft, rgt=lft_of.lft+1)
        else:
            raise ValueError("There is no lft of value: %s" % left_of)
        return node_id
        
    def add_node_right_of(self, name, right_of, description=""):
        """
        add_node_left_of('Toys', 'Food')
        """
        rgt_of = self._db(self._db[self._tablename].name == right_of).select().first()
        if rgt_of:
            self._db(self._db[self._tablename].rgt >= rgt_of.rgt+1).update(rgt=self._db[self._tablename].rgt+2)
            self._db(self._db[self._tablename].lft >= rgt_of.rgt).update(lft=self._db[self._tablename].lft+2)
            node_id = self._db[self._tablename].insert(name=name, description=description, lft=rgt_of.rgt+1, rgt=rgt_of.rgt+2)
        else:
            raise ValueError("There is no lft of value: %s" % right_of)
        return node_id
        
    def delete_node(self, name):
        """
        This will delete all children of this node!
        """
        node = self._db(self._db[self._tablename].name == name).select().first()
        if node:
            children = self._db(self._db[self._tablename].lft >= node.lft)(self._db[self._tablename].rgt <= node.rgt)
            
            diff = node.rgt - node.lft + 1
            rgt = node.rgt
            lft = node.lft
            
            children.delete()
            #node.delete()
            self._db(self._db[self._tablename].id == node.id).delete()
            
            self._db(self._db[self._tablename].lft > rgt).update(lft=self._db[self._tablename].lft - diff)
            self._db(self._db[self._tablename].rgt > rgt).update(rgt=self._db[self._tablename].rgt - diff)
            
            return True
        return False
        
        
    def ancestors(self, name, *fields):
        """
        print ancestors('Apple', db.category.name)
        Food
        Fruit
        """
        node = self._db(self._db[self._tablename].name == name).select().first()
        return self._db(self._db[self._tablename].lft < node.lft)(
                  self._db[self._tablename].rgt > node.rgt).select(
                            orderby=self._db[self._tablename].lft, *fields
                            )

    def descendants(self, name, *fields):
        """ 
        print descendants('Fruit', db.category.name)
        Apple
        """
        node = self._db(self._db[self._tablename].name == name).select().first()
        return self._db(self._db[self._tablename].lft > node.lft)(
                  self._db[self._tablename].rgt < node.rgt).select(
                            orderby=self._db[self._tablename].lft, *fields
                            )
                            
    def get_children(self, name):
        node = self._db(self._db[self._tablename].name == name).select().first()
        
                            
    def is_child_of(self, child, parent):
        child = self._db(self._db[self._tablename].name == child).select().first()
        parent = self._db(self._db[self._tablename].name == parent).select().first()
        
        if not child or not parent:
            return False
        
        return (child.lft > parent.lft & child.rgt < parent.rgt)
                            
    def test_populate(self):
        self._db(self._db[self._tablename].id > 0).delete()
        self.add_node('Food', None)
        self.add_node('Meat', 'Food')
        self.add_node('Fruit', 'Food')
        self.add_node('Red', 'Fruit')
        self.add_node('Yellow', 'Fruit')
        self.add_node('Apple', 'Red')
        self.add_node('Banana', 'Yellow')
        self.add_node('Beef', 'Meat')
        self.add_node('Chicken', 'Meat')
        self.add_node('Fish', 'Meat')
        self.add_node('Salmon', 'Fish')
        self.add_node('Steak', 'Beef')
        self.add_node('Toys', None)
        self.add_node('Lego', 'Toys')
        self.add_node('Batman', 'Toys')
        self.add_node('Bionics', 'Lego')
        
    def as_dict(self):
        categories = self._db().select(
                            self._db[self._tablename].ALL, 
                            orderby=self._db[self._tablename].lft
        )
        
        root = {}
        root['data'] = categories.first()
        children = self.descendants(root['data'].name)
        
        if children:
            current_parent = root
            current_parent['children'] = []
            
            for current_child_data in children:
                current_child = {}
                current_child['data'] = current_child_data
                current_child['children'] = []
                while not self.is_child_of(current_child['data'].name, current_parent['data'].name):
                    current_parent = current_parent.parent
                current_child['parent'] = current_parent
                current_parent['children'].append(current_child)
                current_parent = current_child
                
        return root
        
        
        root = []
        current_parent = None
        
        for cat in categories:
            current = {}
            current['data'] = cat
            current['children'] = []
            current['parent'] = current_parent
        
        root['data'] = categories.first()
        root['children'] = 2
    
    def ul_list_widget(self):
        categories = self._db().select(
                            self._db[self._tablename].ALL, 
                            orderby=self._db[self._tablename].lft
        )
        def widget(url, dostyle=True):
            rgt = []
                
            tree = []
                        
            for cat in categories:
                if len(rgt) > 0:
                    if rgt[-1] > cat.rgt:
                        # open UL
                        pass
                    while rgt[-1] < cat.rgt:
                        rgt.pop()
                        if len(rgt) == 0:
                            break
                         
                branch = UL(_class="branch")
                p=branch
                for i in range(len(rgt)):
                    child = UL(_class="branch_leaf")
                    p.append(LI(child, _class="leaf"))
                    p=child
                p.append(LI(A(cat.name, _href=url+'/'+cat.name), _class="leaf",))
                    
                tree.append(branch)   
                rgt.append(cat.rgt)
            seed = DIV(_class="root")
            for branch in tree:
                seed.append(DIV(branch, _class="root_branch"))
            
            if dostyle:    
                seed.components.extend([XML("""
        <style>
        .branch {
            padding: 0;
            margin: 0;
            padding-left: 10px;
            list-style-type: none;
        }
        .branch_leaf {
            padding: 0;
            margin: 0;
            padding-left: 20px;
            list-style-type: none;
        }
        .leaf {
            list-style-type: none;
        }

        </style>
                """)])
                    
            return seed
        return widget
    
    def select_widget(self):    
        categories = self._db().select(
                            self._db[self._tablename].ALL, 
                            orderby=self._db[self._tablename].lft
        )
        def widget(field, value, **attributes):
            rgt = []
            
            tree = []
                
            attr = OptionsWidget._attributes(field, {}, **attributes)
            
            values = re.compile('[\w\-:]+').findall(str(value))
            
            if hasattr(field.requires, 'options'):
                opts = []
                options = field.requires.options()
            tree.append(OPTION(_value="", _class="branch"))
            for cat in categories:
                if len(rgt) > 0:
                    if rgt[-1] > cat.rgt:
                        # open UL
                        pass
                    while rgt[-1] < cat.rgt:
                        rgt.pop()
                        if len(rgt) == 0:
                            break
                     
                s = ""
                for i in range(len(rgt)):
                    s += "&nbsp;&nbsp;&nbsp;&nbsp;"
                s += cat.name
                branch = OPTION(
                    XML(s),
                    _value=cat.id,
                    _class="branch",
                )
                
                tree.append(branch)   
                rgt.append(cat.rgt)
                
            seed = SELECT(**attr)
                          
            for branch in tree:
                seed.append(branch)
                
            return seed
        return widget
            
    def checkboxes_widget(self):
        categories = self._db().select(
                            self._db[self._tablename].ALL, 
                            orderby=self._db[self._tablename].lft
        )
        def widget(field, value, **attributes):
            rgt = []
                
            tree = []
                
            attr = OptionsWidget._attributes(field, {}, **attributes)
            
            values = re.compile('[\w\-:]+').findall(str(value))
            
            if hasattr(field.requires, 'options'):
                opts = []
                options = field.requires.options()
                        
            for cat in categories:
                if len(rgt) > 0:
                    if rgt[-1] > cat.rgt:
                        # open UL
                        pass
                    while rgt[-1] < cat.rgt:
                        rgt.pop()
                        if len(rgt) == 0:
                            break
                         
                branch = UL(_class="branch")
                p=branch
                for i in range(len(rgt)):
                    child = UL(_class="branch_leaf")
                    p.append(LI(child, _class="leaf"))
                    p=child
                p.append(LI(
                            INPUT(_type='checkbox',
                                  _value=cat.id,
                                  value=(str(cat.id) in values),
                                  _name = field.name,
                                  requires = field.requires
                            ), cat.name, _class="leaf",
                        )
                )
                    
                tree.append(branch)   
                rgt.append(cat.rgt)
            seed = DIV(_class="root")
            for branch in tree:
                seed.append(DIV(branch, _class="root_branch"))
                
            seed.components.extend([XML("""
        <style>
        .branch {
            padding: 0;
            margin: 0;
            padding-left: 10px;
            list-style-type: none;
        }
        .branch_leaf {
            padding: 0;
            margin: 0;
            padding-left: 20px;
            list-style-type: none;
        }
        .leaf {
            list-style-type: none;
        }
        </style>
                """)])
                    
            return seed
        return widget

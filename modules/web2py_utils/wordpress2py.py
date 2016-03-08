#!/bin/python
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
###########################################################
__author__ = "Thadeus Burgess <thadeusb@thadeusb.com>"
__copyright__ = "Copyright 2009-2010 Thadeus Burgess. GNU GPL v3."
__title__ = "Wordpress 2 Python"
__description__ = """
Turns a wordpress export xml file into a python dictionary
taking coffee for donations :)
"""
__version__ = "0.0.2"
###########################################################

from gluon.tools import Storage
plugin_wordpress2py = Storage()
plugin_wordpress2py.meta = {
    'title':'Wordpress To Web2py',
    'author':'Thadeus Burgess <thadeusb@thadeusb.com>',
    'keywords':'database, migration, wordpress, blog',
    'description':'Converts wordpress exported xml+rss into a python dictionary and then imports into web2py DAL',
    'copyright': 'GPL v2',
}

#######################################
#### USAGE
########

# Retrieve a python dict that represents the wordpress database
## data = word2py(open('/path/to/wordpress.2009-11-30.xml', 'r'))

# Insert data into web2py DAL using a schema
## ids_inserted = schema_migrate(db, schema, '/path/to/wordpress.2009-11-30.xml')

# Use the data dictionary to create a custom migration function,
# Dictionary layout is documented in the word2py function.

#######################################
#### SCHEMA KEY PATTERNS
########

#{
#    '<DATA TABLE>': {
#        '<DATA COLUMN>': '<DAL TABLE>/<DAL FIELD>',
#    },
#    '<DATA TABLE>': {
#        '<PYTHON EXEC doit>': {
#            '<DATA COLUMN>': '<DAL TABLE>/<DAL FIELD>',
#        }
#    }
#}


#######################################
#### SCHEMA OPTIONS
########

#    '<DATA TABLE>': {
#        'categories',
#        'tags',
#        'posts',
#        'comments',
#        'post_categories',
#        'post_tags',
#    }

#    '<DATA COLUMN>': {
#        'categories' ->
#            name
#            slug
#            parent
#        'tags' ->
#            name
#            slug
#        'posts' ->
#            id
#            title
#            slug
#            status
#            type
#            link
#            pub_date
#            description
#            content
#            post_date
#            post_date_gmt
#            categories -> list of strings (categories slug)
#            tags -> list of strings (tags slug)
#        'comments' ->
#            id
#            author
#            author_email
#            author_url
#            author_ip
#            date
#            date_gmt
#            content
#            approved
#    }

#    '<EXEC ENVIRONMENT>'
#       THIS CODE MUST BE VALID PYTHON CODE
#       IT MUST SET A VARIABLE NAMED doit TO EITHER TRUE OR FALSE
#       IF TRUE, THE RECORDS IN THE CORRESPONDING DICT ARE INSERTED INTO THE DATABASE
#       THIS CAN BE RECURSIVE

#       EXEC ENVIRONMENT HAS ACCESS TO THESE VARIABLES
#       data <dict> (this is the data from wordpress)
#       data['title'] # sample for posts
#       data['parent'] # sample for categories
#       This data matches options for <DATA COLUMN>


#######################################
#### EXAMPLE SCHEMA SETS MIGRATION
########

default_mengu_blog_schema = {
    'categories': {
        'name': 'category/title',
    },
    'posts': {
        'doit = True if data["type"] == "post" else False': {
            'title': 'post/title',
            'content': 'post/body',
            'post_date': 'post/dateline',
        },
        'doit = True if data["type"] == "page" else False': {
            'title': 'page/title',
            'content': 'page/content',
        },
    },
    'comments': {
        'id_post': 'comment/post_id',
        'author': 'comment/name',
        'author_email': 'comment/email',
        'content': 'comment/comment',
        'date': 'comment/dateline',
    },
    'post_categories': {
        'id_category': 'relations/category',
        'id_post': 'relations/post',
    },
}

default_schema = {
    'categories': {
        'name': 'category/title',
        'parent': 'category/parent',
    },
    'tags': {
        'name': 'tag/title',
    },
    'posts': {
        'title': 'post/title',
        'slug': 'post/slug',
        'status': 'post/status',
        'type': 'post/type',
        'post_date': 'post/pub_date',
        'content': 'post/content',
    },
    'comments': {
        'id_post': 'comment/id_post',
        'author': 'comment/author',
        'author_email': 'comment/email',
        'author_url': 'comment/site',
        'date': 'comment/posted_on',
        'approved': 'comment/approved',
        'content': 'comment/content',
    },
    'post_categories': {
        'id_category': 'category_relations/category',
        'id_post': 'category_relations/post',
    },
    'post_tags': {
        'id_tag': 'tag_relations/tag',
        'id_post': 'tag_relations/post',
    },
}

#######################################
#### EXAMPLE CUSTOM MIGRATION
########

def custom_migrate_to_mengu_database(db):
    data = word2py(open('wordpress_export.xml', 'r'))
    
    category_ids = {}
    post_ids = {}
    comment_ids = {}
    
    for c in data['categories']:
        category_ids[c['name']] = db.category.insert(title=c['name'])
    
    for post in data['posts']:
        if post['type'] == 'post':
            post_id = db.post.insert(
                title = post['title'],
                body = post['content'],
                dateline = post['pub_date'],
            )
            
            for c in post['categories']:
                db.relations.insert(
                    post = post_id,
                    category = category_ids[c]
                )
            
            for c in post['comments']:
                comment_id = db.comment.insert(
                    post_id = post_id,
                    name = c['author'],
                    email = c['author_email'],
                    comment = c['content'],
                    dateline = c['date']
                )
        elif post['type'] == 'page':
            post_id = db.page.insert(
                title = post['title'],
                content = post['content']
            )

def process_columns(schema, data):
    insd = {}
    tables = []
    for column, table_field in schema.items():
        if isinstance(table_field, dict):
            exec column
            if doit:
                return process_columns(table_field, data)
        else:
            table, field = table_field.split('/')
            
            tables.append(table)
            
            insd[field] = data[column]
    
    if len(tables) > 0:
        table = tables[0]
        for t in tables:
            if table != t:
                table = False
    else:
        table = 'none_found'
                
    if table:
        return insd, table
    elif table == 'none_found':
        return None, None
    else:
        raise Exception("Invalid import schema, you may not insert into multiple tables at the same time")
    
import hashlib
def schema_migrate(db, schema, fname):
    data = word2py(open(fname, 'r'))
    
    ids = {
        'category': {},
        'tag': {},
        'post': {},
        'comment': {},
        
    }
    
    if schema.has_key('categories'):
        for category in data['categories']:
            insd, table = process_columns(schema['categories'], category)
            
            ids['category'][category['slug']] = db[table].insert(**insd)
            
    if schema.has_key('tags'):
        for tag in data['tags']:
            insd, table = process_columns(schema['tags'], tag)
            
            ids['tag'][tag['slug']] = db[table].insert(**insd)            
            
    if schema.has_key('posts'):
        for post in data['posts']:
            insd, table = process_columns(schema['posts'], post)
            
            if insd:
                id_post = post['id_post'] = ids['post'][post['title']] = db[table].insert(**insd)
                
                if schema.has_key('post_categories'):
                    for cname in post['categories']:
                        record = {
                            'id_post': id_post,
                            'id_category': ids['category'][cname],
                        }
                        insd, table = process_columns(schema['post_categories'], record)
                        
                        db[table].insert(**insd)
                        
                if schema.has_key('post_tags'):
                    for tname in post['tags']:
                        record = {
                            'id_post': id_post,
                            'id_tag': ids['tag'][tname]
                        }
                        insd, table = process_columns(schema['post_tags'], record)
                        
                        db[table].insert(**insd)
                        
                if schema.has_key('comments'):
                    for comment in post['comments']:
                        comment['id_post'] = id_post
                        insd, table = process_columns(schema['comments'], comment)
                        
                        db[table].insert(**insd)
            else:
                print "NO_DATA", insd, table
                print post
                    
    return ids 

def word2py(xml_file):
    """
    Requires elementtree
    
    Returns python dictionary representing the wordpress blog.
    Certain metadata may be missing.
    
    Content is sorted based on the arrangment of the data in the xml file.
    
    
    File structure:
    
    db {
        title
        link
        description
        pub_date
        language
        categories ->
            name
            slug
            parent
            description (if available)
        tags ->
            name
            slug
        posts ->
            id
            title
            slug
            status
            type
            link
            pub_date
            description
            content
            post_date
            post_date_gmt
            categories -> flat array
            tags -> flat array
            comments ->
                id
                author
                author_email
                author_url
                author_ip
                date
                date_gmt
                content
                approved
    }
    """
    try: # Try the normal import process first
        from elementtree import ElementTree
    except: # We might be on Ubuntu
        try:
            from xml.etree import ElementTree
        except: # Well... 
            raise Exception("Unable to import ElementTree, is it installed correctly?")
        

    #xml_file = open('wordpress.2009-11-30.xml', 'r')

    tree = ElementTree.parse(xml_file)

    db = {
        'title': tree.find('channel/title').text.encode('utf-8'),
        'link': tree.find('channel/link').text,
        'description': tree.find('channel/description').text,
        'pub_date': tree.find('channel/pubDate').text,
        'language': tree.find('channel/language').text,
        'categories': [],
        'tags': [],
        'posts': [],
    }
    
    # Find all categories, and their parents, this just builds a flat dictionary.
    for c in tree.findall('channel/{http://wordpress.org/export/1.0/}category'):
        a_cat = {
            'name': c.find('{http://wordpress.org/export/1.0/}cat_name').text,
            'slug': c.find('{http://wordpress.org/export/1.0/}category_nicename').text,
            'parent': c.find('{http://wordpress.org/export/1.0/}category_parent').text,
        }
        # this is to work around non-existant descriptions.
        d = c.find('{http://wordpress.org/export/1.0/}category_description')
        if d:
            a_cat['description'] = d.text
        
        db['categories'].append(a_cat)

    # Find all tags
    for t in tree.findall('channel/{http://wordpress.org/export/1.0/}tag'):
        a_tag = {
            'name': t.find('{http://wordpress.org/export/1.0/}tag_name').text,
            'slug': t.find('{http://wordpress.org/export/1.0/}tag_slug').text,
        }
        
        db['tags'].append(a_tag)

    # Find all posts/pages, and other misc wordpress content
    for item in tree.findall('channel/item'):
        r = {}
                
        r['id'] = item.find('{http://wordpress.org/export/1.0/}post_id').text
        r['title'] = item.find('title').text
        r['slug'] = item.find('{http://wordpress.org/export/1.0/}post_name').text
        r['status'] = item.find('{http://wordpress.org/export/1.0/}status').text
        r['type'] = item.find('{http://wordpress.org/export/1.0/}post_type').text
        r['link'] = item.find('link').text
        r['pub_date'] = item.find('pubDate').text
        r['description'] = item.find('description').text
        r['content'] = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
        r['post_date'] = item.find('{http://wordpress.org/export/1.0/}post_date').text
        r['post_date_gmt'] = item.find('{http://wordpress.org/export/1.0/}post_date_gmt').text
        
        r['categories'] = []
        r['tags'] = []
        r['comments'] = []
        
        # The posts categories and tags
        cats = item.findall('category')
        for c in cats:
            its = c.items()
            if len(its) > 1:
                if its[0][1] == 'category':
                    r['categories'].append(its[1][1])
                elif its[0][1] == 'tag':
                    r['tags'].append(its[1][1])
                    
        # The posts comments
        comments = item.findall('{http://wordpress.org/export/1.0/}comment')
        
        for comment in comments:
            the_comment = {
                'id': comment.find('{http://wordpress.org/export/1.0/}comment_id').text,
                'author': comment.find('{http://wordpress.org/export/1.0/}comment_author').text,
                'author_email': comment.find('{http://wordpress.org/export/1.0/}comment_author_email').text,
                'author_url': comment.find('{http://wordpress.org/export/1.0/}comment_author_url').text,
                'author_ip': comment.find('{http://wordpress.org/export/1.0/}comment_author_IP').text,
                'date': comment.find('{http://wordpress.org/export/1.0/}comment_date').text,
                'date_gmt': comment.find('{http://wordpress.org/export/1.0/}comment_date_gmt').text,
                'content': comment.find('{http://wordpress.org/export/1.0/}comment_content').text,
                'approved': comment.find('{http://wordpress.org/export/1.0/}comment_approved').text,
            }
             
            r['comments'].append(the_comment)
            
        db['posts'].append(r)
                
    return db

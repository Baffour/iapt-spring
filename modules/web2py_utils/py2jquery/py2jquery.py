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
    License: GPL v3
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

__all__ = [
     #GENERAL FUNCTIONS
     'S', 'valid_filename', 'is_valid_selector', 'get_selector', 
     #JAVASCRIPT GENERATORS
     'js', 
     #SCRIPT CLASSES
     'Manager', 'Var', 'VarDict', 'Script', 'Confirm', 'Delay', 
     'Interval', 'Counter', 'StopTimer', 'Call', 'Event',
]

__events__ = ['blur', 'focus', 'load', 'resize', 'scroll', 'unload', 
                 'beforeunload', 'click', 'dblclick',  'mousedown', 
                 'mouseup', 'mousemove', 'mouseover', 'mouseout', 
                 'mouseenter', 'mouseleave', 'change', 'select',
                 'submit', 'keydown', 'keypress', 'keyup', 'error']

__events_live_notsupported__ = ['blur', 'focus', 'mouseenter', 
                                'mouseleave', 'change', 'submit']

__counters__ = ['up', 'down']

__js_scripts__ = ['embed', 'var', 'setvar', 'function', 
                  'alert', 'ajax', 'replace', 
                  'datetime_format',]

__jquery_plugins__ = {
    'jquery': {'name': 'jquery',
               'version': 1.32,
               'provides': ['jquery'],
               'requires': [],
               'files': [('jquery.min.js', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')],
    },
    
    'jquery.ui': {'name': 'jquery.ui',
               'version': 1.72,
               'provides': ['jquery.ui'],
               'requires': ['jquery'],
               'files': [('jquery.ui.min.js', 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js')],
    },
    
    'jquery.rating': {'name': 'jquery.rating',
                      'version': 1.5,
                      'provides': ['jquery.rating'],
                      'requires': ['jquery'],
                      'files': [('jquery.rating.js', 'http://hg.thadeusb.com/public/.r/Web/py2jquery/raw-file/4caabf1997c8/jquery.plugins/jquery.rating/jquery.rating.js'),
                                ('jquery.rating.css', 'http://hg.thadeusb.com/public/.r/Web/py2jquery/raw-file/4caabf1997c8/jquery.plugins/jquery.rating/jquery.rating.css'),
                                ('jquery.rating.stars.gif', 'http://hg.thadeusb.com/public/.r/Web/py2jquery/raw-file/4caabf1997c8/jquery.plugins/jquery.rating/jquery.rating.stars.gif')
                      ],
    },
    
    'jquery.jeditable': {'name': 'jquery.jeditable',
                      'version': 1.0,
                      'provides': ['jquery.jeditable'],
                      'requires': ['jquery'],
                      'files': [('jquery.jeditable.mini.js', 'http://www.appelsiini.net/download/jquery.jeditable.mini.js'),
                      ],
    },
    
    'jquery.timer': {'name': 'jquery.timer',
                     'version': 1.2,
                     'provides': ['jquery.timer'],
                     'requires': ['jquery'],
                     'files': [('jquery.timer.js', 'http://plugins.jquery.com/files/jquery.timers-1.2.js.txt')],
    },
                      
    'date.format': {'name': 'date.format',
                    'version': 1.2,
                    'provides': 'date.format',
                    'requires': [],
                    'files': [('date.format.js', 'http://stevenlevithan.com/assets/misc/date.format.js')],
    }
}

__cdn_resources__ = {
    'jquery': {
                 'name': 'jquery',
                 'provides': ['jquery'],
                 'requires': [],
                 'files': ['http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js'],
    },
    'jquery.ui': {
                  'name': 'jquery.ui',
                  'provides': ['jquery.ui'],
                  'requires': ['jquery'],
                  'files': ['http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js'],
    },
    'jquery.ui.theme.darkness': {
                 'name': 'jquery.ui.theme.darkness',
                 'provides': ['jquery.ui.theme.darkness'],
                 'requires': ['jquery.ui'],
                 'files': ['http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/ui-darkness/jquery-ui.css'],
    },
    'jquery.ui.theme.smoothness':{
                 'name': 'jquery.ui.theme.smoothness',
                 'provides': ['jquery.ui.theme.smoothness'],
                 'requires': ['jquery.ui'],
                 'files': ['http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/smoothness/jquery-ui.css'],
    },
    'jquery.ui.theme.redmond':{
                 'name': 'jquery.ui.theme.redmond',
                 'provides': ['jquery.ui.theme.redmond'],
                 'requires': ['jquery.ui'],
                 'files': ['http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/redmond/jquery-ui.css'],
    },
    'jquery.ui.theme.humanity': {
                 'name': 'jquery.ui.theme.humanity',
                 'provides': ['jquery.ui.theme.humanity'],
                 'requires': ['jquery.ui'],
                 'files': ['http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/humanity/jquery-ui.css'],
    },
}

"""####################################
           GENERAL FUNCTIONS
"""####################################

def S(filename, request):
    return URL(r=request, c='static', f=filename)

def get_url(req, function, args=None):
    if not isinstance(function, str):
        if not hasattr(function, '__call__'):
            raise TypeError('Invalid function for url. Object is not callable.')
        
        function = URL(r=req, f=function.__name__, args=args)
        
    return function

def valid_filename(filename):
    """
    This checks to make sure the string is a valid filename that does not include
    restricted characters. Invalid characters are stripped.
    
    Returns str with only valid filename characters.
    """
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def is_valid_selector(obj, r=True):
    """
    Checks an object to determine if it is a valid selector.
    
    Object must either be a string (css selector), Script instance,
    or object with an xml() function and _id attribute.
    
    Returns True/False
    """
    if isinstance(obj, str) or \
            isinstance(obj, Script) or \
            (hasattr(obj, 'xml') and obj['_id']):
        return True
    elif r:
        if not hasattr(obj, 'xml'):
            raise TypeError('Invalid object for event. No XML Function.')
        if not obj['_id']:
            raise ValueError('Invalid object for event. No ID Attribute.')
        else:
            raise Error('Object must be Script, or string, or object with xml() function and id attribute.')
    else:
        return False
    
def get_selector_css(obj):
    """
    Returns the css selector for given object.
    """
    selector = ""
    
    if hasattr(obj, 'tag'):
        if obj['_id']:
            selector = "%s" % ob['_id']
        if obj['_name']:
            selector = "%s[name='%s']" % (obj.tag.replace("/", ""), obj['_name'])
        raise ValueError('Invalid component. No id or name attribute')
    elif isinstance(obj, Script):
        selector = obj.name
    elif isinstance(obj, str):
        if obj.startswith('document') or obj == 'this':
            selector = obj
    else:
        selector = obj
            
    return selector
    
def get_selector(obj, css=False):
    """
    Returns the css selector for given object.
    Appends # if css is True
    """
    selector = None
    
    if isinstance(obj, str):
        selector = obj
    elif isinstance(obj, Script):
        selector = obj.name
    else:
        selector = '%s' % (obj['_id'])
    
    if css:
        selector = '#' + selector
    
    return selector

"""####################################
           JAVASCRIPT GENERATORS
"""####################################
class js(object):
    
    @classmethod
    def embed(self, path):
        """
        Takes a path to file and returns a string for inclusion in XML
        Wraps path <script type="text/javascript" src=path> for javascript and <link rel="stylesheet" type="text/css" href=path> for css.
        """
        if path.lower().endswith(".js"):
            return """<script type="text/javascript" src="%s"></script>""" % path
        elif path.lower().endswith(".css"):
            return LINK(_href=path, _rel="stylesheet", _type="text/css").xml()
        else:
            return path
    
    @classmethod
    def var(self, name, value=None):
        """
        Returns a javascript variable
        
        TODO: Add the ability to assign a javascript variable a value.
        """
        js = "var %s" % name
        
        if value != None:
            if isinstance(value, int) or isinstance(value, float):
                js += ' = %s' % value
            else:
                js += ' = "%s"' % value
            
        js += ';'
        
        return js
    
    @classmethod
    def setvar(self, name, value):
        """
        Sets a javascript variable
        """
        js = "%s = " % name
        
        if isinstance(value, int) or isinstance(value, float):
            js += '%s' % value
        else:
            js += '"%s"' % value
        
        js += ';'
        
        return js
    
    @classmethod
    def function(self, name, args=[], xml=""):
        """
        Wraps xml in javascript function with name
        """
        return 'function %s(){%s};' % (name, xml)
    
    @classmethod
    def alert(self, message):
        """
        Returns javascript alert string.
        """
        return 'alert("%s");' % message
    
    @classmethod
    def ajax(self, type="POST", url="#", extra_data="", data="form:first", success="eval(msg);"):
        """
        Returns jQuery.ajax() string with the parameters
        
        Success can be eval(msg); or the object of the html to replace.
        Extra data can be any string to include in the POST vars.
        """
        if success != "eval(msg);":
            success = 'jQuery("%s").html(msg);' % success
        return 'jQuery.ajax({type:"%s", url:"%s", data:%s jQuery("%s").serialize(), '\
                    'success: function(msg){%s} });' % (type, url, extra_data, data, success)
    
    @classmethod
    def replace(self, target, html):
        return 'jQuery("%s").html(%s);' % (target, html)
    
    @classmethod
    def datetime_format(self, datetime, mask):
        """
        Requires date.format.js
        
        Downloadable and documentation available at
        http://blog.stevenlevithan.com/archives/date-time-format
        
        """
        return '''
        dateFormat(%s, '%s')
        ''' % ("%s" % datetime if not isinstance(datetime, Var) else datetime, mask)
    #return 'Math.floor((%s/1000)/60) + ":" + ((%s/1000) %% 60)' % (ms, ms)
# Math.floor(seconds / 60) + ":" + (seconds % 60).toFixed().pad(2, "0")
   
"""####################################
           SCRIPT CLASSES
"""#################################### 

class Var(object):
    """
    Represents a JavaScript variable.
    name - Name of variable in javascript
    value - current value of variable.
    """
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
    def __str__(self):
        return self.name
        
class VarDict(dict):
    """
    Represents a dictionary of JavaScript variables.
    Allows you to reference the javascript variable by
    a python only name. This way you can have unique javascript
    variables.
    
    Example:
    vd = VarDict()
    vd.timer_id = Var('mytimer_uuid_timerid', 200)
    >>>vd
    {'timer_id': Var('mytimer_uuid_timerid', 200)
    >>>vd.timer_id
    'mytimer_uuid_timerid'
    >>>vd.timer_id.value
    200
    """
    def init(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        
    def __getattr__(self, name):
        return self.__getitem__(name)
    def __setattr__(self, name, value):
        self.__setitem__(name, value)

class Manager(object):
    """
    The Manager object is used to dynamically include
    resources and scripts on a page.
    
    include - downloads a resource and/or adds a
              reference to it on the page
    google_load - adds a reference to a google hosted library
                  example: manager.google_load("jqueryui", "1.7.2")
                  more here: http://code.google.com/apis/ajaxlibs/
    add - Adds a script to the page, the script may be a function, variable,
                 or string. If on_ready is True, then the script or function call
                 will be placed in the jQuery(document).on_ready(); event.
                 
    xml - Renders all resources and scripts. If minify is False, it will add line breaks.
          Each time you call this function, it resets any added scripts. You can call this function as many times as you like.
          This way, you can call the script again at the end of your page, in case you need to add scripts
          from a view.
    """
    
    def __init__(self, environment):
        self.environment = Storage(environment)
        self.resources = []
        self.includes = []
        self.on_ready = []
        self.scripts = []
        self.misc = []
        self.vars = VarDict()
        self.called = 0
        
    def require_cdn(self, name):
        try:
            plugin = __cdn_resources__[name]
        except:
            plugin = None
        
        if plugin == None:
            raise ImportError('There is no cdn plugin by given name: %s' % name)
        
        for p in plugin['provides']:
            if p in self.includes:
                return
        
        for r in plugin['requires']:
            if r not in self.includes:
                self.require_cdn(r)
        
        for file in plugin['files']:
            self.include(file)
            
        for p in plugin['provides']:
            self.includes.append(p)
        
    def require(self, name, subfolder="", upgrade=False):
        try:
            plugin = __jquery_plugins__[name]
        except:
            plugin = None
        
        if plugin == None:
            raise ImportError('There is no jquery plugin by given name: %s' % name)
        
        for p in plugin['provides']:
            if p in self.includes:
                return
        
        for r in plugin['requires']:
            if r not in self.includes:
                self.require(r, subfolder=subfolder, upgrade=upgrade)
        
        request = self.environment.request
        
        pieces = (request.folder, 'static', subfolder, plugin['name'])
        folder = os.path.join(*(x for x in pieces if x))
        download = False
        
        if not os.path.exists(folder):
            os.mkdir(folder)
            download = True
            
        if upgrade:
            try:
                version_file = open(os.path.join(folder, 'version.txt'), 'r')
                if float(version_file.readline()) < plugin['version']:
                    download = True
            except:
                download = True
                
        if download:
            for file in plugin['files']:
                file_path = os.path.join(folder, file[0])
                urllib.urlretrieve(file[1], file_path)
            version_file = open(os.path.join(folder, 'version.txt'), 'w')
            version_file.write("%f" % plugin['version'])
            version_file.close()
                
        for file in plugin['files']:
            if file[0].endswith('.js') or file[0].endswith('.css'):
                self.include(URL(r=request, c='static', f="%s%s/%s" % (subfolder, plugin['name'], file[0])))
                
        for p in plugin['provides']:
            self.includes.append(p)
        
    def include(self, path):
        out = path
        if hasattr(path, 'xml'):
            out = path.xml()              
        self.resources.append(out)
        
    def add(self, script, on_ready=False):
        if isinstance(script, Script):
            self.scripts.append(script)
            if on_ready:
                self.on_ready.append(script.name)
        elif isinstance(script, str):
            self.misc.append(script)
        else:
            raise TypeError('Must be of class Script')
                    
    def add_var(self, var):
        if not isinstance(var, Var):
            raise TypeError('Invalid type. var must be of type Var')
        raise Error('Not yet implemented.')
        
    def xml(self, minify=True):
        xml = ""
        var_xml = []
        functions = []
        on_ready = []
        misc = self.misc
                
        if minify:
            minify = ''
        else:
            minify = '\n'
        
        for r in self.resources:
            xml += js.embed(r)
            xml += minify
        
        for script in self.scripts:                
            if script.is_function:
                functions.append(script.xml())
                if script.name in self.on_ready:
                    on_ready.append(script.name + '();')
                    
                for v in script.var.values():
                    var_xml.append(js.var(v.name, v.value))
                    
            elif script.name in self.on_ready:
                    on_ready.append(script.xml())
            else:
                misc.append(script.xml())
                
        for v in self.vars.values():
            var_xml.append(js.var(v.name, v.value))
                
        page_on_ready = "page_on_ready_%d" % self.called
        
        xml += '''<script type="text/javascript">'''
        xml += minify
        xml += minify.join(v for v in var_xml)
        xml += minify
        xml += minify.join(s for s in functions)
        xml += minify
        xml += js.function(page_on_ready, [], minify.join(s for s in on_ready))
        xml += minify
        xml += '''jQuery(document).ready(%s);''' % page_on_ready
        xml += minify
        xml += minify.join(s for s in misc)
        xml += minify
        xml += '''</script>'''
        
        self.resources = []
        self.on_ready = []
        self.scripts = []
        self.called += 1
        
        return XML(xml)
    
class Script(object):
    """
    A base script class.
    
    txt - Optional txt value, useful to turn a str that is javascript into a
          instance of Script.
          
    uuid - Unique identifier for this script. This is required if you are
           using multiple subscriptions to an event/object.
           
    is_function - If this is True, the xml output will be wrapped in
                  function self.name(){self.xml()}
                  
    wrap - Adds function to a string if is_function
    dewrap - Returns the call to the script, if a function () is appended, else just the text.
    
    vars - Represents variables in javascript.
            example 
            >>>var['timer_id'] = 24
            'var timer_id = 24;'
    
    Returns defaults for variables needed in javascript (such as timer_id)
    xml - Renders the script.
    """
    def __init__(self, txt='', uuid='', is_function=False, **kwargs):
        self.txt = txt
        self.uuid = uuid
        self.is_function = is_function
        self.name = "%s__script" % uuid
        self.var = VarDict()
        
    def __str__(self):
        return self.xml()
    
    def wrap(self, xml):
        if self.is_function:
            xml = js.function(self.name, [], xml)
        return xml
    
    def dewrap(self, script):
        if isinstance(script, str):
            return script
        elif script.is_function:
            return '%s();' % (script.name)
        else:
            return script.xml()
    
    def xml(self):
        xml = self.txt
        
        xml = self.wrap(xml)
        
        return xml
    
class Confirm(Script):
    """
    Creates a confirm dialog.
    
    message - message to display in dialog
    if_ok - Script to run if ok is selected
    if_cancel - Script to run if cancel is selected
    """
    def __init__(self, message='', if_ok='', if_cancel='', **kwargs):
        Script.__init__(self, **kwargs)
        self.name = '%s__confirm' % self.uuid
        self.var.answer = Var(self.name + "__answer")
        
        if not isinstance(if_ok, Script) and not isinstance(if_ok, str):
            raise TypeError('if_ok must be type Script or string')
        if not isinstance(if_cancel, Script) and not isinstance(if_cancel, str):
            raise TypeError('if_cancel must be type Script or string')
        
        self.message = message
        self.if_ok = if_ok
        self.if_cancel = if_cancel
               
    def xml(self):
        xml = ''
        
        if_ok_xml = self.dewrap(self.if_ok)
        if_cancel_xml = self.dewrap(self.if_cancel)
        
        xml += '%s = confirm("%s");' % (self.var.answer, self.message)
        xml += 'if(%s==true){%s}else{%s}' % (self.var.answer, if_ok_xml, if_cancel_xml)
        
        xml = self.wrap(xml)
        
        return xml

class Delay(Script):
    """
    Adds a timeout timer to the page.
    
    Delays the execution of Script until the specified timeout.
    
    script - Script to execute when timer ends.
    timeout - Time in ms to delay execution.
    
    global var delay%s_timerid (self.uuid)
    """
    def __init__(self, script, timeout, **kwargs):
        Script.__init__(self, **kwargs)
        
        if not isinstance(script, Script):
            raise TypeError('delay script must be of instance Script.')
        
        self.script = script
        self.timeout = int(timeout)
        
        self.name = "%s__delay" % (self.uuid)
        
        self.var.timer_id = Var("%s__timerid" % (self.name))
        
    def xml(self):
        xml = ''
        
        script_xml = self.dewrap(self.script)
        
        xml += "%s = setTimeout('%s', %s)" % (self.var.timer_id, script_xml, self.timeout)
        
        xml = self.wrap(xml)
        
        return xml
    
class Interval(Delay):
    """
    Adds a interval timer to the page.
    
    Executes Script at each specified interval
    
    script - Script to execute at each interval
    timeout - Time in ms between executions.
    
    global var interval%s_timerid (self.uuid)
    """
    def __init__(self, *args, **kwargs):
        Delay.__init__(self, *args, **kwargs)
        
        self.name = "%s__interval" % (self.uuid)
        self.var.timer_id = Var("%s_timerid" % self.name)
        
    def xml(self):
        xml = ''
        
        script_xml = self.dewrap(self.script)
        
        xml += "%s = setInterval('%s', %s);" % (self.var.timer_id, script_xml, self.timeout)
        
        xml = self.wrap(xml)
        
        return xml
    
class Counter(Delay):
    def __init__(self, type, interval=100, *args, **kwargs):
        Delay.__init__(self, *args, **kwargs)
        
        if type not in __counters__:
            raise ValueError('Counter type must be either up or down')
        
        if not self.is_function:
            raise AttributeError('CountDown objects must be functions. Set is_function to True and add the script to the manager.')
        
        self.name = "%s__count%s" % (self.uuid, type)
        
        self.interval = interval
        self.type = type
        self.sat = []
        
        self.var.timer_id = Var("%s_timerid" % self.name)
        self.var.ms = Var("%s_ms" % self.name, self.timeout if self.type == 'down' else 0)
        self.var.time = Var("%s_time" % self.name, 0)
        
    def add(self, script, interval):
        if not isinstance(script, Script):
            raise TypeError('Invalid counter script for interval, must be of instance Script.')
        
        self.sat.append((script, interval))
        
    def xml(self):
        if self.type == 'down':
            sign = '-'
        else:
            sign = '+'
        
        xml = ''
        
        xml += '''
        %s%s=%d;
        %s+=%d;
        ''' % (self.var.ms, sign, self.interval,
               self.var.time, self.interval)
        
        for f, i in self.sat:
            xml += '''
            if ((%s %% %d) == 0){
                %s
            }
            ''' % (self.var.time, i, self.dewrap(f))
            
        if self.type == 'down':
            xml += "if (%s > 0){" % self.var.ms
        else:
            if self.timeout == -1:
                xml += "if (true){"
            else:
                xml += "if (%s < %s){" % (self.var.ms, self.timeout)
        
        xml += "%s = setTimeout('%s', %s);" % (self.var.timer_id, self.dewrap(self).strip(';'), self.interval)
        
        xml += "}else{%s}" % self.dewrap(self.script)
        
        xml = self.wrap(xml)
        
        return xml
    
class StopTimer(Script):
    """
    Stops a running timer by using its timer_id
    
    timer - Delay or Interval instance
    """
    def __init__(self, timer, **kwargs):
        Script.__init__(self, **kwargs)
        
        if not isinstance(timer, Delay):
            raise TypeError('script must be of type Delay or Interval.')
        
        self.timer = timer
           
        self.name = "%s__stop" % (self.uuid)
        
    def xml(self):
        xml = ''
        
        xml += 'clearTimeout(%s);' % (self.timer.var.timer_id)
        
        xml = self.wrap(xml)
        
        return xml
        
            
class Call(Script):
    """
    Makes an AJAX request to the server with jQuery.
    
    callback - serverside function to call
    args - arguments to function
    success - if specified, replaces dom with server response html. Else it evaluates the response as javascript
    data - form data to add to POST
    extra_data - any other data that should be appended to the POST
    """
    def __init__(self, callback=None, args=[], success="eval(msg);", data="form:first", extra_data="", **kwargs):
        Script.__init__(self, **kwargs)
        
        self.callback = callback
        self.args = args
        
        if not isinstance(callback, str):
            if not hasattr(callback, '__call__'):
                raise TypeError('Invalid function. Object not callable')
            if kwargs['request']:
                request = kwargs['request']
            elif not self.manager:
                raise AttributeError('Call must be supplied either a reference to a request object or Manager object.')
            
            self.url = URL(r=request, f=callback.__name__, args=args)
        else:
            self.url = callback
            
        if is_valid_selector(success):
            self.success = success
            
        if is_valid_selector(data):
            self.data = data
            self.extra_data = extra_data
            
        if isinstance(self.callback, str):
            n = self.callback.split('/')[-1]
        else:
            n = self.callback.__name__
            
        self.name = '%s__call%s' % (n, self.uuid)
        
    def xml(self):
        xml = ""
        
        xml += js.ajax(type="POST",
                    url=self.url,
                    extra_data=self.extra_data,
                    data=self.data,
                    success=self.success)
        
        xml = self.wrap(xml)
            
        return xml
        
class Event(Script):
    """
    Listens for an event on the selected object. Calls a script when event is detected.
    
    event - jQuery event type, must be in in __events__.
    event_obj - object or css selector to listen for event on.
    call - script to execute when event is detected.
    event_args - if True, returns arguments for event
                ['event_target_id', 'event_target_html', 'event_pageX', 'event_pageY', 'event_timeStamp']
    rebind - if True, it will use jQuery.live() else it will use jQuery.bind()
    """
    def __init__(self, event="click", event_obj=None, call=None, extra_data="", event_args=False, rebind=False, **kwargs):
        Script.__init__(self, **kwargs)
        
        if event in __events__:
            self.event = event
        else:
            raise ValueError('Invalid event name.')
        
        if is_valid_selector(event_obj):
            self.event_obj = event_obj
        
        if isinstance(call, Script):
            self.call = call
        else:
            raise TypeError('Invalid call object. Must be instance of Script.')
        
        call.extra_data = extra_data
        if event_args:
            call.extra_data += '"event_target_id=" + encodeURIComponent(e.target.id) + "&event_target_html=" + '\
                'encodeURIComponent(jQuery(e.target).wrap("<div></div>").parent().html()) + '\
                '"&event_pageX=" + e.pageX + "&event_pageY=" + e.pageY + '\
                '"&event_timeStamp=" + e.timeStamp + "&" +'
        
        if rebind:
            self.bind = 'live'
            if self.event in __events_live_notsupported__:
                raise ValueError('Event not supported for jQuery.live()')
        else:
            self.bind = 'bind'
            
        self.name = '%s__%s%s' % (get_selector(self.event_obj), self.event, self.uuid)
        
    def xml(self):
        xml = ""
        
            
        call_xml = self.dewrap(self.call)
            
        xml += 'jQuery("%s").%s("%s", function(e){%s});' % (get_selector(self.event_obj, True), self.bind, self.event, call_xml)

        xml = self.wrap(xml)
        
        return xml
    

"""####################################
           WIDGETS
"""####################################

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

        return DIV(INPUT(_name=field.name, _type='hidden', _id='rating_input_%s' % (id(field))),
                    DIV(_class='rating_widget', _val=value, _num=len(requires.theset), _dbid=id(field)),
                    _class="rating")

class Stars(object):
    """
    A class for implementing a star rating widget.

    value - Current value for this set of stars.
    call - Script to call when star is clicked.
    num - Number of stars
    uuid - REQUIRED name for this set of stars.

    dom - Renders all required HTML and JavaScript events for this set of stars
    js - Returns JavaScript to alter the src attribute of the images in this star set.

    Example:

    def stars():
        callback = Call(rate_stars, request=request)
        # OR       Call(URL(r=request, f='rate_stars', args='') # In case args need to be passed along as well.

        # Create blank set of stars
        stars = Stars(-1, callback, uuid='mystars')

        # Generate the stars, you may need to call XML() on this.
        return dict(stars=stars.dom(manager))

    def rate_stars():
        # Passed from POST
        uuid = request.vars.star_uuid
        val = request.vars.star_val

        # Notice we are using the same uuid, and no callback.
        # Set the value to the selected star.
        stars = Stars(int(val), uuid=uuid)

        # Renders JavaScript that will get eval'd
        return stars.js(request)
    """

    full = 'images/star_full.gif'
    half = 'images/star_half.gif'
    void = 'images/star_void.gif'
    vote = 'images/star_vote.gif'

    def __init__(self, value, call=None, num=5, uuid=''):
        if not isinstance(value, int):
            raise TypeError('Value must be integer')
        if not isinstance(call, Call) and call != None:
            raise TypeError('Invalid call object. Must be instance of Script.')
        if uuid == '':
            raise ValueError('Must be assigned a uuid.')

        self.value = value
        self.call = call
        self.num = num
        self.uuid = uuid

        self.name = "stars%s" % (self.uuid)

    def dom(self, manager):
        if not isinstance(manager, Manager):
            raise TypeError('manager must be instance of Manager')
        if not isinstance(self.call, Call):
            raise TypeError('Invalid call object. Must be instance of Script.')

        r = manager.environment.request

        dom = ""

        stars = []

        for i in range(1, self.num + 1):
            if i <= self.value:
                img = Stars.full
            if i > self.value:
                img = Stars.void

            id = "%s_%d" % (self.name, i)

            sdom = IMG(_src=S(img, r), _id=id)
            stars.append(sdom)
            dom += "%s" % sdom

            js_var = "%s_src_val" % id

            extdata = '"star_uuid=%s&star_val=%d&"+' % (self.uuid, i)
            call = Call(callback=self.call.url, args=self.call.args, success=self.call.success, data=self.call.data,
                        extra_data=self.call.extra_data, uuid=self.call.uuid, name=self.call.name, is_function=self.call.is_function, )
            click = Event("click", sdom, call, extra_data=extdata)

            mouseover = ""
            mouseout = ""
            for star in stars:
                mouseover += 'jQuery("#%s").attr("src", "%s");' % (star['_id'], S(Stars.vote, r))
                mouseout += 'jQuery("#%s").attr("src", %s);' % (star['_id'], "%s_src_val" % star['_id'])

            mouseover = Event("mouseover", sdom, Script(mouseover), is_function=True)
            mouseout = Event("mouseout", sdom, Script(mouseout), is_function=True)

            manager.vars[js_var] = Var(js_var, star['_src'])
            manager.add(mouseover, True)
            manager.add(mouseout, True)
            manager.add(click, True)

        return dom

    def js(self, request):
        js = ""

        for i in range(1, self.num + 1):
            if i <= self.value:
                img = S(Stars.full, request)
            if i > self.value:
                img = S(Stars.void, request)

            id = "%s_%d" % (self.name, i)
            js_var = "%s_src_val" % id

            js += setvar(js_var, "%s" % img)
            js += 'jQuery("#%s").attr("src", "%s");' % (id, img)

        return js
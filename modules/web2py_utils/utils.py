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


import os

from gluon.html import DIV, URL, H2, FORM, LABEL, P, XML, OL, LI
from gluon.utils import hash

STRFTIME = {
    'time_date': '%I:%M %p %d-%m-%Y',
}

def gURL(request):
    def _URL(*args, **kwargs):
        if kwargs.has_key('r'):
            r = kwargs['r']
            del kwargs['r']
        else:
            r = request

        return URL(r=r, *args, **kwargs)
    return _URL

class LayoutManager():
    # layout.template('layout.html')
    def __init__(self, request, response, url, name,
                base='layout.html',
                autooverride=True):
        """
        Set name to None to use default layouts.
        """
        self._request = request
        self._response = response
        self._url = url
        self._name = name
        self._base = base

        if self._name:
            self._templates_dir = os.path.join('layouts', self._name)
            self._static_dir = url(r=request, c='static', f='layouts', args=self._name)
        else:
            self._templates_dir = ''
            self._static_dir = url(r=request, c='static')

        self._autooverride = autooverride
        if autooverride:
            self.override()

    def __call__(self):
        return self.template(self._base)

    def template(self, filename):
        return os.path.join(self._templates_dir, filename)

    def static(self, filename):
        return os.path.join(self._static_dir, filename)

    def override(self):
        if self._name:
            layout_view = self.template(self._response.view)
            if os.path.isfile(os.path.join(self._request.folder, 'views', layout_view)):
                self._response.view = layout_view

class AdminManager():
    def __init__(self, request, URL):
        self.functions = {}
        self.URL = URL
        self.request = request

    def register(self, function):
        self.functions[function.__name__] = function

    def url(self, function, args=None, vars=None):
        return self.URL(
                    r=self.request,
                    c='admin',
                    f='dispatch/%s' % function.__name__,
                    args=args,
                    vars=vars,
        )

class BUTTON(DIV):
    tag = 'button'

def CONFIRM_BOX(request, session,
                title="Delete Record",
                label="Are you sure you want to delete this record?",
                content="", func_yes=lambda v:v, func_no=lambda v:v):
    form = FORM(
        DIV(
            P(LABEL(label), _class="centered"),
            P(BUTTON("Yes", _type="submit", _name="yes", _value="yes"), _class="centered"),
            P(BUTTON("No", _type="submit", _name="no", _value="no"), _class="centered"),
        )
    )

    html = DIV(
        H2(title),
        DIV(
            DIV(
                form,
                P(content),
            _id="padding"),
        _id="user_action"),
    )

    if form.accepts(request.vars, session):
        if request.vars.yes == "yes":
            func_yes()
        else:
            func_no()
    elif form.errors:
        response.flash = "There were errors with the form"

    return html

def w(q):
    return "%" + q.lower() + "%"

def ws(q):
    ws = '%'.join(qs.lower() for qs in q.split(' '))
    return w(ws)

def decode_phone(phone):
    decoded = ""
    for char in phone:
        if char >= "0" and char <= "9":
            decoded += char
    return decoded
   
def encode_phone(phone):
    if len(phone) == 10:
        return '(' + phone[0:3] + ') ' + phone[3:6] + '-' + phone[6:]
    else:
        return ''

def generate_uuid(record, digest_alg='sha512'):
    """
    Generates a unique identifer for the record
    This is used so that the record can be identified
    without the record id being exposed.
    """
    st = ''
    for k,v in record.items():
        st += '%s=%s|' % k, v

    return hash(st, digest_alg=digest_alg)

def only(what, request, response, template='generic', **kw):
    """
    Makes sure that the exposed action
    always returns the ``what`` data.

    @only('json')
    @only('xml')
    @only('html')
    """
    def decorate(f):
        def _lzy():
            request.extension = what
            response.view = template + '.' + what
            return f()
        return _lzy
    return decorate

def only_wrapper(request, response):
    def _only(what, **kw):
        return only(what, request, response, **kw)
    return _only

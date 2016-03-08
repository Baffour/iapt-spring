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


from gluon.html import OL, UL, LI, A

class MenuManager():
    """
    Manages menu's for blogitizor.

    Example usage

    menu = MenuManager()
    main_menu = MenuItem(
        title, url
        activewhen(
            controller ==
            application ==
            action ==
        )
    """
    TITLE_INDEX = 0
    URL_INDEX = 1
    ACTIVE_INDEX = 2

    def __init__(self, request):
        self.menus = {}
        self.request = request

    def add_menu_item(self, menu, title, url, activewhen=dict(c=None,f=None,a=None,custom=None)):
        if not self.menus.has_key(menu):
            self.menus[menu] = []
        self.menus[menu].append(
            [title, url, self.iam(activewhen)]
        )

    def render_menu(self, menu, type='ol'):
        if type == 'ol':
            xml = OL(_id = menu, _class="menu")
        else:
            xml = UL(_id = menu, _class="menu")
        if self.menus.has_key(menu):
            for item in self.menus[menu]:
                if item[MenuManager.ACTIVE_INDEX]:
                    c = "active"
                else:
                    c = None
                xml.append(
                    LI(
                        A(item[MenuManager.TITLE_INDEX], _href=item[MenuManager.URL_INDEX])
                    , _class=c)
                )
        else:
            xml = ""
        return xml

    def is_active_menu(self, when):
        c = when.get('c', None)
        f = when.get('f', None)
        a = when.get('a', None)
        custom = when.get('custom', None)
        i = False

        if c:
            if c == self.request.controller:
                i = True
            else:
                i = False

        if f:
            fs = f.split('|')
            onehit = False
            for fps in fs:
                if fps == self.request.function:
                    onehit = True
            i = onehit and i

        if a:
            if a == self.request.args:
                i = True and i
            else:
                i = False

        if custom:
            for lambfunc in custom:
                i = lambfunc(i)

        return i
    iam = is_active_menu


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


from gluon.validators import *
from gluon.html import *
from gluon.sqlhtml import *

# usage

#from web2py_utils import widgets
##SQLFORM.widgets.string = widgets.UIWidget('string')
#widgets.replace_all(SQLFORM, ui=True)

jqueryui_content = "ui-widget ui-widget-content ui-corner-all "
jqueryui_header = "ui-widget ui-widget-header ui-corner-all "

lookup = dict(
        string = StringWidget,
        text = TextWidget,
        password = PasswordWidget,
        integer = IntegerWidget,
        double = DoubleWidget,
        time = TimeWidget,
        date = DateWidget,
        datetime = DatetimeWidget,
        boolean = BooleanWidget,
        options = OptionsWidget,
        multiple = MultipleOptionsWidget,
        radio = RadioWidget,
        checkboxes = CheckboxesWidget,
)

def Widget(what, **kwargs):
    class Obj(object):
        @staticmethod
        def widget(f, v, **kw):
            return lookup[what].widget(f,v,
                _class="%s %s" % (kwargs.get('_class', ''),
                                    kw.get('_class', '')), 
                **kw)
    return Obj

def UIWidget(what, **kwargs):
    return Widget(what, _class=jqueryui_content + kwargs.get('_class', ''))

def replace_all(sqlform, ui=False, **kwargs):
    if ui:
        callme = UIWidget
    else:
        callme = Widget
    for k,v in sqlform.widgets.items():
        sqlform.widgets[k] = callme(k, **kwargs)


Resizable = Widget('text', _class='resizable')
WMD_Ignore = Widget('text', _class='wmd-ignore')
WMD_Preview = Widget('text', _class='wmd-preview')
WMD_Output = Widget('text', _class='wmd-output')

class ULRadioWidget(OptionsWidget):
    @staticmethod
    def widget(field, value, **attributes):
        """
        generates a UL tag, including INPUT radios (only 1 option allowed)

        see also: :meth:`FormWidget.widget`
        """

        attr = OptionsWidget._attributes(field, {}, **attributes)

        if isinstance(field.requires, IS_NULL_OR)\
             and hasattr(field.requires.other, 'options'):
            opts = [LI(INPUT(_type='radio', _name=field.name,
                             _value='', value=value), '')]
            options = field.requires.other.options()
        elif hasattr(field.requires, 'options'):
            opts = []
            options = field.requires.options()
        else:
            raise SyntaxError, 'widget cannot determine options of %s' % field
        opts += [LI(INPUT(_type='radio', _name=field.name,
                          requires=attr.get('requires',None),
                          hideerror=True,
                          _value=k, value=value), v) for (k, v) in options if str(v)]
        return UL(*opts, **attr)

class ULCheckboxesWidget(OptionsWidget):

    @staticmethod
    def widget(field, value, **attributes):
        """
        generates a TABLE tag, including INPUT checkboxes (multiple allowed)

        see also: :meth:`FormWidget.widget`
        """

        values = re.compile('[\w\-:]+').findall(str(value))

        attr = OptionsWidget._attributes(field, {}, **attributes)

        if hasattr(field.requires, 'options'):
            opts = []
            options = field.requires.options()
        else:
            raise SyntaxError, 'widget cannot determine options of %s' % field

        opts += [LI(INPUT(_type='checkbox', _name=field.name,
                          requires=attr.get('requires',None),
                          hideerror=True,
                          _value=k, value=(k in values)), v) \
                     for (k, v) in options if str(v)]
        return UL(*opts, **attr)

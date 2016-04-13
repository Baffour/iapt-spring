# IAPT Spring Assessment - Group 13

def format_pence_as_pounds(pence):
    return "{0:.2f}".format(pence/100.0)

def load_item(id, editing=False):
    item = db.itm(id)

    if not item:
        raise HTTP(404)

    owner = auth.user is not None and item.auth_user.id == auth.user.id
    is_private = not item.in_have_list and all(x.private for x in db((db.box.id == db.itm2box.box) & (db.itm2box.itm == item)).select(db.box.private))

    if (editing or is_private) and not owner:
        raise HTTP(403)

    return item

def load_want_item(id, editing=False):
    item = db.want_item(id)

    if not item:
        raise HTTP(404)

    if editing and (not auth.user or item.auth_user.id != auth.user.id):
        raise HTTP(403)

    return item

ICONS_FOR_ITEM_TYPES = {
    'book' : 'book',
    'cd' : 'music',
    'dvd' : 'film',
    'game' : 'modal-window'
}

def icon_for_item_type(item_type):
    icon_name = ICONS_FOR_ITEM_TYPES.get(item_type, 'file')
    return XML('<span class="glyphicon glyphicon-{}"></span>'.format(icon_name))

def load_box(id, editing=False):
    box = db.box(id)

    if not box:
        raise HTTP(404)

    if not auth.user or box.auth_user.id != auth.user.id:
        if editing or box.private:
            raise HTTP(403)

    return box

def load_unfiled_box():
    return db((db.box.auth_user==auth.user) & (db.box.unfiled==True)).select()[0]

def load_trade_proposal(id, editing=False):
    prop = db.trade_proposal(id)

    if not prop:
        raise HTTP(404)

    if not auth.user:
        raise HTTP(403)

    if auth.user.id == prop.sender:
        return prop

    if auth.user.id == prop.target:
        if not editing and prop.status != 'pending':
            return prop
        if editing and prop.status == 'sent':
            return prop

    raise HTTP(403)

def items_in(box):
    items_and_boxes = db((db.box.id==db.itm2box.box) & (db.itm2box.itm==db.itm.id) & (db.box.id==box.id))
    return items_and_boxes.select(db.itm.ALL)

def notification_count():
    if not auth.user:
        return 0
    return db((db.notification.auth_user==auth.user) & (db.notification.unread==True)).count()

def load_public_boxes(user):
    return db((db.box.auth_user == user.id) & (db.box.private == False)).select()

def load_all_public_items(user=None):
    return load_all_items_of_visibility_x(False,user=user)

def load_all_private_items(user=None):
    return load_all_items_of_visibility_x(True,user=user)

def load_all_items_of_visibility_x(private,user=None):
    if user is None:
        db_boxes=db(db.box.private == private).select()
    else:
        db_boxes=db((db.box.private == private) & (db.box.auth_user==user)).select()

    item_ids=set()
    for box in db_boxes:
        items = items_in(box)
        item_ids=item_ids.union(item.id for item in items)

    if not private:
        if user is None:
            have_list_items = db(db.itm.in_have_list==True).select()
        else:
            have_list_items = db((db.itm.in_have_list==True) & (db.itm.auth_user==user)).select()
        item_ids=item_ids.union(i.id for i in have_list_items)

    return db(db.itm.id.belongs(item_ids)).select(db.itm.ALL)

def custom_register_form():
    """Adds placeholders and HTML5 validation, which aids in error prevention as users can correct mistakes before submission"""
    form = auth.register()
    form['_class']='signup-form'
    form.custom.widget.email['_placeholder']="Enter your email address"
    form.custom.widget.username['_placeholder']="Choose a username"
    form.custom.widget.password['_placeholder']="Create a password"
    form.custom.widget.password_two['_placeholder']="Confirm your password"
    form.custom.widget.email['_type']="email"
    for inp in form.elements('input'):
        if inp['_type'] != "submit":
            inp['_required'] = 'required'
    return form

def first_n_rows(rows, n):
    """returns the first n row objects in rows maintaining dictionary attributes"""
    temp = rows.__dict__
    new_rows = rows[:n]
    additional_attributes = {key:temp[key] for key in temp if key not in new_rows.__dict__.keys()}
    new_rows.__dict__.update(additional_attributes)
    return new_rows

def sort_rows(rows,f,reverse=False):
    temp = rows.__dict__
    new_rows = rows.sort(f, reverse=reverse)
    additional_attributes = {key:temp[key] for key in temp if key not in new_rows.__dict__.keys()}
    new_rows.__dict__.update(additional_attributes)
    return new_rows

def max_or_default(sequence):
    if sequence is None or len(sequence) == 0:
        return None
    else:
        return max(sequence)

def compress_image(image_name):
    try:
        img_file=os.path.join(uploadfolder, image_name)
        from PIL import Image
        im = Image.open(img_file)
        im.thumbnail((im.width, im.height), Image.ANTIALIAS)
        im.save(img_file, optimize=True,quality=75)
    except:
        pass
        # If compression fails it's not worth raising an error over, this just helps us meet the file size limit if we have
        # large images and a populated database on submission.

def currency_widget(field, value):
    inp = INPUT(_type="number", _value="{0:.2f}".format(float(value)) if (value is not None and value != '') else None,
                _min=0, _step="0.01", _class="form-control currency_input", requires=field.requires, _name=field.name, _id="%s_%s" % (field._tablename, field.name))
    inp['_data-number-to-fixed'] = 2
    inp['_data-number-step-factor'] = 100
    symbol = DIV("£",_class="input-group-addon currency_symbol")
    wrapper = DIV(symbol, inp,_class="currency_group input-group pull-left")
    return wrapper

def profile_page_link(user,*anchor_attributes):
    """Returns URL for profile page of given user (prevents lengthy repetition)"""
    if not user:
        raise HTTP(404)
    return A(user.username,_href=URL('default','profile_page',vars=dict(user=user)),*anchor_attributes)

def breadcrumbs(arg_title=None):
   "Create breadcrumb links for current request"
   # source:http://www.web2pyslices.com/slice/show/1373/easy-breadcrumbs
   # make links pretty by capitalizing and using 'home' instead of 'default'
   pretty = lambda s: s.replace('default', 'Início').replace('_', ' ').capitalize()
   menus = [A(T('Home'), _href=URL(r=request, c='default', f='index'))]
   if request.controller != 'default':
       # add link to current controller
       menus.append(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f='index')))
       if request.function == 'index':
           # are at root of controller
           menus[-1] = A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f=request.function))
       else:
           # are at function within controller
           menus.append(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function)))
       # you can set a title putting using breadcrumbs('My Detail Title')
       if request.args and arg_title:
           menus.append(A(T(arg_title)), _href=URL(r=request, c=request.controller, f=request.function,args=[request.args]))
   else:
       #menus.append(A(pretty(request.controller), _href=URL(r=request, c=request.controller, f='index')))
       if request.function == 'index':
           # are at root of controller
           #menus[-1] = pretty(request.controller)
           pass
           #menus.append(A(pretty(request.controller), _href=URL(r=request, c=request.controller, f=request.function)))
       else:
           # are at function within controller
           menus.append(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function)))
       # you can set a title putting using breadcrumbs('My Detail Title')
       if request.args and arg_title:
           menus.append(A(T(arg_title), _href=URL(r=request, f=request.function,args=[request.args])))

   return XML(' > '.join(str(m) for m in menus))

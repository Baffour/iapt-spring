# IAPT Spring Assessment - Group 13

def load_item(id, editing=False):
    item = db.itm(id)

    if not item:
        raise HTTP(404)

    if editing and (not auth.user or item.auth_user.id != auth.user.id):
        raise HTTP(403)

    return item

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

def items_in(box):
    items_and_boxes = db((db.box.id==db.itm2box.box) & (db.itm2box.itm==db.itm.id) & (db.box.id==box.id))
    return items_and_boxes.select(db.itm.ALL)

def notification_count():
    if not auth.user:
        return 0
    return db((db.notification.auth_user==auth.user) & (db.notification.unread==True)).count()

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
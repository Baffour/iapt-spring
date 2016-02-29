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

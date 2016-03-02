# IAPT Spring Assessment - Group 13

def search():
    pass

def explore():
    newest=__get_n_newest_boxes(2)
    largest=__get_n_largest_boxes(2)
    valuable=__get_n_most_valuable_boxes(2)
    return dict(explorables=[valuable, largest, newest])


def __get_n_newest_boxes(n):
    db_boxes=db(db.box.private == False).select(orderby=~db.box.created_at,limitby=(0, n))
    boxes=__add_calculated_fields(db_boxes)
    boxes.label="Newest Boxes"
    return boxes


def __get_n_largest_boxes(n):
    db_boxes=db(db.box.private == False).select()
    boxes=__add_calculated_fields(db_boxes)
    boxes=boxes.sort(lambda box: box.quantity, reverse=True)
    boxes=boxes[:n]
    boxes.label="Largest Boxes"
    return boxes

def __get_n_most_valuable_boxes(n):
    bxs=db(db.box.private == False).select()
    boxes=__add_calculated_fields(bxs)
    boxes=boxes.sort(lambda box: box.monetary_value, reverse=True)
    boxes=boxes[:n]
    boxes.label="Most Valuable Boxes"
    return boxes

def __add_calculated_fields(boxes):
    for box in boxes:
        box.quantity=len(db(db.itm2box.box==box).select())
        values=db(
                 (db.box.private == False) &
                 (db.itm2box.box==box) &
                 (db.itm2box.itm == db.itm.id)).select(db.itm.monetary_value, distinct=True)
        box.monetary_value=sum([itm.monetary_value for itm in values])
    return boxes

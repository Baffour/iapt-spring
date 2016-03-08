# IAPT Spring Assessment - Group 13

def search():
    results=None
    db_boxes=db(db.box.private == False).select()
    results=[item for box_items in [items_in(box) for box in db_boxes] for item in box_items]
    return dict(results=results)

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
        items = items_in(box)
        box.quantity = len(items)
        box.monetary_value=sum(item.monetary_value for item in items)
    return boxes

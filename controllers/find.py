# IAPT Spring Assessment - Group 13
import web2py_utils.search
import operator

def search():
    results=None
    if request.vars.query is not None:
        items = load_all_public_items()
        results = __search_by_x(request.vars.query, items, lambda x : x.name)

    if results is None:
        response.flash = "Please enter a search query in the form above"
    elif len(results) == 0:
        response.flash = "No results were found for '{0}'".format(request.vars.query)
    elif len(results) == 1:
        response.flash = "Your search for '{0}' returned 1 result".format(request.vars.query)
    else:
        response.flash = "Your search for '{0}' returned {1} results".format(request.vars.query,len(results))
    return dict(results=results)


def __search_by_x(query, items, func):
    """Given a query and a set of item rows, returns a list of item rows whose attribute (defined by func) is similar to the query"""
    match_attr = __full_text_search(query, [func(item) for item in items], min_sim=0.1)
    if len(match_attr) < 2:
        # If no strings similar to query exist, break items down into individual words and query this
        match_attr = set(match_attr + __similar_items_2(query, [func(item) for item in items]))
        print "Fine grained search", match_attr
    else:
        print match_attr
    results = list()
    for mattr in match_attr:
        results.extend([item for item in items if func(item) == mattr])
    return results

def __full_text_search(query, search_in,min_sim=0.0):
    """Given a query and a list of strings to search in, returns all similar strings from the list"""
    tg = web2py_utils.search.Ngram(search_in, ic=True,min_sim=min_sim )
    search_tuples = tg.getSimilarStrings(request.vars.query)
    results_by_match_level = sorted(search_tuples.items(), key=operator.itemgetter(1), reverse=True)
    match_items = [match[0] for match in results_by_match_level]
    return match_items

def __similar_items_2(query, search_in):
    """Splits strings in the search_list into words and returns all strings containing a words similar to the query"""
    results = list()
    for attr in search_in:
        similar = __full_text_search(query, attr.split(' '),min_sim=0.3)
        if len(similar) > 0:
            print attr.split(' ')#, similar
            results.append(attr)
    return results

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

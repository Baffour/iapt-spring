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
            results.append(attr)
    return results

def explore():
    N=4
    boxes = __get_box_groups_of_n(N)
    users = __get_user_groups_of_n(N)
    havelists= __get_have_lists_of_n(N)
    wantlists= __get_want_lists_of_n(N)
    return dict(explore_boxes=boxes,explore_havelists=havelists,explore_wantlists=wantlists,explore_users=users)

def __get_have_lists_of_n(N):
    get_have_list = lambda user: db((db.itm.auth_user==user) & (db.itm.in_have_list==True)).select()
    user_lists = list()
    for user in db(db.auth_user).select():
        to_add = first_n_rows(get_have_list(user), N)
        if len(to_add):
            to_add.label = "User: {0}".format(user.username)
            user_lists.append(to_add)
    return user_lists

def __get_want_lists_of_n(N):
    get_want_list = lambda user: db(db.want_item.auth_user==user).select()
    user_lists = list()
    for user in db(db.auth_user).select():
        to_add = first_n_rows(get_want_list(user), N)
        if len(to_add):
            to_add.label = "User: {0}".format(user.username)
            user_lists.append(to_add)
    return user_lists

def __get_box_groups_of_n(N):
    newest = first_n_rows(__get_newest_boxes(), N)
    largest = first_n_rows(__get_largest_boxes(), N)
    valuable = first_n_rows(__get_most_valuable_boxes(), N)
    popular = first_n_rows(__get_most_popular_boxes(), N)
    return [valuable, popular, newest, largest]

def __get_user_groups_of_n(N):
    popular = first_n_rows(__get_most_popular_users(), N)
    largest = first_n_rows(__get_users_with_largest_boxes(), N)
    return [popular, largest]

def __get_most_popular_users():
    db_users = db(db.auth_user).select()
    users = __add_calculated_user_info(db_users)
    users = sort_rows(users, lambda user: get_user_popularity(user), reverse=True)
    users.label = "Most Popular Users"
    return users

def __get_users_with_largest_boxes():
    db_users = db(db.auth_user).select()
    users = __add_calculated_user_info(db_users)
    box_sizes = lambda user: [len(items_in(box)) for box in load_public_boxes(user)]
    users = sort_rows(users, lambda user: max_or_default(box_sizes(user)), reverse=True)
    users.explore_info.append(size_of_users_largest_box)
    users.label = "Users with Largest Boxes"
    return users

def __get_newest_boxes():
    db_boxes=db(db.box.private == False).select(orderby=~db.box.created_at)
    boxes=__add_calculated_box_info(db_boxes)
    boxes.explore_info.append(date_created)
    boxes.label = "Newest Boxes"
    return boxes


def __get_largest_boxes():
    db_boxes=db(db.box.private == False).select()
    boxes=__add_calculated_box_info(db_boxes)
    boxes=sort_rows(boxes, lambda box: box.itemcount, reverse=True)
    boxes.explore_info.append(itemcount)
    boxes.label="Largest Boxes"
    return boxes

def __get_most_valuable_boxes():
    bxs=db(db.box.private == False).select()
    boxes=__add_calculated_box_info(bxs)
    boxes=sort_rows(boxes, lambda box: box.monetary_value, reverse=True)
    boxes.explore_info.append(monetary_value)
    boxes.label="Most Valuable Boxes"
    return boxes

def __get_most_popular_boxes():
    bxs=db(db.box.private == False).select()
    boxes=__add_calculated_box_info(bxs)
    boxes=sort_rows(boxes, lambda box: box.popularity, reverse=True)
    boxes.explore_info.append(popularity)
    boxes.label="Most Popular Boxes"
    return boxes

def __add_calculated_box_info(boxes):
    for box in boxes:
        items = items_in(box)
        box.itemcount = len(items)
        box.monetary_value=sum(item.monetary_value for item in items)
        box.popularity = sum(get_item_popularity(item) for item in items)
    boxes.explore_info = [users_name]
    return boxes

def __add_calculated_user_info(users):
    for user in users:
        public_items = [b for b in load_all_public_items() if b.auth_user.id == user.id]
        public_boxes = db((db.box.auth_user == user.id) & (db.box.private == False)).select()
        user.itemcount = len(public_items)
        user.boxcount = len(public_boxes)
        user.popularity = get_user_popularity(user)
    public_itemcount = dict(itemcount)
    public_itemcount['tooltip']= 'Public Items'
    users.explore_info = [public_boxcount, public_itemcount, popularity]
    return users

size_of_users_largest_box = {
            'tooltip':'Largest Box Size',
            'icon' : 'glyphicon-th',
            'data_display' : 'Box of {0}',
            'data' :lambda user: max_or_default([len(items_in(box)) for box in load_public_boxes(user)])
            }

date_created = {
    'tooltip':'Date Created',
    'icon' : 'glyphicon-time',
    'data_display' : '{0}',
    'data': lambda box : box.created_at.strftime("%d/%m/%Y")
}

monetary_value = {
    'tooltip':'Value',
    'icon' : 'glyphicon-credit-card',
    'data_display' : '{0}',
    'data' : lambda box : format_pence_as_pounds(box.monetary_value)
}

itemcount = {
    'tooltip': 'Items',
    'icon' : 'glyphicon-unchecked',
    'data_display' : '{0} Items',
    'data' : lambda x : x.itemcount
}

popularity = {
    'tooltip' : 'Total Item Likes',
    'icon' : 'glyphicon-heart',
    'data_display' : '{0}',
    'data' : lambda x: x.popularity
}

public_boxcount = {
    'tooltip' : 'Public Boxes',
    'icon' : 'glyphicon-th-large',
    'data_display' : '{0} Boxes',
    'data' : lambda user: user.boxcount
}

users_name = {
    'tooltip' : 'View Profile',
    'icon' : 'glyphicon-user',
    'data_display' : '{0}',
    'data' : lambda box: box.auth_user.username,
    'href' : lambda box: URL('default','profile_page',vars=dict(user=box.auth_user.username))
}

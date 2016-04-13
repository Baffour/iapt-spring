class Tag:
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
        'data_display' : '£{0}',
        'data' : lambda x : format_pence_as_pounds(x.monetary_value)
    }

    itemcount = {
        'tooltip': 'Items',
        'icon' : 'glyphicon-unchecked',
        'data_display' : '{0} Items',
        'data' : lambda x : x.itemcount
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
        'href' : lambda box: URL('default','profile_page',vars=dict(user=box.auth_user.id))
    }

    item_type = {
        'tooltip' : 'Type',
        'icon' : 'glyphicon-list',
        'data_display' : '{0}',
        'data' : lambda item: ITEM_TYPES[item.itm_type].capitalize()
    }

    public_itemcount = dict(itemcount)
    public_itemcount['tooltip']= 'Public Items'

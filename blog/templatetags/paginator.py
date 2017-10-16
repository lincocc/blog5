from django import template

register = template.Library()


@register.inclusion_tag('blog/paginator.html', takes_context=True)
def pagination(context, *args, **kwargs):
    paginator = context['paginator']
    page_obj = context['page_obj']
    is_paginated = context['is_paginated']
    object_list = context['object_list']

    page_num = page_obj.number

    pagination_required = is_paginated
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_ENDS))
                page_range.append(None)
                page_range.extend(
                    range(page_num - ON_EACH_SIDE, page_num if page_num >= paginator.num_pages else page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(None)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    def plus_one(l):
        res = []
        for o in l:
            if o is not None:
                res.append(o + 1)
            else:
                res.append(o)
        return res

    page_range = plus_one(page_range)
    return {
        'pagination_required': pagination_required,
        'page_range': page_range,
        'page_num': page_num,
        'page_obj': page_obj,
    }

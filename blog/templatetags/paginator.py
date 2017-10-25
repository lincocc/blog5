from django import template

register = template.Library()


@register.inclusion_tag('blog/paginator.html', takes_context=True)
def pagination(context, *args, **kwargs):
    paginator = context['paginator']
    page_obj = context['page_obj']
    is_paginated = context['is_paginated']

    page_num = page_obj.number

    pagination_required = is_paginated
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        if paginator.num_pages <= 10:
            page_range = paginator.page_range
        else:
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS + 1):
                page_range.extend(range(1, ON_ENDS + 1))
                page_range.append(None)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(1, page_num + 1))

            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS + 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(None)
                page_range.extend(range(paginator.num_pages - ON_ENDS + 1, paginator.num_pages + 1))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages + 1))

    return {
        'pagination_required': pagination_required,
        'page_range': page_range,
        'page_num': page_num,
        'page_obj': page_obj,
    }

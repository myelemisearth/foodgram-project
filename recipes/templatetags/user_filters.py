from django import template

register = template.Library()


@register.filter
def get_tag_url(variable, array):
    tag_url = ''
    for item in array:
        if variable != item:
            tag_url += f'tag={item}&'
    if variable not in array:
        tag_url += f'tag={variable}'
    return tag_url


@register.filter
def get_tag_list(variable, arg):
    return variable.getlist(arg)


@register.filter
def get_recipe_remainder(total, displayed):
    return total - displayed

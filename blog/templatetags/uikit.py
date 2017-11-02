from django import template
from django.forms.widgets import Input, Select, RadioSelect, CheckboxSelectMultiple, Textarea, CheckboxInput
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def uikit_form(form, *args, **kwargs):
    rendered_fields = []
    for field in form:
        rendered_fields.append(render_field(field))

    return mark_safe(render_error(form) + '\n'.join(rendered_fields))


@register.simple_tag
def uikit_form_button(text, name=''):
    return mark_safe('<button class="uk-button uk-button-default" name={} type="submit">{}</button>'.format(name, text))


@register.simple_tag
def uikit_button(text, button_type, name=''):
    return mark_safe(
        '<button class="uk-button uk-button-default" name="{}" type="{}">{}</button>'.format(name, button_type, text))


def render_field(field):
    widget = field.field.widget
    if isinstance(widget, CheckboxInput):
        uk_class = 'uk-checkbox'
    elif isinstance(widget, Input):
        uk_class = 'uk-input'
    elif isinstance(widget, Textarea):
        uk_class = 'uk-textarea'
    elif isinstance(widget, Select):
        uk_class = 'uk-select'
    elif isinstance(widget, RadioSelect):
        uk_class = 'uk-radio'
    elif isinstance(widget, CheckboxSelectMultiple):
        uk_class = 'uk-checkbox'
    else:
        uk_class = ''

    attrs = field.field.widget.attrs
    classes = attrs.get('class', '')
    attrs['class'] = add_css_class(classes, uk_class + ' uk-form-width-medium')

    if isinstance(widget, CheckboxInput):
        return wrap_form_checkbox(field.as_widget(), field.label)
    else:
        return wrap_form_row(field.label_tag(attrs={'class': 'uk-form-label'}) + wrap_form_controls(field.as_widget()))


def render_error(form):
    form_errors = get_fields_errors(form) + form.non_field_errors()
    template = get_template('blog/form_errors.html')
    return template.render({'errors': form_errors})


def get_fields_errors(form):
    form_errors = []
    for field in form:
        if not field.is_hidden and field.errors:
            form_errors += field.errors
    return form_errors


def wrap_form_controls(html):
    return '<div class="uk-form-controls">{}</div>'.format(html)


def wrap_form_row(html):
    return '<div class="uk-margin">{}</div>'.format(html)


def wrap_form_checkbox(html, label):
    return '<div class="uk-margin"><label>{} {}</label></div><br>'.format(html, label)


def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return ''
    return force_text(value)


def split_css_classes(css_classes):
    """
    Turn string into a list of CSS classes
    """
    classes_list = text_value(css_classes).split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class, prepend=False):
    """
    Add a CSS class to a string of CSS classes
    """
    classes_list = split_css_classes(css_classes)
    classes_to_add = [c for c in split_css_classes(css_class)
                      if c not in classes_list]
    if prepend:
        classes_list = classes_to_add + classes_list
    else:
        classes_list += classes_to_add
    return ' '.join(classes_list)

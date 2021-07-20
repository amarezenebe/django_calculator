from django import template
from django.conf import settings

register=template.Library()


@register.filter(name='HtmlField')
def HtmlField(field, otherCss=None):
    # do not forget to put space at the end
    css="form-input "
    if otherCss:
        css=css + otherCss
    field.field.widget.attrs.update({'class': css})
    # print(field)
    return field


@register.filter(name='companyError')
def companyError(strings):
    return 'company/handle/company_errors/' + str(strings) + ".html"


@register.simple_tag
def to_list(field):
    return field.split(',')


@register.simple_tag
def formset(index, name):
    names=name.split(',')
    return str(",".join([f"form-{index}-{name}" for name in names]))


@register.filter(name='contain')
def contain(value, sub):
    return True if str(value).count(sub) > 0 else False


@register.filter(name='test')
def test(o):
    # print(((o.nav.amare)))
    # print(o.resolver_match.url_name)
    # 'app_name', 'app_names', 'args', 'func', 'kwargs', 'namespace', 'namespaces', 'route', 'url_name', 'view_name'
    return o


@register.filter(name='testit')
def testit(o):
    return o


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d=context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k]=v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag(takes_context=True)
def is_active(context, value):
    request=context['request']
    try:
        s=request.resolver_match.app_names[0] + ":" + request.resolver_match.url_name
    except Exception as e:
        s=""

    if s == value:
        return "bg-white text-black px-2"
    else:
        return "text-white"


@register.simple_tag
def settings_value(name):
    x=getattr(settings, name, "loading...")
    return x

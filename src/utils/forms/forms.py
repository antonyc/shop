# -*- coding: utf-8 -*-
__author__ = 'chapson'

from ..policy import javascript_block
from django.forms import Form, ModelForm
from django.forms.forms import BoundField
from django.forms.util import ErrorList
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class AmadikaErrorList(ErrorList):
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<ul class="' + javascript_block('form__errorlist') + '">%s</ul>'
                % ''.join([u'<li>%s</li>' % conditional_escape(force_unicode(e)) for e in self]))


def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
    "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
    top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
    output, hidden_fields = [], []

    for name, field in self.fields.items():
        html_class_attr = ''
        bf = BoundField(self, field, name)
        bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
        if bf.is_hidden:
            if bf_errors:
                top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
            hidden_fields.append(unicode(bf))
        else:
            # Create a 'class="..."' atribute if the row should have any
            # CSS classes applied.
            css_classes = bf.css_classes(javascript_block('form__row'))
            if css_classes:
                html_class_attr = ' class="%s"' % css_classes

            if errors_on_separate_row and bf_errors:
                output.append(error_row % force_unicode(bf_errors))

            if bf.label:
                label = conditional_escape(force_unicode(bf.label))
                # Only add the suffix if the label does not end in
                # punctuation.
                if self.label_suffix:
                    if label[-1] not in ':?.!':
                        label += self.label_suffix
                label = bf.label_tag(label) or ''
            else:
                label = ''

            if field.help_text:
                help_text = help_text_html % force_unicode(field.help_text)
            else:
                help_text = u''
            output.append(normal_row % {
                'errors': force_unicode(bf_errors),
                'label': force_unicode(label),
                'field': unicode(bf),
                'help_text': help_text,
                'html_class_attr': html_class_attr
            })

    if top_errors:
        output.insert(0, error_row % force_unicode(top_errors))

    if hidden_fields: # Insert any hidden fields in the last row.
        str_hidden = u''.join(hidden_fields)
        if output:
            last_row = output[-1]
            # Chop off the trailing row_ender (e.g. '</td></tr>') and
            # insert the hidden fields.
            if not last_row.endswith(row_ender):
                # This can happen in the as_p() case (and possibly others
                # that users write): if there are only top errors, we may
                # not be able to conscript the last row for our purposes,
                # so insert a new, empty row.
                last_row = (normal_row % {'errors': '', 'label': '',
                                          'field': '', 'help_text':'',
                                          'html_class_attr': html_class_attr})
                output.append(last_row)
            output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
        else:
            # If there aren't any rows in the output, just append the
            # hidden fields.
            output.append(str_hidden)
    return mark_safe(u'\n'.join(output))

def as_ul(self):
    "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
    return self._html_output(
        normal_row = u'<li%(html_class_attr)s>%(label)s %(field)s%(errors)s%(help_text)s</li>',
        error_row = u'<li class="' + javascript_block('form__error') + '">%s</li>',
        row_ender = '</li>',
        help_text_html = u' <span class="helptext">%s</span>',
        errors_on_separate_row = False)

class AmadikaModelForm(ModelForm):
    required_css_class = javascript_block('form__required_row')
    extra_classes = javascript_block("form__row")
    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = AmadikaErrorList
        super(AmadikaModelForm, self).__init__(*args, **kwargs)

    as_ul = as_ul
    _html_output = _html_output

class AmadikaForm(Form):
    required_css_class = javascript_block('form__required_row')
    extra_classes = javascript_block("form__row")
    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = AmadikaErrorList
        super(AmadikaForm, self).__init__(*args, **kwargs)

    as_ul = as_ul
    _html_output = _html_output
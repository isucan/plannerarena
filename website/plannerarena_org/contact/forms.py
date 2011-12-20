from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from widgets import RecaptchaChallenge, RecaptchaResponse, EmailDestination

class RecaptchaForm(forms.Form):
    recaptcha_challenge_field = forms.CharField(label=_('Recaptcha challenge'),
            widget=RecaptchaChallenge)
    recaptcha_response_field = forms.CharField(
                widget = RecaptchaResponse,
                label = _('Recaptcha test response'),
                help_text = _('Please enter the two words on the image separated by a space.'),
                error_messages = {
                    'required': _('You did not enter any of the two words shown in the image.')
            }) 

    def __init__(self, *args, **kwargs):
        theme = kwargs.get('recaptcha_theme', '')
        if 'recaptcha_theme' in kwargs:
            del kwargs['recaptcha_theme']
        self._request = kwargs.get('request', '')
        if 'request' in kwargs:
            del kwargs['request']

        super(RecaptchaForm, self).__init__(*args, **kwargs)
        self.fields['recaptcha_response_field'].widget.theme = theme

    def clean_recaptcha_response_field(self):
        if 'recaptcha_challenge_field' in self.cleaned_data:
            self._validate_captcha()
        return self.cleaned_data['recaptcha_response_field']

    def _validate_captcha(self):
        rcf = self.cleaned_data['recaptcha_challenge_field']
        rrf = self.cleaned_data['recaptcha_response_field']
        if rrf == '':
            raise forms.ValidationError(_('You did not enter any of the two words shown in the image.'))
        else:
            from recaptcha.client import captcha as recaptcha
            ip = self._request.META['REMOTE_ADDR']
            private_key = getattr(settings, "RECAPTCHA_PRIVATE_KEY")
            check = recaptcha.submit(rcf, rrf, private_key, ip)
            if not check.is_valid:
                raise forms.ValidationError(_('The words you entered did not match the image.'))
  
class RecaptchaContactForm(RecaptchaForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        recipients = kwargs.get('recipients', [])
        if 'recipients' in kwargs:
            del kwargs['recipients']

        super(RecaptchaContactForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.input_type = 'email'

        for field_name in ['recipient', 'name', 'email', 'subject', 'message']:
            field = self.fields[field_name]
            if field.required:
                field.widget.attrs['required'] = 'true'

        recipient = self.fields['recipient']
        if len(recipients) > 0:
            recipient.choices = recipients
            recipient.initial = recipients[0][0]
            recipient.default = recipients[0][0]
            recipient.widget.is_hidden = len(recipients) == 1

    recipient = forms.ChoiceField(label=_('recipient'), choices=[], widget=EmailDestination)
    name = forms.CharField(label=_('name'))
    email = forms.EmailField(label=_('email'))
    subject = forms.CharField(label=_('subject'))
    message = forms.CharField(label=_('message'), widget=forms.Textarea)


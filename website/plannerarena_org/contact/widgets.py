from django import forms
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.conf import settings

class RecaptchaResponse(forms.Widget):
    is_hidden = True

    def render(self, *args, **kwargs):
        from recaptcha.client import captcha as recaptcha

        public_key = getattr(settings, "RECAPTCHA_PUBLIC_KEY")
        theme = getattr(self, 'theme', '')
        if not theme:
            theme = getattr(settings, "RECAPTCHA_THEME")

        recaptcha_options = u"<script type='text/javascript'> " + \
                "var RecaptchaOptions = {"

        if theme:
            recaptcha_options += " theme: '" + theme + "',"

        recaptcha_options += " lang: '" + get_language()[0:2] + "'" + \
                "}; </script>\n"

        return mark_safe(recaptcha_options + recaptcha.displayhtml(public_key))

class RecaptchaChallenge(forms.Widget):
    is_hidden = True
    def render(self, *args, **kwargs):
        return ""

class EmailDestination(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        if len(self.choices) + len(choices) == 1:
            self.is_hidden = True
            return forms.HiddenInput(attrs=self.attrs).render(name, value, attrs=attrs)
        else:
            self.is_hidden = False
            return super(EmailDestination, self).render(name, value, attrs=attrs, choices=choices)


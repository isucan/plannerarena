from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import ContactPluginModel, ContactRecipient
from forms import RecaptchaContactForm

class ContactPlugin(CMSPluginBase):
    model = ContactPluginModel
    name = _('Contact form')
    render_template = 'contact/contact.html'

    def create_form(self, context, instance, recipients):
        request = context['request']
        recaptcha_theme = context.get('recaptcha_theme', '')
        FormClass = RecaptchaContactForm

        if request.method == "POST":
            return FormClass(request.POST, recipients=recipients, \
                    recaptcha_theme=recaptcha_theme, request=request)
        else:
            return FormClass(recipients=recipients, recaptcha_theme=recaptcha_theme)

    def send(self, form, request):
        subject = form.cleaned_data['subject']
        if not subject:
            subject = _('No subject')

        recipient = ContactRecipient.objects.get(pk=form.cleaned_data['recipient'])

        page_url = 'http://%(domain)s%(page)s' % \
                { 'domain': Site.objects.get_current().domain,
                  'page': request.current_page.get_absolute_url()
                }

        email_context = {
                'form': form.cleaned_data,
                'page_url': page_url,
                'request_meta': {
                    'REMOTE_ADDR': request.META.get('REMOTE_ADDR', ''),
                    'HTTP_USER_AGENT': request.META.get('HTTP_USER_AGENT', '')
                    }
                }

        email_message = EmailMessage(
            _("[Contact page] %(subject)s") % { 'subject': subject },
            render_to_string("contact/email.txt", email_context),
            '',
            [recipient.email],
            headers = { 'Reply-To': form.cleaned_data['email'] })

        email_message.send(fail_silently=False)

    def render(self, context, instance, placeholder):
        request = context['request']
        recipients = []
        if instance.group:
            recipientObjects = ContactRecipient.objects.filter(group=instance.group)
            if recipientObjects.count() > 0:
                recipients = recipientObjects.values_list('pk', 'display_name').order_by('display_name')

        context.update({
            'recipients_len': len(recipients),
        })

        form = self.create_form(context, instance, recipients)

        if request.method == 'POST' and form.is_valid():
            self.send(form, request)
        elif len(recipients) > 0:
            context.update({
                'form': form,
            })

        return context

plugin_pool.register_plugin(ContactPlugin)

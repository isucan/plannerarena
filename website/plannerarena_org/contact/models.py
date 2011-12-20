from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin

class ContactGroup(models.Model):
    title = models.CharField(_('title'), max_length=150)

    class Meta:
        verbose_name = _('contacts group')
        verbose_name_plural = _('groups of contacts')

    def __unicode__(self):
        return self.title

class ContactRecipient(models.Model):
    group = models.ForeignKey(ContactGroup, verbose_name=_('group'))
    display_name = models.CharField(_('name'), max_length=150)
    email = models.EmailField(_('email'), max_length=100)

    class Meta:
        verbose_name = _('recipient')
        verbose_name_plural = _('recipients')
        unique_together = (('group', 'email'), ('group', 'display_name'))

    def __unicode__(self):
        return self.display_name

class ContactPluginModel(CMSPlugin):
    group = models.ForeignKey(ContactGroup, null=True, on_delete=models.SET_NULL, \
            verbose_name=_('group'), \
            help_text=_('The group of email addresses allowed in the destination field for the contact form.'))

    def copy_relations(self, oldinstance):
        self.group = oldinstance.group

    def __unicode__(self):
        if self.group:
            return self.group.title
        return _('<no recipients>')

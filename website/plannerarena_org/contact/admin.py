from models import ContactGroup, ContactRecipient
from django.contrib import admin

class RecipientsInline(admin.TabularInline):
    model = ContactRecipient
    extra = 2

class ContactGroupAdmin(admin.ModelAdmin):
    inlines = [RecipientsInline]

admin.site.register(ContactGroup, ContactGroupAdmin)

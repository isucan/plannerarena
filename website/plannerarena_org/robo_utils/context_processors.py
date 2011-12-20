from django.conf import settings
from django.contrib.sites.models import Site

def sites(request):
    current_site = Site.objects.get_current()
    return {'site': {'id': current_site.id, 'name': current_site.name, 'domain': current_site.domain}}

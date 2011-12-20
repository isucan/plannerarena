from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^sub/', 'results.views.subindex'),
    url(r'^', 'results.views.index'),
)
 

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^geometric/', 'problems.views.subindex_geometric'),
    url(r'^control/', 'problems.views.subindex_control'),
    url(r'^', 'problems.views.index'),
)

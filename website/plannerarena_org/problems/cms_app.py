from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class ProblemsApphook(CMSApp):
    name = 'Problems app'
    urls = ['problems.urls']

apphook_pool.register(ProblemsApphook)

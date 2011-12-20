from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class ResultsApphook(CMSApp):
    name = 'Results App'
    urls = ['results.urls']

apphook_pool.register(ResultsApphook)
 

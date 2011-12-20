from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from tst.menu import *

class TSTApphook(CMSApp):
    name = 'test app'
    urls = ['tst.urls']

apphook_pool.register(TSTApphook)

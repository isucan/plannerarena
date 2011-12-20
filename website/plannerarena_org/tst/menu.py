from django.core.urlresolvers import reverse
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode

class TopLevelMenu(CMSAttachMenu):
    name = 'blah blah menu'
    def get_nodes(self, req):
        nodes = []
        nodes.append(NavigationNode('FF', reverse('tst.views.subindex'), 0))
        return nodes

menu_pool.register_menu(TopLevelMenu)

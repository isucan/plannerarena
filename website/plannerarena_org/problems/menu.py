from django.core.urlresolvers import reverse
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode

class ProblemsMenu(CMSAttachMenu):
    name = 'Problems Menu'
    def get_nodes(self, req):
        nodes = []
        nodes.append(NavigationNode('Geometric', reverse('problems.views.subindex_geometric'), 0))
        nodes.append(NavigationNode('Control', reverse('problems.views.subindex_control'), 0))
        return nodes

menu_pool.register_menu(ProblemsMenu)

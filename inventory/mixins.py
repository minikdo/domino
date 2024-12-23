from django.shortcuts import redirect


class InventorySessionMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(session_data={'inventory_id': self.inventory,
                                    'group_id': self.group,
                                    'show_hidden': self.show_hidden,})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.inventory = request.session.get('inventory_id')
        self.group = request.session.get('group_id')
        self.shelf = request.session.get('shelf_id')
        self.show_hidden = request.session.get('show_hidden', False)
        
        if self.inventory is None:
            return redirect('inventory:inventory_select')

        return super().dispatch(request, *args, **kwargs)

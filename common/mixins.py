class CreatedByMixin(object):
    """ add user id to form """

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

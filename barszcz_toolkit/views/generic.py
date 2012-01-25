from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required



class LoginRequiredView(View):
    """
    View that requires user to be logged in.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


class OwnerSingleObjectView(SingleObjectMixin, LoginRequiredView):
    """
    Mixin that allows access to objects only for it's owner
    (owner field in model must be called 'user').
    """

    def get_object(self, queryset=None):
        """
        we need to ensure object is owned by request.user.
        """
        obj = super(OwnerSingleObjectView, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


class CreateViewWithMessage(CreateView):
    """
    Standard create view but using messages framework to set message
    that object was created.
    """

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _('%(class_verbose_name)s "%(object_name)s" was created.') % {'class_verbose_name': self.object._meta.verbose_name, 'object_name': unicode(self.object)}, fail_silently=True)
        return super(CreateViewWithMessage, self).form_valid(form)


class UpdateViewWithMessage(UpdateView):
    """
    Standard update view but using messages framework to set message
    that object was updated.
    """

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _('%(class_verbose_name)s "%(object_name)s" was updated.') % {'class_verbose_name': self.object._meta.verbose_name, 'object_name': unicode(self.object)}, fail_silently=True)
        return super(UpdateViewWithMessage, self).form_valid(form)


class DeleteViewWithMessage(DeleteView):
    """
    Standard update view but using messages framework to set message
    that object was deleted.
    """

    def delete(self, request, *args, **kwargs):
        """
        Delete object and add message to request.
        """
        self.object = self.get_object()
        self.object.delete()
        # this lie was added:
        messages.success(request, _('%(class_verbose_name)s "%(object_name)s" was deleted.') % {'class_verbose_name': self.object._meta.verbose_name, 'object_name': unicode(self.object)}, fail_silently=True)
        return HttpResponseRedirect(self.get_success_url())


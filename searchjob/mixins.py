from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class BaseUserHasAttrMixins:
    attr_name = None
    redirect_url = None
    inverse = False

    def get_redirect_url(self):
        return self.redirect_url

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, self.attr_name) ^ self.inverse:
            return super().dispatch(request, *args, **kwargs)
        return redirect(self.get_redirect_url())


class UserHasAttrMixin(LoginRequiredMixin, BaseUserHasAttrMixins):
    pass


class UserHasCompany(BaseUserHasAttrMixins):
    attr_name = 'company'
    redirect_url = reverse_lazy('start')


class UserHasNotCompany(UserHasAttrMixin):
    attr_name = 'company'
    redirect_url = reverse_lazy('edit_company')
    inverse = True


class PaginateMixins:
    paginate_by = 4

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect


class CustomLoginRequired(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("""Вы не авторизованы!
                                      Пожалуйста, выполните вход."""))
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)

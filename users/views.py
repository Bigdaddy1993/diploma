from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from users.forms import UserProfileForm, UserRegisterForm
from users.models import Payment, User
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Возвращает текущего пользователя
        """
        return self.request.user


class PaymentCreate(CreateView):

    def get(self, request, *args, **kwargs):
        """
        Создает продукт в страйпе, цену, сессию
        и редиректит на сайт страйпа
        если пользователь уже оплатил подписку то выбрасывает
        исключение в виде ограничения прав доступа
        """
        if request.user.payment:
            raise PermissionDenied
        else:
            user = User.objects.get(pk=request.user.pk)
            payment = Payment.objects.create(date=datetime.now())
            create_stripe_product(payment.pk, payment.date)
            price = create_stripe_price()
            session_id, link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = link
            user.payment = payment
            user.save()
            payment.save()
            return redirect(payment.link)


class PaymentListView(ListView):
    model = Payment
    queryset = Payment.objects.all()

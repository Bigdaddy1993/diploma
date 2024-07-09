from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, Payment
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


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
        return self.request.user


# class PaymentCreateView(CreateView):
#     model = Payment
#     # queryset = Payment.objects.all()
#     template_name = 'users/payment_form.html'
#     fields = '__all__'

def perform_create(request):
    if request.method == 'GET':
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
            return HttpResponsePermanentRedirect(payment.link)


class PaymentListView(ListView):
    model = Payment
    queryset = Payment.objects.all()

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import FormView
from .forms import OTPForm, ForgetPasswordForm
from .models import User, OTP

from datetime import datetime, timedelta
import random
import string


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_otp(user):
    code = random.randint(10000, 99999)
    OTP.objects.create(user=user, code=code)
    return code


def send_otp(user):
    code = generate_otp(user)

    send_mail(
        "Your OTP Code :",
        f"Hi There . There Is Your Code : {code}",
        "efi.dragon20002gmail.com",
        [user.email, ]
    )

    print('send ', code, 'to email ', user.email)


def update_user(request, session, user_entered_code):
    user = User.objects.get(username__exact=session['username'], email__exact=session['email'])
    otp = OTP.objects.get(user__exact=user, code__exact=user_entered_code)

    if str(user_entered_code) == otp.code:

        if 'set_new_password' in session:
            new_pass = generate_random_password()
            user.set_password(new_pass)
            send_mail(
                "رمز ورود شما تغییر کرد :",
                f"رمز عبور شما به ' {new_pass} ' تغییر پیدا کرد .",
                "efi.dragon20002gmail.com",
                [session['email'], ]
            )
            print(new_pass)
        elif 'email' in session:
            user.email = session['email']

        user.save()
        del session
        del otp


def check_delay(request):
    now = datetime.now()

    if 'delay' in request.session:
        str_time = request.session['delay']['time']         # use user  last_request  instead  <========================
        last_try = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    else:
        last_try = now

    if last_try <= now:
        delay = now + timedelta(minutes=3)
        request.session['delay'] = {
            'time': delay.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return True

    time_left = last_try - now
    total_seconds = int(time_left.total_seconds())
    return False, total_seconds


class VerifyView(FormView):
    """
    Verify phone number with otp.
    """
    form_class = OTPForm
    template_name = 'accounts/otp.html'
    success_url = reverse_lazy('shop:home')

    def form_valid(self, form):
        cd = form.cleaned_data
        user_entered_code = cd['code']

        try:
            if 'user_info' in self.request.session:
                session = self.request.session['user_info']
                update_user(self.request, session, user_entered_code)
            return redirect('items:home_page')

        except OTP.DoesNotExist:
            messages.error(self.request, 'کد مورد نظر موجود نیست!')

        return super().form_valid(form)


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "با موفقیت وارد شدید !"
    next_page = reverse_lazy('items:home_page')


class ForgetPasswordView(FormView):
    form_class = ForgetPasswordForm
    template_name = 'accounts/forget_password.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User.objects.get(email__exact=cd['email'])
        delay = check_delay(self.request)
        if delay is True:
            send_otp(user)

            self.request.session['user_info'] = {
                'username': user.username,
                'email': cd['email'],
                'set_new_password': True
            }

            return redirect('auth:verify')

        else:
            messages.warning(self.request, f"{delay[1]} ثانیه صبر کنید.. ")
            form.add_error(None, f"{delay[1]} ثانیه صبر کنید.. ")
            return self.form_invalid(form)

        return super().form_valid(form)

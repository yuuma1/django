from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView       
from .forms import UserInfoChangeForm

class PasswordReset(PasswordResetView):
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    template_name = 'ragistration/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'ragistration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'ragistration/password_reset_complete.html'


class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/change.html'
    form_class = UserInfoChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs

class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/create.html'
    success_url =  reverse_lazy('accounts:profile')
    def form_valid(self, form):
        print(self.request.POST['next'])
        if self.request.POST['next'] == 'back':
            return render(self.request, 'registration/create.html', {'form': form})
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'registration/create_confirm.html', {'form': form})
        elif self.request.POST['next'] == 'regist':
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('snsapp:top'))


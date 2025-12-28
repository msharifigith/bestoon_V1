from django.contrib.auth.models import User
from django import forms
from web.models import income, out


class Incomeforms(forms.Form):
    # person = forms.ForeignKey(User, on_delete=models.CASCADE)
    text = forms.CharField(max_length=255)
    time = forms.DateTimeField()
    amount = forms.IntegerField()
    image = forms.ImageField()


class Comand_forme(forms.Form):
    subject = forms.CharField(max_length=500, required=True, label="موضوع")
    masege = forms.CharField(required=True, label="پیام")
    name = forms.CharField(max_length=50, required=True, label="نام")
    last_name = forms.CharField(required=True, label="نام خانوادگی")
    phone = forms.CharField(max_length=11, label="تلفن")
    email = forms.CharField(max_length=25, required=True, label="ایمیل")


class Share_forme(forms.Form):
    subject = forms.CharField(max_length=50, required=True, label='موضوع')
    massage = forms.CharField(max_length=500, required=True, label='متن')
    name = forms.CharField(max_length=50, required=True, label='نام')
    phone = forms.CharField(max_length=11, label='تلفن')
    to = forms.EmailField(required=True, label='ایمیل')
    # url = forms.CharField(required=True, label='آدرس')


class add_post_income(forms.ModelForm):
    class Meta:
        model = income
        fields = ['text', 'amount', 'image']


class add_post_out(forms.ModelForm):
    class Meta:
        model = out
        fields = ['text', 'amount', 'image']




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

from .models import income, out
from .serialaizer import income_serializers, out_serializers
from web.forms import Incomeforms, Comand_forme, Share_forme, add_post_income
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from .forms import *
from django.shortcuts import render


# Create your views here.
class Home_page(APIView):
    def get(self, request):
        return render(request, "parent/base.html", )


# INCOME

class income_views_all(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users-dashboard/child/income_Expenditure.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            # If not logged in, redirect to login page
            return redirect('account:login')  # Adjust with your actual login URL name
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        queryset = income.objects.filter(person=request.user.id)

        serializer_class = income_serializers(queryset, many=True, context={'request': request})
        return Response({'all': serializer_class.data, 'income_or_expend': 'income', })


# class income_views_search(APIView):
#     def get(self, request):
#         search = request.GET['text']
#         queryset = income.objects.filter(text__contains=search)
#         serializer = income_serializers(queryset, many=True)
#         return Response(serializer.data)


def post_income(request, pk):
    if request.user.is_authenticated:
        query = get_object_or_404(income, pk=pk)
        return render(request, 'users-dashboard/child/post.html', {'post': query, 'income_or_expend': 'income'})
    else:
        return redirect('account:login')


def income_delete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(income, pk=pk)
        if request.method == 'POST':
            post.delete()
            return redirect('web:income_all')
        return render(request, 'users-dashboard/child/post.html', {'post': post, 'income_or_expend': 'income'})
    else:
        return redirect('account:login')


def income_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = add_post_income(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)  # Save the new post to the database
                post.person = request.user
                post.save()
                return redirect('web:income_all')  # Redirect to a page that lists all posts (or another success page)
        else:
            form = add_post_income()
        return render(request, 'users-dashboard/child/add.html', {'form': form, 'income_or_expend': 'income'})
    else:
        return redirect('account:login')


def income_edit(request, pk):
    if request.user.is_authenticated:
        posts = get_object_or_404(income, pk=pk)

        if request.method == 'POST':
            form = add_post_income(request.POST, request.FILES, instance=posts)
            if form.is_valid():
                form.save()
                return redirect('web:income_all')
        else:
            form = add_post_income(instance=posts)

        return render(request, 'users-dashboard/child/edite.html',
                      {'form': form, 'post': posts, 'income_or_expend': 'income'})
    else:
        return redirect('account:login')


def income_share_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(income, pk=pk)
        if request.method == 'POST':
            form = Share_forme(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                subject = form.cleaned_data["subject"]
                massage = form.cleaned_data["massage"]
                phone = form.cleaned_data["phone"]
                to = form.cleaned_data["to"]

                url = request.build_absolute_uri(reverse('web:post', args=(pk,)))

                msg = f"name {name}  \n phone{phone} \n massage {massage} \n go to page {url} "

                send_mail(subject, msg, 'mahdisharifih@gmail.com', [to], fail_silently=False)
                messages.success(request, 'Email sent successfully!')

                return render(request, 'users-dashboard/child/share.html',
                              {'form': form, 'post': post, 'income_or_expend': 'income'})

        form = Share_forme()
        return render(request, 'users-dashboard/child/share.html',
                      {'form': form, 'post': post, 'income_or_expend': 'income'})
    else:
        return redirect('account:login')


def income_featured(request, pk):
    if request.user.is_authenticated:

        post = get_object_or_404(income, pk=pk)
        if post.featured:
            post.featured = False
            post.save()
            return redirect('web:income_all')

        elif not post.featured:
            post.featured = True
            post.save()
            return redirect('web:income_all')
    else:
        return redirect('account:login')


# ================OUT======================
class out_views_all(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users-dashboard/child/income_Expenditure.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            # If not logged in, redirect to login page
            return redirect('account:login')  # Adjust with your actual login URL name
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        queryset = out.objects.filter(person=request.user.id)
        serializer_class = out_serializers(queryset, many=True, context={'request': request})
        return Response({'all': serializer_class.data, 'income_or_expend': 'out'})


class out_views_search(APIView):
    def get(self, request):
        search = request.GET['text']
        queryset = out.objects.filter(text__contains=search)
        serializers = out_serializers(queryset, many=True)
        return Response(serializers.data, status=200)


def post_out(request, pk):
    if request.user.is_authenticated:
        query = out.objects.get(pk=pk)
        return render(request, 'users-dashboard/child/post.html', {'post': query, 'income_or_expend': 'out'})
    else:
        return redirect('account:login')


def out_delete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(out, pk=pk)
        if request.method == 'POST':
            post.delete()
            return redirect('web:out_all')
        return render(request, 'users-dashboard/child/post.html', {'post': post, 'income_or_expend': 'out'})
    else:
        return redirect('account:login')


def out_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = add_post_out(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)  # Save the new post to the database
                post.person = request.user
                post.save()
                return redirect('web:out_all')  # Redirect to a page that lists all posts (or another success page)
        else:
            form = add_post_out()
        return render(request, 'users-dashboard/child/add.html', {'form': form, 'income_or_expend': 'out'})
    else:
        return redirect('account:login')


def out_edit(request, pk):
    if request.user.is_authenticated:
        posts = get_object_or_404(out, pk=pk)

        if request.method == 'POST':
            form = add_post_out(request.POST, request.FILES, instance=posts)
            if form.is_valid():
                form.save()
                return redirect('web:out_all')
        else:
            form = add_post_out(instance=posts)

        return render(request, 'users-dashboard/child/edite.html',
                      {'form': form, 'post': posts, 'income_or_expend': 'out'})
    else:
        return redirect('account:login')


def out_share_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(out, pk=pk)

        if request.method == 'POST':
            form = Share_forme(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                subject = form.cleaned_data["subject"]
                massage = form.cleaned_data["massage"]
                phone = form.cleaned_data["phone"]
                to = form.cleaned_data["to"]

                url = request.build_absolute_uri(reverse('web:out_post', args=(pk,)))

                msg = f"name {name}  \n phone{phone} \n massage {massage} \n go to page {url} "

                send_mail(subject, msg, 'mahdisharifih@gmail.com', [to], fail_silently=False)
                messages.success(request, 'Email sent successfully!')

                return render(request, 'users-dashboard/child/share.html',
                              {'form': form, 'post': post, 'income_or_expend': 'out'})

        form = Share_forme()
        return render(request, 'users-dashboard/child/share.html',
                      {'form': form, 'post': post, 'income_or_expend': 'out'})
    else:
        return redirect('account:login')


def out_featured(request, pk):
    if request.user.is_authenticated:

        post = get_object_or_404(out, pk=pk)
        if post.featured:
            post.featured = False
            post.save()
            return redirect('web:out_all')

        elif not post.featured:
            post.featured = True
            post.save()
            return redirect('web:out_all')

        else:
            # Otherwise, redirect to 'income_default' view (named URL pattern)
            return redirect('web:show_featured')

    else:
        return redirect('account:login')


# 555555555555555555555555555555555555555

# llllllllllllllllll
class Transaction_Registration(TemplateView):
    template_name = 'users-dashboard/child/Transaction_Registration.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            # If not logged in, redirect to login page
            return redirect('account:login')  # Adjust with your actual login URL name
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # You can safely access the user here because dispatch ensured they are authenticated
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Comand_forme(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                last_name = form.cleaned_data["last_name"]
                subject = form.cleaned_data["subject"]
                masege = form.cleaned_data["masege"]
                phone = form.cleaned_data["phone"]
                email = form.cleaned_data["email"]
                msg = f"name {name} \n family {last_name} \n phone{phone} \n email {email} \n masege {masege} "

                send_mail(subject, msg, 'mahdisharifih@gmail.com', ['mahdisharifih@gmail.com'], fail_silently=False)

                sent = True
                return render(request, 'users-dashboard/child/send_report.html', {'form': form, 'sent': sent})

        form = Comand_forme()
        return render(request, 'users-dashboard/child/send_report.html', {'form': form, })
    else:
        return redirect('account:login')


def show_featured(request):
    if request.user.is_authenticated:

        incoms = income.objects.filter(person=request.user.pk)
        outes = out.objects.filter(person=request.user.pk)
        incom = incoms.filter(featured=True)
        oute = outes.filter(featured=True)
        return render(request, 'users-dashboard/child/show_featured.html', {'income': incom, 'out': oute})
    else:
        return redirect('account:login')




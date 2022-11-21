from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import F
from .models import Pres, Category
from .forms import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail



def email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail('от '+request.user.email+', тема:'+form.cleaned_data['subject'],form.cleaned_data['content'],"shevchenko1999viktor@mail.ru",["shevchenko1999viktor@mail.ru"], fail_silently=False)
            if mail==1:
                messages.success(request, 'Письмо отправлено!')
                return redirect('home')
            else:
                messages.success(request, 'Письмо не отправлено!')
        else:
            messages.error(request, 'ОШИБКА')
    else:
        form = ContactForm()
    return render(request, 'pres/email.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка в регистрации')
    else:
        form = UserRegisterForm()
    return render(request,'pres/register.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request,'pres/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

class HomePres(MyMixin ,ListView):
    model = Pres
    template_name = 'pres/home_pres_list.html'
    context_object_name = 'pres'
    extra_context = {'title':'Презентации'}
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.get_upper('Главная страница')
        return context



class PresByCategory(MyMixin, ListView):
    model = Pres
    template_name = 'pres/home_pres_list.html'
    context_object_name = 'pres'
    allow_empty = False
    paginate_by = 5
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Презентации ::'
        context['title_pres'] = self.get_upper(Category.objects.get(id=self.kwargs['category_id']).title)
        return context
    def get_queryset(self):
        return Pres.objects.filter(category_id = self.kwargs['category_id'])

class ViewPres(DetailView):
    model = Pres
    #pk_url_kwarg = 'pres_id'
    template_name = 'pres/pres_detail.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Презентации ::'
        context['pres_item'] = Pres.objects.get(id=self.kwargs['pk'])
        pres = Pres.objects.get(id=self.kwargs['pk'])
        pres.views = F('views') + 1
        pres.save()
        return context

class CreatePres(LoginRequiredMixin,CreateView):
    form_class = PresForm
    template_name = 'pres/add_pres.html'
    success_url = reverse_lazy('home')
    login_url = 'home'


def index(request):
    pres = Pres.objects.all()
    categories = Category.objects.all()
    context = {
        'pres':pres,
        'title': 'Список презентаций',
    }
    return render(request,template_name='pres/index.html',context = context)



def get_category(request, category_id):
    pres = Pres.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request,'pres/category.html',{'pres':pres,'category':category})

def view_pres(request, pres_id):
    #pres = Pres.objects.get(pk=pres_id)
    pres = get_object_or_404(Pres,pk=pres_id)
    context = {'pres_item':pres}
    return render(request,'pres/view_pres.html',context)

def add_pres(request):
    if request.method == 'POST':
        form = PresForm(request.POST,request.FILES)
        if form.is_valid():
            pres = form.save()
            return redirect('home')
    else:
        form = PresForm()
    return render(request,'pres/add_pres.html',{'form':form})
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from .forms import ContactForm




def NewsDetailView(request, news):
    model = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news':model
    }
    return render(request, 'news/single_page.html', context)
    
    
# def homePageView(request):
#     news_list = News.published.all().order_by('-publish_time')
#     categories = Category.objects.all()
#     local_one = News.published.filter().order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name='Mahaliy').order_by('-publish_time')[1:5]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_one': local_one,
#         'local_news': local_news
#     }
    
#     return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')
        context['local_news'] = News.published.all().filter(category__name='Local').order_by('-publish_time')[:5]
        context['foreign_news'] = News.published.all().filter(category__name='Foreign').order_by('-publish_time')[:5]
        context['technology_news'] = News.published.all().filter(category__name='Technology').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]
        
        return context
    




class ContactUsPage(TemplateView):
    template_name = 'news/contact.html'
    
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)
    
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h2>Thanks</h2>')
        
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)
    
    
    
class ErorrPageView(TemplateView):
    
    template_name = 'news/404.html'
    
    

class AboutPageView(TemplateView):
    
    template_name = 'news/about.html'
    
    

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Local')
        return news
    
    
    
class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign_news.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Foreign')
        return news
    
    
    
class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology_news.html'
    context_object_name = 'technology_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Technology')
        return news
    
    
    
class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news
    
    
    

    


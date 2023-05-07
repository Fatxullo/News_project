from django.db.models import Q
from hitcount.views import HitCountDetailView, HitCountMixin
from hitcount.utils import get_hitcount_model
from django.shortcuts import get_object_or_404, render, HttpResponse
from config.custom_permission import OnlyLoggedSuperUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import News, Category
from .forms import ContactForm, CommentForm




def NewsDetailView(request, news):
    
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    
    
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response =  HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['message'] = hit_count_response.hit_counted
        hitcontext['total_hits'] = hits
    
    #for comment section
    comments = news.comments.filter(active=True)
    new_comment = None
    comments_count = comments.count()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) # new comment object but not save to base
            new_comment.news = news
            new_comment.user = request.user # finding this comments user and asigning to this news comment
            new_comment.save() # saving to database
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
        
    context = {
        'news': news,
        'comments ': comments,
        'comments_count': comments_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'news/single_page.html', context)

    
    

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
    


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')
    

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)
    
    context = {
        'admin_user': admin_user
    }
    
    return render(request, 'pages/admin_page.html', context)


class SearchView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'
    
    def get_queryset(self):
        query = self.request.GET.get('search') 
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
            
        )
            
            
    

    


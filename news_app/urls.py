from django.urls import path
from .views import (
    NewsDetailView,
    HomePageView,
    ContactUsPage,
    ErorrPageView,
    AboutPageView,
    LocalNewsView,
    ForeignNewsView,
    TechnologyNewsView,
    SportNewsView,
    NewsUpdateView,
    NewsDeleteView,
    NewsCreateView,
    admin_page_view,
    SearchView
) 


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:news>/', NewsDetailView, name='single_page'),
    path('news/<slug>/edit', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', ContactUsPage.as_view(), name='contact_us_page'),
    path('404/', ErorrPageView.as_view(), name='404_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('category-local/', LocalNewsView.as_view(), name='local_news_page'),
    path('category-foreign/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('category-technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('category-sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('admin-page/', admin_page_view, name='admin_page'),
    path('search', SearchView.as_view(), name='search_results')
    
]

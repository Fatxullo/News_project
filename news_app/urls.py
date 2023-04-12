from django.urls import path
from .views import (
    # NewsListView,
    NewsDetailView,
    HomePageView,
    ContactUsPage,
    ErorrPageView,
    AboutPageView,
    LocalNewsView,
    ForeignNewsView,
    TechnologyNewsView,
    SportNewsView
) 


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    # path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:news>/', NewsDetailView, name='single_page'),
    path('contact-us/', ContactUsPage.as_view(), name='contact_us_page'),
    path('404/', ErorrPageView.as_view(), name='404_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page')
]

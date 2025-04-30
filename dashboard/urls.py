from django.contrib import admin
from django.urls import path
from dashboard import views

admin.site.site_header = "Wizora"
admin.site.site_title = "Wizora Users"
admin.site.index_title = "Wizora"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('birthday', views.birthday_view, name='birthday'),
    path('anniversary', views.anniversary_view, name='anniversary'),
    path('homepage', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save-event/', views.save_event_reminder, name='save_event_reminder'),
    path('wishboard/', views.wishboard, name='wishboard'),
    path('edit-wish/<int:wish_id>/', views.edit_wish, name='edit_wish'),
    path('delete-wish/<int:wish_id>/', views.delete_wish, name='delete_wish'),
    path('birthday_templates/', views.birthday_templates, name='birthday_templates'),
    path('anniversary_templates/', views.anniversary_templates, name='anniversary_templates'),
    path('personal_details/',views.personal_details,name='personal_details')
]

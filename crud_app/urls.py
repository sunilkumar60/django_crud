from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('first/', views.firstFunction, name ="first"),
    path('users', views.users, name ="users.index"),
    path('users/create', views.create, name ="users.create"),
    path('users/edit/<int:user_id>', views.updateUser, name ="users.edit"),
    path('users/delete/<int:user_id>', views.deleteUser, name ="user.delete"),
]

urlpatterns += static(settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT) 
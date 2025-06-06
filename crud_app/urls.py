from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'  # Optional, for namespacing your app URLs

urlpatterns = [
    path('first/', views.firstFunction, name="first"),
    path('user/', include([
        # authentication routes
        path('login/', views.login, name="login"),
        path('signup/', views.signup, name="signup"),
        # user CRUD routes
        path('list/', views.users, name="index"),
        path('create/', views.create, name="create"),
        path('edit/<int:user_id>/', views.updateUser, name="edit"),
        path('delete/<int:user_id>/', views.deleteUser, name="delete"),
    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

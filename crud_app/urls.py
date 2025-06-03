from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('first/', views.firstFunction, name ="first"),
    path('user/', include([
        # authentication routes
        path('login', views.login, name="users.login"),
        path('signup', views.signup, name="users.signup"),
        # user curd routes
        path('', views.users, name="users.index"),
        path('create', views.create, name="users.create"),
        path('edit/<int:user_id>', views.updateUser, name="users.edit"),
        path('delete/<int:user_id>', views.deleteUser, name="user.delete")
    ])),
    
    # path('users', views.users, name ="users.index"),
    # path('users/create', views.create, name ="users.create"),
    # path('users/edit/<int:user_id>', views.updateUser, name ="users.edit"),
    # path('users/delete/<int:user_id>', views.deleteUser, name ="user.delete"),
]

urlpatterns += static(settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT) 
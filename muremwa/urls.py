from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView   # redirect on to the blog's app
from django.conf import settings
from django.conf.urls.static import static
from . import views
from blog.views import PostApiList, PostApiDetail

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # Blog app
    path('blog/', include("blog.urls")),

    # redirect to signup
    path('', RedirectView.as_view(url="/blog/")),

    # Accounts and authentication
    path('accounts/', include("django.contrib.auth.urls")),

    # signup
    path('signup/', views.signup, name="signup"),

    # profile
    path('profile/', views.profile, name="profile"),

    # profile/change-image/
    path('profile/change-image/', views.profile_image, name='change-image'),

    # profile/edit/
    path('profile/edit/', views.edit_user_details, name='edit-profile'),

    # ajax validation
    path('ajax/validate_username', views.validate_username, name="validate_username"),

    # api/all-posts/
    path('api/all-posts/', PostApiList.as_view(), name="api-list"),

    # api/post/23/
    path('api/post/<int:pk>/', PostApiDetail.as_view(), name="api-post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


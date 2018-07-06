from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView   # redirect on to the blog's app
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # Blog app
    path('blog/', include("blog.urls")),

    # redirect to blog
    path('', RedirectView.as_view(url="/blog/")),

    # Accounts and authentication
    path('accounts/', include("django.contrib.auth.urls")),

    # signup
    path('signup/', views.signup, name="signup")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


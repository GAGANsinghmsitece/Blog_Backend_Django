"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.settings import local
from webmash import views
import httplib2
from urllib.parse import urlencode
from django.http import HttpResponse

PROXY_FORMAT = u"http://%s/%s" % (local.PROXY_DOMAIN, u"%s")

def proxy(request, url):
    conn = httplib2.Http()
    # optionally provide authentication for server
    #conn.add_credentials('admin','admin-password')
    if request.method == "GET":
        url_ending = "%s?%s" % (url, urlencode(request.GET))
        url = PROXY_FORMAT % url_ending
        resp, content = conn.request(url, request.method)
        return HttpResponse(content)

urlpatterns = [
    path('webmash/code/blog/gugu/sapora/social/me/admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api',views.api_main,name='api_main'),
    path('api/categories',views.api_categories,name='api_categories'),
    path('api/categories/<int:cat>',views.api_category_detail,name='api_category_detail'),
    path("api/posttags",views.api_posttags,name='api_posttags'),
    path("api/posttags/<int:tag>",views.api_tagdetail,name='api_tagdetail'),
    path("api/post/<int:pkid>",views.api_mainpost,name='api_mainpost'),
    path("api/author",views.api_writer,name="api_writer"),
    path('post/',views.main,name='main'),
    path('',views.main,name='main'),
    path('category',views.category,name='category'),
    path('category/<slug:arg>/',views.catdetail,name='catdetail'),
    path('post/<int:pkid>/',views.postdetail,name='postdetail'),
    path('post_tags',views.posttags,name='posttags'),
    path('post_tags/<slug:arg>/',views.tagdetail,name='tagdetail'),
    path(r'^(?P<url>.*)$', proxy),
    path('search',views.search,name="search")
]

urlpatterns +=staticfiles_urlpatterns()
urlpatterns +=static(local.MEDIA_URL , document_root=local.MEDIA_ROOT)
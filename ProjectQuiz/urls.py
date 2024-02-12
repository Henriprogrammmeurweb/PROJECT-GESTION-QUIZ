
import debug_toolbar
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', include('AppAccount.urls')),
    path('start-quiz/', include('AppQuiz.urls')),
    path('answer/', include('AppAswer.urls')),
]

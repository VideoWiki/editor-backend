from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('sentence_detection.urls')),

    # path('smz/', include('summarization.urls')),

    path('transaction/', include('transaction.urls')),
    path('api/', include('extract_file.urls')),
    path('api/', include('music_library.urls')),
    path('community/', include('community.urls')),



    # for customize user
    path('api/', include('user.urls')),

    # video
    path('api/', include('video.urls')),

    # motion
    path('api/', include('motions.urls')),

    # pitch for vw
    path('api/', include('pitch_for_vw.urls')),

    # authentication
    path('api/auth/login/', obtain_jwt_token),
    path('api/auth/refresh-token/', refresh_jwt_token),
    path('api/auth/verify-token/', verify_jwt_token),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

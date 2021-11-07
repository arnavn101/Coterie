"""hackathon_project_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
import authUser.views
import statsUser.views
import profileUser.views
import locationUser.views
import matchesUser.views
from django.conf.urls.static import static
from hackathon_project_backend.settings import PROFILE_PICTURES, PROFILE_PICTURES_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/account/create', csrf_exempt(authUser.views.CreateAccount.as_view())),
    path('auth/account/login', csrf_exempt(authUser.views.LoginAccount.as_view())), # Implement change password
    path('auth/account/verify', csrf_exempt(authUser.views.VerifyAccount.as_view())),
    path('profile/manage', csrf_exempt(profileUser.views.UpdateProfile.as_view())),
    path('profile/exists', csrf_exempt(profileUser.views.ExistsProfile.as_view())),
    path('profile/details', csrf_exempt(profileUser.views.DetailsProfile.as_view())),
    path('profile/availselections', csrf_exempt(profileUser.views.FieldsSelectionAvail.as_view())),
    path('location/coords', csrf_exempt(locationUser.views.SendCoords.as_view())),
    path('location/bluetooth', csrf_exempt(locationUser.views.SendBluetoothData.as_view())),
    path('matches/request/send', csrf_exempt(matchesUser.views.CreateMatchRequest.as_view())),
    path('matches/request/accept', csrf_exempt(matchesUser.views.AcceptMatchRequest.as_view())),
    path('matches/request/reject', csrf_exempt(matchesUser.views.RejectMatchRequest.as_view())),
    path('matches/request/cancel', csrf_exempt(matchesUser.views.CancelMatchRequest.as_view())),
    path('matches/matchlist', csrf_exempt(matchesUser.views.MatchList.as_view())),
    path('matches/recommendations', csrf_exempt(matchesUser.views.MatchRecommendation.as_view())),
    path('matches/recommendations/cards', csrf_exempt(matchesUser.views.UIDCardsRecommends.as_view())),
    path('matches/card', csrf_exempt(matchesUser.views.UIDCard.as_view())),
    path('statboard', csrf_exempt(statsUser.views.UserStats.as_view())),
] + static(PROFILE_PICTURES_ROOT, document_root=PROFILE_PICTURES)

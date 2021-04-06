from django.urls import path
from . import views

urlpatterns = [
	# overview
	path('', views.apiOverview, name="api-overview"),

	# user crud
	path('user-list/', views.userList, name="user-list"),
	path('user-detail/<str:pk>/', views.userDetail, name="user-detail"),
	path('user-create/', views.userCreate, name="user-create"),
	path('user-update/<str:pk>/', views.userUpdate, name="user-update"),
	path('user-delete/<str:pk>/', views.userDelete, name="user-delete"),

	# stra crud
	path('strat-list/', views.strategyList, name="stret-list"),
	path('strat-detail/<str:pk>/', views.strategyDetail, name="stret-detail"),
	path('strat-create/', views.strategyCreate, name="stret-create"),
	path('strat-update/<str:pk>/', views.strategyUpdate, name="stret-update"),
	path('strat-delete/<str:pk>/', views.strategyDetail, name="stret-delete"),

	# result crud
	path('result-list/', views.resultList, name="result-list"),
	path('result-detail/<str:pk>/', views.resultDetail, name="result-detail"),
	path('result-create/', views.resultCreate,  name="result-create"),
	path('result-update/<str:pk>/', views.resultUpdate, name="result-update"),
	path('result-delete/<str:pk>/', views.resultDetail, name="result-delete"),
]

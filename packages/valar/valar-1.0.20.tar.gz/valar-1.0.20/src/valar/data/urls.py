from django.urls import path, include

from ..data import views

urlpatterns = [
    path('<str:db>/<str:entity>/save_one', views.save_one),
    path('<str:db>/<str:entity>/save_many', views.save_many),
    path('<str:db>/<str:entity>/save_file', views.save_file),

    path('<str:db>/<str:entity>/update_many', views.update_many),
    path('<str:db>/<str:entity>/delete_one', views.delete_one),
    path('<str:db>/<str:entity>/delete_many', views.delete_many),
    path('<str:db>/<str:entity>/find_one', views.find_one),
    path('<str:db>/<str:entity>/find_many', views.find_many),
    path('find_file/<str:bucket_name>/<str:object_name>', views.find_file),
    path('<str:db>/<str:entity>/tree', views.tree),

    # path('data/<str:db>/<str:entity>/', include('src.valar.data.urls')),

    path('add_fields', views.add_fields),
    path('fields', views.fields),
    path('meta', views.meta),
    path('metas', views.metas),
]

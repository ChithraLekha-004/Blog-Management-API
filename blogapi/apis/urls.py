from django.urls import path
from . import views

urlpatterns = [
    path('apis',views.blogApi),
    path('apis/<int:key>',views.blogApi),
    path('apis/<int:key>/comments',views.comments),
    path('apis/<int:key>/comments/<int:comment_id>',views.comments)
]

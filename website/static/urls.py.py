from django.urls import path
from .models import InstagramPostPage

urlpatterns = [
    # Other URL patterns
    path('get_post_content/<int:post_id>/', InstagramPostPage.get_post_content, name='get_post_content'),
]

from django.urls import path, include

from .views import home,send_push,save_info
from django.views.generic import TemplateView

urlpatterns = [
                path('', home), 
                path('send_push/', send_push),  
                path('save_subscription/',save_info),
                path('test/', TemplateView.as_view(template_name='test.html'))
                
              ]
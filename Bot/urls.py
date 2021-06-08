import re
from .views import (list,
retrive,
update,
create,add_xp,
delete)
from django.urls import path 

urlpatterns =[
    path('list/',list),
    path('update/',update), 
    path('create/',create), 
    path('<int:pk>/',retrive),
    path('<int:pk>/xp/',add_xp), 
    path('delete/<int:pk>/',delete)
]
from django.urls import path,include
from .import views
from .views import DetailPostView

urlpatterns = [

    path('detail/<int:id>/',DetailPostView.as_view(), name='detail_book'),
    path('buy/<int:book_id>/', views.borrow, name='borrow'),
    path('return/<int:purchase_id>/', views.return_book, name='return_book'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('home/', views.home, name='home'),
    path("change-password/", views.change_password, name="change_password"),
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('catalog/', views.catalog, name='catalog'), 
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('upgrade/<str:level>/', views.upgrade_membership, name='upgrade_membership'),
    path("membership/", views.membership, name="membership"),
    path("payment/", views.payment, name="payment"),
    path("process-payment/", views.process_payment, name="process_payment"),
    path('payment_done/', views.payment_done, name='payment_done'),

    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path("api/users/<int:user_id>/delete/", views.delete_user_api, name="delete_user_api"),
    path("api/add-book/", views.add_book, name="add_book"),
    path("add-book/", views.add_book, name="add_book"),
    path("api/books/", views.book_list, name="book_list"),
    path("api/books/<int:book_id>/", views.book_detail, name="book_detail"),

]

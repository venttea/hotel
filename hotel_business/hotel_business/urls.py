from django.contrib import admin
from django.urls import path
from hotel import views

urlpatterns = [

    # Админка
    path('admin/', admin.site.urls),

    # Вход в систему
    path('', views.login_view, name='login'),

    # Вход в систему
    path('login/', views.login_view, name='login'),

    # Выход из системы
    path('logout/', views.logout_view, name='logout'),

    # Главная страница (после авторизации)
    path('home/', views.home, name='home'),

    # Список услуг доступный всем
    path('services/', views.service_list, name='service_list'),

    # Страница имеющихся бронирований
    path('bookings/', views.booking_list, name='booking_list'),

    # Страница создания бронирования
    path('bookings/create/', views.booking_create, name='booking_create'),

    # Просмотр списка клиентов для менеджера
    path('manager/clients/', views.client_list, name='client_list'),

    # Страница номерного фонда с фильтрацией
    path('manager/rooms/', views.room_list, name='room_list'),

    # Страница записи клиента на услугу для менеджера
    path('manager/book-service/', views.book_service, name='book_service'),
]
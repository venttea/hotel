from django.contrib import admin
from django.urls import path
from hotel import views as hotel_views

urlpatterns = [

    # Админка
    path('admin/', admin.site.urls),

    # Вход в систему
    path('', hotel_views.login_view, name='login'),
    path('login/', hotel_views.login_view, name='login'),
    path('logout/', hotel_views.logout_view, name='logout'),

    # Главная страница (после входа)
    path('home/', hotel_views.home, name='home'),

    # Страница доступная без авторизации
    path('services/', hotel_views.service_list, name='service_list'),

    # Страница имеющихся бронирований
    path('bookings/', hotel_views.booking_list, name='booking_list'),

    # Страница создания бронирования
    path('bookings/create/', hotel_views.booking_create, name='booking_create'),

    # Просмотр списка клиентов от лица менеджера
    path('manager/clients/', hotel_views.client_list, name='client_list'),

    # Просмотр услуг от лмца менеджера
    path('manager/services/', hotel_views.manager_service_list, name='manager_service_list'),

    # Страница номерного фонда
    path('manager/rooms/', hotel_views.room_list, name='room_list'),

    # Страница записи клиента на услугу
    path('manager/book-service/', hotel_views.book_service, name='book_service'),

    # Страница просмотра записей клиентов на услуги
    path('manager/service-bookings/', hotel_views.view_service_bookings, name='view_service_bookings'),
]
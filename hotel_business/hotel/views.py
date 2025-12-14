from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Service, Booking, Guest, Suite, Category, ServiceBooking
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Service, Booking, Guest, Suite


# Обработка входа пользователя в систему
def login_view(request):
    if request.method == 'POST':

        # Получение логина и пароля из формы
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Проверка существования пользователя с такими данными
        if user is not None:

            # Вход в систему, в случае, если данные есть в системе
            login(request, user)
            return redirect('home')
        else:

            # В случае неудачи - вывод ошибки
            return render(request, 'hotel/login.html', {'error': 'Неверный логин или пароль'})

    # Демонстрация страницы авторизации
    return render(request, 'hotel/login.html')


# Обработка выхода из системы
def logout_view(request):
    logout(request)
    return redirect('login')


# Демонстрация списка услуг всем пользователям
def service_list(request):
    services = Service.objects.all()
    return render(request, 'hotel/service_list.html', {'services': services})


# Главная страница после авторизации
# Декоратор следит за тем, авторизован ли пользователь
@login_required
def home(request):
    return render(request, 'hotel/home.html')


# Страница бронирований пользователя
@login_required
def booking_list(request):

    # Поиск гостя по имени пользователя
    username = request.user.username
    if username == 'ivanov':
        guest = Guest.objects.get(FIO__contains='Иванов')
    elif username == 'petrova':
        guest = Guest.objects.get(FIO__contains='Петрова')
    elif username == 'sidorov':
        guest = Guest.objects.get(FIO__contains='Сидоров')
    else:
        guest = None

    # Поиск бронирований пользователя
    if guest:
        user_bookings = Booking.objects.filter(Guest_id=guest)
    else:
        user_bookings = Booking.objects.none()

    # Передача найденных данных в шаблон
    return render(request, 'hotel/booking_list.html', {'bookings': user_bookings})


# Страница создания бронирования (пока не рабочая)
@login_required
def booking_create(request):
    if request.method == 'POST':
        return redirect('booking_list')
    return render(request, 'hotel/booking_create.html')


# === ФУНКЦИОНАЛ МЕНЕДЖЕРА ===


# Проверка: является ли пользователь менеджером?
def is_manager(user):
    return user.username == "Менеджер"


# Просмотр списка клиентов
@login_required
@user_passes_test(is_manager)
def client_list(request):
    clients = Guest.objects.all()
    return render(request, 'hotel/client_list.html', {'clients': clients})

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


# Просмотр услуг с поиском
@login_required
@user_passes_test(is_manager)
def manager_service_list(request):
    services = Service.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        services = services.filter(Name__icontains=search_query)

    return render(request, 'hotel/service_list.html', {
        'services': services,
        'search_query': search_query
    })


# Просмотр номерного фонда с фильтрацией
@login_required
@user_passes_test(is_manager)
def room_list(request):
    rooms = Suite.objects.all()
    categories = Category.objects.all()

    # Фильтр по количеству кроватей
    beds = request.GET.get('beds')
    if beds:
        rooms = rooms.filter(Quantity_bed=beds)

    # Фильтр по категории
    category = request.GET.get('category')
    if category:
        rooms = rooms.filter(Category_id=category)

    return render(request, 'hotel/room_list.html', {
        'rooms': rooms,
        'categories': categories,
        'current_beds': beds or '',
        'current_category': category or ''
    })


# Запись клиента на услугу
@login_required
@user_passes_test(is_manager)
def book_service(request):
    if request.method == 'POST':
        guest_id = request.POST.get('guest')
        service_id = request.POST.get('service')
        date = request.POST.get('date')

        # Сохранение записи
        ServiceBooking.objects.create(
            guest_id=guest_id,
            service_id=service_id,
            booking_date=date
        )
        return redirect('book_service')

    guests = Guest.objects.all()
    services = Service.objects.all()

    return render(request, 'hotel/book_service.html', {
        'guests': guests,
        'services': services
    })


# Страница просмотра записей клиентов на услуги
@login_required
@user_passes_test(is_manager)
def view_service_bookings(request):
    bookings = ServiceBooking.objects.all().order_by('-booking_date')
    return render(request, 'hotel/view_bookings.html', {'bookings': bookings})
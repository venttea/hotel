from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import *
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


# Главная страница после авторизации
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
    elif username == "kozlova":
        guest = Guest.objects.get(FIO__contains="Козлова")
    elif username == "vasilev":
        guest = Guest.objects.get(FIO__contains="Васильев")
    elif username == "nikolaeva":
        guest = Guest.objects.get(FIO__contains="Николаева")
    elif username == "morozov":
        guest = Guest.objects.get(FIO__contains="Морозов")
    elif username == "orlova":
        guest = Guest.objects.get(FIO__contains="Орлова")
    else:
        guest = None

    # Поиск бронирований пользователя
    if guest:
        user_bookings = Booking.objects.filter(Guest_id=guest)
    else:
        user_bookings = Booking.objects.none()
    return render(request, 'hotel/booking_list.html', {'bookings': user_bookings})


# Страница создания бронирования (НЕ РАБОЧАЯ)
@login_required
def booking_create(request):
    if request.method == 'POST':
        return redirect('booking_list')
    return render(request, 'hotel/booking_create.html')


# === ФУНКЦИОНАЛ МЕНЕДЖЕРА ===


# Проверка: является ли пользователь менеджером?
def is_manager(user):
    return user.username == "Менеджер"

# Отображение услуг всем типам пользователей
def service_list(request):
    services = Service.objects.all()

    # Поиск для менеджера
    search_query = request.GET.get('q', '')
    if request.user.is_authenticated and request.user.username == "Менеджер" and search_query:
        services = services.filter(Name__icontains=search_query)

    # Поиск пользователя для расчета цены с учетом скидки
    guest = None
    if request.user.is_authenticated and request.user.username != "Менеджер":
        try:
            username = request.user.username
            if username == "ivanov":
                guest = Guest.objects.get(FIO__contains="Иванов")
            elif username == "petrova":
                guest = Guest.objects.get(FIO__contains="Петрова")
            elif username == "sidorov":
                guest = Guest.objects.get(FIO__contains="Сидоров")
            elif username == "kozlova":
                guest = Guest.objects.get(FIO__contains="Козлова")
            elif username == "vasilev":
                guest = Guest.objects.get(FIO__contains="Васильев")
            elif username == "nikolaeva":
                guest = Guest.objects.get(FIO__contains="Николаева")
            elif username == "morozov":
                guest = Guest.objects.get(FIO__contains="Морозов")
            elif username == "orlova":
                guest = Guest.objects.get(FIO__contains="Орлова")
        except:
            guest = None

    # Список услуг с рассчитаными ценами
    services_data = []

    for service in services:
        service_data = {
            'service': service,
            'original_price': service.Price,
            'discounted_price': service.Price,
            'has_discount': False,
            'discount_percent': 0
        }

        # Расчет скидки для клиента
        if guest and guest.Discount > 0:
            discount_decimal = guest.Discount / 100
            discounted_price = float(service.Price) * (1 - discount_decimal)

            # Обновление данных услуги
            service_data.update({
                'discounted_price': discounted_price,
                'has_discount': True,
                'discount_percent': guest.Discount
            })

        # Добавление услуги в общий список
        services_data.append(service_data)

    # Подготовка данных для шаблона
    context = {
        'services_data': services_data,
        'guest': guest,
        'user': request.user,
    }

    # Доп. данные для менеджера
    if request.user.is_authenticated and request.user.username == "Менеджер":
        context['search_query'] = search_query
    return render(request, 'hotel/service_list.html', context)


# Отображение номерного фонда с фильтрацией
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


# Отображение страницы "Запись клиента на услугу"
@login_required
@user_passes_test(is_manager)
def book_service(request):
    if request.method == 'POST':
        guest_id = request.POST.get('guest')
        service_id = request.POST.get('service')
        date = request.POST.get('date')

        try:
            # Объекты для сообщения
            guest = Guest.objects.get(id=guest_id)
            service = Service.objects.get(id=service_id)

            # Сохранение записи
            ServiceBooking.objects.create(
                guest_id=guest_id,
                service_id=service_id,
                booking_date=date
            )


        # Сообщение об ошибке
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')

        # Перенаправление на страницу "Запись на услугу"
        return redirect('book_service')

    guests = Guest.objects.all()
    services = Service.objects.all()

    return render(request, 'hotel/book_service.html', {
        'guests': guests,
        'services': services
    })
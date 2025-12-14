from django.contrib.auth.models import User
from django.db import models


# ДОКУМЕНТ (паспорт)
class Document(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    date_of_issue = models.DateField()
    issued_by = models.CharField(max_length=200)

    def __str__(self):
        return f"Паспорт {self.series} {self.number}"


# КАТЕГОРИЯ
class Category(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.price} руб."


# ПРЕДМЕТ
class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ГОСТЬ
class Guest(models.Model):
    FIO = models.CharField(max_length=100)
    Number_of_phone = models.CharField(max_length=11)
    Date_of_birth = models.DateField()
    Document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='guests')
    Discount = models.IntegerField()

    def __str__(self):
        return f"{self.FIO} (тел: {self.Number_of_phone})"


# НОМЕР
class Suite(models.Model):
    Floor = models.IntegerField()
    Quantity_room = models.IntegerField()
    Quantity_bed = models.IntegerField()
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='suites')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Номер №{self.id} - {self.Category_id.title} ({self.Quantity_room} комн., {self.Quantity_bed} мест)"


# ОСНАЩЕНИЕ
class Equipment(models.Model):
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='equipments')
    Item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='equipments')

    class Meta:
        unique_together = (('Category_id', 'Item_id'),)

    def __str__(self):
        return f"{self.Category_id.title} - {self.Item_id.name}"


# БРОНИРОВАНИЕ
class Booking(models.Model):
    Guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    Room_id = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='bookings')
    Arrival_date = models.DateField()
    Departure_date = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Paid_fact = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Бронь #{self.id} - {self.Guest_id.FIO} ({self.Arrival_date} - {self.Departure_date})"


# УСЛУГА
class Service(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name} - {self.Price} руб."


# ОКАЗАНИЕ УСЛУГИ
class Provision(models.Model):
    Booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='provisions')
    Service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='provisions')
    Quantity = models.IntegerField()
    Date_of_provision = models.DateField()

    def __str__(self):
        return f"Услуга '{self.Service_id.Name}' для брони #{self.Booking_id.id} ({self.Date_of_provision})"


# РОЛИ
class UserRole(models.Model):
    ROLE_CHOICES = (('admin', 'Администратор'), ('manager', 'Менеджер'), ('client', 'Клиент'))
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


# Связывает каждого пользователя (User) с его ролью и, если он клиент, с записью в таблице Guest.
# Стандартный User уже содержит логин, пароль, email, имя и фамилию.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    guest = models.OneToOneField('Guest', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'


# Запись на услуги
class ServiceBooking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='service_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest.FIO} - {self.service.Name} ({self.booking_date})"
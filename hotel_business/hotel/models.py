from django.contrib.auth.models import User
from django.db import models


# ДОКУМЕНТ (паспорт)
class Document(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    date_of_issue = models.DateField()
    issued_by = models.CharField(max_length=200)


# КАТЕГОРИЯ
class Category(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


# ПРЕДМЕТ
class Item(models.Model):
    name = models.CharField(max_length=100)


# ГОСТЬ
class Guest(models.Model):
    FIO = models.CharField(max_length=100)
    Number_of_phone = models.CharField(max_length=11)
    Date_of_birth = models.DateField()
    Document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='guests')
    Discount = models.IntegerField()


# НОМЕР
class Suite(models.Model):
    Floor = models.IntegerField()
    Quantity_room = models.IntegerField()
    Quantity_bed = models.IntegerField()
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='suites')
    is_available = models.BooleanField(default=True)


# ОСНАЩЕНИЕ
class Equipment(models.Model):
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='equipments')
    Item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='equipments')

    class Meta:
        unique_together = (('Category_id', 'Item_id'),)


# БРОНИРОВАНИЕ
class Booking(models.Model):
    Guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    Room_id = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='bookings')
    Arrival_date = models.DateField()
    Departure_date = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Paid_fact = models.DecimalField(max_digits=10, decimal_places=2)


# УСЛУГА
class Service(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.CharField(max_length=100)


# ОКАЗАНИЕ УСЛУГИ
class Provision(models.Model):
    Booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='provisions')
    Service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='provisions')
    Quantity = models.IntegerField()
    Date_of_provision = models.DateField()


# РОЛИ
class UserRole(models.Model):
    ROLE_CHOICES = (('admin', 'Администратор'), ('manager', 'Менеджер'), ('client', 'Клиент'))
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)


# Связывает каждого пользователя (User) с его ролью и, если он клиент, с записью в таблице Guest.
# Стандартный User уже содержит логин, пароль, email, имя и фамилию.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    guest = models.OneToOneField('Guest', on_delete=models.SET_NULL, null=True, blank=True)
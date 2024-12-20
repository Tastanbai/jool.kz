# from django.conf import settings
# from django.db import models

# class Seat(models.Model):
#     bus = models.ForeignKey('Bus', on_delete=models.CASCADE, related_name='bus_seats')
#     seat_number = models.IntegerField()
#     is_reserved = models.BooleanField(default=False)
#     reserved_by = models.CharField(max_length=255, null=True, blank=True)
#     reserved_phone = models.CharField(max_length=15, null=True, blank=True)
#     reserved_email = models.EmailField(null=True, blank=True)

#     def __str__(self):
#         return f"Seat {self.seat_number} on {self.bus.number}"




# class Bus(models.Model):
#     number = models.CharField(max_length=10)
#     from_location = models.CharField(max_length=100)
#     to_location = models.CharField(max_length=100)
#     departure_date = models.DateField(null=True)
#     departure_time = models.TimeField(null=True)
#     seats = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return f"Bus {self.number} from {self.from_location} to {self.to_location}"

#     def get_free_seats(self):
#         # Получаем количество свободных мест
#         return self.bus_seats.filter(is_reserved=False)

#     def get_free_seats_count(self):
#         # Возвращаем количество свободных мест
#         return self.get_free_seats().count()

#     def get_reserved_seats_count(self):
#         # Возвращаем количество занятых мест
#         return self.get_reserved_seats().count()
    
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=Bus)
# def create_seats(sender, instance, created, **kwargs):
#     if created:
#         for i in range(1, instance.seats + 1):
#             Seat.objects.create(bus=instance, seat_number=i)

from django.conf import settings
from django.db import models

class Seat(models.Model):
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE, related_name='bus_seats')
    seat_number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    reserved_by = models.CharField(max_length=255, null=True, blank=True)
    reserved_phone = models.CharField(max_length=15, null=True, blank=True)
    reserved_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.bus.number}"

class Bus(models.Model):
    BUS_TYPES = (
        ('sitting', 'Сидящий'),
        ('sleeping', 'Спящий'),
    )

    number = models.CharField(max_length=10)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_date = models.DateField(null=True)
    departure_time = models.TimeField(null=True)
    seats = models.IntegerField()  # Количество мест в автобусе
    price = models.DecimalField(max_digits=10, decimal_places=2)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES, default='sitting')  # Новое поле для типа автобуса

    def __str__(self):
        return f"{self.get_bus_type_display()} Bus {self.number} from {self.from_location} to {self.to_location}"

    def get_free_seats(self):
        # Получаем количество свободных мест
        return self.bus_seats.filter(is_reserved=False)

    def get_free_seats_count(self):
        # Возвращаем количество свободных мест
        return self.get_free_seats().count()

    def get_reserved_seats_count(self):
        # Возвращаем количество занятых мест
        return self.bus_seats.filter(is_reserved=True).count()

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Bus)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.seats + 1):
            Seat.objects.create(bus=instance, seat_number=i)
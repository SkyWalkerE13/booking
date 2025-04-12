from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Hotel, Room
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем заполнение базы данных...')

        # Создаем отели
        hotels = [
            {
                'name': 'Гранд Отель',
                'description': 'Роскошный 5-звездочный отель в центре города.',
                'address': 'ул. Центральная, 1, Москва',
                'rating': 4.8,
            },
            {
                'name': 'Морской бриз',
                'description': 'Уютный отель на берегу моря.',
                'address': 'Приморский бульвар, 15, Сочи',
                'rating': 4.5,
            },
            {
                'name': 'Бизнес Плаза',
                'description': 'Современный отель для деловых поездок.',
                'address': 'пр. Ленина, 42, Санкт-Петербург',
                'rating': 4.3,
            },
        ]

        for hotel_data in hotels:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            if created:
                self.stdout.write(f'Создан отель: {hotel.name}')
            else:
                self.stdout.write(f'Отель уже существует: {hotel.name}')

        # Создаем номера для каждого отеля
        room_types = ['standard', 'deluxe', 'suite', 'family']
        #prices = {'standard': 3000, 'deluxe': 5000, 'suite': 8000, 'family': 6000}
        prices = {'standard': 35, 'deluxe': 55, 'suite': 90, 'family': 65}
        capacities = {'standard': 2, 'deluxe': 2, 'suite': 3, 'family': 4}

        for hotel in Hotel.objects.all():
            for room_type in room_types:
                # Создаем 3-5 номеров каждого типа
                for i in range(random.randint(3, 5)):
                    room_number = f"{100 + i + 1}" if room_type == 'standard' else \
                        f"{200 + i + 1}" if room_type == 'deluxe' else \
                            f"{300 + i + 1}" if room_type == 'suite' else f"{400 + i + 1}"

                    room, created = Room.objects.get_or_create(
                        hotel=hotel,
                        number=room_number,
                        defaults={
                            'room_type': room_type,
                            'description': f"Комфортабельный номер типа {room_type}",
                            'price_per_night': prices[room_type],
                            'capacity': capacities[room_type],
                            'available': True,
                        }
                    )

                    if created:
                        self.stdout.write(f'Создан номер: {room.number} в отеле {hotel.name}')
                    else:
                        self.stdout.write(f'Номер уже существует: {room.number} в отеле {hotel.name}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
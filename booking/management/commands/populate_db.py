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
                'description': 'Роскошный 5-звездочный отель в центре города с прекрасным видом и первоклассным обслуживанием.',
                'address': 'ул. Центральная, 1, Москва',
                'rating': 4.8,
            },
            {
                'name': 'Морской бриз',
                'description': 'Уютный отель на берегу моря, идеальный для спокойного семейного отдыха.',
                'address': 'Приморский бульвар, 15, Сочи',
                'rating': 4.5,
            },
            {
                'name': 'Бизнес Плаза',
                'description': 'Современный отель с конференц-залами и всем необходимым для деловых поездок.',
                'address': 'пр. Ленина, 42, Санкт-Петербург',
                'rating': 4.3,
            },
            {
                'name': 'Горный Пик',
                'description': 'Живописный отель в горах с потрясающими видами и доступом к лыжным трассам.',
                'address': 'ул. Горная, 8, Красная Поляна',
                'rating': 4.7,
            },
            {
                'name': 'Золотые пески',
                'description': 'Премиум-отель на первой линии пляжа с собственной территорией и бассейнами.',
                'address': 'Набережная ул., 42, Анапа',
                'rating': 4.6,
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
        # Цены в долларах США
        prices = {'standard': 35, 'deluxe': 55, 'suite': 90, 'family': 65}
        capacities = {'standard': 2, 'deluxe': 2, 'suite': 3, 'family': 4}
        
        for hotel in Hotel.objects.all():
            # Для каждого отеля создаем несколько номеров каждого типа
            for room_type in room_types:
                # Количество номеров для каждого типа (от 3 до 6)
                count = random.randint(3, 6)
                for i in range(count):
                    room_number = f"{100 + i + 1}" if room_type == 'standard' else \
                                f"{200 + i + 1}" if room_type == 'deluxe' else \
                                f"{300 + i + 1}" if room_type == 'suite' else f"{400 + i + 1}"
                    
                    # Варьируем цену немного для каждого номера
                    price_variation = random.uniform(0.9, 1.1)
                    price = round(prices[room_type] * price_variation, 2)  # Цена в долларах США
                    
                    room, created = Room.objects.get_or_create(
                        hotel=hotel,
                        number=room_number,
                        defaults={
                            'room_type': room_type,
                            'description': f"Комфортабельный номер с прекрасным видом.",
                            'price_per_night': price,
                            'capacity': capacities[room_type],
                            'available': True,
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'Создан номер: {room.number} в отеле {hotel.name}')
                    else:
                        self.stdout.write(f'Номер уже существует: {room.number} в отеле {hotel.name}')
        
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!')) 
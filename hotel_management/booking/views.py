import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Room, Booking, Payment, Hotel
from .forms import BookingForm, PaymentForm, RoomSearchForm
from django.utils import timezone
from datetime import timedelta
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum, Q, Avg
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout

def hotels(request):
    hotels = Hotel.objects.all()  # Получение всех отелей
    return render(request, 'booking/hotels.html', {'hotels': hotels})
# Представление для главной страницы
def home(request):
    hotels = Hotel.objects.all()[:6]  # Показываем только 6 отелей на главной
    return render(request, 'booking/home.html', {'hotels': hotels})




# Представление для страницы контактов

def contact(request):
    return render(request, 'booking/travel-agency-html-template/contact.html')


# Представление для списка всех отелей
def hotels(request):
    # Initialize hotels with a default value
    hotels = []

    # Get filter parameters from request
    location = request.GET.get('location')
    check_in = request.GET.get('check_in')

    # Apply filters if provided
    if location:
        hotels = Hotel.objects.filter(location=location)
    elif check_in:
        # Filter by check-in date
        hotels = Hotel.objects.filter(available_from__lte=check_in)
    else:
        # Default case: show all hotels
        hotels = Hotel.objects.all()

    return render(request, 'booking/hotels.html', {'hotels': hotels})

# Представление для страницы отеля
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'booking/hotel_detail.html', {'hotel': hotel})


# Представление для просмотра номеров отеля
def hotel_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'booking/hotel_rooms.html', {'hotel': hotel, 'rooms': rooms})


# Представление для страницы номера
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    # Логика бронирования
    return render(request, 'booking/book_room.html', {'room': room})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


# Представление для поиска номеров
def search_rooms(request):
    query = request.GET.get('query', '')
    hotel_name = request.GET.get('hotel_name', '')
    room_type = request.GET.get('room_type', '')
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    guests = request.GET.get('guests', '')

    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(hotel__name__icontains=query) | rooms.filter(description__icontains=query)

    if hotel_name:
        rooms = rooms.filter(hotel__name__icontains=hotel_name)

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if guests:
        rooms = rooms.filter(capacity__gte=int(guests))

    return render(request, 'booking/search_results.html', {
        'rooms': rooms,
        'query': query,
        'hotel_name': hotel_name,
        'room_type': room_type,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests
    })


# Представление для входа в систему
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Представление для выхода из системы
def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')


def index(request):
    return render(request, 'booking/travel-agency-html-template/index.html')  # Убедитесь, что путь правильный
def about(request):
    return render(request, 'booking/travel-agency-html-template/about.html')
#def contact(request):
    #return render(request, 'booking/travel-agency-html-template/contact.html')

def destination(request):
    return render(request, 'booking/travel-agency-html-template/destination.html')

def booking(request):
    return render(request, 'booking/travel-agency-html-template/booking.html')

def service(request):
    return render(request, 'booking/travel-agency-html-template/service.html')

def package(request):
    return render(request, 'booking/travel-agency-html-template/package.html')

def team(request):
    return render(request, 'booking/travel-agency-html-template/team.html')

def testimonial(request):
    return render(request, 'booking/travel-agency-html-template/testimonial.html')

def page_not_found(request):
    return render(request, 'booking/travel-agency-html-template/404.html')

# Представление для входа в систему
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})

# Представление для выхода из системы
def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')

# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Аккаунт создан для {user.username}!")
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})
    
def home(request):
    """Домашняя страница с показом доступных номеров"""
    # Получаем только необходимые поля, которые есть в базе данных
    # Не используем фильтр по available, так как этого поля нет в базе
    rooms = Room.objects.all().values('id', 'number', 'room_type', 'description', 'price_per_night')[:6]
    
    # Преобразуем значения словаря в объекты для более удобного использования в шаблоне
    class RoomProxy:
        def __init__(self, data):
            self.id = data['id']
            self.number = data['number']
            self.room_type = data['room_type']
            self.description = data['description']
            self.price_per_night = data['price_per_night']
            
        def get_room_type_display(self):
            room_types = dict(Room.ROOM_TYPES)
            return room_types.get(self.room_type, "")
    
    proxy_rooms = [RoomProxy(room) for room in rooms]
    return render(request, 'booking/home.html', {'rooms': proxy_rooms})

def room_list(request):
    """Список всех номеров с фильтрацией"""
    form = RoomSearchForm(request.GET)
    rooms = Room.objects.all()

    if form.is_valid():
        check_in = form.cleaned_data.get('check_in_date')
        check_out = form.cleaned_data.get('check_out_date')
        room_type = form.cleaned_data.get('room_type')
        capacity = form.cleaned_data.get('capacity')

        if check_in and check_out:
            # Исключаем номера, которые забронированы в указанный период
            booked_rooms = Booking.objects.filter(
                Q(check_in_date__lte=check_out) & Q(check_out_date__gte=check_in),
                status__in=['pending', 'confirmed', 'checked_in']
            ).values_list('room_id', flat=True)

            rooms = rooms.exclude(id__in=booked_rooms)

        if room_type:
            rooms = rooms.filter(room_type=room_type)

        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)

    paginator = Paginator(rooms, 9)  # Показываем по 9 номеров на странице
    page = request.GET.get('page')
    rooms = paginator.get_page(page)

    return render(request, 'booking/room_list.html', {'rooms': rooms, 'form': form})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'booking/hotel_detail.html', {'hotel': hotel})

def hotel_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'booking/hotel_rooms.html', {'hotel': hotel, 'rooms': rooms})


def room_detail(request, room_id):
    """Детальная информация о номере"""
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})

def search_rooms(request):
    query = request.GET.get('query', '')
    hotel_name = request.GET.get('hotel_name', '')
    room_type = request.GET.get('room_type', '')
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    guests = request.GET.get('guests', '')
    
    rooms = Room.objects.all()
    
    if query:
        rooms = rooms.filter(hotel__name__icontains=query) | rooms.filter(description__icontains=query)
    
    if hotel_name:
        rooms = rooms.filter(hotel__name__icontains=hotel_name)
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    if guests:
        rooms = rooms.filter(capacity__gte=int(guests))
    
    return render(request, 'booking/search_results.html', {
        'rooms': rooms,
        'query': query,
        'hotel_name': hotel_name,
        'room_type': room_type,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests
    }) 


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user

            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']

            # Расчет общей стоимости
            days = (check_out - check_in).days
            booking.total_price = room.price_per_night * days
            booking.save()

            messages.success(request, 'Бронирование создано успешно!')
            return redirect('booking_detail', booking_id=booking.booking_id)
    else:
        initial_data = {
            'check_in_date': timezone.now().date(),
            'check_out_date': timezone.now().date() + timedelta(days=1)
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'booking/book_room.html', {'form': form, 'room': room})

@login_required
def booking_detail(request, booking_id):
    """Детали бронирования"""
    booking = get_object_or_404(Booking, booking_id=booking_id, guest=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})


@login_required
def payment_process(request, booking_id):
    """Обработка оплаты"""
    booking = get_object_or_404(Booking, booking_id=booking_id, guest=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_price

            # Интеграция с платежной системой будет здесь
            # Для примера, считаем платеж успешным
            payment.status = 'completed'
            payment.transaction_id = f"TR-{uuid.uuid4().hex[:10]}"
            payment.save()

            # Обновляем статус бронирования
            booking.status = 'confirmed'
            booking.save()

            messages.success(request, 'Оплата прошла успешно!')
            return redirect('booking_detail', booking_id=booking.booking_id)
    else:
        form = PaymentForm()

    return render(request, 'booking/payment.html', {'form': form, 'booking': booking})


@login_required
def my_bookings(request):
    """Список бронирований пользователя"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """Отмена бронирования"""
    booking = get_object_or_404(Booking, booking_id=booking_id, guest=request.user)

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронирование успешно отменено.')
    else:
        messages.error(request, 'Невозможно отменить это бронирование.')

    return redirect('my_bookings')


# Добавляем функции для администраторской панели

def is_staff(user):
    """Проверка, является ли пользователь админом"""
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    """Главная страница админ-панели"""
    # Статистика по бронированиям
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    # Недавние бронирования
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    context = {
        #'total_bookings': total_bookings,
        #'pending_bookings': pending_bookings,
        #'confirmed_bookings': confirmed_bookings,
        #'cancelled_bookings': cancelled_bookings,
        #'recent_bookings': recent_bookings,

        'total_bookings': 0,
        'confirmed_bookings': 0,
        'pending_bookings': 0,
        'cancelled_bookings': 0,
        'recent_bookings': []
    }
    return render(request, 'admin/dashboard.html', context)



@login_required
@user_passes_test(is_staff)
def admin_bookings(request):
    """Управление бронированиями"""
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Применяем фильтры
    status = request.GET.get('status')
    hotel = request.GET.get('hotel')
    check_in_from = request.GET.get('check_in_from')
    check_in_to = request.GET.get('check_in_to')
    
    if status:
        bookings = bookings.filter(status=status)
    if hotel:
        bookings = bookings.filter(room__hotel_id=hotel)
    if check_in_from:
        bookings = bookings.filter(check_in__gte=check_in_from)  # строка ~385
    if check_in_to:
        bookings = bookings.filter(check_in__lte=check_in_to) 
    
    # Пагинация
    paginator = Paginator(bookings, 10)  # 10 бронирований на страницу
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)
    
    # Получаем список отелей для фильтра
    hotels = Hotel.objects.all()
    
    context = {
        'bookings': bookings,
        'hotels': hotels,
    }
    return render(request, 'booking/admin_bookings.html', context)

@login_required
@user_passes_test(is_staff)
def admin_booking_detail(request, booking_id):
    """Детальная информация о бронировании"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = AdminBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование успешно обновлено.')
            return redirect('admin_booking_detail', booking_id=booking.id)
    else:
        form = AdminBookingForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'booking/admin_booking_detail.html', context)

@login_required
@user_passes_test(is_staff)
def admin_booking_confirm(request, booking_id):
    """Подтверждение бронирования"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, f'Бронирование #{booking.id} успешно подтверждено.')
    else:
        messages.error(request, 'Подтверждение невозможно для данного статуса бронирования.')
    
    return redirect('admin_bookings')

@login_required
@user_passes_test(is_staff)
def admin_booking_cancel(request, booking_id):
    """Отмена бронирования"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Бронирование #{booking.id} отменено.')
    else:
        messages.error(request, 'Отмена невозможна для данного статуса бронирования.')
    
    return redirect('admin_bookings')

@login_required
@user_passes_test(is_staff)
def admin_booking_complete(request, booking_id):
    """Отметить бронирование как завершенное"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'confirmed':
        booking.status = 'completed'
        booking.save()
        messages.success(request, f'Бронирование #{booking.id} отмечено как завершенное.')
    else:
        messages.error(request, 'Невозможно завершить бронирование с текущим статусом.')
    
    return redirect('admin_bookings')

@login_required
@user_passes_test(is_staff)
def admin_hotels(request):
    """Управление отелями"""
    hotels = Hotel.objects.all()
    
    # Применяем фильтры
    search = request.GET.get('search')
    min_rating = request.GET.get('min_rating')
    sort = request.GET.get('sort', 'name')
    
    if search:
        hotels = hotels.filter(
            Q(name__icontains=search) | 
            Q(address__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if min_rating:
        hotels = hotels.filter(rating__gte=min_rating)
    
    # Аннотируем количество бронирований для каждого отеля
    hotels = hotels.annotate(booking_count=Count('rooms__bookings'))
    
    # Сортировка
    hotels = hotels.order_by(sort)
    
    # Пагинация
    paginator = Paginator(hotels, 6)  # 6 отелей на страницу
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)
    
    context = {
        'hotels': hotels,
    }
    return render(request, 'booking/admin_hotels.html', context)

@login_required
@user_passes_test(is_staff)
def admin_hotel_add(request):
    """Добавление нового отеля"""
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save()
            messages.success(request, f'Отель "{hotel.name}" успешно добавлен.')
            return redirect('admin_hotels')
    else:
        form = HotelForm()
    
    context = {
        'form': form,
        'title': 'Добавление отеля',
    }
    return render(request, 'booking/admin_hotel_form.html', context)

@login_required
@user_passes_test(is_staff)
def admin_hotel_edit(request, hotel_id):
    """Редактирование отеля"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            hotel = form.save()
            messages.success(request, f'Отель "{hotel.name}" успешно обновлен.')
            return redirect('admin_hotels')
    else:
        form = HotelForm(instance=hotel)
    
    context = {
        'form': form,
        'hotel': hotel,
        'title': 'Редактирование отеля',
    }
    return render(request, 'booking/admin_hotel_form.html', context)

@login_required
@user_passes_test(is_staff)
def admin_rooms(request):
    """Управление номерами"""
    rooms = Room.objects.all()
    
    # Применяем фильтры
    hotel = request.GET.get('hotel')
    room_type = request.GET.get('room_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    available = request.GET.get('available')
    
    if hotel:
        rooms = rooms.filter(hotel_id=hotel)
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)
    if available:
        rooms = rooms.filter(available=(available == '1'))
    
    # Пагинация
    paginator = Paginator(rooms, 9)  # 9 номеров на страницу
    page_number = request.GET.get('page')
    rooms = paginator.get_page(page_number)
    
    # Получаем список отелей для фильтра
    hotels = Hotel.objects.all()
    
    context = {
        'rooms': rooms,
        'hotels': hotels,
        'room_types': Room.ROOM_TYPES,
    }
    return render(request, 'booking/admin_rooms.html', context)

@login_required
@user_passes_test(is_staff)
def admin_room_add(request):
    """Добавление нового номера"""
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Номер "{room.number}" успешно добавлен.')
            return redirect('admin_rooms')
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'title': 'Добавление номера',
    }
    return render(request, 'booking/admin_room_form.html', context)

@login_required
@user_passes_test(is_staff)
def admin_room_edit(request, room_id):
    """Редактирование номера"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Номер "{room.number}" успешно обновлен.')
            return redirect('admin_rooms')
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
        'room': room,
        'title': 'Редактирование номера',
    }
    return render(request, 'booking/admin_room_form.html', context)

@login_required
@user_passes_test(is_staff)
def admin_room_toggle_availability(request, room_id):
    """Изменение доступности номера"""
    room = get_object_or_404(Room, id=room_id)
    room.available = not room.available
    room.save()
    
    status = "доступен" if room.available else "недоступен"
    messages.success(request, f'Номер "{room.number}" теперь {status}.')
    
    return redirect('admin_rooms')

@login_required
@user_passes_test(is_staff)
def admin_users(request):
    """Управление пользователями"""
    users = User.objects.all()
    
    # Применяем фильтры
    search = request.GET.get('search')
    is_active = request.GET.get('is_active')
    is_staff = request.GET.get('is_staff')
    sort = request.GET.get('sort', 'username')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) | 
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if is_active is not None:
        users = users.filter(is_active=(is_active == '1'))
    
    if is_staff is not None:
        users = users.filter(is_staff=(is_staff == '1'))
    
    # Аннотируем количество бронирований для каждого пользователя
    if sort == '-booking_count':
        users = users.annotate(booking_count=Count('bookings')).order_by('-booking_count')
    else:
        users = users.order_by(sort)
    
    # Пагинация
    paginator = Paginator(users, 10)  # 10 пользователей на страницу
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
    }
    return render(request, 'booking/admin_users.html', context)

@login_required
@user_passes_test(is_staff)
def admin_user_detail(request, user_id):
    """Детальная информация о пользователе"""
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user_profile': user,
        'bookings': bookings,
    }
    return render(request, 'booking/admin_user_detail.html', context)

@login_required
@user_passes_test(is_staff)
def admin_user_edit(request, user_id):
    """Редактирование пользователя"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные пользователя "{user.username}" успешно обновлены.')
            return redirect('admin_users')
    else:
        form = UserForm(instance=user)
    
    context = {
        'form': form,
        'user_profile': user,
    }
    return render(request, 'booking/admin_user_form.html', context)

@login_required
@user_passes_test(is_staff)
def admin_user_toggle_active(request, user_id):
    """Включение/отключение пользователя"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "активирован" if user.is_active else "деактивирован"
    messages.success(request, f'Пользователь "{user.username}" {status}.')
    
    return redirect('admin_users')

@login_required
@user_passes_test(is_staff)
def admin_user_toggle_staff(request, user_id):
    """Изменение статуса администратора"""
    user = get_object_or_404(User, id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    
    status = "администратор" if user.is_staff else "обычный пользователь"
    messages.success(request, f'Пользователь "{user.username}" теперь {status}.')
    
    return redirect('admin_users')

@login_required
@user_passes_test(is_staff)
def admin_reviews(request):
    """Управление отзывами"""
    reviews = Review.objects.all().order_by('-created_at')
    
    # Фильтры
    hotel = request.GET.get('hotel')
    min_rating = request.GET.get('min_rating')
    
    if hotel:
        reviews = reviews.filter(hotel_id=hotel)
    if min_rating:
        reviews = reviews.filter(rating__gte=min_rating)
    
    # Пагинация
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    # Отели для фильтра
    hotels = Hotel.objects.all()
    
    context = {
        'reviews': reviews,
        'hotels': hotels,
    }
    return render(request, 'booking/admin_reviews.html', context)

@login_required
@user_passes_test(is_staff)
def admin_review_delete(request, review_id):
    """Удаление отзыва"""
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, 'Отзыв успешно удален.')
    return redirect('admin_reviews')

@login_required
@user_passes_test(is_staff)
def admin_reports(request):
    """Страница отчетов и аналитики"""
    # Получаем параметры периода из запроса
    period = request.GET.get('period', 'this_month')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Определяем даты начала и конца периода
    today = timezone.now().date()
    
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif period == 'this_week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == 'last_week':
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)
    elif period == 'this_month':
        start_date = today.replace(day=1)
        end_date = today
    elif period == 'last_month':
        if today.month == 1:
            last_month = today.replace(year=today.year-1, month=12, day=1)
        else:
            last_month = today.replace(month=today.month-1, day=1)
        start_date = last_month
        end_date = today.replace(day=1) - timedelta(days=1)
    elif period == 'this_year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif period == 'custom' and start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        # По умолчанию - текущий месяц
        start_date = today.replace(day=1)
        end_date = today
    
    # Получаем данные для предыдущего периода (для сравнения)
    period_length = (end_date - start_date).days + 1
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=period_length - 1)
    

# В функции admin_reports (примерно строки 640-650):
    bookings = Booking.objects.filter(
        check_in_date__gte=start_date,    # ПРАВИЛЬНОЕ имя поля
        check_in_date__lte=end_date       # ПРАВИЛЬНОЕ имя поля
    )
    total_bookings = bookings.count()
    
    # Доход
    confirmed_bookings = bookings.filter(status__in=['confirmed', 'completed'])
    total_revenue = confirmed_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    while current_date <= end_date:
        bookings_at_date = Booking.objects.filter(
            check_in_date__lte=current_date,      # ПРАВИЛЬНОЕ имя поля
            check_out_date__gt=current_date,      # ПРАВИЛЬНОЕ имя поля
            status__in=['confirmed', 'completed']
        ).count()

    prev_total_bookings = prev_bookings.count()
    prev_confirmed_bookings = prev_bookings.filter(status__in=['confirmed', 'completed'])
    prev_total_revenue = prev_confirmed_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Вычисляем изменения
    if prev_total_bookings > 0:
        bookings_change = ((total_bookings - prev_total_bookings) / prev_total_bookings) * 100
    else:
        bookings_change = 100 if total_bookings > 0 else 0
    
    if prev_total_revenue > 0:
        revenue_change = ((total_revenue - prev_total_revenue) / prev_total_revenue) * 100
    else:
        revenue_change = 100 if total_revenue > 0 else 0
    
    # Заполняемость
    # Например, для простоты можем посчитать как процент забронированных номеров
    # от общего количества номеров в выбранный период
    total_rooms = Room.objects.count()
    total_room_days = total_rooms * period_length
    
    booked_room_days = 0
    current_date = start_date
    while current_date <= end_date:
        bookings_at_date = Booking.objects.filter(
            check_in__lte=current_date,
            check_out__gt=current_date,
            status__in=['confirmed', 'completed']
        ).count()
        booked_room_days += bookings_at_date
        current_date += timedelta(days=1)
    
    occupancy_rate = (booked_room_days / total_room_days) * 100 if total_room_days > 0 else 0
    



def add_review(request, slug):
    """
    Представление для добавления отзыва о комнате
    """
    if not request.user.is_authenticated:
        return redirect('login')

    room = get_object_or_404(Room, slug=slug)

    if request.method == 'POST':
        # Обработка POST-запроса
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        Review.objects.create(
            room=room,
            user=request.user,
            content=content,
            rating=rating
        )

        return redirect('room_detail', slug=slug)

    return render(request, 'booking/add_review.html', {'room': room})

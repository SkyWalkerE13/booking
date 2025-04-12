from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Booking
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Представление для главной страницы
def home(request):
    hotels = Hotel.objects.all()[:6]  # Показываем только 6 отелей на главной
    return render(request, 'booking/home.html', {'hotels': hotels})

# Представление для страницы "О нас"
def about(request):
    return render(request, 'booking/about.html')

# Представление для страницы контактов
def contact(request):
    return render(request, 'booking/contact.html')

# Представление для списка всех отелей
def hotels(request):
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
    return render(request, 'registration/register.html', {'form': form}) 
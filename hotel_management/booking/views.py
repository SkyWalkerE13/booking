import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Room, Booking, Payment
from .forms import BookingForm, PaymentForm, RoomSearchForm
from django.utils import timezone
from datetime import timedelta
import json


def home(request):
    """Домашняя страница с показом доступных номеров"""
    rooms = Room.objects.filter(is_available=True)[:6]
    return render(request, 'booking/home.html', {'rooms': rooms})


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


def room_detail(request, room_id):
    """Детальная информация о номере"""
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})


@login_required
def book_room(request, room_id):
    """Бронирование номера"""
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.guest = request.user

            # Проверка доступности номера
            check_in = booking.check_in_date
            check_out = booking.check_out_date
            conflicting_bookings = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in_date__lt=check_out,
                check_out_date__gt=check_in
            )

            if conflicting_bookings.exists():
                messages.error(request, 'Номер недоступен в выбранные даты.')
                return redirect('room_detail', room_id=room.id)

            # Расчет общей стоимости
            days = (check_out - check_in).days
            booking.total_price = room.price_per_night * days
            booking.save()

            messages.success(request, 'Бронирование создано успешно!')
            return redirect('booking_detail', booking_id=booking.booking_id)
    else:
        # Предзаполнение дат (сегодня и завтра)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        form = BookingForm(initial={'check_in_date': today, 'check_out_date': tomorrow})

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
    bookings = Booking.objects.filter(guest=request.user).order_by('-booking_date')
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


# Админский функционал
@login_required
def admin_dashboard(request):
    """Админ-панель для управления отелем"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен.')
        return redirect('home')

    # Статистика
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    active_bookings = Booking.objects.filter(status__in=['confirmed', 'checked_in']).count()

    # Последние бронирования
    recent_bookings = Booking.objects.order_by('-booking_date')[:10]

    # Доход за последние 30 дней
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_payments = Payment.objects.filter(status='completed', payment_date__gte=thirty_days_ago)
    total_revenue = sum(payment.amount for payment in recent_payments)

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'active_bookings': active_bookings,
        'recent_bookings': recent_bookings,
        'total_revenue': total_revenue,
    }

    return render(request, 'admin/dashboard.html', context)


@login_required
def manage_rooms(request):
    """Управление номерами (список/добавление/редактирование)"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен.')
        return redirect('home')

    rooms = Room.objects.all()
    return render(request, 'admin/manage_rooms.html', {'rooms': rooms})


@login_required
def manage_bookings(request):
    """Управление бронированиями"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен.')
        return redirect('home')

    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'admin/manage_bookings.html', {'bookings': bookings})


@login_required
def generate_reports(request):
    """Генерация отчетов"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен.')
        return redirect('home')

    # Отчет о доходах по месяцам
    # Отчет о заполняемости номеров
    # Отчет о популярных типах номеров

    return render(request, 'admin/reports.html')

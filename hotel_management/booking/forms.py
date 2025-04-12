from django import forms
from django.utils import timezone
from django.contrib.auth.models import User 
from .models import Booking, Payment, Room, Hotel
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        
class RoomSearchForm(forms.Form):
    """Форма для поиска номеров"""
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    room_type = forms.ChoiceField(choices=[('', '---')] + list(Room.ROOM_TYPES), required=False)
    capacity = forms.IntegerField(min_value=1, required=False)

class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']
        
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError('Дата выезда должна быть позже даты заезда.')

            today = timezone.now().date()
            if check_in < today:
                raise forms.ValidationError('Дата заезда не может быть в прошлом.')

        return cleaned_data


class PaymentForm(forms.ModelForm):
    """Форма для обработки платежей"""
    card_number = forms.CharField(max_length=16, min_length=16, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_holder = forms.CharField(max_length=100, required=True)
    expiry_date = forms.CharField(max_length=5, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, min_length=3, required=True,
                          widget=forms.TextInput(attrs={'placeholder': '123'}))

    class Meta:
        model = Payment
        fields = ['payment_method']

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        # Базовая валидация номера карты
        if not card_number.isdigit():
            raise forms.ValidationError('Номер карты должен содержать только цифры.')
        return card_number


class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'check_in_date', 'check_out_date', 'guests', 'status', 'total_price']  # исправлено!
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),  # исправлено!
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),  # исправлено!
        }

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address', 'rating', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'number', 'room_type', 'description', 'price_per_night', 'capacity', 'available', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
from django import forms
from .models import Booking, Payment, Room


class RoomSearchForm(forms.Form):
    """Форма для поиска номеров"""
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    room_type = forms.ChoiceField(choices=[('', '---')] + list(Room.ROOM_TYPES), required=False)
    capacity = forms.IntegerField(min_value=1, required=False)


class BookingForm(forms.ModelForm):
    """Форма для создания бронирования"""

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'adults', 'children', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

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
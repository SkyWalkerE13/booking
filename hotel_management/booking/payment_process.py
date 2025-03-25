from .payment_gateway import get_payment_gateway


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

            # Получаем данные платежа из формы
            payment_data = {
                'card_number': form.cleaned_data.get('card_number'),
                'card_holder': form.cleaned_data.get('card_holder'),
                'expiry_date': form.cleaned_data.get('expiry_date'),
                'cvv': form.cleaned_data.get('cvv'),
            }

            # Обрабатываем платеж через выбранный платежный шлюз
            gateway = get_payment_gateway(payment.payment_method)
            result = gateway.process_payment(payment.amount, payment_data, booking.booking_id)

            # Обновляем данные платежа
            payment.status = result.get('status', 'failed')
            payment.transaction_id = result.get('transaction_id', '')
            payment.save()

            if payment.status == 'completed':
                # Обновляем статус бронирования
                booking.status = 'confirmed'
                booking.save()

                messages.success(request, 'Оплата прошла успешно!')
                return redirect('booking_detail', booking_id=booking.booking_id)
            else:
                messages.error(request, 'Ошибка при обработке платежа. Пожалуйста, попробуйте еще раз.')
    else:
        form = PaymentForm()

    return render(request, 'booking/payment.html', {'form': form, 'booking': booking})
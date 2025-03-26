import uuid
from decimal import Decimal
import stripe

stripe.api_key = "#"


class PaymentGateway:
    """Базовый класс для интеграции с платежными системами"""

    def process_payment(self, amount, payment_data, booking_id):
        """
        Обрабатывает платеж

        Параметры:
        amount (Decimal): сумма платежа
        payment_data (dict): информация о платеже (данные карты и т.д.)
        booking_id (str): идентификатор бронирования

        Возвращает:
        dict: результат операции с transaction_id и status
        """
        pass


class StripeGateway(PaymentGateway):
    """Реализация Stripe платежной системы"""

    def process_payment(self, amount, payment_data, booking_id):
        # В реальной интеграции здесь был бы код для Stripe
        # Например:
         try:
             payment_intent = stripe.PaymentIntent.create(
                 amount=int(amount * 100),  # Stripe использует центы
                 currency="rub",
                 payment_method_types=["card"],
                 metadata={"booking_id": str(booking_id)}
             )
             return {
                 "transaction_id": payment_intent.id,
                 "status": "completed" if payment_intent.status == "succeeded" else "pending",
                 "details": payment_intent
             }
         except stripe.error.StripeError as e:
             return {
                "transaction_id": None,
                 "status": "failed",
                 "error": str(e)
             }

        # Для демонстрации вернем успешный результат
             return {
            "transaction_id": f"tr_{uuid.uuid4().hex[:16]}",
            "status": "completed",
            "details": {"card_last4": payment_data.get("card_number", "")[-4:]}
        }


class PayPalGateway(PaymentGateway):
    """Реализация PayPal платежной системы"""

    def process_payment(self, amount, payment_data, booking_id):
        # Реализация для PayPal
        # ...

        # Для демонстрации
        return {
            "transaction_id": f"pp_{uuid.uuid4().hex[:16]}",
            "status": "completed",
            "details": {"email": payment_data.get("email", "")}
        }


def get_payment_gateway(payment_method):
    """
    Фабричный метод для получения нужного платежного шлюза

    Параметры:
    payment_method (str): код метода оплаты

    Возвращает:
    PaymentGateway: экземпляр соответствующего платежного шлюза
    """
    gateways = {
        "credit_card": StripeGateway(),
        "debit_card": StripeGateway(),
        "paypal": PayPalGateway(),
        # Другие методы оплаты
    }

    return gateways.get(payment_method, StripeGateway())

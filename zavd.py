from abc import ABC, abstractmethod
from random import randint


class Asset(ABC):
    """Абстрактний клас фінансового активу."""
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount

    @abstractmethod
    def get_value_uah(self) -> float:
        """Повертає вартість активу в гривнях (UAH)."""
        pass


class CurrencyAsset(Asset):
    """Клас традиційної валюти (фіат)."""
    def __init__(self, name: str, amount: float, rate_to_uah: float):
        super().__init__(name, amount)
        # Приватний атрибут (інкапсуляція)
        self.__rate_to_uah = rate_to_uah

    @property
    def rate(self) -> float:
        """Властивість-геттер для курсу валюти."""
        return self.__rate_to_uah

    def get_value_uah(self) -> float:
        
        return self.amount * self.__rate_to_uah


class CryptoAsset(Asset):
    """Клас криптовалютного активу (з волатильністю)."""
    def __init__(self, name: str, amount: float, base_rate_to_uah: float):
        super().__init__(name, amount)
        self.base_rate_to_uah = base_rate_to_uah

    def get_value_uah(self) -> float:
     
        volatile_rate = self.base_rate_to_uah + randint(-500, 500)
        return self.amount * volatile_rate


class Portfolio:
    """Клас портфеля для зберігання активів."""
    def __init__(self):
      
        self.__assets = []

    def add(self, asset: Asset):
        """Додає актив до портфеля."""
        self.__assets.append(asset)

    def total_value_uah(self) -> float:
        """Сума вартості всіх активів (поліморфізм через get_value_uah())."""
        return sum(asset.get_value_uah() for asset in self.__assets)





FIXED_RATES = {
    "USD": 41.5,
    "EUR": 45.0,
    "GBP": 52.0,
    "BTC": 3_800_000.0,
    "UAH": 1.0
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Інструмент (tool) для конвертації валют на основі CurrencyAsset.
    """
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()

    if from_curr not in FIXED_RATES or to_curr not in FIXED_RATES:
        raise ValueError("Непідтримувана валюта для конвертації.")

    
    asset = CurrencyAsset(name=from_curr, amount=amount, rate_to_uah=FIXED_RATES[from_curr])
    
    
    value_in_uah = asset.get_value_uah()
    
    
    target_rate = FIXED_RATES[to_curr]
    result = value_in_uah / target_rate
    
    
    cross_rate = asset.rate / target_rate

   
    return {
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "result": round(result, 4 if to_curr == "BTC" else 2),
        "rate": round(cross_rate, 4)
         }


class FIAgent:
    """Симуляція AI-агента — фінансового консультанта."""
    def __init__(self):
        self.prompt = (
            "Ви є фінансовим консультантом з обміну валют. "
            "Ви конвертуєте суми між валютами та пояснюєте поточний курс. "
            "Відповідайте виключно українською мовою."
        )

    def ask(self, query: str, amount: float, from_curr: str, to_curr: str) -> str:
        """Обробка запиту користувача за допомогою інструменту конвертації."""
        try:
            # Агент використовує інструмент (tool)
            data = convert_currency(amount, from_curr, to_curr)
            
            # Формування текстової відповіді агента українською мовою
            response = (
                f"**Запит користувача:** \"{query}\"\n"
                f"**Фінансовий консультант:** Вітаю! З радістю допоможу вам із розрахунком. "
                f"На основі поточних фіксованих курсів, {data['amount']} {data['from']} "
                f"дорівнює **{data['result']} {data['to']}**.\n"
                f"Поточний крос-курс становить: 1 {data['from']} = {data['rate']} {data['to']}. "
                f"(Базові курси до гривні: {data['from']} = {FIXED_RATES[data['from']]} UAH, "
                f"{data['to']} = {FIXED_RATES[data['to']]} UAH).\n"
            )
            return response
        except Exception as e:
            return f"Помилка агента: {str(e)}"


# =====================================================================
# Демонстрація роботи програми
# =====================================================================

if __name__ == "__main__":
    print("--- 1. Тестування ООП структури (Портфель активів) ---")
    portfolio = Portfolio()
    
    # Додаємо активи
    portfolio.add(CurrencyAsset("USD", 100, 41.5))     # 100 * 41.5 = 4150 UAH
    portfolio.add(CurrencyAsset("EUR", 50, 45.0))      # 50 * 45.0 = 2250 UAH
    portfolio.add(CryptoAsset("BTC", 0.005, 3800000)) # З волатильністю (~19000 UAH)
    
    print(f"Загальна вартість портфеля в UAH: {portfolio.total_value_uah():,.2f} грн\n")

    print("--- 2. Демонстрація роботи AI-агента (3 запитання) ---")
    agent = FIAgent()
    
    # Запитання 1: USD в EUR
    q1 = "Підкажіть, скільки я отримаю євро, якщо обміняю 500 доларів?"
    print(agent.ask(q1, amount=500, from_curr="USD", to_curr="EUR"))
    print("-" * 50)

    # Запитання 2: BTC в USD
    q2 = "Яка вартість 0.025 біткоїна в доларах США зараз?"
    print(agent.ask(q2, amount=0.025, from_curr="BTC", to_curr="USD"))
    print("-" * 50)

    # Запитання 3: GBP в UAH
    q3 = "Мені потрібно обміняти 150 фунтів стерлінгів на гривні. Яка це буде сума?"
    print(agent.ask(q3, amount=150, from_curr="GBP", to_curr="UAH"))
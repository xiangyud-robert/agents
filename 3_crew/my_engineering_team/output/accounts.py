class Account:
    def __init__(self, user_id: str, initial_deposit: float):
        self.user_id = user_id
        self.balance = initial_deposit
        self.shares = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(f"Deposited: ${amount:.2f}")

    def withdraw(self, amount: float) -> bool:
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append(f"Withdrew: ${amount:.2f}")
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        total_cost = get_share_price(symbol) * quantity
        if total_cost > self.balance:
            return False
        self.balance -= total_cost
        if symbol in self.shares:
            self.shares[symbol] += quantity
        else:
            self.shares[symbol] = quantity
        self.transactions.append(f"Bought {quantity} shares of {symbol} for ${total_cost:.2f}")
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.shares or self.shares[symbol] < quantity:
            return False
        total_sale = get_share_price(symbol) * quantity
        self.balance += total_sale
        self.shares[symbol] -= quantity
        if self.shares[symbol] == 0:
            del self.shares[symbol]
        self.transactions.append(f"Sold {quantity} shares of {symbol} for ${total_sale:.2f}")
        return True

    def calculate_portfolio_value(self) -> float:
        value = self.balance
        for symbol, quantity in self.shares.items():
            value += get_share_price(symbol) * quantity
        return value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.shares

    def get_transaction_history(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol, 0.0)
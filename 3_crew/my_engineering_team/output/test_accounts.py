import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(user_id='user123', initial_deposit=1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_withdraw_success(self):
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_failure(self):
        result = self.account.withdraw(1100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.shares['AAPL'], 3)

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 3)
        result = self.account.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertNotIn('AAPL', self.account.shares)

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_calculate_portfolio_value(self):
        self.account.deposit(200.0)
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        value = self.account.calculate_portfolio_value()
        self.assertEqual(value, 200.0 + 2 * 150.0 + 1 * 700.0)

    def test_calculate_profit_loss(self):
        self.account.deposit(200.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_profit_loss(), 200.0 + 2 * 150.0 - 1000.0)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})

    def test_get_transaction_history(self):
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        history = self.account.get_transaction_history()
        self.assertEqual(history, ["Deposited: $100.00", "Withdrew: $50.00"])

if __name__ == '__main__':
    unittest.main()
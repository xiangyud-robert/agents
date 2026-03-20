import gradio as gr
from accounts import Account

# Initialize account for a single user
user_account = Account(user_id="user1", initial_deposit=1000.0)

def create_account(initial_deposit):
    global user_account
    user_account = Account(user_id="user1", initial_deposit=initial_deposit)
    return f"Account created with initial deposit: ${initial_deposit:.2f}"

def deposit_funds(amount):
    user_account.deposit(amount)
    return f"Deposited: ${amount:.2f}"

def withdraw_funds(amount):
    if user_account.withdraw(amount):
        return f"Withdrew: ${amount:.2f}"
    else:
        return "Insufficient funds to withdraw."

def buy_shares(symbol, quantity):
    if user_account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}."
    else:
        return "Insufficient funds or incorrect share quantity."

def sell_shares(symbol, quantity):
    if user_account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}."
    else:
        return "You do not own enough shares to sell."

def portfolio_value():
    value = user_account.calculate_portfolio_value()
    return f"Total Portfolio Value: ${value:.2f}"

def profit_loss():
    profit_loss = user_account.calculate_profit_loss()
    return f"Profit/Loss: ${profit_loss:.2f}"

def report_holdings():
    holdings = user_account.get_holdings()
    return f"Current Holdings: {holdings}"

def transaction_history():
    transactions = user_account.get_transaction_history()
    return "\n".join(transactions)

with gr.Blocks() as demo:
    gr.Markdown("### Simple Trading Account Management System")
    initial_deposit = gr.Number(label="Initial Deposit", value=1000.0)
    create_account_btn = gr.Button("Create Account")
    create_account_output = gr.Textbox(label="Create Account Output")

    deposit_amount = gr.Number(label="Deposit Amount")
    deposit_btn = gr.Button("Deposit Funds")
    deposit_output = gr.Textbox(label="Deposit Output")

    withdraw_amount = gr.Number(label="Withdraw Amount")
    withdraw_btn = gr.Button("Withdraw Funds")
    withdraw_output = gr.Textbox(label="Withdraw Output")

    symbol = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
    buy_quantity = gr.Number(label="Buy Quantity")
    buy_btn = gr.Button("Buy Shares")
    buy_output = gr.Textbox(label="Buy Output")

    sell_quantity = gr.Number(label="Sell Quantity")
    sell_btn = gr.Button("Sell Shares")
    sell_output = gr.Textbox(label="Sell Output")

    portfolio_value_btn = gr.Button("Portfolio Value")
    portfolio_value_output = gr.Textbox(label="Portfolio Value Output")
    
    profit_loss_btn = gr.Button("Profit/Loss")
    profit_loss_output = gr.Textbox(label="Profit/Loss Output")

    holdings_btn = gr.Button("Report Holdings")
    holdings_output = gr.Textbox(label="Holdings Output")

    transactions_btn = gr.Button("Transaction History")
    transactions_output = gr.Textbox(label="Transaction History Output")

    create_account_btn.click(create_account, inputs=initial_deposit, outputs=create_account_output)
    deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(buy_shares, inputs=[symbol, buy_quantity], outputs=buy_output)
    sell_btn.click(sell_shares, inputs=[symbol, sell_quantity], outputs=sell_output)
    portfolio_value_btn.click(portfolio_value, outputs=portfolio_value_output)
    profit_loss_btn.click(profit_loss, outputs=profit_loss_output)
    holdings_btn.click(report_holdings, outputs=holdings_output)
    transactions_btn.click(transaction_history, outputs=transactions_output)

demo.launch()
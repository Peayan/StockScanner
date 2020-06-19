from tkinter import *

class StockItem:
    """UI object used to display stock data including name, current price, amount owed etc"""
    def __init__(self, root, name, rowindex):
        self.root = root
        rowindex += 1

        # stock name
        self.name = StringVar()
        self.name_entry = Entry(self.root, textvariable=self.name)
        self.name_entry.grid(row=rowindex, column=0)

        # market open
        self.market_open = StringVar()
        self.market_open.set("Open")
        self.market_open_text = Label(self.root, textvariable=self.market_open, width="7", justify="left", font=("Courier", 20, 'bold'), bg="green")
        self.market_open_text.grid(row=rowindex, column=1)

        # current price
        self.price = StringVar()
        self.price.set("0")
        self.stock_price_text = Label(self.root, textvariable=self.price, font=("Courier", 20))
        self.stock_price_text.grid(row=rowindex, column=2)

        # bought Price
        self.bought_price = StringVar()
        self.bought_price.set("0")
        self.bought_price_entry = Entry(self.root, textvariable=self.bought_price)
        self.bought_price_entry.grid(row=rowindex, column=3)

        # quantity owned
        # 3.0898, 161
        self.quantity = StringVar()
        self.quantity.set("0")
        self.quantity_entry = Entry(self.root, textvariable=self.quantity)
        self.quantity_entry.grid(row=rowindex, column=4)

        #bought worth
        self.bought_worth = StringVar()
        self.bought_worth.set("0")
        self.stock_bought_worth = Label(self.root, textvariable=self.bought_worth, font=("Courier", 15))
        self.stock_bought_worth.grid(row=rowindex, column=5)

        #current worth
        self.current_worth = StringVar()
        self.current_worth.set("0")
        self.stock_current_worth = Label(self.root, textvariable=self.current_worth, font=("Courier", 15))
        self.stock_current_worth.grid(row=rowindex, column=6)

        #profit/loss
        self.profit_loss = StringVar()
        self.profit_loss.set("0")
        self.stock_profit = Label(self.root, textvariable=self.profit_loss, font=("Courier", 15))
        self.stock_profit.grid(row=rowindex, column=7)

    def read_in_stock_data(self, data_list):
        """Applies the stock data read in from the open file function to the relevant ui variables"""
        if (len(data_list) != 3):
            print("Can't load stock data - insufficient values")
        else:
            self.name.set(data_list[0])
            self.bought_price.set(data_list[1])
            self.quantity.set(data_list[2])

    def remove_grid(self):
        """Removes all grid compononets from the UI objects i.e resets the UI"""
        self.name_entry.grid_remove()
        self.market_open_text.grid_remove()
        self.stock_price_text.grid_remove()
        self.bought_price_entry.grid_remove()
        self.quantity_entry.grid_remove()
        self.stock_bought_worth.grid_remove()
        self.stock_current_worth.grid_remove()
        self.stock_profit.grid_remove()

    def set_price(self, new_price):
        """Update all the relevant UI fields which rely on the pricing of the active stock"""
        spent_total_worth = float(self.bought_price.get()) * float(self.quantity.get())
        current_total_worth = float(self.quantity.get()) * float(new_price)
        profit_loss = current_total_worth - spent_total_worth

        self.price.set("")
        self.price.set(float("{:.3f}".format(new_price)))

        self.bought_worth.set("")
        self.bought_worth.set(spent_total_worth)

        self.current_worth.set("")
        self.current_worth.set(float("{:.2f}".format(current_total_worth)))

        self.profit_loss.set("")
        self.profit_loss.set(float("{:.2f}".format(current_total_worth - spent_total_worth)))
        if(profit_loss < 0):
            self.stock_profit.configure(bg='red')
        elif profit_loss > 0:
            self.stock_profit.configure(bg='green')


    def set_market_state(self, market_state):
        """Sets a flag to determine if the stock's traded market is currently open"""
        if market_state:
            self.market_open.set("Open")
            self.market_open_text.configure(bg="green")
        else:
            self.market_open.set("Closed")
            self.market_open_text.configure(bg="red")

    def get_name(self):
        """Returns the name field of the stock object"""
        return self.name_entry.get()

    def get_current_price(self):
        """Returns the price field of the stock object"""
        return self.price.get()
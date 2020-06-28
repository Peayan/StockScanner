import datetime as dt
import yfinance as yf
import matplotlib.dates as mdates
import tkinter.filedialog
from tkinter import *
from tkcalendar import *
from matplotlib import pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc

class StockItem:
    """UI object used to display stock data including name, current price, amount owed etc"""
    def __init__(self, root, name, rowindex, ftse_tickers):
        self.root = root
        self.start_date = dt.datetime.now()
        self.end_date = dt.datetime.now()
        self.start_date_text = StringVar(value="Select Start Date")
        self.end_date_text = StringVar(value="Select End Date")

        #indexer to help position new stock item on a new row
        rowindex += 1

        # stock name
        self.name = StringVar()
        self.name.set("III")
        self.name_entry = OptionMenu(self.root, self.name, *ftse_tickers)
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

        # Buy In Price
        self.buy_in_price = StringVar()
        self.buy_in_price.set("0")
        self.buy_in_price_entry = Entry(self.root, textvariable=self.buy_in_price)
        self.buy_in_price_entry.grid(row=rowindex, column=3)

        # quantity owned
        self.quantity = StringVar()
        self.quantity.set("0")
        self.quantity_entry = Entry(self.root, textvariable=self.quantity)
        self.quantity_entry.grid(row=rowindex, column=4)

        #bought worth
        self.investment_worth = StringVar()
        self.investment_worth.set("0")
        self.stock_investment_worth = Label(self.root, textvariable=self.investment_worth, font=("Courier", 15))
        self.stock_investment_worth.grid(row=rowindex, column=5)

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

        #Calender for OHLC
        self.calendar_start_button = Button(self.root, text="Select Date(s)", width=15, command=self.setup_calendar_window)
        self.calendar_start_button.grid(row=rowindex, column=8)

    def setup_calendar_window(self):
        """Opens new window with a calendar widget to let the user select the start/end date of the OHLC period"""
        #Calender Pop up
        self.calendar_window = Toplevel(self.root)
        self.calendar_window.title("OHLC Graph")
        self.calendar_window.geometry("450x200")
        today = dt.datetime.today()
        self.calendar = Calendar(self.calendar_window, selectmode='day', year=today.year, month=today.month, day=today.day)
        self.calendar.grid(row=0, column=0)

        #Create a new frame to help position buttons alongside calender widget
        frame = Frame(self.calendar_window)
        frame.grid(row=0, column=1, padx=50)
        self.start_date_button = Button(frame, text="Start Date", width=15, command=self.set_start_date)
        self.start_date_button.grid(row=0, column=0, pady=5)
        self.end_date_button = Button(frame, text="End Date", width=15, command=self.set_end_date)
        self.end_date_button.grid(row=1, column=0)
        self.make_graph_button = Button(frame, text="Export Graph...", width=15, command=lambda: self.make_OHLC_graph(self.name, self.start_date, self.end_date))
        self.make_graph_button.grid(row=2, column=0, pady=30)

    def set_start_date(self):
        """Updates the start date button UI and stores the date we should start the OHLC graph from"""
        self.start_date_button.config(text=f"Start - {self.calendar.get_date()}")
        self.start_date = dt.datetime.strptime(self.calendar.get_date(), '%m/%d/%y')

    def set_end_date(self):
        """Updates the end date button UI and stores the date we should end the OHLC graph from"""
        self.end_date_button.config(text=f"End - {self.calendar.get_date()}")
        self.end_date = dt.datetime.strptime(self.calendar.get_date(), '%m/%d/%y')

    def make_OHLC_graph(self, ticker, start_date, end_date):
        """Produces a matplot graph for the stock in question during a given period and exports it as a png"""
        data = yf.download(ticker.get(), start_date, end_date)
        data.reset_index(inplace=True)

        # Converts each datetime into a numerical format
        data['Date'] = data['Date'].map(mdates.date2num)

        # Visualise setup
        ax = plt.subplot()
        ax.grid(True)
        ax.set_title(f"{ticker.get()} Share Price", color='red')
        ax.set_axisbelow(True)
        ax.set_facecolor('black')
        ax.figure.set_facecolor('#121212')
        ax.tick_params(axis='x', colors='red')
        ax.tick_params(axis='y', colors='red')

        #Format x axis to display date values in a dd/mm format
        fmt = mdates.DateFormatter('%d/%m')
        ax.xaxis.set_major_formatter(fmt)

        #Set axis names
        plt.xlabel('Date - dd/mm', fontsize=10, color='black')
        plt.ylabel('(£) Price', fontsize=10, color='black')

        ##Setup candlestick graph
        candlestick_ohlc(ax, data.values, width=0.5, colorup='#00ff00', colordown='red')

        #Open file explorer to allow user to save graph out as a png file
        filetypes = [('Image Files', '*.PNG')]
        dwindow = tkinter.filedialog.asksaveasfilename(initialdir = "./", initialfile=f"{self.name.get()}_OHLC_Graph", title="Select file", filetypes=filetypes) + ".png"
        file = open(dwindow, "w+")
        plt.savefig(file.name)

    def read_in_stock_data(self, data_list):
        """Applies the stock data read in from the open file function to the relevant ui variables"""
        if (len(data_list) != 3):
            print("Can't load stock data - insufficient values")
        else:
            self.name.set(data_list[0])
            self.buy_in_price.set(data_list[1])
            self.quantity.set(data_list[2])

    def remove_grid(self):
        """Removes all grid compononets from the UI objects i.e resets the UI"""
        self.name_entry.grid_remove()
        self.market_open_text.grid_remove()
        self.stock_price_text.grid_remove()
        self.buy_in_price_entry.grid_remove()
        self.quantity_entry.grid_remove()
        self.stock_investment_worth.grid_remove()
        self.stock_current_worth.grid_remove()
        self.stock_profit.grid_remove()

    def set_price(self, new_price):
        """Update all the relevant UI fields which rely on the pricing of the active stock"""
        investment_total = float(self.quantity.get()) * float(self.buy_in_price.get())
        current_total_worth = float(self.quantity.get()) * float(new_price)
        profit_loss = current_total_worth - investment_total

        self.price.set("")
        self.price.set(float("{:.3f}".format(new_price)))

        self.investment_worth.set("")
        self.investment_worth.set(investment_total)

        self.current_worth.set("")
        self.current_worth.set(float("{:.2f}".format(current_total_worth)))

        self.profit_loss.set("")
        self.profit_loss.set(float("{:.2f}".format(current_total_worth - investment_total)))

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
        return self.name.get()

    def get_current_price(self):
        """Returns the price field of the stock object"""
        return self.price.get()
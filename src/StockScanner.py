from bs4 import BeautifulSoup as soup
from StockItem import *
import tkinter.filedialog
import datetime
import requests
import time
import lxml

######################################################################

def download_ftse_tickers():
    FTSE_100 = "https://en.wikipedia.org/wiki/FTSE_100_Index"

    ftse = requests.get(FTSE_100)
    page = soup(ftse.text, 'lxml')

    table = page.find('table', {'id': 'constituents'})
    rows = table.find_all('tr')
    ftse_tickers = []
    for row in rows[1:]:
        ftse_tickers.append(row.findAll('td')[1].text + ".L")

    return ftse_tickers

######################################################################

def add_new_stock(ftse_tickers):
    """Adds an empty stock template to the list of tracked stocks"""
    add_new_stock_button.grid(row=(len(stock_list) + 4), column=4)
    stock_list.append(StockItem(root, "", len(stock_list)+2, ftse_tickers))

######################################################################

def setup_header_names():
    """Use to create the tkinter header label tags for each column in the program"""
    header_stock_name = Label(root, text="Stock", font=("Courier", 15))
    header_stock_name.grid(row=0, column=0, padx=15)

    header_market_open = Label(root, text="Market Open", font=("Courier", 15))
    header_market_open.grid(row=0, column=1, padx=15)

    header_stock_current_price = Label(root, text="Current Price", font=("Courier", 15))
    header_stock_current_price.grid(row=0, column=2, padx=15)

    header_stock_buy_in_price = Label(root, text="Buy In Price(£)", font=("Courier", 15))
    header_stock_buy_in_price.grid(row=0, column=3, padx=15)

    header_stock_num_shares = Label(root, text="# Shares", font=("Courier", 15))
    header_stock_num_shares.grid(row=0, column=4, padx=15)

    header_stock_bought_worth = Label(root, text="Bought Worth", font=("Courier", 15))
    header_stock_bought_worth.grid(row=0, column=5, padx=15)

    header_stock_current_worth = Label(root, text="Current Worth", font=("Courier", 15))
    header_stock_current_worth.grid(row=0, column=6, padx=15)

    header_profit_loss = Label(root, text="Profit/Loss", font=("Courier", 15))
    header_profit_loss.grid(row=0, column=7, padx=15)

######################################################################

def setup_buttons(tickers):
    """Creates the pause and default stock slot buttons"""
    pause_text = Label(root, text="Pause", font=("Courier", 15))
    pause_text.grid(row=10, column=6)
    paused_application = BooleanVar()
    paused_application.set(True)
    paused_button = Checkbutton(variable=paused_application)
    paused_button.grid(row=10, column=7)

    add_new_stock_button = Button(root, pady=5, width=10, text="+", command=add_new_stock)
    return add_new_stock_button, paused_application

######################################################################

def open_file():
    """Menu option to load in stock data from an external text file"""
    canUsefiletypes = [('Text Files', '*.txt'), ('All files', '*')]
    dialogueWindow = tkinter.filedialog.Open(root, filetypes = canUsefiletypes)
    file = dialogueWindow.show()

    if file != "":
        FileToRead = open(file, "r")

        for stock in stock_list:
            stock.remove_grid()

        stock_list.clear()

        stock_file_data = []
        for lines in FileToRead:
            stock_file_data.append(lines)

        loaded_stock_data = []
        for index, stock in enumerate(stock_file_data):
            data = str(stock).split(',')
            stock_name = data[0]
            stock_owned = data[1]
            stocked_purchase_price = data[2].strip()

            #Add the three values we want into a list into a list
            loaded_stock_data.append([stock_name, stock_owned, stocked_purchase_price])

        for index, stock in enumerate(loaded_stock_data):
            add_new_stock()
            stock_list[index].read_in_stock_data(stock)

######################################################################

def save_file():
    """Menu option to save current stock data to an external text file"""
    canUsefiletypes = [('Text Files', '*.txt'), ('All files', '*')]
    dialogueWindow = tkinter.filedialog.asksaveasfilename(title="Select file", filetypes=canUsefiletypes)
    dialogueWindow += (".txt")
    file = open(dialogueWindow, "w+")

    for index, stock in enumerate(stock_list):
        file.write(stock_list[index].name.get() + "," + stock_list[index].bought_price.get() + "," + stock_list[index].quantity.get() + "\n")

######################################################################

def new_file():
    """Menu option to empty current stock list"""
    for stock in stock_list:
        stock.remove_grid()
    add_new_stock()

##################################################################

def check_if_markets_open(stock):
    """Uses timezones to determine whether the exchange the stock is sold on is currently open or closed"""
    current_time = datetime.datetime.now()

    #return false if it's the weekend as markets are closed
    if datetime.date.today().weekday() >= 5:
        return False

    LSE_open = current_time.replace(hour=8, minute=0, second =0, microsecond=0)
    LSE_close = current_time.replace(hour=16, minute=30, second =0, microsecond=0)
    NYSE_open = current_time.replace(hour=14, minute=30, second=0, microsecond=0)
    NYSE_close = current_time.replace(hour=21, minute=0, second=0, microsecond=0)

    if ".L" in stock:
        if current_time > LSE_open and current_time < LSE_close:
            return True
        else:
            return False
    else:
        if current_time > NYSE_open and current_time < NYSE_close:
            return True
        else:
            return False

##################################################################

def update_stock_prices():
    """Sets active price of stock via yahoo finance's web listing and updates relevant UI fields to display this"""
    if paused_application.get() == False:
        for index, stock_to_check in enumerate(stock_list):
            stock = stock_to_check.get_name()
            if stock != "":
                market_state = check_if_markets_open(stock)
                if market_state or stock_to_check.get_current_price() == '0':
                    req = requests.get(f"https://uk.finance.yahoo.com/quote/{stock}?p={stock}")
                    something = soup(req.text, 'html.parser')
                    item_price = 0
                    try:
                        item_price = something.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
                    except:
                        pass
                    something.decompose()
                    stock_list[index].set_market_state(market_state)
                    item_price = item_price.replace(",","")

                    if ".L" in stock:  #LSE market shows stock in pence
                        stock_list[index].set_price(float(item_price) / 100)
                    else:
                        stock_list[index].set_price(float(item_price))
                else:
                    stock_list[index].set_market_state(market_state)

    root.after(1000, update_stock_prices)

##################################################################

tickers = download_ftse_tickers()

root = Tk()
root.title('Stock Info')
root.geometry("1350x200")

stock_list = []
setup_header_names()
add_new_stock_button, paused_application = setup_buttons(tickers)
add_new_stock(tickers)

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=new_file)
filemenu.add_command(label='Open...', command=open_file)
filemenu.add_command(label='Save...', command=save_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

update_stock_prices()
root.mainloop()


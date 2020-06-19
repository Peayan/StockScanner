# Stock Scanner
A UI python program to help track stock prices and show profits/losses based on number of shares owned and initial purchase price.

The program continuously scrapes the relevant yahoo finance page for the stock in question (current price is displayed if market is open, otherwise the closing price is shown) and displays it to the user in a simple UI layout. 

Please make sure you 'PAUSE' the software whilst entering in any data in the fields as the program will continously attempt to pull new information from the the internet unless this option is pressed. 

You may enter the stock name, amount of stock you own, and how much you paid for the stock as input fields and the program will in turn calculate your profits/loss based on the current market price.

You are able to use 3 menu options in the program;

New - Empties currenty stock list 
Save - Saves the stocks currently tracked into an external .txt which the user can specify name/path
Open - Load in stock data from an external .txt file to be added into the active stock_list 

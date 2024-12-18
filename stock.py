print('hello world')

import wealthsimple

# email = 'jassep1974@gmail.com'
# password = 'Jaskirat2512+'

# def my_two_factor_function():
#     MFACode = ""
#     while not MFACode:
#         # Obtain user input and ensure it is not empty
#         MFACode = input("Enter 2FA code: ")
#     return MFACode

# ws = wealthsimple.WSTrade(
#     email,
#     password,
#     two_factor_callback=my_two_factor_function,
# )


# https://github.com/yusuf8ahmed/Wsimple

from wsimple.api import Wsimple

def get_otp():
    return input("Enter otpnumber: \n>>>")

# email = str(input("Enter email: \n>>>"))
# password = str(input("Enter password: \n>>>"))

email = ''
password = ''

ws = Wsimple(email, password, otp_callback=get_otp) 

# always check if wealthsimple is working (return True if working or an error)
if ws.is_operational(): 
  # check the current operation status of internal Wealthsimple Trade
  print(ws.current_status())
  print('Exchange rate')
  print(ws.get_exchange_rate()) 
  # return a list of securities that include GOOG and GOOGL
  print(ws.find_securities("GOOG")) 
  print('Stoxk')
  print(ws.stock("AMZN")) 
  print('Stoxk2')
  print(ws.public_find_securities_by_ticker('AMZN')) 
  
  # # create deposit order for 2000 CAD into your account
  # ws.make_deposit(2000)
  
  # # create withdrawal order for 6000 CAD into your account
  # ws.make_withdrawal(6000)
  
  # return opening and closing of the exchange NYSE
  print(ws.get_market_hours(exchange="NYSE"))
# Currency Converter

A Python3 currency converter using exchange rates from [ExchangeRate-API](https://www.exchangerate-api.com/) with hourly rate updates and [Redis server](https://redis.io/) for cache.

You can run the converter as a CLI application or a web API application. The converter allows conversion from/to [these currencies](https://www.exchangerate-api.com/supported-currencies) and is able to decode currency symbols<a href="#note1" id="note1ref"><sup>1</sup></a> based on the [following definitions](http://www.localeplanet.com/api/auto/currencymap.json).


### Prerequisites

This application requires a running Redis server, you can configure the connection to a Redis server in data_storage.py module. See [Redis documentation](https://redis.io/topics/quickstart) on how to set up a Redis server or use [this article](https://medium.com/@furkanpur/installation-redis-on-windows-10-13fbb055be7c) if you are on a Windows machine.

The converter also uses the following python packages:
```
flask==0.12.2
click==6.7
redis==2.10.6
```
You can use requirements.txt to set up your environment.

## How to use the converter

The application uses 3 input parameters - ```[amount]```, ```[input_currency]``` and optional ```[output_currency]```. It provides conversion of ```[amount]``` in ```[input_currency]``` to ```[output_currency]``` or all available currencies if ```[output_currency]``` was not specified. The ```[input_currency]``` and  ```[output_currency]``` can be specified either by a 3 letter currency code following [ISO&nbsp;4217](http://www.xe.com/iso4217.php) or by a currency symbol<a href="#note1" id="note1ref"><sup>1</sup></a>.

### CLI application
Simply run currency_converter.py module with listed parameters.

Example uses:

a)
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
```
Result:
```
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2541.21
    }
}
```
b)
```
./currency_converter.py --amount 10.92 --input_currency £ 
```
Result:
```
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 12.25,
        "AED": 55.53,
        "AMD": 7257.99,
        ...
    }
}
```

### Web API application

To start the server for the web API, run the following commands:
```
$ export FLASK_APP=currency_converter.py
$ flask run
```
Use ```set``` instead of ```export``` to run the server on Windows machines. Head over to the [Flask documentation](http://flask.pocoo.org/docs/0.12/quickstart/) if you need more information about Flask.

Example uses:

a)
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
```
Result:
```
{
  "input": {
    "amount": 0.9, 
    "currency": "CNY"
  }, 
  "output": {
    "AUD": 0.18
  }
}
```
b)
```
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
```
Result:
```
{
  "input": {
    "amount": 10.92, 
    "currency": "GBP"
  }, 
  "output": {
    "AED": 55.53, 
    "AMD": 7257.99, 
    "ANG": 26.94, 
    ...
  }
}
```

### Using converter module alone

You can also use the Converter object from the converter module as it is. It can decode currency symbols for you or you can call the conversion method without the CLI/API in your project. Note that this will still require a running Redis server for data storage.

```
from converter import Converter

c = Converter()
print(c.decode_symbol("$"))
print(c.convert_currency(amount=100, input_currency="CZK", output_currency="£"))
```
Result:
```
USD
{'input': {'amount': 100, 'currency': 'CZK'}, 'output': {'GBP': 3.51}}
```
 
---



<a id="note1" href="#note1ref"><sup>1</sup></a> *Symbol mapping*

symbol|currency code| |symbol|currency code | |symbol|currency code
---|---|---|---|---|---|---|---
$|USD| |Rp|IDR| |₱|PHP
€|EUR| |₪|ILS| |₨|PKR
£|GBP| |₹|INR| |zł|PLN
د.إ.|AED| |د.ع.|IQD| |₲|PYG
դր.|AMD| |﷼|IRR| |ر.ق.|QAR
Kz|AOA| |د.أ.|JOD| |RON|RON
KM|BAM| |￥|JPY| |дин.|RSD
৳|BDT| |Ksh|KES| |руб.|RUB
лв.|BGN| |៛|KHR| |ر.س.|SAR
د.ب.|BHD| |₩|KRW| |kr|SEK
R$|BRL| |د.ك.|KWD| |฿|THB
P|BWP| |₸|KZT| |د.ت.|TND
CHF|CHF| |ل.ل.|LBP| |TL|TRY
¥|CNY| |රු.|LKR| |NT$|TWD
Kč|CZK| |د.م.|MAD| |TSh|TZS
Kr.|DKK| |MKD|MKD| |₴|UAH
ج.م.|EGP| |K|MMK| |UZS|UZS
ብር|ETB| |MUR|MUR| |Bs.F.|VEF
GHS|GHS| |RM|MYR| |₫|VND
Q|GTQ| |₦|NGN| |FCFA|XAF
L|HNL| |ر.ع.|OMR| |CFA|XOF
kn|HRK| |B$|PAB| |R|ZAR
Ft|HUF| |S/|PEN| ||


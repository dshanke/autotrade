[Home](index.html)

### Fetching Financial data from Yahoo

[Previous](lesson2.html)

#### Install & setup some python libraries

Create a file under your `tutorials` folder and name it as `requirements.txt`

```text
numpy>=1.15
lxml>=4.5.1
multitasking>=0.0.7
pandas>=0.24
requests>=2.20
python-dateutil>=2.7.3
pytz>=2017.3
six>=1.5
charset-normalizer~=2.0.0
urllib3>=1.21.1
certifi>=2017.4.17
idna>=2.5
yfinance==0.1.63
plotting==0.0.7
IbPy2
```

From PyCharm open a terminal and type and enter the following commands:
```powershell
cd %HOMEPATH%\algoworkshop\tutorials
pip install -v -r requirements.txt
```

The above command will take about 2-5 minutes to complete.
What we are doing here installing a set of python libraries that we are going to use.

Next, download the following zip package
* [backtrader zip package](backtrader.zip)

Extract the zip file.
The zip file contains a folder by name `backtrader`.  

Copy this `backtrader` folder under location `%HOMEPATH%\algoworkshop\tutorials`.

![](img/y1.jpg)


### Get Yahoo finance data - ***Our first financial program***

#### pandas dataframe - brief note
Before we discuss getting financial data from yahoo let's just briefly understand how the data will be received.
Think that when we request for yahoo data using the yahoo api, it receives an excel sheet which is nothing but table of rows and columns.
Only, - this table is held in-memory of the computer and not in a file.
Every row is for a specific date.
The date is known as the index column.
And then every other column contains data like open price, close price, mid price, etc.


#### 3 line Program - Download file which contains historical price information 

Create a file under `tutorials` folder and name it as `01.download_data_yfinance.py`
```python
import yfinance as yf
data = yf.download('SPY', start='2000-01-01', end='2021-10-21')
data.to_csv('spy.csv')
```

Do you now see a `spy.csv` file in your tutorial's folder?

[Next](lesson4.html)
### Fetching Financial data from Yahoo

#### Install some python libraries

From PyCharm open a terminal and run teh following commands:
```
pip install IbPy2

```


### pandas dataframe
Before we discuss getting financial data from yahoo let's just briefly understand how the data will be received.
Think that when we request for yahoo data using the yahoo api, it receives an excel sheet which is nothing but table of rows and columns.
Only, - this table is held in-memory of the computer and not in a file.
Every row is for a specific date.
The date is known as the index column.
And then every other column contains data like open price, close price, mid price, etc.



### Get Yahoo finance data

Download the following zip package
* [backtrader zip package](https://ddtrades.github.io/autotrade/backtrader.zip)

Extract the zip file.
The zip file contains a folder by name `backtrader`.
Copy this `backtrader` folder under location `%HOMEPATH%\algoworkshop\tutorials`.

![](https://ddtrades.github.io/autotrade/img/y1.jpg)






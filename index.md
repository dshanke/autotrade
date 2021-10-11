# Workshop - TradingBot


## Agenda

* Install & Setup
* First Python Program
* Get Data From Yahoo Finance
* Backtest AAPL share trading using Yahoo Finance Data
* Connect to IBKR TWS workstation
* Get Data From IBKR
  * Seconds Data
  * Minute Data
  * 10 Minute
* First Live Trade - Buy/Sell Order
* Live Trade using SMA strategy
  * Minute Data



## Install & Setup

### Create workshop folders (where we wil install software and write our python code in)
* Open cmd prompt (In windows search type cmd and press enter. a cmd terminal will open)
* Type the following to create folder `algoworkshop\software`

```
cd %HOMEPATH%

mkdir \a algoworkshop\software

exit
```

### Download the following:

* [Anaconda Python](https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe)
* [Pycharm Community Edition](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC)


### Install Anaconda python package

Double-click on the Anaconda package that you have downloaded and follow the step-by-step instructions as shown below:

---
Screen 1
![Step 1](https://ddtrades.github.io/autotrade/img/a-1.jpg)

---
Screen 2
![Step 2](https://ddtrades.github.io/autotrade/img/a-2.jpg)

---
Screen 3
![Step 3](https://ddtrades.github.io/autotrade/img/a-3.jpg)

---
Screen 4
![Step 4](https://ddtrades.github.io/autotrade/img/a-4.jpg)

---
Screen 5
![Step 5](https://ddtrades.github.io/autotrade/img/a-5.jpg)

---
Screen 6
![Step 6](https://ddtrades.github.io/autotrade/img/a-6.jpg)

---
Screen 7
![Step 7](https://ddtrades.github.io/autotrade/img/a-7.jpg)

---
Screen 8
![Step 8](https://ddtrades.github.io/autotrade/img/a-8.jpg)

---
Screen 9
![Step 9](https://ddtrades.github.io/autotrade/img/a-9.jpg)

### Configure Anaconda Environment

In your windows search bar type 'Anaconda Navigator' and click on it and follow the below steps:

---
Screen 1
![](https://ddtrades.github.io/autotrade/img/an-1.jpg)

---
Screen 2
![](https://ddtrades.github.io/autotrade/img/an-2.jpg)

---
Screen 3
![](https://ddtrades.github.io/autotrade/img/an-3.jpg)

---
Screen 4
![](https://ddtrades.github.io/autotrade/img/an-4.jpg)

Wait for the creation to complete and then close it

---
Screen 5
![](https://ddtrades.github.io/autotrade/img/an-5.jpg)


### Install Pycharm

Double-click on the Pycharm package that you have downloaded and follow the step-by-step instructions as shown below:

---
Screen 1
![](https://ddtrades.github.io/autotrade/img/p-1.jpg)

If Windows prompt you asking 'Do you want to allow this app to make changes to your device?' click Yes and proceed.

---
Screen 2
![](https://ddtrades.github.io/autotrade/img/p-2.jpg)

---
Screen 3
![](https://ddtrades.github.io/autotrade/img/p-3.jpg)

---
Screen 4
![](https://ddtrades.github.io/autotrade/img/p-4.jpg)

---
Screen 5
![](https://ddtrades.github.io/autotrade/img/p-5.jpg)

---
Screen 6
![](https://ddtrades.github.io/autotrade/img/p-6.jpg)



### Configure & Setup Pycharm with Anaconda

From your desktop Double-click on Pycharm shortcut to launch the Pycharm application.

---
![](https://ddtrades.github.io/autotrade/img/py-0.jpg)

---
If prompted with below dialogue select 'Do not import settings' and press Next.

![](https://ddtrades.github.io/autotrade/img/py-1.jpg)

---
Customize PyCharm
![](https://ddtrades.github.io/autotrade/img/py-2.jpg)

---
Close PyCharm
![](https://ddtrades.github.io/autotrade/img/py-3.jpg)


### First Python Program

---
Close PyCharm
From your desktop Double-click on Pycharm shortcut to launch the Pycharm application.  And click on New Project

---
![](https://ddtrades.github.io/autotrade/img/pr-1.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-2.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-3.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-4.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-5.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-6.jpg)

---
![](https://ddtrades.github.io/autotrade/img/pr-7.jpg)

---
Right click on tutorial folder and add a new file to the project.
Name the file `lesson1.py`

![](https://ddtrades.github.io/autotrade/img/pr-8.jpg)







### Download the following and extract the content to `%HOMEPATH%\algoworkshop` folder
* [Backtrader zip package](https://ddtrades.github.io/autotrade/backtrader.zip)





### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/ddtrades/autotrade/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.

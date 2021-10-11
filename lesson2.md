### A few python concepts before we start with algo trading lessons

Trust me!
Programming is easy.

You need 'NOT' know everything and every construct of python and/or programming for you to start writing some workable programs.
Here are a few things that will help you kick-start your journey.

* Program file: `A text file where you write your program`

* Statement: `A line in the program file that instructs the computer to do something`

* Function: Think of it as a command. For e.g. You press an electric switch. A bulb will light up. `press_switch` can be expressed as function. You need not know how exacty is the light bulb turned on. all you need to know is when you `press_switch` the bulb will light up.
In our first program `print` was a function. It is responsible for printing the input that you have provided which is `HELLO WORLD!`.


Let's use Python Console to quickly go over some Python concepts. In PyCharm application, using the Menu on Top click on `Tools -> Python or Debug Console`
This will open up the python console which looks like shown below:

![](https://ddtrades.github.io/autotrade/img/pr1.jpg)



* Comments in python
```
# if line starts with # it is a single line comment

"""
multiline comments are embedded within """
this is line 1
this is line 2
this is line 3
"""
```

* Math Operations:
```
#addition
print(10 + 20)

#subtraction
print(45 + 30)

#multiplication
print(100 * 50)

#subtraction
print(10 + 20)

#division
print(10 + 20)
```


* Variable: Let's remember our school days - where algebra was either the most interesting subject or the most hated subject. But we all might remember defining the unknown as 'x'.
  `x` & `y` are example of variable. We can use any alphanumeric characters as a variable & we save values in it.
```
x=10
print(x)
y=11
print(y)

print(x * y)

#string defined in double quote
first_name="danish"
#string defined in single quote
last_name='ali'
print(first_name)
print(last_name)
print(first_name + " " + last_name)

```

* list and how to access a specific entry in the list?
```
#list of numbers
a = [1, 2, 3, 4, 5,]
print(a)

#a list can be acessed using index to refer the value in the list. the index begins at 0
print(a[0])
print(a[2])

#list of strings
b = [ "first", "second", "fourth", "fifth"]
print(b)
print(b[2])
print(b[3])

#list of decimal numbers (in python is is known as flot
c = [ 10.25, 65.81, 45.23, 9.07]
print(c[0])
print(c[2])

#mixed list 
d = [ 10.25, "hello", 97, "end", begin"]
print(d) 
```

* Dictionary - a list of key-value pair
```
#a dictionary with one key-value pair
a = { "name": "jack"}
print(a)
print(a["name"])

#a dictionary with multiple key-value pair
a = { "name": "jack", "age": 33, "address": "someplace, some country" }
print(a["name"])
print(a["address"])

```

* How to print all values in list one at a time
```
c = [ 10.25, 65.81, 45.23, 9.07]
for number in c:
  print("number is: ", number)
  

#another way to roint
for number in c:
  print(f"number is: {number}")

#yet another way to roint
for number in c:
  print("number is: {}".format(number))

  
#Note the indentation is very important. Indentation is way of telling the python interpreter that the statement is a sub part of its predecessor statement
#if you mess up indentation you can mess up the program pretty bad
```

* Function in python 
  * Think of it as a book library. 
  * Anybody who has access to the library can borrow a book, read the book and then return it back to the library
  * If a book already exist then you do not need to write the exactly same thing
function is similar in nature. Once a programmer writes a function, he can use the function any number of times as long he has access to that function.
```
def print_hello():
    print("hello")

print_hello()
```

If you write a function you are the owner, and you can invoke it from your program by calling it as shown above.
However, is the function is written by someone else, and you would like to use it then you will need to import the function into your program before you can use it.
How do we do that? Simply using an import statement.
As an example if you waht to print the date & time of your system then you can use the datetime module.
Let's see how we can do that?

```
import datetime

print(dt.datetime.now())

x = dt.datetime.now()

print(x)
```



* Conditional Statement
Human's by nature are logical thinkers. An example of logical think is:
```
If Traffic Light is showing Red, STOP
Else If Traffic Light is showing Green, GO
Else If Traffic Light is showing Orange Start Stopping.

```

If it was a self-driving car then the program that would run inside the car would be similar in nature
using a variable which tells you the current color of the signal

```
#let's write a function which tell us what to do
def what_should_i_do(color):
  if color == "green":
    print("go")
  else if color == "red":
    print("stop")
  else if color == "orange":
    print("prepare to stop")

what_should_i_do("green")

```


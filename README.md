# Pyanair

Basic app using Ryanair endpoint and requests library to get flights on given day

## Setup

To install, simply download the repo and install requests library using pip
~~~
pip install requests
~~~

## Example of usage

~~~
/path/to/script/main.py 1 0 0 0 KTW ATH RT 2022-08-03 2022-08-15
~~~

Where following parameters are:
Adult, Teen, Children, Infant, Origin, Destination, trip type (RT, OW), Date of flight, Date of back flight

Example response might look like this:

![resp](https://user-images.githubusercontent.com/44212070/181095246-9454b31d-cfb0-4712-87c7-7e9f236e3469.png)


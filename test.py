import datetime

today = datetime.datetime.now()

def greeting(name, dob):
	dob = dob.datedatetime()
	print(f"hello " + name + " you are " + dob + " years old good morning")
name = input('enter your name:')
dob = input ('enter your age:')

greeting(name, dob)
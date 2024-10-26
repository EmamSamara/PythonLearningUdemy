my_integer = 10   #ما بأثر شو تسمي المتغير بس حطلو اي اسم وحط القيمة الي بدك ياها 
my_float = 3.14
my_string = 'emam'
my_boolean=True

print(type(my_integer))   #print the type of the variable
print(type(my_float))
print(type(my_string))
print(type(my_boolean))

print(my_integer)
print(my_boolean)
print(my_string)
print(my_boolean)


user_name = input('please enter your name  : ')
my_fav_num= input('please enter your fav num :  ')
print('my name is ' , user_name , 'and my fav num' , my_fav_num)

sum=0
num1=float(input('enter the first number '))    #we put the float bc in python the INPUT take the user input as a STRING 
num2=float(input('enter the second number '))
sum=num1+num2
print('the sum is ',sum)


age = int(input('please enter your age  '))
if age>=18:print('you are old enough to vote')   #thats the way the IF type in python
else:print('you are not old enough to vote')


number=int(input('enter a number to check if its even or odd '))
if number%2==0:print('the number ', number , 'is even')
else:print('the number ', number , 'is odd')

num =int(input('please enter a number : '))  #the use enter a number and the program print the number decreasing to zero
for i in range(num , -1 ,-1):print(i)







#test

# for x in range(3):
#     print(x)#pgr1

# for x in range(3,6):
#       print(x)pgr2

# for x in range(2,10,2):
#     print(x)#pgr3

 for attemtpt in range(1,3):
     password=input('enter your passowerd:')
     if password==correct_password:
         print('login successful')
         break
     else:
         print('wrong password')
         if attempt==3:
            print('account locked')



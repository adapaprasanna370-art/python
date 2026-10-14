# rama_height=1.3
# raja_height=1.7
# if rama_height>raja_height:
#     print('rama height is taller')
# else:
#     print('raja is taller')#pgm1


total = float(input('enter total amount:'))
if total >=1000:
    discount = total * 0.10
    final_amount = total-discount
    print('discount applied:',discount)
    print('final amount to pay:',final_amount)
else:
    print('no discount applied')
    print('total amount:',total)
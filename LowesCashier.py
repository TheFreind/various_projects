from random import choice, random, randint
"""
This is a program about practising my read and write functions. I will write customer transaction history to a text file, and then
Jennifer will review it at the end of the day and choose to delete SCAMS.
"""

paymentMethods = ["Cash", "Debit", "Credit", "Gift", "Check", "SCAM"]
storeNum = 1719
manager = "Jennifer Philips"

# Customer's order is wholly random: random cost, random quantity of items, and random pay method
# It is then written to a new text file called 'transcationHistory', which will be pulled in another file
with open('transactionHistory.txt', 'w') as f:
    for x in range(10):
        transactionCost = round( random() * 100, 2)
        transactionQty = randint(1, 10)
        customer_pay_method = choice(paymentMethods) 

        f.write(f"|| COST: ${transactionCost}  QTY: {transactionQty}  METHOD: {customer_pay_method} \n")
        f.write(f"|| Thank you for shopping at Lowe's! Ask our manager, {manager}, for improvements! \n")




import mysql.connector as db
from datetime import datetime
from tabulate import tabulate


def searchIndex(list_a,index):
    for i in range(len( list_a)):
        if list_a[i][0] == index:
            return i
    else:
        return None
    



def order_picking(order_list):
    while True:
        print()
        print('Please check the avaliable items and quantity: ')
        
        
        print(tabulate(data,headers=['veg_id','veg_name','quantity','price'],tablefmt='psql'))
        try:

            select_id=int(input('Please select the item id : '))
            index=searchIndex(data,select_id)
            if data[index] [0] != select_id:
                raise
            
            while True:
                
                selected_quantiry=float(input('Please select the quantity : '))
                if selected_quantiry <0 or selected_quantiry > data[index] [2]:
                    print()
                    print("Please select  the quantity form the above list of iteams")
                else:
                    break
                
                
        except :
            print()
            print('please choose iteam id in above list of items')
            continue
        

        
        total_price = data[index][3] * selected_quantiry
        data[index][2]=data[index][2]-selected_quantiry
        order_list.append([select_id,data[index][1],data[index][3],selected_quantiry,total_price])
     
        print('Do you need anythig ...?')
        next_order=input('YES enter 1 : NO Enter any Characher : ')
        if next_order != '1':
            return order_list
def order_display(order_list):
    print(order_list)
    print(tabulate(order_list,headers=['veg_id','veg_name','quantity','price','total_price'],tablefmt='psql'))
    total_price=sum([each[-1] for each in order_list])
    print()
    print('total bill for your orders id : ',total_price)
    return total_price
def order_change(order_list,data):
    while True:
        
        order_display(order_list)
        while True:
            
            iteam_id=int(input( 'please select the iteam id : '))
            index_of_order_list=searchIndex(order_list,iteam_id)
            if index_of_order_list != None:
                
                break
            else:
                print('Please select the iteam id in your order List ' )
       
        index =   searchIndex(data,iteam_id)
        while True:
            iteam_quantity=int(input( 'please select the iteam quantity : '))
            if iteam_quantity <0:
                print('Iteam Quantity should be greater than or equal to zero')
            elif iteam_quantity > data[index][3]+  order_list[index_of_order_list] [3]:
                print('Iteam Quantity should be greater than stock value')
            else:
                break
        if order_list[index_of_order_list][3] <= iteam_quantity:
            diff=iteam_quantity - order_list[index_of_order_list][3]
            data[index][3] =data[index][3] +diff
        else:
            diff=order_list[index_of_order_list][3]-iteam_quantity
            data[index][3] = data[index][3] - diff
        order_list[index_of_order_list][3]=iteam_quantity
        order_list[index_of_order_list][4]=order_list[index_of_order_list][2]*order_list[index_of_order_list][3]
        order_list=list(filter(lambda n :  n[3] !=0,order_list))
        print('Did you like to make change in you order : ')
        change=input('YES - enter 1 : NO - Enter any Characher : ')
        if change != '1':
            return order_list
    
        

connection=db.connect(user='root',password='Qazplm@123',host='localhost')
cur=connection.cursor()
cur.execute('select  * from store.vegetable')
data=cur.fetchall()
data=list(map(list,data))
order_list = []
print('WELCOME TO STORE')


order_list=order_picking(order_list)
total_price=order_display(order_list)
print()
print('Did you like to make change in you order : ')
change=input('YES enter 1 : NO Enter any Characher : ')
if change == '1':
    while True:
        print('Please chose a option to change order or add orders ')
        order_option=input('YES to change enter 1 :  Enter any Characher  to add new orders : ')
        if order_option == '1':
            order_list=order_change(order_list,data)
            total_price=order_display(order_list)
        else:
            order_list=order_picking(order_list)
            total_price=order_display(order_list)
        
        print('Did you want to make any changes...? ')
        order_option=input("YES to change enter 1 :  Enter any Characher  to conform orders: ")
        if order_option != '1':
            break
print()
print('Please Conform Your order : ')
conform=input('Enter 1 to Confore ,Any Characher to Cancle : ')
if conform == '1':
    user_name=input("Please Enter Your Name : ")
    user_number=input('Please Enter Your mobile NUmber :  ')
    order_list=list(filter(lambda n :  n[3] !=0,order_list))
    cur.execute('select * from store.customer')
    user_details=cur.fetchall()
    for each in user_details:
        if each[-1]==user_number:
            cust_id=each[0]
            break
    else:
        cust_id=len(user_details)+1
        args1=(cust_id,user_name,user_number)
        cur.callproc('store.insert_cst',args1)
    
    print('Customer name : ',user_name)
    print('Customer number : ',user_number)
    print('Customer id : ',cust_id)
    total_price=order_display(order_list)
    cur.execute('select * from store.transaction_Details')
    transaction_details=cur.fetchall()
    args2=(len(transaction_details)+1,cust_id,total_price)
    cur.callproc('store.insert_tran',args2)
    for each in order_list:
        args3=(each[0],each[3])
        cur.callproc('store.update_qty',args3)
        cur.execute('select * from store.orders')
        transaction=cur.fetchall()
        args4=(len(transaction)+1,cust_id,len(transaction_details)+1,each[1],each[2],each[3])
        cur.callproc('store.insert_ord',args4)
        
    print('Your orders items')
    
    print('Please pay rupees of ',total_price)
else:
    print('your orders are cancled')
print(" * "*40)
cur.close()
connection.close()

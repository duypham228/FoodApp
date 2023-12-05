import tkinter as tk
from controllers import accountController, customerController, ownerController, deliverController

def clearWindow():
    for widget in window.winfo_children():
        widget.destroy()


def customer_home(cController):
    clearWindow()
    customerHomeFrame = tk.Frame(window)
    customerHomeFrame.pack()

    restaurants = cController.getRestaurants()
    label = tk.Label(customerHomeFrame, text="Restaurants")
    label.pack()
    for restaurant in restaurants:
        restaurantBtn = tk.Button(
            customerHomeFrame, 
            text=restaurant.name,
            width=20,
            height=2,
            command=lambda rsnt = restaurant: customer_restaurant(cController,rsnt)
        )
        restaurantBtn.pack()
    
    label= tk.Label(customerHomeFrame, text="Address")
    label.pack()
    for address in cController.getAddresses():
        label = tk.Label(customerHomeFrame, text=str(address.address_id) + ": " + address.street + ", " + address.city + ", " + str(address.zip))
        label.pack()

    addrBtn = tk.Button(
        customerHomeFrame, 
        text = "Add Address",
        width=20,
        height=2,
        command = lambda : addAddress(cController)
    )
    addrBtn.pack()
    
    label= tk.Label(customerHomeFrame, text="Payment Method")
    label.pack()
    for pymt in cController.getPayments():
        label = tk.Label(customerHomeFrame, text=str(pymt.credit_card_id) + ": " + str(pymt.card_number) )
        label.pack()

    pymtBtn = tk.Button(
        customerHomeFrame, 
        text = "Add Payment",
        width=20,
        height=2,
        command = lambda : addPymt(cController)
    )
    pymtBtn.pack()

def addPymt(cController):
    clearWindow()
    pymtFrame = tk.Frame(window)
    pymtFrame.pack()
    label = tk.Label(pymtFrame, text="Card Information")
    label.grid(row=0)

    label = tk.Label(pymtFrame, text="Card Number: ")
    label.grid(row=1, column=0)
    cNumEntry = tk.Entry(pymtFrame)
    cNumEntry.grid(row=1, column=1)
    
    label = tk.Label(pymtFrame, text="Holder Name")
    label.grid(row=2, column=0)
    cNameEntry = tk.Entry(pymtFrame)
    cNameEntry.grid(row=2, column=1)
   
    label = tk.Label(pymtFrame, text="Expiration Date")
    label.grid(row=3, column=0)
    exprEntry = tk.Entry(pymtFrame)
    exprEntry.grid(row=3, column=1)
    
    label = tk.Label(pymtFrame, text="CVV")
    label.grid(row=4, column=0)
    cvvEntry = tk.Entry(pymtFrame)
    cvvEntry.grid(row=4, column=1)

    addBtn = tk.Button(
        pymtFrame,
        text="Add New Payment",
        width=5,
        height=2,
        command = lambda : submitPymt(cController, cNumEntry, cNameEntry, exprEntry, cvvEntry)
    )
    addBtn.grid(row=5)

def submitPymt(cController, cNumEntry, cNameEntry, exprEntry, cvvEntry):
    cController.addPayment(cNumEntry.get(), cNameEntry.get(), exprEntry.get(), cvvEntry.get())
    customer_home(cController)

def addAddress(cController):
    clearWindow()
    addressFrame = tk.Frame(window)
    addressFrame.pack()
    label = tk.Label(addressFrame, text="Address")
    label.grid(row=0)

    label = tk.Label(addressFrame, text="Street")
    label.grid(row=1, column=0)
    streetEntry = tk.Entry(addressFrame)
    streetEntry.grid(row=1, column=1)
    
    label = tk.Label(addressFrame, text="City")
    label.grid(row=2, column=0)
    cityEntry = tk.Entry(addressFrame)
    cityEntry.grid(row=2, column=1)
   
    label = tk.Label(addressFrame, text="State")
    label.grid(row=3, column=0)
    stateEntry = tk.Entry(addressFrame)
    stateEntry.grid(row=3, column=1)
    
    label = tk.Label(addressFrame, text="Zipcode")
    label.grid(row=4, column=0)
    zipEntry = tk.Entry(addressFrame)
    zipEntry.grid(row=4, column=1)

    addBtn = tk.Button(
        addressFrame,
        text="Add New Address",
        width=5,
        height=2,
        command = lambda : submitAddr(cController, streetEntry, cityEntry, stateEntry, zipEntry )
    )
    addBtn.grid(row=5)

def submitAddr(cController, streetEntry, cityEntry, stateEntry, zipEntry):
    cController.addAddress(streetEntry.get(), cityEntry.get(), stateEntry.get(), zipEntry.get())
    customer_home(cController)

def customer_restaurant(cController,restaurant):
    clearWindow()
    customerRestaurantFrame = tk.Frame(window)
    customerRestaurantFrame.pack()

    cController.pickRestaurant(restaurant.restaurant_id)


    label = tk.Label(customerRestaurantFrame, text=restaurant.name)
    label.pack()
    label = tk.Label(customerRestaurantFrame,text="Menu")
    label.pack()
    for food in cController.getFoods():
        foodLabel = tk.Label(customerRestaurantFrame, text=str(food.food_id) + ") " + food.name + " - " + food.description)
        foodLabel.pack()
    
    label = tk.Label(customerRestaurantFrame, text="Order Now")
    label.pack()
    
    label = tk.Label(customerRestaurantFrame, text="Food ID")
    label.pack(side=tk.LEFT)
    foodIDEntry = tk.Entry(customerRestaurantFrame)
    foodIDEntry.pack(side=tk.LEFT)
    
    label = tk.Label(customerRestaurantFrame, text="Quantity")
    label.pack(side=tk.LEFT)
    quantityEntry = tk.Entry(customerRestaurantFrame)
    quantityEntry.pack(side=tk.LEFT)
    
    addItemBtn = tk.Button(
        customerRestaurantFrame, 
        text = "add Item",
        width = 2,
        height = 2,
        command = lambda: addToCart(cController, foodIDEntry, quantityEntry)
    )
    addItemBtn.pack(side = tk.LEFT)

    label = tk.Label(customerRestaurantFrame, text="")
    label.pack()
    label = tk.Label(customerRestaurantFrame, text="Order")
    label.pack()
    
    for order_line in cController.order.order_list:
        label = tk.Label(customerRestaurantFrame, text=f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label.pack()
    
    label = tk.Label(customerRestaurantFrame, text="")
    label.pack()

    cktOutBtn = tk.Button(
        customerRestaurantFrame, 
        text = "checkout",
        width = 2,
        height = 2,
        command= lambda : checkout(cController)
    )
    cktOutBtn.pack()

def addToCart(cController, foodid,quantity):
        cController.addToCart(foodid.get(),int(quantity.get()))
        label = tk.Label(text=cController.getFood(foodid.get()).name + " - " + quantity.get() + " - " + str(cController.getFood(foodid.get()).price * int(quantity.get())))
        label.pack()
    
def checkout(cController):
    clearWindow()
    chktFrame = tk.Frame(window)
    chktFrame.pack()

    label = tk.Label(chktFrame, text="Checkout")
    label.pack()

    label = tk.Label(chktFrame, text="Cart")
    label.pack()
    for order_line in cController.order.order_list:
        label = tk.Label(chktFrame, text=f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label.pack()

    label = tk.Label(chktFrame, text="Total: $" + str(cController.getCartTotal()) )
    label.pack()
    editOrderBtn = tk.Button(
        chktFrame,
        text = "Edit Order",
        width = 5,
        height=2,
        command = lambda : customer_restaurant(cController, cController.restaurant)
    )
    editOrderBtn.pack()


    label = tk.Label(chktFrame, text="Select Payment")
    label.pack()
    currPymtSelLabel = tk.Label(chktFrame, text ="Current Payment Method: ")
    currPymtSelLabel.pack()
    pymtList = tk.Listbox(chktFrame, selectmode=tk.SINGLE)
    pymtList.pack(pady=10)
    for pymt in cController.getPayments():
        pymtList.insert(tk.END, pymt.card_number)
 


    label = tk.Label(chktFrame, text="Select Delivery Address")
    label.pack()
    currDelAddrLabel = tk.Label(chktFrame, text ="Current Deliver Address: ")
    currDelAddrLabel.pack()
    dAddrList = tk.Listbox(chktFrame, selectmode=tk.SINGLE)
    dAddrList.pack(pady=10)
    for addr in cController.getAddresses():
        dAddrList.insert(tk.END, str(addr.address_id) + ": " + addr.street + ", " + addr.city + ", " + str(addr.zip))

    selPymtIndx = None
    selDelAddrIndx = None

    def selPymt():
        nonlocal selPymtIndx 
        if(pymtList.curselection()):
            selPymtIndx = pymtList.curselection()[0]
            currPymtSelLabel.config(text="Current Payment Method: " + str(cController.getPayments()[pymtList.curselection()[0]].card_number))
       
            
    def selDAddr():
        nonlocal selDelAddrIndx
        if(dAddrList.curselection()):
            selDelAddrIndx = dAddrList.curselection()[0]
            currDelAddrLabel.config(text= "Current Deliver Address: " + cController.getAddresses()[dAddrList.curselection()[0]].street)

    pymtList.bind("<<ListboxSelect>>", lambda event: selPymt())
    dAddrList.bind("<<ListboxSelect>>", lambda event: selDAddr())

    submitBtn = tk.Button(
        chktFrame,
        text = "Submit",
        width = 5,
        height=2,
        command = lambda : submitOrder(cController, selPymtIndx, selDelAddrIndx)
    )
    submitBtn.pack()
  
def submitOrder(cController, selected_payment, selected_address):
    clearWindow()
    receiptFrame = tk.Frame(window)
    receiptFrame.pack()
    label = tk.Label(receiptFrame, text="Items")
    label.pack()
    for order_line in cController.order.order_list:
        label = tk.Label(receiptFrame, text=f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label.pack()

    label = tk.Label(receiptFrame, text="Total: $" + str(cController.getCartTotal()) )
    label.pack()

    address = cController.getAddresses()[selected_address]
    payment = cController.getPayments()[selected_payment]

    label = tk.Label(receiptFrame, text=f"Delivery Address: {address.street}, {address.city}, {address.state}, {address.zip}")
    label.pack()

    label = tk.Label(receiptFrame, text=f"Payment Method {payment.card_number}: {payment.holder_name}")
    label.pack()
    cController.checkout(payment.credit_card_id,address.address_id)
    
    newOrder = tk.Button(
        receiptFrame,
        text="New Order",
        width=5,
        height=2,
        command= lambda: login_window()
    )
    newOrder.pack()
    
def owner_home(oController):
    clearWindow()
    ownerHomeFrame = tk.Frame(window)
    ownerHomeFrame.pack()

    

    label = tk.Label(ownerHomeFrame, text = "Welcome, " + oController.user.first_name)
    label.pack()

    label = tk.Label(ownerHomeFrame, text = "Restarants")

    for restaurant in oController.getRestaurants():
        restaurantBtn = tk.Button(
            ownerHomeFrame, 
            text=restaurant.name,
            width=20,
            height=2,
            command=lambda rsnt = restaurant: owner_restaurant(oController,rsnt)
        )
        restaurantBtn.pack()

    addBtn = tk.Button(
        ownerHomeFrame,
        text = "Add Restaurant",
        width = 20,
        height = 5,
        command = lambda: addRestaurant(oController)
    )
    addBtn.pack()


def addRestaurant(oController):
    clearWindow()
    addRsntFrame = tk.Frame(window)
    addRsntFrame.pack()

    label = tk.Label(addRsntFrame, text = "Restaurant Information")
    label.grid(row = 0 )
    label = tk.Label(addRsntFrame, text="Restaurant Name")
    label.grid(row = 1, column = 0)
    nameEntry = tk.Entry(addRsntFrame)
    nameEntry.grid(row = 1, column=1)
    label = tk.Label(addRsntFrame, text="Phone Number")
    label.grid(row = 2, column = 0)
    numEntry = tk.Entry(addRsntFrame)
    numEntry.grid(row = 2, column=1)
    label = tk.Label(addRsntFrame, text="Email")
    label.grid(row = 3, column = 0)
    emailEntry = tk.Entry(addRsntFrame)
    emailEntry.grid(row = 3, column=1)
    label = tk.Label(addRsntFrame, text="Description")
    label.grid(row = 4, column = 0)
    descEntry = tk.Entry(addRsntFrame)
    descEntry.grid(row = 4, column=1)
    
    label = tk.Label(addRsntFrame, text = "Address Information")
    label.grid(row = 5 )
    label = tk.Label(addRsntFrame, text= "Street")
    label.grid(row = 6, column = 0)
    streetEntry = tk.Entry(addRsntFrame)
    streetEntry.grid(row = 6, column=1)
    label = tk.Label(addRsntFrame, text="City")
    label.grid(row = 7, column = 0)
    cityEntry = tk.Entry(addRsntFrame)
    cityEntry.grid(row = 7, column=1)
    label = tk.Label(addRsntFrame, text="State")
    label.grid(row = 8, column = 0)
    stateEntry = tk.Entry(addRsntFrame)
    stateEntry.grid(row = 8, column=1)
    label = tk.Label(addRsntFrame, text="Zipcode")
    label.grid(row = 9, column = 0)
    zipcodeEntry = tk.Entry(addRsntFrame)
    zipcodeEntry.grid(row = 9, column=1)

    createBtn = tk.Button(
        addRsntFrame,
        text = "Create Restaurant",
        width=5,
        column = 2,
        command= lambda : createRsnt(oController, nameEntry.get(), numEntry.get(), emailEntry.get(), descEntry.get(), streetEntry.get(), cityEntry.get(), stateEntry.get(), zipcodeEntry.get())
    )
    createBtn.pack()

def createRsnt(oController, name, number, email, desc, strret, city, state, zip):
    rstn = oController.addRestaurant(name, number, email, desc, street, city, state, zip)
    owner_home(oController)

def owner_restaurant(oController,rsnt):
    clearWindow()
    oRsntFrame = tk.Frame(window)
    oRsntFrame.pack()

    oController.setRestaurant(rsnt.restaurant_id)

    label = tk.Label(oRsntFrame, text=oController.restaurant.name)
    label.pack()

    addr = oController.getRestaurantAddress()
    label = tk.Label(oRsntFrame, text = f"Address: {addr.street}, {addr.city}, {addr.state}, {addr.zip}" )
    label.pack()

    label = tk.Label(oRsntFrame, text="Menu")
    label.pack()

    for food in oController.getFoods():
        label = tk.Label(oRsntFrame, text = f"{food.food_id}: {food.name} - {food.description} - {food.price}")
        label.pack()

    addFoodBtn = tk.Button(
        oRsntFrame,
        width = 5,
        height = 2,
        command = lambda: addFood(oController)
    )

    label = tk.Label(oRsntFrame, text = "Pending Orders")
    label.pack()

    for order in oController.getPendingOrders():
        label = tk.Label(oRsntFrame,text = f"{order.order_id} : {oController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            oRsntFrame,
            text = "View Order Details",
            width=2,
            height=2, 
            command = lambda ordr = order : viewOrderDetails(oController, ordr)
        )
        detailBtn.pack()

    label = tk.Label(oRsntFrame, text = "Processing Orders")
    label.pack()

    for order in oController.getProcessingOrders():
        label = tk.Label(oRsntFrame,text = f"{order.order_id} : {oController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            oRsntFrame,
            text="View Order Details",
            width=2,
            height=2, 
            command = lambda ordr = order : viewOrderDetails(oController, ordr)
        )
        detailBtn.pack()

    label = tk.Label(oRsntFrame, text = "Ready Orders")
    label.pack()

    for order in oController.getReadyOrders():
        label = tk.Label(oRsntFrame,text = f"{order.order_id} : {oController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            oRsntFrame,
            text= "View Order Details",
            width=8,
            height=1, 
            command = lambda ordr = order : viewOrderDetails(oController, ordr)
        )
        detailBtn.pack()

    backBtn = tk.Button(
        oRsntFrame,
        text = "back",
        width=10,
        height=1,
        command= lambda: owner_home(oController)
    )
    backBtn.pack()

def addFood(oController):
    clearWindow()
    addFoodFrame = tk.Frame(window)
    addFoodFrame.pack()

    label = tk.Label(addFoodFrame, text = "New Menu Item")
    label.grid(row = 0)

    label = tk.Label(addFoodFrame, text="Food Name")
    label.grid(row = 1, column = 0)
    nameEntry = tk.Entry(addFoodFrame)
    nameEntry.grid(row=1, column=1)
    label = tk.Label(addFoodFrame, text="Price")
    label.grid(row = 2, column = 0)
    priceEntry = tk.Entry(addFoodFrame)
    priceEntry.grid(row=2, column=1)
    label = tk.Label(addFoodFrame, text="Description")
    label.grid(row = 3, column = 0)
    descEntry = tk.Entry(addFoodFrame)
    descEntry.grid(row=3, column=1)

    addFoodBtn = tk.Button(
        addFoodFrame,
        width=5,
        height=2,
        command= lambda : submitFood(oController, nameEntry.get(), priceEntry.get(), descEntry.get())
    )

def submitFood(oController, name, price, desc):
    oController.addFood(name, price, desc)
    owner_restaurant(oController, oController.restaurant)

def viewOrderDetails(oController, order):
    
    clearWindow()
    viewOrderFrame = tk.Frame(window)
    viewOrderFrame.pack()

    label = tk.Label(viewOrderFrame, text = f"Order #{order.order_id}")
    label.pack()

    print("length" + str(len(order.order_list)))

    for order_line in oController.getOrderById(order.order_id).order_list:
        print(f"order: {order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label = tk.Label(viewOrderFrame, text=f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label.pack()

    processBtn = tk.Button(
        viewOrderFrame,
        text = "Process Order",
        width =5,
        height = 2,
        command = lambda: processOrder(oController, order)
    )
    processBtn.pack()

    completeBtn = tk.Button(
        viewOrderFrame,
        text = "Complete Order",
        width =5,
        height = 2,
        command = lambda : completeOrder(oController, order)
    )
    completeBtn.pack()

def processOrder(oController, order):
    oController.processOrder(order.order_id)
    owner_restaurant(oController, oController.restaurant)

def completeOrder(oController, order):
    oController.completeOrder(order.order_id)
    owner_restaurant(oController, oController.restaurant)

def viewDeliveryDetails(dController, order):
    
    clearWindow()
    viewDelFrame = tk.Frame(window)
    viewDelFrame.pack()

    label = tk.Label(viewDelFrame, text = f"Order #{order.order_id}")
    label.pack()

    print("length" + str(len(order.order_list)))

    for order_line in dController.getOrderById(order.order_id).order_list:
        label = tk.Label(viewDelFrame, text=f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
        label.pack()

    processBtn = tk.Button(
        viewDelFrame,
        text = "Pick Up Order",
        width =5,
        height = 2,
        command = lambda: pickupOrder(dController, order)
    )
    processBtn.pack()

    completeBtn = tk.Button(
        viewDelFrame,
        text = "Complete Order",
        width =5,
        height = 2,
        command = lambda : deliveredOrder(dController, order)
    )
    completeBtn.pack()

def pickupOrder(dController, order):
    dController.pickupOrder(order.order_id)
    deliver_home(dController)

def deliveredOrder(dController, order):
    dController.completeOrder(order.order_id)
    deliver_home(dController)

def deliver_home(dController):
    clearWindow()
    dHomeFrame = tk.Frame(window)
    dHomeFrame.pack()

    label = tk.Label(dHomeFrame, text = "Ready Orders")
    label.pack()

    for order in dController.getReadyOrders():
        label = tk.Label(oRsntFrame,text = f"{order.order_id} : {dController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            dHomeFrame,
            text = "View Order Details",
            width=2,
            height=2, 
            command = lambda ordr = order : viewDeliveryDetails(dController, ordr)
        )
        detailBtn.pack()

    label = tk.Label(dHomeFrame, text = "Delivering Orders")
    label.pack()

    for order in dController.getDeliveringOrders():
        label = tk.Label(dHomeFrame,text = f"{order.order_id} : {dController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            dHomeFrame,
            text = "View Order Details",
            width=2,
            height=2, 
            command = lambda ordr = order : viewDeliveryDetails(dController, ordr)
        )
        detailBtn.pack()

    label = tk.Label(dHomeFrame, text = "Delivered Orders")
    label.pack()

    for order in dController.getDeliveredOrders():
        label = tk.Label(dHomeFrame,text = f"{order.order_id} : {dController.getCustomerById(order.customer_id).first_name} - {order.status} ")
        label.pack()
        detailBtn = tk.Button(
            dHomeFrame,
            text = "View Order Details",
            width=2,
            height=2, 
            command = lambda ordr = order : viewDeliveryDetails(dController, ordr)
        )
        detailBtn.pack()



def on_login(user):
    
    if user is not None:
        if user.user_type == "customer":
            cController = customerController()
            cController.setUser(user)
            return customer_home(cController)
        elif user.user_type == "owner":
            oController = ownerController()
            oController.setUser(user)
            return owner_home(oController)
        elif user.user_type == "deliver":
            dController = deliverController()
            dController.setUser(user)
            return deliver_home(dController)
    return login_window



def login_window():
    clearWindow()
    
    loginWindowFrame = tk.Frame(window)
    loginWindowFrame.pack()
    window.title("Login Window")
    UsernameLabel = tk.Label(loginWindowFrame, text="Username")
    UsernameEntry = tk.Entry(loginWindowFrame)
    PasswordLabel = tk.Label(loginWindowFrame,text="Password")
    PasswordEntry = tk.Entry(loginWindowFrame) 
    LoginBtn = tk.Button(
        loginWindowFrame,
        text="Login",
        width=25,
        height=5,
        command=lambda: on_login(accountController.login(UsernameEntry.get(),PasswordEntry.get()))
    )
    UsernameLabel.pack()
    UsernameEntry.pack()
    PasswordLabel.pack()
    PasswordEntry.pack()
    LoginBtn.pack()

def register():
    clearWindow()
    registerFrame = tk.Frame(window)
    registerFrame.pack()

    label = tk.Label(registerFrame, text="Register")
    label.grid(row=0)

    label = tk.Label(registerFrame, text="Username")
    label.grid(row=1,column=0)
    uNameEntry = tk.Entry(registerFrame)
    uNameEntry.grid(row=1,column=1)

    label = tk.Label(registerFrame, text="Password")
    label.grid(row=2, column=0)
    passwordEntry = tk.Entry(registerFrame)
    passwordEntry.grid(row=2, column=1)

    label = tk.Label(registerFrame, text="First Name")
    label.grid(row=3, column=0)
    fNameEntry = tk.Entry(registerFrame)
    fNameEntry.grid(row=3, column=1)

    label = tk.Label(registerFrame, text="Last Name")
    label.grid(row=4, column=0)
    lNameEntry = tk.Entry(registerFrame)
    lNameEntry.grid(row=4, column=1)

    label = tk.Label(registerFrame, text="Email")
    label.grid(row=5, column=0)
    emailEntry = tk.Entry(registerFrame)
    emailEntry.grid(row=5, column=1)


    label = tk.Label(registerFrame, text="User Type")
    label.grid(row=6, column=0)
    userType = tk.StringVar()
    userTypeMenu= tk.OptionMenu(
        registerFrame,
        userType,
        *["customer", "owner", "deliver"]
    )
    userTypeMenu.grid(row=6, column=1)

    def submit(username,password, first_name, last_name, email, user_type):
        user = accountController.register(username, password, first_name, last_name, email, user_type)
        on_login(user)

    submitBtn = tk.Button(
        registerFrame,
        text = "Submit",
        width=5,
        height=2,
        command= lambda : submit(uNameEntry.get(), passwordEntry.get(), fNameEntry.get(), lNameEntry.get(), emailEntry.get(), userType.get())
    )

    submitBtn.grid(row=7)





def home():
    clearWindow()
    homeFrame = tk.Frame(window)
    window.title("Home")
    loginBtn = tk.Button(
        text="Login",
        width=25,
        height=5,
        command=login_window
    )
    registerBtn = tk.Button(
        text="Register",
        width=25,
        height=5,
        command=register
    )

    loginBtn.pack()
    registerBtn.pack()


window = tk.Tk()
home()
window.mainloop()


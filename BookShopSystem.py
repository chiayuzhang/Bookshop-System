from turtle import clear, color
import PySimpleGUI as sg
import json


def add_book_window():
    layout = [
        [sg.Text("Enter the number of book")],
        [sg.Input( key = 'number', size= (20,1))],
        [sg.Button("OK",size = (20,1))]
    ]
    window = sg.Window("Add book Window", layout)
    
    total = 0 
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        if event == "OK":
            total = int(values['number'])
            break
            
    window.close()
    return total


def view_buyerhistory(data,id):

    layout = [
        [sg.Text('Book ID : '), sg.Text(data['paydata'][id]['bookbuyID'])],
        [sg.Text('Quantity : '), sg.Text(data['paydata'][id]['Quantities'])],
        [sg.Button("OK")]
    ]
    window = sg.Window("Purchase History", layout, element_justification="center")

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
    
    window.close()
    

def payment(price,email):
    layout =[
            [sg.Text("Total = "), sg.Text("RM"), sg.Text(price)],
            [sg.Text("Name On Card")],
            [sg.Input()],
            [sg.Text('Card Number')],
            [sg.Input(key = 'in1',enable_events=True,size =(6,1)), sg.Input(key ='int2',enable_events=True,size =(6,1))
            ,sg.Input(key ='int3',enable_events=True,size =(6,1)),sg.Input(key = 'int4',enable_events=True,size =(6,1))],
            [sg.Text('Month'), sg.Text("            Year")],
            [sg.Combo(['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December'], key = 'month'), 
            sg.Combo(['2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032'], key = 'year')],
            [sg.Text("Card CVV2/CVC2/4DBC")],
            [sg.Input(password_char = "*", size = (6,1))],
            [sg.Text('Card Issuer Country [optional]')],
            [sg.Combo(['Malaysia', 'Singapore','Hong Kong', 'United States', 'United Kingdom'])],
            [sg.Button('Submit', size = (10,1))]
            ]
    
    tab_window = sg.Window('Payment', layout)

    while True:
        event, values = tab_window.read()
        
        if event ==sg.WIN_CLOSED:
            break

        if event == 'Submit':
            with open('shoppingcart.json',"r") as s:
                shop = json.load(s)
            with open('payment.json',"r") as p:
                payment = json.load(p)

            buyid = []
            quan = []
            for i in shop:
                if i['userEmail'] == email:
                    buyid.append(i['BookID'])
                    quan.append(i['Quantity'])

            jdata = {
                "userEmail"  : email,
                "bookbuyID"  : buyid , 
                "Quantities" : quan
            }
            payment['paydata'].append(jdata)
            jsonData = json.dumps(payment, indent=2)

            outfile = open("payment.json","w")
            outfile.write(jsonData)
            outfile.close()
            
            num = 0
            for i in range(len(shop)):
                if shop[i]["userEmail"] == email:
                    num += 1
            while num >0 :
                for i in shop:
                    if i['userEmail'] == email:
                        shop.remove(i)
                        num -= 1
            open('shoppingcart.json', 'w').write(json.dumps(shop,indent= 2))

            sg.Popup("Payment Done")
            tab_window.close()



    tab_window.close


def tab_buyer(email,User,cmb):
    sg.theme('BluePurple')

    with open('book.json') as f:
        book = json.load(f)
    
    with open('User.json',"r") as json_file:
        admin = json.load(json_file)

    tab2_products = []

    # convert json data to Table data
    t_products = []
    for item in book["bookdata"]:
        t = []
        t.append(item["bookID"])
        t.append(item["bookAuthor"])
        t.append(item["bookTitle"])
        t.append(item["bookPrice"])
        t.append(item["bookCategory"])
        t.append(item["bookQuantity"])
        t_products.append(t)

    header_list = ['BookID', 'Quantity', 'Title','Price']
    heading_list1 =["ID","Author","Title","Price","Category","Quantity"]
    hearder_list2 = ['BookID', 'Quantity', 'Title','Price']

    fon = ("Helvetica", 14)

    id = ""
    for id_user in range(len(admin['Userdata'])):
        if email == admin['Userdata'][id_user]["userEmail"]:
            id = admin['Userdata'][id_user]['userID']
            break

    tab1_layout = [
        [sg.Text(""),sg.Input("", key ="search"),sg.Button("Search")],
        [sg.Table(values=t_products, headings=heading_list1,
                enable_events=True,
                key='TABLE1',
                select_mode='extended',
                auto_size_columns=False,
                col_widths=[10,10,30,10,10,10],
                justification='center')],
        [sg.Text('Enter the Number of Book')],
        [sg.Input(key="quant")],
        [sg.Button('Add'),sg.Button('View Book Information')]
    ]


    tab2_layout = [
        [sg.Table(values=tab2_products, headings=header_list,
                enable_events=True,
                key='TABLE2',
                select_mode='extended',
                auto_size_columns=False,
                col_widths=[10,10,30],
                justification='center')],
        [sg.Button('OK'),sg.Button('Delete', size=(10,1))]
    ]

    tab3_layout = [
                    [sg.Table(values=tab2_products, headings= hearder_list2,
                        enable_events=True, key='TABLE3',
                        num_rows=28,
                        select_mode='extended', 
                        col_widths=[10,10,30],
                        size=(400, 400), 
                        auto_size_columns=False, 
                        justification='center')],
                [sg.Button('Payment', size=(20,1))]

                
    ]

    tab4_layout = [
                [sg.Text("Email : ", size = (10,1), font = fon),sg.Text(email, key ="e", size=(20,1), font = fon)],
                [sg.Text("Name : ", size = (10,1), font = fon),sg.Text(User, key ="u", size = (20,1), font = fon)],
                [sg.Text("User ID : ", size = (10,1), font = fon),sg.Text(id, key = "id", size = (20,1), font = fon)],
                [sg.Text("User Type : ", size = (10,1), font = fon),sg.Text(cmb, key ="cmB", size = (20,1), font = fon)],
                [sg.Button("CHANGE PASSWORD",size=(30,1)), sg.Button("DELETE", size= (30,1))],
                [sg.Button('LOGOUT', size=(40,1))]
                
    ]

    tab_group_layout = [
        [
            sg.Tab('Products', tab1_layout, font='Arial 15', key='-TAB1-'),
            sg.Tab('Shopping Cart', tab2_layout, key='-TAB2-'),
            sg.Tab("Payment", tab3_layout,key='-TAB3-'),
            sg.Tab('User detail',tab4_layout, key='-TAB4',element_justification="center")
        ]
    ]

    layout = [[sg.TabGroup(tab_group_layout, enable_events=True,
                        key='-TABGROUP-', size=(750, 550))]]

    window = sg.Window('My window with tabs', layout,
                    size=(800, 600))


    tab2_products = []
    jtab2_products = []
    while True:
        event, values = window.read()

        if event == 'Search':
                book_big_data= []
                book_Tittle =[]
                for i in book['bookdata']:
                    #convert to upper case
                    str1 = i["bookTitle"].upper()
                    str2 = values["search"].upper()
                    book_search = str1.find(str2)
                    if book_search != -1  :
                        book_Tittle.append(i["bookID"])
                
                for i in book_Tittle:
                    for q in book["bookdata"]:
                        if i == q["bookID"]:
                            book_search_data = []
                            book_search_data.append(q["bookID"])
                            book_search_data.append(q["bookAuthor"])
                            book_search_data.append(q["bookTitle"])
                            book_search_data.append(q["bookPrice"])
                            book_search_data.append(q["bookCategory"])
                            book_search_data.append(q["bookQuantity"])
                            book_big_data.append(book_search_data)

                window['TABLE1'].update(values = book_big_data)

        if event == 'Add':
            for item in values['TABLE1']:
                # you must check quantity is enough
                t_products[int(item)][5] = t_products[int(item)
                                                    ][5] - int(values['quant'])

                found = False
                for index in range(len(tab2_products)):
                    if tab2_products[index][0] == t_products[item][0]:
                        found = True
                        break

                if found:
                    # depends if you have enough
                    tab2_products[index][1] = tab2_products[index][1] + \
                        int(values['quant'])
                else:
                    t = []
                    t.append(t_products[item][0])
                    t.append(int(values['quant']))
                    t.append(t_products[item][2])
                    t.append(t_products[item][3])
                    tab2_products.append(t)

                    d = {}
                    d['userEmail'] = email
                    d['BookID'] = t_products[item][0]
                    d['Quantity'] = int(values['quant'])
                    d['Title'] = t_products[item][2]
                    d['Price']=t_products[item][3]
                    jtab2_products.append(d)

            window['TABLE1'].update(values=t_products)
            window['TABLE2'].update(values=tab2_products)
            window['TABLE3'].update(values=tab2_products)
           
        if event == 'OK':
            jdata = json.dumps(jtab2_products, indent=2)
            sg.Popup("The book is added into Shopping cart")
            with open('shoppingcart.json', 'w') as f:
                f.write(jdata)
                
        if event == "Delete":
            for item in values["TABLE2"]:
                tab2_products.pop(item)
                sg.popup("Deleted Successfull")

            window['TABLE2'].update(values=tab2_products)
            window['TABLE3'].update(values=tab2_products)

        if event == "LOGOUT":
            window.close()
            main_window()
        
        if event == "CHANGE PASSWORD":
            change_password()
        
        if event == "DELETE":
            jfile = "user.json"
            keyword = "Userdata"
            ID = id_user
            delete_book_button(jfile,keyword,ID)

            with open('shoppingcart.json',"r") as json_file:
                shop = json.load(json_file)

            num = 0
            for i in range(len(shop)):
                if shop[i]["userEmail"] == email:
                    num += 1

            while num >0 :
                for i in shop:
                    if i['userEmail'] == email:
                        shop.remove(i)
                        num -= 1

            open('shoppingcart.json', 'w').write(json.dumps(shop,indent= 2))
            window.close()
            main_window()

        if event == "View Book Information":
            searchBook(book,values["TABLE1"][0])    


        if event == "Payment":
            with open('book.json',"r") as f:
                book = json.load(f)
            with open('shoppingcart.json',"r") as s:
                shop = json.load(s)

            price = 0 
            for b in range (len(book['bookdata'])):
                for s in range (len(shop)):
                    if book['bookdata'][b]["bookID"] == shop[s]["BookID"]:
                        price += book["bookdata"][b]['bookPrice'] * float(shop[s]['Quantity'])

            price_format = "{:.2f}".format(price)
            payment(price_format,email)


            for num in range(len(tab2_products)):
                tab2_products.pop(num)
            
            window['TABLE2'].update(values=tab2_products)
            window['TABLE3'].update(values=tab2_products)

        if event is None:
            break

    window.close()
  

def new_window(text):
    layout = [
        [sg.Text(text, key="new")],
        [sg.Text("Please press OK to exit")],
        [sg.Button("OK")]
        ]
    window = sg.Window("New Window", layout, element_justification="center")

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
    
    window.close()

def register_button():
    layout = [
        [sg.Text("     Email", size=(10,1)), sg.Input ( key = 'e') ],
        [sg.Text("  Username ", size=(10,1)), sg.Input ( key = 'u') ],
        [sg.Text("  Password", size=(10,1)), sg.Input ( key = 'p', password_char = "*") ],
        [sg.Button('Create'),sg.Button('Exit')]
    ]
    window = sg.Window("Register Account", layout, element_justification='center', size=(300,130))

    with open('user.json','r+') as json_file: 
        data = json.load(json_file)
        
    while True:
        event, values = window.read()

        if event is None or event == 'Exit' :
            window.close()
            break

        elif event == "Create":
            # search for existing register email
            found = False
            for jdata in data["Userdata"]:
                if values["e"] == jdata["userEmail"]:
                    found = True #check all the file if found, found = true
                    break 

            #after searching the file
            if found == True:
                text ="There has a similar account, Please change it"
                new_window(text)
                break

            else:
                num = 1
                for id in data['Userdata']:
                    if id['userType'] == "Buyer":
                        num += 1

                jdata = {
                    "userEmail"   : values['e'],
                    "userID"      : str(num),
                    "userName"    : values['u'],
                    "userPass"    : values['p'],
                    "userType"    : 'Buyer'
                    
                }
                data['Userdata'].append(jdata)
                jsonData = json.dumps(data, indent=2)

                outfile = open("user.json","w")
                outfile.write(jsonData)
                outfile.close()
                
                text = "Account has been created"
                new_window(text)
                break

        window.close()

def change_password():
    layout = [
        [sg.Text("Email", size = (12,1)), sg.Input (key = 'email', size = (20,1))],
        [sg.Text("New Password", size = (12,1)), sg.Input (key = 'new', size = (20,1))],
        [sg.Button("OK")]
    ]
    window = sg.Window("Change Password",  layout, element_justification='center')

    with open('user.json','r+') as json_file: 
        data = json.load(json_file)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        elif event == "OK": 
            passWord = -1
            for i in range (len(data['Userdata'])) :
                if values['email'] == data["Userdata"][i]['userEmail'] :
                    passWord = i
                    break

            if passWord == -1:
                sg.Popup('Email not found')
            else:
                password = values['new']
                data["Userdata"][i]['userPass'] = password
                sg.Popup("Change Sucessful")
                window.close()

            open('user.json', "w").write(
                json.dumps(data, indent= 4)
            )
    window.close()

def new_window_logout():
    layout = [
        [sg.Text("Logout Successfully")]
        [sg.Button("OK")]
    ]
    window = sg.Window("Inform Window",layout)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        
    window.close()

def user_information(email, user, ID, cmb):
    layout= [
        [sg.Text("Email     : ", size = (10,1)),sg.Text(email, key ="e", size=(20,1), text_color='red')],
        [sg.Text("Name      : ", size = (10,1)),sg.Text(user, key ="u", size = (20,1))],
        [sg.Text("User ID   : ", size = (10,1)),sg.Text(ID, key = "id", size = (20,1))],
        [sg.Text("User Type   : ", size = (10,1)),sg.Text(cmb, key ="cmB", size = (20,1))],
        [sg.Button('Change Password'),sg.Button('Delete Account'),sg.Button("Back")]
    ]

    window = sg.Window("User Detail", layout, size= (400,300))

    with open('user.json','r+') as json_file: 
        data = json.load(json_file)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED :
            break
        
        if event == "Back":
            window.close()
            new_window_admin(email,user,cmb)
        
        if event == "Logout" :
            window.close()
            main_window()

        if event == "Delete Account" :
            index = -1
            for i in range (len(data['Userdata'])) :
                if email == data["Userdata"][i]['userEmail']:
                    index = i
                    break

            if index == -1 :
                sg.Popup('Account is not found')
            else:
                data['Userdata'].pop(index)
                open('user.json', "w").write(
                    json.dumps(data, sort_keys=True, indent= 4, separators=(',', ':'))
                )
                sg.Popup("Account has been deleted")
                window.close()
                main_window()

        if event == "Change Password":
            change_password()

    window.close()



def searchBook(data,s_book):
    fon= ("Arial",13)
    sz = (14,1)
    layout = [
        [sg.Text("Book ID:",size=sz,font=fon), sg.Text(data['bookdata'][s_book]["bookID"],text_color='red')],
        [sg.Text("Book NAME:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookTitle"],text_color='red')],
        [sg.Text("Book AUTHOR:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookAuthor"],text_color='red')],
        [sg.Text("Book PRICE:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookPrice"],text_color='red')],
        [sg.Text("Book CATEGORY:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookCategory"],text_color='red')],       
        [sg.Text("Book QUANTITY:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookQuantity"],text_color='red')],
        [sg.Text("Book YEAR:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookYear"],text_color='red')],
        [sg.Text("Book PAGE:",size=sz,font=fon),sg.Text(data['bookdata'][s_book]["bookPage"],text_color='red')]
    ]
    
    window = sg.Window("New Window", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()

##############Create a new window for the add book function when the book is added.###############
def Addbook(text):
    layout = [
        [sg.Text(text, key="new")],
        [sg.Button("OK")]
    ]
    window = sg.Window("New Window", layout)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        
    window.close()


def add_book_button(inside):
    layout = [
        [sg.Text("Title ",size = (10,1)), sg.Input ( key = 'b',size = (20,1)) ],
        [sg.Text("Author " ,size = (10,1)), sg.Input (key = 'c',size = (20,1))  ],
        [sg.Text("Price" ,size = (10,1)),sg.Input (key = 'd',size = (20,1))],
        [sg.Text("Category", size = (10,1)), sg.Input (key = 'e',size = (20,1))],
        [sg.Text("Quantity",size = (10,1)), sg.Input (key = 'f',size = (20,1))],
        [sg.Text("Year",size = (10,1)), sg.Input(key = 'g',size = (20,1))],
        [sg.Text("Page",size = (10,1)), sg.Input(key = 'h',size =(20,1))],
        [sg.Button('Add'),sg.Button('Exit')]
    ]

    window = sg.Window("Add Book Service", layout,element_justification = "center")
    with open('book.json','r+') as json_file: 
        data = json.load(json_file)

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == 'Add':
            num = len(data['bookdata']) + 1

            jdata = {
                "bookAuthor"      : values['c'],
                "bookCategory"    : values['e'],
                "bookID"          : str(num)  ,
                "bookPage"        : values['h'],
                "bookPrice"       : values['d'],                                                    
                "bookQuantity"    : values['f'],
                "bookTitle"       : values['b'],     
                "bookYear"        : values['g'],
            }
            
            inside.append(jdata["bookID"])
            inside.append(jdata["bookAuthor"])
            inside.append(jdata["bookTitle"])
            inside.append(jdata["bookPrice"])
            inside.append(jdata["bookCategory"])
            inside.append(jdata["bookQuantity"])

            data['bookdata'].append(jdata)
            jsonData = json.dumps(data, indent = 4)

            outfile = open("book.json", "w")
            outfile.write(jsonData)
            outfile.close()
            text = 'The book is added.'
            Addbook(text)

    window.close()

def add_admin_user(inside):
    layout = [
        [sg.Text("Email ",size = (10,1)), sg.Input ( key = 'email',size = (20,1)) ],
        [sg.Text("Name " ,size = (10,1)), sg.Input (key = 'name',size = (20,1))  ],
        [sg.Text("Password" ,size = (10,1)), sg.Input ( key = 'pass', size = (20,1), password_char = "*")],
        [sg.Button('Add'),sg.Button('Exit')]
    ]

    window = sg.Window("Add New Admin User", layout,element_justification = "center")
    with open('user.json','r+') as json_file: 
        data = json.load(json_file)

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == 'Add':

            found = False
            for jdata in data["Userdata"]:
                if values["email"] == jdata["userEmail"]:
                    found = True #check all the file if found, found = true
                    break 

            #after searching the file
            if found == True:
                text ="There has a similar account, Please change it"
                Addbook(text)
                break

            else:
                num = 1
                for id in data['Userdata']:
                    if id['userType'] == "Admin":
                        num += 1

                adata = {
                    "userEmail" : values['email'],
                    "userID"    : str(num),
                    "userName"  : values["name"]  ,
                    "userPass"  : values['pass'],
                    "userType"  : "Admin"
                }
                
                inside.append(adata["userID"])
                inside.append(adata["userName"])
                inside.append(adata["userEmail"])
                inside.append(adata["userPass"])
                inside.append(adata["userType"])

                data['Userdata'].append(adata)
                jsonData = json.dumps(data, indent = 4)

                outfile = open("user.json", "w")
                outfile.write(jsonData)
                outfile.close()
                text='A New Admin Users is added.'
                Addbook(text)

    window.close()

def view_book_button():
    layout = [
        [sg.Text("Buyer Name:"), sg.Input (key = 'by')],
        [sg.Button('View'),sg.Button('Exit')]
    ]

    window = sg.Window("View Buyer Page", layout,element_justification = "center")
    with open('book.json','r+') as json_file: 
        data = json.load(json_file)

    while True:
        event, values = window.read()
        
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == 'View':
            pass

        window.close()


def search_book_button():
    layout = [
        #[sg.Text("Title"), sg.Input ( key = 'title') ],
        #[sg.Text("Author"), sg.Input (key = 'author') ],
        [sg.Text("Title"), sg.Input (key = 'title')],
        #[sg.Text("Year"),sg.Input (key = 'year')],
        [sg.Button('Search'),sg.Button('Exit')],
    ]
    
    window = sg.Window("Search Book Service", layout,element_justification = "center")
    with open('book.json',"r") as json_file:
        data = json.load(json_file)
        
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        elif event == 'Search':
            s_book = -1
            S_book =[]
            for s in range (len(data['bookdata'])) :
                if values["title"]== data["bookdata"][s]['bookTitle'] :
                    s_book = s

            searchBook(s_book)
            
                        
    window.close()


def delete_book_button(jfile, keyword, index):

    with open(jfile,'r+') as json_file: 
        data = json.load(json_file)

    if index == -1:
        print ('not found')
    else:
        data[keyword].pop(index)

    open(jfile, "w").write(
        json.dumps(data, sort_keys=True, indent= 4, separators=(',', ':'))
    )
    sg.Popup("Deleted successful")


def table_function_book():

    with open('book.json',"r") as json_file:
        data = json.load(json_file)

    book_data=[]
    for i in data["bookdata"]:
        inside_data = []
        inside_data.append(i["bookID"])
        inside_data.append(i["bookAuthor"])
        inside_data.append(i["bookTitle"])
        inside_data.append(i["bookPrice"])
        inside_data.append(i["bookCategory"])
        inside_data.append(i["bookQuantity"])

        # inside_data.append(i["bookTitle"])

        book_data.append(inside_data)
            
    heading_list =["ID","Author","Title","Price","Category","Quantity"]
    # heading_list2 = ["Name","ID","Book"]

    sg.theme('BluePurple')
    layout =[
        [sg.Text(""),sg.Input("", key ="search"),sg.Button("Search")],
        [sg.Table(values=book_data, headings=heading_list,
                enable_events=True, key='table1',
                num_rows=28,
                select_mode='extended', 
                col_widths=[6,10,30,10,10,10],
                size=(400, 400), 
                auto_size_columns=False, 
                justification='center')],
        [sg.Button('Add', size=(10,1)), sg.Button('Delete', size=(10,1)),
        sg.Button('View Book Information', size=(20,1)),sg.Button('Exit', size=(10,1))]
    ]
    window = sg.Window('Admin Page', layout, size=(800, 600))

    while True:
        event, values = window.Read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        elif event == "Add":
            inside = []
            add_book_button(inside)
            book_data.append(inside)
            window['table1'].update(values = book_data)


        elif event == "Delete":
            jfile = "book.json"
            json_keyword = "bookdata"
            for i in values['table1']:
                delete_book_button(jfile,json_keyword,i)
                print(book_data[i])
                book_data.remove(book_data[i])
                window['table1'].update(values=book_data)

        elif event == "View Book Information" :
            searchBook(data,values["table1"][0])


        if event == 'Search':
            book_big_data= []
            book_Tittle =[]
            for i in data['bookdata']:
                #convert to upper case
                str1 = i["bookTitle"].upper()
                str2 = values["search"].upper()
                book_search = str1.find(str2)
                if book_search != -1  :
                    book_Tittle.append(i["bookID"])
            
            for i in book_Tittle:
                for q in data["bookdata"]:
                    if i == q["bookID"]:
                        book_search_data = []
                        book_search_data.append(q["bookID"])
                        book_search_data.append(q["bookAuthor"])
                        book_search_data.append(q["bookTitle"])
                        book_search_data.append(q["bookPrice"])
                        book_search_data.append(q["bookCategory"])
                        book_search_data.append(q["bookQuantity"])
                        book_big_data.append(book_search_data)

            window['table1'].update(values = book_big_data)


    window.close()

def table_function_admin():

    with open('user.json',"r") as json_file:
        data = json.load(json_file)

    admin_data=[]
    for i in data["Userdata"]:
        inside_data = []
        inside_data.append(i["userID"])
        inside_data.append(i["userName"])
        inside_data.append(i["userEmail"])
        inside_data.append(i["userPass"])
        inside_data.append(i["userType"])

        admin_data.append(inside_data)
            
    heading_list =["ID","Name","Email Address","Password","User Type"]

    sg.theme('BluePurple')
    layout =[
        [sg.Text(""),sg.Input("", key ="s"),sg.Button("Search")],
        [sg.Table(values=admin_data, headings=heading_list,
                enable_events=True, key='table1',
                num_rows=28,
                select_mode='extended', 
                col_widths=[6,10,30,10,10,15],
                size=(400, 400), 
                auto_size_columns=False, 
                justification='center')],
        [sg.Button('Add', size=(10,1)), sg.Button('Delete', size=(10,1)),
        sg.Button('View Shopping History',size=(20,1)),
        sg.Button('Exit', size=(10,1))]
    ]
    window = sg.Window('Admin Page', layout, size=(800, 600))

    while True:
        event, values = window.Read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        elif event == "Search":
            user_big_data= []
            user_name =[]
            for i in data["Userdata"]:
                #convert to upper case
                str1 = i["userName"].upper()
                str2 = values["s"].upper()
                book_search = str1.find(str2)
                if book_search != -1  :
                    user_name.append(i["userID"])
            
            for i in user_name:
                for q in data["Userdata"]:
                    if i == q["userID"]:
                        user_search_data = []
                        user_search_data.append(q["userID"])
                        user_search_data.append(q["userName"])
                        user_search_data.append(q["userEmail"])
                        user_search_data.append(q["userPass"])
                        user_search_data.append(q["userType"])
                        user_big_data.append(user_search_data)

            window['table1'].update(values = user_big_data)

        elif event == "Delete":
            jfile = "user.json"
            keyword = "Userdata"
            for i in values['table1']:
                delete_book_button(jfile,keyword,i)
                print(admin_data[i])
                admin_data.remove(admin_data[i])
                window['table1'].update(values=admin_data)
        
        elif event == "Add":
            inside = []
            add_admin_user(inside)
            admin_data.append(inside)
            window['table1'].update(values = admin_data)



        elif event == "View Shopping History":
            with open('payment.json',"r") as json_file:
                payment = json.load(json_file)

            id = -1
            for i in range(len(payment['paydata'])):
                for item in values['table1']:
                    if data['Userdata'][item]['userEmail'] == payment['paydata'][i]['userEmail']:
                        print(item)
                        print(data['Userdata'][item]['userEmail'])
                        print(payment['paydata'][i]['userEmail'])
                        id = i

            if id == -1 :
                sg.Popup("Not Found")
            
            else:
                view_buyerhistory(payment,id)

            
            

        



    window.close()

def new_window_admin(Email_user, user, cmb):
    sg.theme('BluePurple')
    fon = "Helvetica" 
    layout = [
            [sg.Text('Bookshop System',justification='center',size=(100,1), font=(fon, 25))],
            [sg.Button('Book Information', size =(20,1))],
            [sg.Button('User Information', size =(20,1))],
            [sg.Button('User Detail', size =(20,1))],
            [sg.Button('Logout', size =(20,1))]
    ]

    admin_window = sg.Window(" Adminisator\'s Page",layout, element_justification='center', size=(400,250))

    with open('book.json','r+') as json_file: 
        data = json.load(json_file)
    
    with open('user.json','r+') as json_file: 
        adminData = json.load(json_file)

    while True:
        event,values = admin_window.read()
        
        if event is None:
            break
        
        elif event == "Logout":
            admin_window.close()
            main_window()

        elif event == 'Book Information':
            table_function_book()

        elif event == "User Information":
            table_function_admin()

        elif event == "User Detail": 
            admin_window.close()
            id = ""
            for i in range(len(adminData['Userdata'])):
                if Email_user == adminData['Userdata'][i]["userEmail"]:
                    id = adminData['Userdata'][i]['userID']
                    break
            user_information(Email_user, user, id, cmb)
            

    admin_window.close()




##Main Window
def main_window():
    sg.theme('BluePurple')
    fon = "Helvetica"
    layout = [
        [sg.Image("bookshop.png",size=(50,40))],
        [sg.Text('Bookshop System',justification='center',size=(100,1), font=(fon, 15))],
        [sg.Text("     Email", size=(10,1)), sg.Input ( key = 'email') ],
        [sg.Text("  Password", size=(10,1)), sg.Input ( key = 'pass', password_char = "*") ],
        [sg.Combo(['Admin', 'Buyer'], size=(20,1), key = 'CMB') ],
        [sg.Button('Login', size =(12,1)),sg.Button("Register", size =(12,1)),sg.Button('Exit', size =(12,1))]
    ]

    main_window=sg.Window("Login Account",layout, element_justification='center', size=(380,230))

    with open('user.json','r+') as json_file: 
        data = json.load(json_file)
    
    with open('book.json','r+') as json_file: 
        book = json.load(json_file)

    while True:
        event, values = main_window.read() 

        u = ""
        cmb = values['CMB']
        e = values['email']

        for i in data['Userdata']:
            if e == i['userEmail']:
                u = i['userName'].upper()
                break

        if event is None or event == 'Exit' :
            break

        if event == 'Login' :
            for p in data['Userdata']:
                if p['userEmail'] == values['email'] and p['userPass'] == values["pass"] and p['userType'] == values['CMB'] :   
                    main_window.close()
                    if values['CMB'] == "Admin":
                        new_window_admin(e, u, cmb)

                    if values['CMB'] == "Buyer":
                        tab_buyer(e,u,cmb)

                num =0
                num_of_userdata = len(data['Userdata'])
                for q in data['Userdata']:
                    if q['userEmail'] != values["email"] or q['userPass'] != values["pass"] or q['userType'] != values['CMB']: 
                        num += 1  

                if num_of_userdata == num :
                    sg.Popup("Login Failed","Pls Try Again.")
                    break
            
        if event == "Register":
            register_button()     
            
            
    main_window.close()


main_window()
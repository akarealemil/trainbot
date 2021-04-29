print("Welcome to the best phone sorter program itw!")
login_or_register = str(input("Do you want to login or register?: \n"))

register = open("logindata.txt","a+") 

if login_or_register == "register":
        register.write(input("Type your new user: "))
        register.write(input("Type your new password: "))
        register.close()

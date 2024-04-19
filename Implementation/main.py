import datetime

def verify(users,username,password):    
    for usr in users.items():
        if usr[0] == username and usr[1] == password:
            return True
    return False

def login(db):
    user = input() #insert user
    password = input() #insert password
    verify(db, user, password)

def readUserDatabase(fileName):
    db = dict()
    with open(fileName, 'r') as f:
        for line in f:
            username, password,email,phoneNumber,balance = line.rstrip().split('/')
            db[username] = [password,email,phoneNumber,balance]
    return db


def addUser(fileName,username,password,email,phoneNumber,balance,currencyCode):
    with open(fileName,'a') as f:
        f.write(username+"/"+password+"/"+email+"/"+phoneNumber,+"/"+balance+"/"+currencyCode)
        
def saveTransactions(db,SRCuser,DSTuser,amount):
    s = str(amount)
    srcFname = SRCuser+".txt"
    dstFname = DSTuser+".txt"
    
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    srcSTR = formatted_datetime+"-> [+"+s+"] RECEIVED MONEY FROM"+SRCuser+"- [CURRENT BALANCE ="+str(db[DSTuser][3])+"]"
    dstSTR = formatted_datetime+"-> [-"+s+"] SENT MONEY TO"+DSTuser+"- [CURRENT BALANCE ="+str(db[SRCuser][3])+"]"
    with open(srcFname,'a') as f:
        f.write(srcSTR+"\n")
    with open(dstFname,'a') as f:
        f.write(dstSTR+"\n")
        
def addBalance(db, user, amount):
    db[user][3] += amount


def removeBalance(db, user, amount):
    final = db[user][3] - amount < 0
    if final < 0:
        print("You don't have enough money")
        return False
    db[user][3] = final
    return True

def transactions(db,SRCuser,DSTuser,amount):
    if not removeBalance(db, SRCuser, amount):
        return False
    else:
        addBalance(db, DSTuser, amount)
        
def currencyExchange(amount,SRCcode,DSTcode):
    # CODE 1 = EUR - (EUROPE)
    # CODE 2 = USD - (USA)
    # CODE 3 = GBP - (UK)
    # CODE 4 = BRL - (BRAZIL)
    if SRCcode == DSTcode:
        return amount
    
    if SRCcode == 1:
        if DSTcode == 2:
            exchange = 1.07
        elif DSTcode == 3:
            exchange = 0.86
        else:
            exchange = 5.54
    elif SRCcode == 2:
        if DSTcode == 1:
            exchange = 0.94
        elif DSTcode == 3:
            exchange = 0.81
        else:
            exchange = 5.20
    elif SRCcode == 3:
        if DSTcode == 1:
            exchange = 1.16
        elif DSTcode == 2:
            exchange = 1.24
        else:
            exchange = 6.44
    else:
        if DSTcode == 1:
            exchange = 0.18
        elif DSTcode == 2:
            exchange = 0.19
        else:
            exchange = 0.16
    
    return amount * exchange

def checkUsername(u, db):
    for user in db.keys():
        if u == user:
            return False
    return True


def checkPasswords(password1, password2):
    if password1 != password2:
        return False
    else:
        return True
        
def signUp(db, fname):
    email = input()  # insert email
    user = input()  # inert Username
    password = input()  # insert password
    repeatpassword = input()  # repeat password
    phonenumber = input()  # insert PhoneNumber
    balance = 0

    if not checkUsername(user, db):
        print("User already taken!")
        return False
    elif not checkPasswords(password, repeatpassword):
        print("Passwords must be the same!")
        return False
    else:
        addUser(fname, user, password, email, phonenumber, balance)
        db[user] = [password, email, phonenumber, balance]
    
    
if __name__ == "__main__":
    fname = "users.txt"
    users = readUserDatabase(fname)
    print(users)
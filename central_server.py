# SERVER MUST HAVE CODES OF THE LOCKERS NOT LOCKERS GIVING CENTRAL 

#2 addresses for every compartment

# one door can only be open at a time
#add more lockers

from typing import Union
import httpx
from fastapi import FastAPI
import time
import random
import string
import traceback

app = FastAPI()

# FAKE DATABASE OF ORDERS     SWITCH TO A REAL DATABASE
fakeDataBaseOrders = []
fakeDataBaseCompletedOrders = []

fakeDataBaseLockers = []

id = 0
#------------------LOCKER SERVERS
LOCKER_SERVER = "http://127.0.0.1:8001"
# --------------------------------------------------------------------------
def createID():
    tmp = string.digits + string.ascii_letters
    return ''.join(random.choice(tmp) for i in range(10))

def checkIfOrderExists(orderID, returnOrder = False):
    if (returnOrder):
        return next((item for item in fakeDataBaseOrders if item['orderID'] == orderID), None)
    
    return any(item["orderID"] == orderID for item in fakeDataBaseOrders)

def checkIfOrderPaid(orderID):
    return next((item['status'] == "paid" for item in fakeDataBaseOrders if item['orderID'] == orderID),False)  
    
#---------------------ROOT
@app.get("/")
def read_root():
    return {"CENTRAL": "SERVER"}
#-------------------------------------------------------------------------


# -------------------GET [ REQUEST ]  
# LOCKER STATUS BY IP 
@app.get("/display-locker")
async def check_locker_status():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LOCKER_SERVER}/status")
        return {"locker_status": response.json()}
    
# ----------------------------------------------------------------------------

#-------------------- POST [ RESPONSE ] 2
# [ Locker Battery, TimeStamp]  --- can change later #####


@app.post("/locker-update")
async def receive_locker_update(data: dict):
    print("SUCCESS: ", data, " received")
    
    lockerExists = False
    
    for i, item in enumerate(fakeDataBaseLockers):
        if item['ip'] == data['ip']:
            fakeDataBaseLockers[i] = data
            lockerExists = True
        
    if not lockerExists:
        fakeDataBaseLockers.append(data)
        
        
    
    return({
        "status" : data["battery"],
        "time" : time.strftime("%H %M")
        })
# ------------------UPDATE REGISTRY AND HEALTH STATUS OF LOCKER 
# UPDATE HAPPENS HERE

# ---------------------------------------------------------------

# PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE PURCHASE
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# POST [ RESPONSE ] 3
@app.post("/create-order")
async def createOrder(orderInfo: dict):
    print("CREATING ORDER...")
    global id
    
    try:
        id += 1
        
        productID = orderInfo["productID"]
        quantity = orderInfo["quantity"]
        lockerID = orderInfo["lockerID"]
        
        # Find product ID multiply it by the quantity
        fakeCost = 499
        fakeTotal = fakeCost * quantity
        
        # Generate Random ID
        chars = string.ascii_letters
        
        numbersLetters = string.ascii_letters + string.digits
        fakeID = "order-" + createID()
        print("ORDER ID: " + fakeID)
        
        tmpOrder = {
            "id" : id,
            "orderID" : fakeID,
            "productID" : productID,
            "quantity" : quantity,
            "totalCost" : fakeTotal,
            "lockerID" : lockerID,
            "status" : "pending"
        }
        
        fakeDataBaseOrders.append(tmpOrder)
        return {"status" : "success", "orderID" : fakeID}
        
    except Exception as e:
        print("SOMETHING WENT WRONG OOPSY")
        return {"status" : str(e)}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SHOW ALL ORDERS
@app.get("/display-orders")
async def displayOrders():
    return {
        "orders" : fakeDataBaseOrders
    }
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SHOW ALL COMPLETED ORDERS
@app.get("/display-completed-orders")
async def displayOrders():
    return {
        "orders" : fakeDataBaseCompletedOrders
    }


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- INITIATE PAYMENT
@app.post("/initiate-payment")
async def tryToPay(orderID : dict):
    try:
        orderIdString = orderID['orderID']

        
        if not checkIfOrderExists(orderIdString):
            return {"afterPayment" : "order does not exist"}
        
        #   ------------------------------------------------- PAYMENT PORTAL
        paymentSuccessful = True
        #    SIMULATING SUCCESS
        if paymentSuccessful:
            paymentID = "payment-"+createID()
            
            for order in fakeDataBaseOrders:
                if order['orderID'] == orderIdString:
                    order['status'] = "paid"
                return {
                    
                    "afterPayment" : "Payment Successful",
                    "pickupStatus" : "Order Ready for Pickup",
                    "paymentID" : paymentID
                }
        else:
            return {
                "afterPayment" : "Payment Unsuccessful"
            }
            
        
        
            
    except Exception as e:
        print(str(e))
        return {
            "ERROR" : str(e),
            "TRACE" : str(traceback.print_exc())
        }
        
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- REQUEST OPEN
@app.post("/request-open")
async def requestOpenDoor(orderAndLocation : dict):
    
    try:
        userLongitude = orderAndLocation['userLongitude']
        userLatitude = orderAndLocation['userLatitude']
        
        lockerLongitude = orderAndLocation['lockerLongitude']
        lockerLatitude = orderAndLocation['lockerLatitude']
        
        orderID = orderAndLocation['orderID']
        
        inProximity = False

        if (checkIfOrderExists(orderID)):       
            # "id" : id,
            # "orderID" : fakeID,
            # "productID" : productID,
            # "quantity" : quantity,
            # "totalCost" : fakeTotal,
            # "lockerID" : lockerID,
            # "status" : "pending"
            Order = checkIfOrderExists(orderID, True)
            
            # "id" : locker_id_info["id"],
            # "ip" : locker_id_info['ip'],
            # "status" : locker_status_info["status"],
            # "battery" : locker_status_info["battery"],
            lockerIp = next((item['ip'] for item in fakeDataBaseLockers if Order['lockerID'] == item['id']), None)
            
            if lockerIp == None:
                return{"IP ISSUE" : "IP of locker does not exist"}
            
            
            # Some sort of math that compares the gps locations 
            inProximity = True
            
            if (inProximity and checkIfOrderPaid(orderID)):
                # -----------------------------------------------# POST [REQUEST] 3
                #  -------------------------------------------- UNLOCK DOOR
                # USE CODE TO OPEN 
                async with httpx.AsyncClient() as client:
                    response = await client.get(lockerIp + "/open-locker")
                    print(response)
                    # maybe a check here to make sure the lock opened and
                    # the user took their package, maybe a confirmation from app
                    # for now, I will keep it simple
                    
                    
                    foundOrder = False
                    
                    for i, item in enumerate(fakeDataBaseOrders):
                        if item['orderID'] == orderID:
                            tmp = item
                            del fakeDataBaseOrders[i]
                            
                            tmp['status'] = "completed"
                            fakeDataBaseCompletedOrders.append(tmp)
                            break
                        
                    return{
                        "response" : response.json()
                    } 
                            
            else:
                print("Too far or Payment not found")
                return({"Unable To Open" : "Too far or Payment not found"})
        else:
            return({"Error" : "Order cannot be found"})

    except Exception as e:
        return{
            "Error" : str(e),
            "TRACE" : str(traceback.print_exc())

        }
        
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= VIEW DASHBOARD
        # [ GET ] RESPONSE
@app.get("/view-dashboard")
async def viewDashboardInformation():
    return {"dashboard" : fakeDataBaseLockers}

        # =--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= EMERGENCY OPEN
@app.post("/emergency-open")
async def emergencyOpen(ip : dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ip['lockerIp'] + "/open-locker")
            return(response.json())
    except Exception as e:
        return {"Error" : str(e)}
    
    
            
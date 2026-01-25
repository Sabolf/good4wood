from typing import Union
import httpx
from fastapi import FastAPI
import time
import random
import string

app = FastAPI()

# FAKE DATABASE OF ORDERS
fakeDataBase = []
id = 0
#------------------LOCKER SERVERS
LOCKER_SERVER = "http://127.0.0.1:8001"
# --------------------------------------------------------------------------
def createID():
    tmp = string.digits + string.ascii_letters
    return ''.join(random.choice(tmp) for i in range(10))
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
        lockerLoc = orderInfo["lockerLoc"]
        
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
            "lockerLoc" : lockerLoc,
            "status" : "pending"
        }
        
        fakeDataBase.append(tmpOrder)
        return {"status" : "success"}
        
    except Exception as e:
        print("SOMETHING WENT WRONG OOPSY")
        return {"status" : str(e)}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SHOW ALL ORDERS
@app.get("/display-orders")
async def displayOrders():
    return {
        "orders" : fakeDataBase
    }
    
@app.post("/initiate-payment")
async def tryToPay(orderID : dict):
    try:
        
        
        orderFound = any(item["orderID"] == orderID["orderID"] for item in fakeDataBase)
        if not orderFound:
            return {"afterPayment" : "order does not exist"}
        #   ------------------------------------------------- PAYMENT PORTAL
        paymentSuccessful = True
        #    SIMULATING SUCCESS
        if paymentSuccessful:
            paymentID = "payment-"+createID()
            for order in fakeDataBase:
                if order['orderID'] == orderID:
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
            
        
        
            
    except:
        print("FAIL")
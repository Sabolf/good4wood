from typing import Union
import httpx
from fastapi import FastAPI
import time
app = FastAPI()

# FAKE DATABASE OF ORDERS
fakeDataBase = []
id = 0
#------------------LOCKER SERVERS
LOCKER_SERVER = "http://127.0.0.1:8001"
# --------------------------------------------------------------------------

#---------------------ROOT
@app.get("/")
def read_root():
    return {"CENTRAL": "SERVER"}
#-------------------------------------------------------------------------


# -------------------GET [ REQUEST ]  1
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
        
        orderID = orderInfo["orderID"]
        productID = orderInfo["productID"]
        quantity = orderInfo["quantity"]
        totalCost = orderInfo["totalCost"]
        currency = orderInfo["currency"]
        lockerLoc = orderInfo["lockerLoc"]
        
        
        tmpOrder = {
            "id" : id,
            "orderID" : orderID,
            "productID" : productID,
            "quantity" : quantity,
            "totalCost" : totalCost,
            "currency" : currency,
            "lockerLoc" : lockerLoc,
            "status" : "pending"
        }
        
        fakeDataBase.append(tmpOrder)
        return {"status" : "success"}
        
    except Exception as e:
        print("SOMETHING WENT WRONG OOPSY")
        return {"status" : str(e)}

@app.get("/display-orders")
async def displayOrders():
    return {
        "orders" : fakeDataBase
    }
import httpx
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI()
# ----------------------------GENERAL INFO ABOUT LOCKER
locked = True

CENTRAL_SERVER_IP = "http://127.0.0.1:8000"

locker_id_info = {
    "name" : "Chicago01",
    "location" : "ChicagoAddress",
    "ip" : "http://127.0.0.1:8001",
    "id" : "1234"
}

locker_status_info = {
    "status" : "on",
    "battery" : "77%",
    "signal-strength" : "50dBm",
    "locked" : locked
}

# ---------------------------------------------------------------------------------

#--------------------------------POST [ REQUEST ] 2
# [UPDATING GENERAL INFO OF LOCKER TO CENTRAL SERVER]
async def send_update():
    while True:
        try:
    #on/off /temp/ humidity/ 
            update_json = {
                "id" : locker_id_info["id"],
                "ip" : locker_id_info['ip'],
                "status" : locker_status_info["status"],
                "battery" : locker_status_info["battery"],
            }
    
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{CENTRAL_SERVER_IP}/locker-update", json=update_json, timeout=10
                )
                
                # return response.json()
                print(response.json())
        except Exception as e:
            print(str(CENTRAL_SERVER_IP + " " + str(e)))
            
        await asyncio.sleep(30)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- open-locker
# ----------------------- POST [ RESPONSE ] 3




    # -------------------------------------LOOP TASK FOR SENDING UPDATES TO CENTRAL 
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Start UP background task
    task = asyncio.create_task(send_update())
    yield
    #Shut DOWN
    task.cancel()
# ---------------------------------------------------------------------------------------------


app = FastAPI(lifespan=lifespan)
    

# -------------------------ROOT
@app.get("/")
def read_root():
    return {"LOCKER": "SERVER"}
# ------------------------------------------------

#---------------------------GET [ RESPONSE ]   1
@app.get("/status")
async def locker_status():
    return {"TEST STATUS" : "OFF"}
# -------------------------------------------------------------

# --------------------------GET [ RESPONSE ] 3   
@app.get("/open-locker")
async def openLockerDoor():
    global locked
    
    print("Opening door...")
    
    if not locked:
        return{
            "lockerDoor" : "already open"
        }
    locked = False
    print("Lock Disengaged...")
    return {
        "locked" : locked
    }
    
# --------------------------get [SELF CHANGE] 4
@app.get("/close-locker")
async def openLockerDoor():
    global locked
    
    print("Door was closed successfully")
    
    
    locked = True
    print("Lock Engaged...")
    return {
        "locked" : locked
    }
    
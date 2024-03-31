from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import SQLdb as db
import simplejson as json

app = FastAPI()

origins = [
    "http://localhost:63342" #TODO: change this number as per the port number used then.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/adminPass")
async def getAdminPass(adminID : str):
    print(adminID)
    adminId = int(adminID)
    res = db.getAdminPassword(adminId)
    print(res)
    return res
@app.get("/addToCart")
async def addToCart(customerID : int, productID : int, price, quantity : int):
    print(customerID, productID, price, quantity)
    res = db.addProductToCart(customerID, productID, price, quantity)
    print(res)
    return res


@app.get("/customerPass")
async def getAdminPass(customerID : str):
    print(customerID)
    customerId = int(customerID)
    res = db.getCustomerPassword(customerId)
    print(res)
    return res

@app.get("/customerCart")
async def getCustomerCart(customerID : str):
    res = db.getCustomerCart(customerID)
    print(res)
    return res
@app.get("/allProducts")
async def getAllProducts():
    res = db.getAllProducts()
    print(res)
    return res


@app.get("/itemsByCriteria")
async def getItemsByCriteria(criteria: str):
    print(criteria)
    res = db.getItemsInOrder(criteria)
    print(res)
    return res

@app.get("/priceOfProduct")
async def getPriceOfProduct(productID : str):
    print(productID)
    res = db.getPriceOfProduct(productID)
    return res

@app.get("/mostLeastBought")
async def getMostLeastBought(order: str):
    res = db.ExtremumBought(order)
    print(res)
    return res

# @app.get("/addToCart")
# async def addToCart(product : int, cutsomer: int):

@app.get("/checkout")
async def checkout(customerID : str):
    # clearCart =  db.clearCart(customerID)
    print("ye toh ho gaya /////////////////////////////////////////////////////////")
    res = db.checkout(customerID)
    print(res)
    print("ye bhi ")
    hehe = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
    return hehe

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

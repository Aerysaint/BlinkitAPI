import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="shawarma",
    password="123456789!",
    database="deadline4"
)

mycursor = mydb.cursor()


def execSQL(query: str):
    mycursor.execute(query)
    result = mycursor.fetchall()

    return result

def execUpdates(query: str):
    mycursor.execute(query)
    mydb.commit()
    result = mycursor.fetchall()

    return result

def getAdminPassword(adminID: int):
    query = f"""SELECT Password
  FROM Admin
  WHERE Admin.Login_ID= {adminID}"""
    result = execSQL(query)
    # print(type(result))
    return result


def getCustomerPassword(customerID: int):
    query = f"""SELECT Password
   FROM Customer
   WHERE Customer.Customer_ID= {customerID}"""
    result = execSQL(query)
    # print(type(result))
    return result


def getAllProducts():
    query = """SELECT * 
  FROM deadline4.product;"""
    result = execSQL(query)
    return result


def getItemsInOrder(criteria: str):
    cr = criteria
    query = f"""SELECT *
  FROM deadline4.Product
  order by {cr}; """
    result = execSQL(query)
    # print(type(result))
    return result


def ExtremumBought(order: str):
    query = f""" SELECT P.*, COUNT(OH.Product_ID) AS Num_of_Purchases
FROM Product P
LEFT JOIN Order_History OH ON P.Product_ID = OH.Product_ID
GROUP BY P.Product_ID
ORDER BY Num_of_Purchases {order};
  """
    result = execSQL(query)
    print(result)
    return result


def getCustomerCart(customerID: str):
    query = f"""SELECT
    Product.Product_ID,
    Product.Product_Name,
    Product.Brand,
    Product.Price,
    Product_in_Cart.Quantity
FROM
    Product
JOIN
    Product_in_Cart ON Product.Product_ID = Product_in_Cart.Product_ID
WHERE
    Product_in_Cart.Customer_ID = {customerID};
"""
    result = execSQL(query)
    print(result)
    return result


def addProductToCart(customerID: int, productID: int, price, quantity: int):
    query = f"""
INSERT INTO Product_in_Cart (Customer_ID, Product_ID, Price, Quantity)
VALUES
({customerID}, {productID}, {price}, {quantity});

"""
    result = execUpdates(query)
    print(result)
    return result


def getTotalPrice(customerID: int):
    query = f"""SET @total_price := (SELECT SUM(`Price` * `Quantity`) FROM `Product_in_Cart` WHERE `Customer_ID` = {customerID});"""
    result = execSQL(query)
    print(result)
    return result


def prepareOrder():
    query = f"""INSERT INTO `Order` (`Price`, `Order_Date`, `Payment_Type`)
VALUES
(@total_price, CURRENT_DATE(), 'Cod');

SET @order_id := LAST_INSERT_ID();"""
    result = execUpdates(query)
    print(result)
    return result


def getPriceOfProduct(productID: str):
    query = f"""SELECT Price
  FROM Product
  WHERE Product_ID = {productID};"""
    result = execSQL(query)
    print(result)
    return result


def putInHistory(customerID: int):
    query = f"""INSERT INTO `Order_History` (`Customer_ID`, `Product_ID`, `Price`, `Date_of_Purchase`)
SELECT
    {customerID},
    `Product_ID`,
    (SELECT SUM(Price * Quantity) FROM Product_in_Cart WHERE Customer_ID = {customerID}),
    CURRENT_DATE()
FROM
    `Product_in_Cart`
WHERE
    `Customer_ID` = {customerID};
"""
    result = execUpdates(query)
    print(result)
    return result

def getCartPrice(customerID: int):
    query = f"""SELECT SUM(Price * Quantity) FROM Product_in_Cart WHERE Customer_ID = {customerID};"""
    result = execSQL(query)
    print(result)
    return result[0][0]

def insertOrder(price, orderType):
    query = f"""INSERT INTO `Order` (`Price`, `Order_Date`, `Payment_Type`)
VALUES ('{price}', CURRENT_DATE(), '{orderType}');
"""
    result = execUpdates(query)
def getOrderId():
    query = """SELECT LAST_INSERT_ID();"""
    result = execSQL(query)
    return result[0][0]

def clearCart(customerID: str):
    print("I'm here")
    query = f"""DELETE FROM product_in_cart WHERE Customer_ID = {customerID};
"""
    result = execUpdates(query)
    print(result)
    return result


async def checkout(customerID: str):
    print(customerID)
    print("hello")
    price = await getCartPrice(customerID)
    await insertOrder(price, "CoD")
    print("here1")
    orderID = await getOrderId()
    print("here2")
    await clearCart(customerID)
    print("doen")
    # putInHistory(customerID)
    query = f"""
-- Step 3: Inserting into Customer_Order table to link customer with the order
INSERT INTO `Customer_Order` (`Customer_ID`, `Order_ID`)
VALUES
    ({customerID}, {orderID});

-- Step 4: Assigning a delivery agent to the order (Assuming random assignment)
SET @RandomAgentID := (SELECT Agent_ID FROM Delivery_Agent ORDER BY RAND() LIMIT 1);

-- Step 5: Inserting into Order_Delivery table to link order with delivery agent
INSERT INTO `Order_Delivery` (`Agent_ID`, `Order_ID`)
VALUES
    (@RandomAgentID, @OrderID);
  DELETE FROM product_in_cart WHERE Customer_ID = {customerID};"""
    result = execUpdates(query)
    print(result)
    # clearCart(customerID)
    return result




# def testing():
#   query = """INSERT INTO Product(Product_ID, Product_Name, Brand, Price, Quantity, Expiry_Date)
# Values
# (2, 'Product2', 'BrandB', 29.99, 50, '2024-11-30');"""
#   execSQL(query)
#
# testing()
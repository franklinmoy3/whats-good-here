"""Defines all the functions related to the database"""
from app import db

# TODO: CREATE TRIGGER THAT DETECTS IF NEW RATING IS FROM THE SAME USER

def fetch_queried_restaurants_2() -> dict:
    """Performs advanced query 2

    Returns:
        A list of dictionaries
    """
    query_string = "SELECT DishName, AvgRating FROM (SELECT DishName, AvgRating, DishID FROM Restaurants NATURAL JOIN Dishes WHERE RestaurantID = 1 GROUP BY DishID HAVING AvgRating >= 4) AS Alias ORDER BY AvgRating DESC LIMIT 0, 15;"
    conn = db.connect()
    query_results = conn.execute(query_string).fetchall()
    conn.close()
    dish_list = []
    for result in query_results:
        item = {
            "DishName": result[0],
            "AvgRating": result[1]
        }
        dish_list.append(item)
    return dish_list

def fetch_queried_restaurants_1() -> dict:
    """Performs advanced query 1

    Returns:
        A list of dictionaries
    """
    query_string = "SELECT Max(AvgRating) AS MaxRating, RestaurantName FROM Dishes NATURAL JOIN Restaurants GROUP BY RestaurantID ORDER BY MaxRating DESC;"
    conn = db.connect()
    query_results = conn.execute(query_string).fetchall()
    conn.close()
    restaurant_list = []
    for result in query_results:
        item = {
            "MaxRating": result[0],
            "RestaurantName": result[1]
        }
        restaurant_list.append(item)

    return restaurant_list

def fetch_restaurants() -> dict:
    """Reads all restaurants listed in the Restaurants table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Restaurants;").fetchall()
    conn.close()
    restaurant_list = []
    for result in query_results:
        item = {
            "RestaurantID": result[0],
            "RestaurantName": result[1],
            "ZipCode": result[2],
            "Address": result[3]
        }
        restaurant_list.append(item)

    return restaurant_list

def fetch_restaurant_info(restaurant_id: int) -> dict:
    """Searches database for restaurants with the desired name
    
    Args:
        restaurant_id (int): Targeted RestaurantID

    Returns:
        List of dictionaries
    """
    conn = db.connect()
    query = f"SELECT * FROM Restaurants WHERE RestaurantID = {restaurant_id};"
    query_results = conn.execute(query).fetchall()
    conn.close()
    restaurant_list = []
    for result in query_results:
        item = {
            "RestaurantID": result[0],
            "RestaurantName": result[1],
            "ZipCode": result[2],
            "Address": result[3]
        }
        restaurant_list.append(item)

    return restaurant_list

def search_restaurants_by_name(search_query: str) -> dict:
    """Searches database for restaurants with the desired name
    
    Args:
        search_query (str): Name of restaurant to search

    Returns:
        List of dictionaries
    """
    conn = db.connect()
    query = f"SELECT * FROM Restaurants WHERE RestaurantName LIKE \'%%{search_query}%%\';"
    query_results = conn.execute(query).fetchall()
    conn.close()
    restaurant_list = []
    for result in query_results:
        item = {
            "RestaurantID": result[0],
            "RestaurantName": result[1],
            "ZipCode": result[2],
            "Address": result[3]
        }
        restaurant_list.append(item)

    return restaurant_list

def insert_new_restaurant(restaurant_name: str, zip_code: int, address: str) -> None:
    """Insert new restaurant into Restaurants table
    
    Args:
        restaurant_name (str): Name of restaurant
        zip_code (int): Zip code of restaurant
        Address (str): Price of new dish

    Returns: 
        None
    """

    conn = db.connect()
    query = "INSERT INTO Restaurants (RestaurantName, ZipCode, Address) VALUES (\'{}\', {}, \'{}\');".format(restaurant_name, zip_code, address)
    conn.execute(query)
    conn.close()

def update_restaurant_entry(restaurant_id: int, restaurant_name: str, zip_code: int, address: str) -> None:
    """Updates restaurant entry based on given RestaurantID

    Args:
        restaurant_id (int): Targeted RestaurantID
        restaurant_name (str): Updated name of restaurant (can be the same as the prior value)
        zip_code (int): Updated ZipCode of restaurant (can be the same as the prior value)
        address (str): Updated Address of restaurant (can be the same as the prior value)

    Returns:
        None
    """

    conn = db.connect()
    query = "UPDATE Restaurants SET RestaurantName = \'{}\', ZipCode = {}, Address = \'{}\' WHERE RestaurantID = {};".format(restaurant_name, zip_code, address, restaurant_id)
    conn.execute(query)
    conn.close()

def remove_restaurant_by_id(restaurant_id: int) -> None:
    """ Remove restaurant based on RestaurantID 
    
    Args:
        restaurant_id (int): Targeted RestaurantID
    
    Returns:
        None
    """
    conn = db.connect()
    query = "DELETE FROM Restaurants WHERE RestaurantID = {};".format(restaurant_id)
    conn.execute(query)
    conn.close()

def fetch_dishes(restaurant_id: int) -> dict:
    """ Reads all dish items for the input restaurant_id

    Args:
        restaurant_id (int): Targeted RestaurantID

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query = "SELECT * FROM Dishes WHERE RestaurantID = {};".format(restaurant_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    dish_list = []
    for result in query_results:
        item = {
            "DishID": result[0],
            "RestaurantID": result[1],
            "DishName": result[2],
            "Price": result[3],
            "AvgRating": result[4],
            "MedRating": result[5],
            "BestRating": result[6]
        }
        dish_list.append(item)

    return dish_list

def insert_new_dish(restaurant_id: int, dish_name: str, price: float) -> None:
    """Insert new dish into Dishes table for the given RestaurantID.
    
    Args:
        restaurant_id (int): Target RestaurantID
        dish_name (str): Name of new dish
        price (float): Price of new dish

    Returns: 
        None
    """

    conn = db.connect()
    query = "INSERT INTO Dishes (DishID, RestaurantID, DishName, Price, AvgRating) VALUES (1, {}, \'{}\', {}, 0);".format(restaurant_id, dish_name, price)
    conn.execute(query)
    conn.close()

def update_dish_entry(dish_id: int, restaurant_id: int, dish_name: str, price: float) -> None:
    """Updates dish entry based on given dish_id

    Args:
        dish_id (int): Targeted DishID
        restaurant_id (int): Targeted RestaurantID
        dish_name (str): Updated name of dish (can be the same as the prior value)
        price (float): Updated price of dish (can be the same as the prior value)

    Returns:
        None
    """

    conn = db.connect()
    query = "UPDATE Dishes SET DishName = \'{}\', Price = {} WHERE DishID = {} AND RestaurantID = {};".format(dish_name, price, dish_id, restaurant_id)
    conn.execute(query)
    conn.close()

def remove_dish_by_id(dish_id: int, restaurant_id: int) -> None:
    """ Remove entries based on DishID 
    
    Args:
        dish_id (int): Targeted DishID
        restaurant_id (int): Targeted RestaurantID
    
    Returns:
        None
    """
    conn = db.connect()
    query = "DELETE FROM Dishes WHERE DishID = {} AND RestaurantID = {};".format(dish_id, restaurant_id)
    conn.execute(query)
    conn.close()

def fetch_ratings(restaurant_id: int, dish_id: int) -> dict:
    """ Reads all rating items for the input restaurant_id and dish_id

    Args:
        restaurant_id (int): Targeted RestaurantID
        dish_id (int): Targeted DishID

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query = "SELECT * FROM Ratings WHERE RestaurantID = {} AND DishID = {};".format(restaurant_id, dish_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    rating_list = []
    for result in query_results:
        item = {
            "RatingID": result[0],
            "UserRating": result[1],
            "DishID": result[2],
            "UserID": result[3],
            "RestaurantID": result[4]
        }
        rating_list.append(item)

    return rating_list

def insert_new_rating(restaurant_id: int, dish_id: int, rating: float, user_id: int) -> None:
    """Insert new dish into Dishes table for the given RestaurantID.
    
    NOTE: SQLAlchemy requires a raw connection and a cursor object to call a stored procedure.
          Remember that raw connections are transactions that need committing.

    Args:
        restaurant_id (int): Target RestaurantID
        dish_id (int): Target DishID
        rating (float): User's rating of dish out of 5
        user_id (int): UserID of user who left this rating

    Returns: 
        None
    """

    conn = db.connect()
    # Check if the user has already rated the dish at this restaurant 
    query = f"SELECT RatingID FROM Ratings WHERE RestaurantID = {restaurant_id} AND DishID = {dish_id} AND UserID = {user_id}"
    query_results = conn.execute(query).fetchall()
    # Insert into the table only if the user hasn't, update existing rating otherwise
    if len(query_results) == 0:
        query = "INSERT INTO Ratings (RatingID, UserRating, DishID, UserID, RestaurantID) VALUES (1, {}, {}, {}, {});".format(rating, dish_id, user_id, restaurant_id)
    else:
        target_rID = query_results[0][0]
        query = f"UPDATE Ratings SET UserRating = {rating} WHERE RatingID = {target_rID} AND RestaurantID = {restaurant_id} AND DishID = {dish_id} AND UserID = {user_id}"
    conn.execute(query)
    conn.close()
    conn = db.raw_connection()
    cursor_obj = conn.cursor()
    cursor_obj.callproc("RatingsUpdateProc", [restaurant_id, dish_id, user_id])
    conn.commit()
    cursor_obj.close()
    conn.close()

def update_rating_entry(rating_id: int, dish_id: int, restaurant_id: int, rating: float) -> None:
    """Updates dish entry based on given dish_id

    Args:
        rating_id (int): Targeted RatingID
        dish_id (int): Targeted DishID
        restaurant_id (int): Targeted RestaurantID
        rating (float): Updated rating (can be the same as the prior value, for now)

    Returns:
        None
    """

    conn = db.connect()
    query = "UPDATE Ratings SET UserRating = {} WHERE DishID = {} AND RestaurantID = {} AND RatingID = {};".format(rating, dish_id, restaurant_id, rating_id)
    conn.execute(query)
    conn.close()

def remove_rating_by_id(rating_id: int, dish_id: int, restaurant_id: int) -> None:
    """ Remove entries based on RatingID 
    
    Args:
        rating_id (int): Targeted RatingID
        dish_id (int): Targeted DishID
        restaurant_id (int): Targeted RestaurantID
    
    Returns:
        None
    """
    conn = db.connect()
    query = "DELETE FROM Ratings WHERE RatingID = {} AND DishID = {} AND RestaurantID = {};".format(rating_id, dish_id, restaurant_id)
    conn.execute(query)
    conn.close()

def insert_new_user(user_name: str) -> None:
    """Insert new user into Users table.
    
    Args:
        user_name (str): Name of new user
        
    Returns: 
        None
    """

    conn = db.connect()
    query = "INSERT INTO Users (UserName, NumRatings) VALUES (\'{}\', 0);".format(user_name)
    conn.execute(query)
    conn.close()

def fetch_users() -> dict:
    """Fetches all of the Users in the Users table

    Args:
        None
    
    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query = "SELECT * FROM Users;"
    query_results = conn.execute(query).fetchall()
    conn.close()
    user_list = []
    for result in query_results:
        item = {
            "UserID": result[0],
            "UserName": result[1],
            "NumRatings": result[2],
        }
        user_list.append(item)

    return user_list

def update_user_entry(user_id: int, user_name: str) -> None:
    """Updates user entry based on given user_id

    Args:
        user_id (int): Targeted UserID
        user_name (str): Updated UserName

    Returns:
        None
    """

    conn = db.connect()
    query = "UPDATE Users SET UserName = \'{}\' WHERE UserID = {};".format(user_name, user_id)
    conn.execute(query)
    conn.close()

def remove_user_by_id(user_id: int) -> None:
    """ Remove user based on UserID 
    
    Args:
        user_id (int): Targeted UserID
    
    Returns:
        None
    """
    conn = db.connect()
    query = "DELETE FROM Users WHERE UserID = {};".format(user_id)
    conn.execute(query)
    conn.close()

def check_password(attempt: str, user_id: int) -> bool:
    """Check the UserID and password used for addition, editing, and removal"""
    if attempt != "CHANGETHISTOWHATEVERYOUWANT":
        return False
    conn = db.connect()
    query = f"SELECT UserName FROM Users WHERE UserID = {user_id};"
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return False
    return True

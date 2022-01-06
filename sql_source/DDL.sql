CREATE TABLE Users (
        UserID INT NOT NULL AUTO_INCREMENT,
        UserName VARCHAR(25) NOT NULL,
        NumRatings INT NOT NULL DEFAULT 0,
        PRIMARY KEY(UserID)
);
 
CREATE TABLE Cities (
        ZipCode INT NOT NULL,
        CityName VARCHAR(100) NOT NULL,
        PRIMARY KEY(ZipCode)
);
 
CREATE TABLE Visited (
        ZipCode INT NOT NULL,
        UserID INT NOT NULL,
        PRIMARY KEY(ZipCode, UserID),
        FOREIGN KEY (ZipCode) REFERENCES Cities(ZipCode)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
 
CREATE TABLE Restaurants(
        RestaurantID INT NOT NULL AUTO_INCREMENT,
        RestaurantName VARCHAR(75) NOT NULL,
        ZipCode INT NOT NULL,
        Address VARCHAR(100) NOT NULL,
        PRIMARY KEY (RestaurantID)
);
 
CREATE TABLE Dishes (
        DishID INT NOT NULL,
        RestaurantID INT NOT NULL,
        DishName VARCHAR(75) NOT NULL,
        Price DECIMAL(10, 2) NOT NULL,
        AvgRating DECIMAL(10,1) DEFAULT 0.0,
        MedRating DECIMAL(10,1) DEFAULT 0.0,
        BestRating DECIMAL(10,1) DEFAULT 0.0,
        PRIMARY KEY(DishID, RestaurantID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
 
CREATE TABLE Ratings (
        RatingID INT NOT NULL,
        UserRating DECIMAL(10,1) NOT NULL,
        DishID INT NOT NULL,
        UserID INT NOT NULL,
        RestaurantID INT NOT NULL,
        PRIMARY KEY (RatingID, DishID, RestaurantID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY (DishID, RestaurantID) REFERENCES Dishes(DishID, RestaurantID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX DishIndex ON Dishes(DishID);
CREATE INDEX RatingsIndex ON Ratings(DishID);

DELIMITER $$
# Custom AUTO_INCREMENT behavior for DishID as InnoDB has undesired behavior on AUTO_INCREMENT for composite keys
DROP TRIGGER IF EXISTS DishAutoIncrement$$
CREATE TRIGGER DishAutoIncrement BEFORE INSERT ON Dishes
FOR EACH ROW
BEGIN
	SET new.DishID = (SELECT IFNULL(MAX(DishID), 0) + 1
						FROM Dishes
                        WHERE RestaurantID = new.RestaurantID);
END$$

# Custom AUTO_INCREMENT behavior for RatingID as InnoDB has undesired behavior on AUTO_INCREMENT for composite keys
DROP TRIGGER IF EXISTS RatingAutoIncrement$$
CREATE TRIGGER RatingAutoIncrement BEFORE INSERT ON Ratings
FOR EACH ROW
BEGIN
	SET new.RatingID = (SELECT IFNULL(MAX(RatingID), 0) + 1
						FROM Ratings
                        WHERE RestaurantID = new.RestaurantID AND DishID = new.DishID);
END$$
DELIMITER ;
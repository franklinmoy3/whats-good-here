/* Checks for a UserID's existing rating for a dish and adjusts the count for how many unique dishes that user has rated. */
DELIMITER $$
DROP TRIGGER IF EXISTS CheckExistingRating$$
CREATE TRIGGER CheckExistingRating 
	BEFORE INSERT ON Ratings
	FOR EACH ROW
BEGIN
	SET @prevNumRatings = (SELECT NumRatings FROM Users WHERE UserID = new.UserID);
    SET @newNumRatings = (SELECT COUNT(RatingID) FROM Ratings WHERE UserID = new.UserID);
    IF @prevNumRatings != @newNumRatings THEN
        UPDATE Users SET NumRatings = @newNumRatings WHERE UserID = new.UserID;
	END IF;
END$$

/* Updates the statistics of dishes */
DROP PROCEDURE IF EXISTS RatingsUpdateProc$$
CREATE PROCEDURE RatingsUpdateProc(IN restaurant_id INT, IN dish_id INT, IN user_id INT)
BEGIN
	DECLARE dID INT;
    DECLARE count_ratingID INT;
    DECLARE avg_rating DECIMAL;
    DECLARE currIndex INT DEFAULT 0;
    DECLARE currRating DECIMAL(10,1);
    DECLARE medianRating DECIMAL(10,1) DEFAULT 0.0;
    DECLARE done INT DEFAULT 0;
    DECLARE cur1 CURSOR FOR SELECT DishID, COUNT(RatingID), AVG(UserRating) FROM Ratings WHERE RestaurantID = restaurant_id GROUP BY DishID;
    DECLARE cur2 CURSOR FOR SELECT UserRating FROM Dishes NATURAL JOIN Ratings WHERE DishID = dish_id AND RestaurantID = restaurant_id ORDER BY UserRating;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    # First AQ - Recalculate the BestRatings (Using modified MAL Rating formula) for dishes at this restaurant
	OPEN cur1;
	SET @restaurant_rating_avg = (SELECT AVG(AverageRating) FROM (SELECT RestaurantID, AVG(UserRating) AS AverageRating FROM Ratings NATURAL JOIN Dishes GROUP BY DishID, RestaurantID) AS alias WHERE RestaurantID = restaurant_id);
    REPEAT
		FETCH cur1 INTO dID, count_ratingID, avg_rating;
        SET @best_rating = ((count_ratingID * avg_rating + @restaurant_rating_avg * 1) / (count_ratingID + 1));
        IF @best_rating > 5.0 THEN
			SET @best_rating = 5.0;
		END IF;
		UPDATE Dishes SET BestRating = @best_rating WHERE RestaurantID = restaurant_id AND DishID = dID;
    UNTIL done
    END REPEAT;
	CLOSE cur1;
    SET done = 0;
    
    # Second AQ - Update the median rating for the dish that was just rated using cursor cur2
	SET @numRatings = (SELECT ratingCount FROM (SELECT COUNT(RatingID) AS ratingCount, DishID, RestaurantID FROM Dishes NATURAL JOIN Ratings GROUP BY DishID, RestaurantID) AS alias WHERE DishID = dish_id AND RestaurantID = restaurant_id);
    OPEN cur2;
    REPEAT
		FETCH cur2 INTO currRating;
        IF currIndex = FLOOR(@numRatings / 2) THEN
			SET medianRating = currRating;
            SET done = 1;
        END IF;
        SET currIndex = currIndex + 1;
    UNTIL done
    END REPEAT;
	CLOSE cur2;
    UPDATE Dishes SET MedRating = medianRating WHERE DishID = dish_id AND RestaurantID = restaurant_id;

	# Third AQ - Update AvgRating for the dish that was just rated
    SET @new_avg = (SELECT AVG(UserRating) FROM Dishes NATURAL JOIN Ratings WHERE DishID = dish_id AND RestaurantID = restaurant_id GROUP BY RestaurantID, DishID);
	UPDATE Dishes SET AvgRating = @new_avg WHERE DishID = dish_id AND RestaurantID = restaurant_id;
END$$

/* Update the number of reviews for each critic */ 
DROP PROCEDURE IF EXISTS ForceUpdateNumRatings$$
CREATE PROCEDURE ForceUpdateNumRatings()
BEGIN
	DECLARE cnt INT;
    DECLARE uid INT;
    DECLARE done INT DEFAULT 0;
	DECLARE cur1 CURSOR FOR SELECT UserID, COUNT(RatingID) FROM Ratings GROUP BY UserID;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN cur1;
	REPEAT
		FETCH cur1 INTO uid, cnt;
        UPDATE Users SET NumRatings = cnt WHERE UserID = uid;
    UNTIL done
    END REPEAT;
    CLOSE cur1;
END$$

/* Update the dish stats for all dishes */
DROP PROCEDURE IF EXISTS ForceUpdateDishStats$$
CREATE PROCEDURE ForceUpdateDishStats()
BEGIN
	DECLARE restaurant_id INT;
    DECLARE done1 INT DEFAULT 0;
	DECLARE done2 INT DEFAULT 0;
    DECLARE cur1 CURSOR FOR SELECT RestaurantID FROM Restaurants;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done1 = 1;
    OPEN cur1;
        REPEAT
			FETCH cur1 INTO restaurant_id;
			SET @dish_id = 1;
            SET @dish_count = (SELECT COUNT(DishID) FROM Dishes WHERE RestaurantID = restaurant_id);
            SET done2 = 0;
            REPEAT
				CALL RatingsUpdateProc(restaurant_id,@dish_id,1);
                SET @dish_id = @dish_id + 1;
                IF @dish_id > @dish_count THEN
					SET done2 = 1;
				END IF;
            UNTIL done2
            END REPEAT;
        UNTIL done1
        END REPEAT;
    CLOSE cur1;
END$$
DELIMITER ;

/* Duplicate Ratings Checker Script */
SELECT UserID, RestaurantID, DishID, RatingID, COUNT(*) as cnt
FROM Ratings
GROUP BY UserID, RestaurantID, DishID, RatingID
HAVING cnt > 1;
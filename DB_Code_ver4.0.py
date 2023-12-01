import pymysql
import uuid
import datetime

def connect_db():
    return pymysql.connect(host='192.168.56.101', port=3308, user='root', passwd='1234', db='RestaurantDB', charset='utf8')

def login():
    # 데이터베이스 연결
    db = connect_db()
    cursor = db.cursor()

    # 사용자에게 ID와 비밀번호 입력 받기
    user_id = input("Enter your ID: ")
    password = input("Enter your password: ")

    # 데이터베이스에서 사용자 검증
    sql = "SELECT * FROM User WHERE UserID = %s AND Password = %s"
    cursor.execute(sql, (user_id, password))
    result = cursor.fetchone()

    # 로그인 성공 또는 실패 메시지 출력
    if result:
        print("로그인이 성공했습니다.")
        return True, user_id  # 로그인 성공과 함께 사용자 ID 반환
    else:
        print("ID 또는 비밀번호가 잘못되었습니다.")
        return False, None  # 로그인 실패

    db.close()

def sign_up():
    # 데이터베이스 연결
    db = connect_db()
    cursor = db.cursor()

    # 사용자 정보 입력 받기
    user_id = input("Enter your new ID: ")
    password = input("Enter your password: ")
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    address = input("Enter your address: ")
    phone_number = input("Enter your phone number: ")
    email_address = input("Enter your email address: ")

    # 데이터베이스에 사용자 정보 추가
    sql = """
    INSERT INTO User (UserID, Password, Name, Age, Address, PhoneNumber, EmailAddress) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (user_id, password, name, age, address, phone_number, email_address))
        db.commit()
        print("회원가입이 완료되었습니다.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()

def view_my_page(user_id):
    # 데이터베이스 연결
    db = connect_db()
    cursor = db.cursor()

    try:
        # 로그인한 사용자의 정보 출력
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        user_info = cursor.fetchone()
        if user_info:
            print("\nUser Information:")
            print(f"ID: {user_info[0]}, Name: {user_info[2]}, Age: {user_info[3]}, Address: {user_info[4]}, Phone: {user_info[5]}, Email: {user_info[6]}")
        else:
            print("\nUser Information: No data available.")

        # 사용자가 등록한 식당 정보 출력
        cursor.execute("SELECT * FROM Restaurant WHERE UserID = %s", (user_id,))
        restaurants = cursor.fetchall()
        if restaurants:
            print("\nRegistered Restaurants:")
            for rest in restaurants:
                print(f"ID: {rest[0]}, Name: {rest[1]}, Address: {rest[2]}, Category: {rest[3]}, Rating: {rest[4]}")
        else:
            print("\nRegistered Restaurants: No data available.")

        # 사용자가 작성한 리뷰 출력
        cursor.execute("SELECT * FROM Review WHERE UserID = %s", (user_id,))
        reviews = cursor.fetchall()
        if reviews:
            print("\nWritten Reviews:")
            for review in reviews:
                print(f"ID: {review[0]}, Title: {review[1]}, Content: {review[2]}, Date: {review[3]}, Rating: {review[4]}")
        else:
            print("\nWritten Reviews: No data available.")

        # 사용자가 작성한 코멘트 출력
        cursor.execute("SELECT * FROM Comment WHERE UserID = %s", (user_id,))
        comments = cursor.fetchall()
        if comments:
            print("\nWritten Comments:")
            for comment in comments:
                print(f"ID: {comment[0]}, Content: {comment[1]}, Date: {comment[2]}, Like/Dislike: {comment[3]}")
        else:
            print("\nWritten Comments: No data available.")

        # 사용자의 즐겨찾기 정보 출력
        cursor.execute("SELECT * FROM Favorite WHERE UserID = %s", (user_id,))
        favorites = cursor.fetchall()
        if favorites:
            print("\nFavorite Restaurants:")
            for favorite in favorites:
                print(f"ID: {favorite[0]}, Restaurant ID: {favorite[2]}")
        else:
            print("\nFavorite Restaurants: No data available.")

    except Exception as e:
        print(f"Error: {e}")

    db.close()

def view_restaurants():
    # 데이터베이스 연결
    db = connect_db()
    cursor = db.cursor()

    try:
        # 모든 식당 정보 조회
        sql = "SELECT * FROM Restaurant"
        cursor.execute(sql)
        restaurants = cursor.fetchall()

        if restaurants:
            print("\nRestaurant List:")
            for rest in restaurants:
                print(f"ID: {rest[0]}, Name: {rest[1]}, Address: {rest[2]}, Category: {rest[3]}, Rating: {rest[4]}")
        else:
            print("\nNo restaurants found in the system.")

    except Exception as e:
        print(f"Error: {e}")

    db.close()

def search_restaurants(user_id):
    # 데이터베이스 연결
    db = connect_db()
    cursor = db.cursor()

    # 검색 조건 입력 받기
    name = input("Enter restaurant name (or leave blank): ")
    location = input("Enter location (or leave blank): ")
    category = input("Enter category (or leave blank): ")
    rating = input("Enter minimum rating (or leave blank): ")

    # 정렬 기준 선택
    print("Choose sorting criteria:")
    print("1. Rating")
    print("2. Number of Reviews")
    sort_choice = input("Enter your choice (1 or 2): ")

    # 검색 쿼리 구성
    sql = "SELECT * FROM Restaurant WHERE "
    conditions = []
    params = []

    if name:
        conditions.append("Name LIKE %s")
        params.append(f"%{name}%")
    if location:
        conditions.append("Address LIKE %s")
        params.append(f"%{location}%")
    if category:
        conditions.append("Category = %s")
        params.append(category)
    if rating:
        conditions.append("Rating >= %s")
        params.append(rating)

    if not conditions:
        print("No search criteria entered. Displaying all restaurants.")
        sql = "SELECT * FROM Restaurant"
    else:
        sql += " AND ".join(conditions)

    if sort_choice == '1':
        sql += " ORDER BY Rating DESC"
    elif sort_choice == '2':
        # 리뷰 수에 따라 정렬하기 위해 서브쿼리 사용
        sql = """
            SELECT Restaurant.*, IFNULL(ReviewCount, 0) AS ReviewCount 
            FROM Restaurant 
            LEFT JOIN (
                SELECT RestaurantID, COUNT(*) AS ReviewCount 
                FROM Review 
                GROUP BY RestaurantID
            ) AS ReviewCounts ON Restaurant.RestaurantID = ReviewCounts.RestaurantID
            """

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY ReviewCount DESC"

    # 식당 검색 및 결과 출력
    try:
        cursor.execute(sql, tuple(params))
        restaurants = cursor.fetchall()

        if restaurants:
            print("\nSearch Results:")
            for rest in restaurants:
                print(f"ID: {rest[0]}, Name: {rest[1]}, Address: {rest[2]}, Category: {rest[3]}, Rating: {rest[4]}")
        else:
            print("\nNo matching restaurants found.")

    except Exception as e:
        print(f"Error: {e}")

    if restaurants:
        fav_choice = input("\nEnter the ID of the restaurant you want to add to favorites (or press Enter to skip): ")
        if fav_choice:
            try:
                sql = "INSERT INTO Favorite (FavoriteID, UserID, RestaurantID) VALUES (UUID(), %s, %s)"
                cursor.execute(sql, (user_id, fav_choice))
                db.commit()
                print("Restaurant added to favorites.")
            except Exception as e:
                print(f"Error: {e}")
                db.rollback()

    db.close()

def add_restaurant(user_id):
    db = connect_db()
    cursor = db.cursor()

    # 식당 기본 정보 입력 받기
    name = input("Enter restaurant name: ")
    address = input("Enter restaurant address: ")
    category = input("Enter restaurant category: ")
    rating = input("Enter initial rating (1.0 to 5.0): ")

    # 식당 중복 확인
    cursor.execute("SELECT * FROM Restaurant WHERE Name = %s AND Address = %s", (name, address))
    if cursor.fetchone():
        print("Restaurant already exists in the database.")
        db.close()
        return

    # 식당 ID 자동 생성 (UUID 사용)
    restaurant_id = str(uuid.uuid4())

    # 식당 정보 추가
    try:
        sql = "INSERT INTO Restaurant (RestaurantID, Name, Address, Category, Rating, UserID) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (restaurant_id, name, address, category, rating, user_id))
        db.commit()
        print(f"Restaurant added successfully with ID {restaurant_id}.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    # 식당 연락처 추가
    while True:
        contact_number = input("Enter restaurant contact number (or press Enter to finish): ")
        if not contact_number:
            break
        try:
            sql = "INSERT INTO Rest_Num (ContactNumber, RestaurantID) VALUES (%s, %s)"
            cursor.execute(sql, (contact_number, restaurant_id))
            db.commit()
            print("Contact number added.")
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()

    db.close()


def delete_restaurant(user_id):
    db = connect_db()
    cursor = db.cursor()

    # 삭제할 식당의 ID 입력 받기
    restaurant_id = input("Enter the ID of the restaurant you want to delete: ")

    # 사용자가 등록한 식당인지 확인
    cursor.execute("SELECT * FROM Restaurant WHERE RestaurantID = %s AND UserID = %s", (restaurant_id, user_id))
    restaurant = cursor.fetchone()
    if not restaurant:
        print("Restaurant not found or you do not have permission to delete this restaurant.")
        db.close()
        return

    # 식당 정보 삭제
    try:
        # 연관된 연락처 정보 먼저 삭제
        cursor.execute("DELETE FROM Rest_Num WHERE RestaurantID = %s", (restaurant_id,))

        # 식당 정보 삭제
        cursor.execute("DELETE FROM Restaurant WHERE RestaurantID = %s", (restaurant_id,))
        db.commit()
        print("Restaurant deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()

def add_comment(user_id, review_id):
    db = connect_db()
    cursor = db.cursor()

    content = input("Enter your comment: ")
    try:
        comment_id = str(uuid.uuid4())
        sql = "INSERT INTO Comment (CommentID, Content, DateOfCreation, ReviewID, UserID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (comment_id, content, datetime.datetime.now(), review_id, user_id))
        db.commit()
        print("Comment added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()

def update_comment_likes(user_id, comment_id, like_dislike):
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = "UPDATE Comment SET LikeDislike = LikeDislike + %s WHERE CommentID = %s"
        cursor.execute(sql, (like_dislike, comment_id))
        db.commit()
        print("Comment updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()

def view_reviews(user_id):
    db = connect_db()
    cursor = db.cursor()

    # 조회할 식당의 ID 입력 받기
    restaurant_id = input("Enter the ID of the restaurant to view reviews: ")

    # 해당 식당의 리뷰 조회
    try:
        cursor.execute("SELECT * FROM Review WHERE RestaurantID = %s", (restaurant_id,))
        reviews = cursor.fetchall()

        if not reviews:
            print("No reviews found for this restaurant.")
        else:
            for review in reviews:
                print(f"\nReview ID: {review[0]}, Title: {review[1]}, Rating: {review[4]}")
                print(f"Content: {review[2]}")
                print(f"Date: {review[3]}")

                # 해당 리뷰의 댓글 조회
                cursor.execute("SELECT * FROM Comment WHERE ReviewID = %s", (review[0],))
                comments = cursor.fetchall()

                if comments:
                    print("Comments:")
                    for comment in comments:
                        print(f"- {comment[1]} (Date: {comment[2]}, Likes/Dislikes: {comment[3]})")
                else:
                    print("No comments on this review.")

    except Exception as e:
        print(f"Error: {e}")

    # 사용자가 댓글을 추가할 수 있는 옵션
    add_comment_choice = input("\nWould you like to add a comment to any review? (yes/no): ")
    if add_comment_choice.lower() == 'yes':
        review_id_to_comment = input("Enter the ID of the review you want to comment on: ")
        add_comment(user_id, review_id_to_comment)

    # 댓글에 좋아요/싫어요 추가
    update_like_dislike_choice = input("\nWould you like to like/dislike any comment? (yes/no): ")
    if update_like_dislike_choice.lower() == 'yes':
        comment_id_to_update = input("Enter the ID of the comment you want to like/dislike: ")
        like_or_dislike = int(input("Enter 1 for like or -1 for dislike: "))
        update_comment_likes(user_id, comment_id_to_update, like_or_dislike)

    db.close()

def write_review(user_id):
    db = connect_db()
    cursor = db.cursor()

    # 리뷰 정보 입력 받기
    restaurant_id = input("Enter the ID of the restaurant you are reviewing: ")
    title = input("Enter the title of your review: ")
    content = input("Enter your review content: ")
    rating = float(input("Enter your rating for the restaurant (1.0 to 5.0): "))

    # 현재 날짜와 시간
    now = datetime.datetime.now()

    # 리뷰 ID 자동 생성 (UUID 사용)
    review_id = str(uuid.uuid4())

    # 리뷰 정보 데이터베이스에 추가
    try:
        sql = "INSERT INTO Review (ReviewID, Title, Content, DateOfCreation, Rating, UserID, RestaurantID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (review_id, title, content, now, rating, user_id, restaurant_id))
        db.commit()
        print(f"Review added successfully with ID {review_id}.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()

def delete_user(user_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        # 사용자의 댓글과 리뷰 삭제
        cursor.execute("DELETE FROM Comment WHERE UserID = %s", (user_id,))
        cursor.execute("DELETE FROM Review WHERE UserID = %s", (user_id,))
        cursor.execute("DELETE FROM Favorite WHERE UserID = %s", (user_id,))

        # 사용자가 등록한 식당 ID 조회
        cursor.execute("SELECT RestaurantID FROM Restaurant WHERE UserID = %s", (user_id,))
        restaurant_ids = cursor.fetchall()

        # 각 식당에 대한 연락처 정보 삭제
        for (restaurant_id,) in restaurant_ids:
            cursor.execute("DELETE FROM Rest_Num WHERE RestaurantID = %s", (restaurant_id,))

        # 사용자가 등록한 식당 삭제
        cursor.execute("DELETE FROM Restaurant WHERE UserID = %s", (user_id,))

        # 사용자 계정 삭제
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        db.commit()
        print("User account and all related data have been deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    db.close()



def main():
    is_logged_in = False  # 사용자 로그인 상태를 추적하는 변수
    logged_in_user_id = None  # 로그인한 사용자의 ID를 저장하는 변수

    while True:
        if not is_logged_in:
            # 로그인 하기 전 메뉴
            print("\n===== Welcome to RestaurantDB =====")
            print("1. Login")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                is_logged_in, logged_in_user_id = login()  # 로그인 함수 수정 필요
            elif choice == '2':
                sign_up()
            elif choice == '3':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

        else:
            # 로그인 후 메뉴
            print("\n===== RestaurantDB Management System =====")
            print("1. View My Page")
            print("2. View Restaurants")
            print("3. Search Restaurants")
            print("4. Add Restaurant")
            print("5. Delete Restaurant")
            print("6. View Reviews")
            print("7. Write Review")
            print("8. Delete User")
            print("9. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                view_my_page(logged_in_user_id)

            elif choice == '2':
                view_restaurants()

            elif choice == '3':
                search_restaurants(logged_in_user_id)

            elif choice == '4':
                add_restaurant(logged_in_user_id)

            elif choice == '5':
                delete_restaurant(logged_in_user_id)

            elif choice == '6':
                view_reviews(logged_in_user_id)

            elif choice == '7':
                write_review(logged_in_user_id)

            elif choice == '8':
                delete_user(logged_in_user_id)
                is_logged_in = False

            elif choice == '9':
                is_logged_in = False
                print("Logged out successfully.")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

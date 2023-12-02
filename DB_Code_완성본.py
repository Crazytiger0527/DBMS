import pymysql  # pymysql 라이브러리를 임포트합니다. 이 라이브러리는 Python에서 MySQL 데이터베이스를 사용할 수 있게 해줍니다.
import uuid  # uuid 라이브러리를 임포트합니다. 이 라이브러리는 고유한 ID를 생성하는데 사용됩니다.
import datetime  # datetime 라이브러리를 임포트합니다. 날짜와 시간을 다루는데 사용됩니다.

# 이 함수는 pymysql을 사용하여 MySQL 데이터베이스에 연결합니다.
def connect_db():
    return pymysql.connect(
        host='192.168.56.101',  # 데이터베이스 서버의 호스트 주소입니다.
        port=3308,  # 데이터베이스 서버의 포트 번호입니다.
        user='root',  # 데이터베이스 사용자 이름입니다.
        passwd='1234',  # 데이터베이스 사용자 비밀번호입니다.
        db='RestaurantDB',  # 연결할 데이터베이스의 이름입니다.
        charset='utf8'  # 사용할 문자 인코딩입니다. 여기서는 'utf8'을 사용합니다.
    )

# 로그인 기능
def login():
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== Login ====================")
    user_id = input("Enter your ID: ")  # 사용자에게 ID 입력을 요청합니다.
    password = input("Enter your password: ")  # 사용자에게 비밀번호 입력을 요청합니다.
    print("================================================")

    sql = "SELECT * FROM User WHERE UserID = %s AND Password = %s"  # 사용자의 ID와 비밀번호를 검증하기 위한 SQL 쿼리입니다.
    cursor.execute(sql, (user_id, password))  # 쿼리를 실행하고, 사용자가 입력한 ID와 비밀번호로 검색합니다.
    result = cursor.fetchone()  # 쿼리 결과에서 첫 번째 행을 가져옵니다.

    if result:
        print("\n🎉 Login Successful! Welcome to RestaurantDB 🎉\n")
        return True, user_id  # 로그인이 성공하면 True와 사용자 ID를 반환합니다.
    else:
        print("\n❌ Login Failed: Incorrect ID or Password ❌\n")
        return False, None  # 로그인 실패 시 False와 None을 반환합니다.

    db.close()  # 데이터베이스 연결을 종료합니다.

# 회원가입
def sign_up():
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== Sign Up ====================")
    user_id = input("Enter your new ID: ")  # 사용자에게 새로운 ID 입력을 요청합니다.
    password = input("Enter your password: ")  # 사용자에게 비밀번호 입력을 요청합니다.
    name = input("Enter your name: ")  # 사용자의 이름을 입력받습니다.
    age = input("Enter your age: ")  # 사용자의 나이를 입력받습니다.
    address = input("Enter your address: ")  # 사용자의 주소를 입력받습니다.
    phone_number = input("Enter your phone number: ")  # 사용자의 전화번호를 입력받습니다.
    email_address = input("Enter your email address: ")  # 사용자의 이메일 주소를 입력받습니다.
    print("==================================================")

    sql = """
    INSERT INTO User (UserID, Password, Name, Age, Address, PhoneNumber, EmailAddress) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """  # 사용자 정보를 User 테이블에 삽입하기 위한 SQL 쿼리문입니다.
    try:
        cursor.execute(sql, (user_id, password, name, age, address, phone_number, email_address))  # 쿼리를 실행합니다.
        db.commit()  # 변경 사항을 데이터베이스에 커밋(확정)합니다.
        print("\n🌟 Registration Successful! Welcome to RestaurantDB 🌟\n")
    except Exception as e:
        print(f"\n❌ Error during registration: {e} ❌\n")  # 에러 발생 시 메시지를 출력합니다.
        db.rollback()  # 에러 발생 시, 이전 상태로 롤백합니다.

    db.close()  # 데이터베이스 연결을 종료합니다.

# 사용자의 마이페이지를 보여주는 함수입니다.
def view_my_page(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    try:
        print("\n==================== My Page ====================")

        # 로그인한 사용자의 정보를 출력합니다.
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))  # User 테이블에서 해당 사용자의 정보를 조회합니다.
        user_info = cursor.fetchone()  # 조회 결과 중 첫 번째 행을 가져옵니다.
        print("\n👤 User Information:")
        if user_info:
            # 사용자 정보가 있는 경우, 해당 정보를 출력합니다.
            print(f"ID: {user_info[0]} | Name: {user_info[2]} | Age: {user_info[3]}")
            print(f"Address: {user_info[4]} | Phone: {user_info[5]} | Email: {user_info[6]}")
        else:
            # 사용자 정보가 없는 경우, 메시지를 출력합니다.
            print("No data available.")

        # 사용자가 등록한 식당 정보를 출력합니다.
        print("\n🍴 Registered Restaurants:")
        cursor.execute("SELECT * FROM Restaurant WHERE UserID = %s", (user_id,))  # Restaurant 테이블에서 해당 사용자가 등록한 식당을 조회합니다.
        restaurants = cursor.fetchall()  # 모든 조회 결과를 가져옵니다.
        if restaurants:
            # 등록한 식당이 있는 경우, 식당 정보를 출력합니다.
            for rest in restaurants:
                print(f"ID: {rest[0]} | Name: {rest[1]} | Address: {rest[2]}")
                print(f"Category: {rest[3]} | Rating: {rest[4]}")
        else:
            # 등록한 식당이 없는 경우, 메시지를 출력합니다.
            print("No data available.")

        # 사용자가 작성한 리뷰를 출력합니다.
        print("\n📝 Written Reviews:")
        cursor.execute("SELECT * FROM Review WHERE UserID = %s", (user_id,))  # Review 테이블에서 해당 사용자가 작성한 리뷰를 조회합니다.
        reviews = cursor.fetchall()  # 모든 조회 결과를 가져옵니다.
        if reviews:
            # 작성한 리뷰가 있는 경우, 리뷰 정보를 출력합니다.
            for review in reviews:
                print(f"ID: {review[0]} | Title: {review[1]} | Date: {review[3]}")
                print(f"Rating: {review[4]} | Content: {review[2]}")
        else:
            # 작성한 리뷰가 없는 경우, 메시지를 출력합니다.
            print("No data available.")

        # 사용자가 작성한 코멘트를 출력합니다.
        print("\n💬 Written Comments:")
        cursor.execute("SELECT * FROM Comment WHERE UserID = %s", (user_id,))  # Comment 테이블에서 해당 사용자가 작성한 코멘트를 조회합니다.
        comments = cursor.fetchall()  # 모든 조회 결과를 가져옵니다.
        if comments:
            # 작성한 코멘트가 있는 경우, 코멘트 정보를 출력합니다.
            for comment in comments:
                print(f"ID: {comment[0]} | Date: {comment[2]}")
                print(f"Like/Dislike: {comment[3]} | Content: {comment[1]}")
        else:
            # 작성한 코멘트가 없는 경우, 메시지를 출력합니다.
            print("No data available.")

        # 사용자의 즐겨찾기 정보를 출력합니다.
        print("\n❤️ Favorite Restaurants:")
        cursor.execute("SELECT * FROM Favorite WHERE UserID = %s", (user_id,))  # Favorite 테이블에서 해당 사용자의 즐겨찾기 정보를 조회합니다.
        favorites = cursor.fetchall()  # 모든 조회 결과를 가져옵니다.
        if favorites:
            # 즐겨찾기 정보가 있는 경우, 해당 정보를 출력합니다.
            for favorite in favorites:
                print(f"ID: {favorite[0]} | Restaurant ID: {favorite[2]}")
        else:
            # 즐겨찾기 정보가 없는 경우, 메시지를 출력합니다.
            print("No data available.")

        print("==================================================")

    except Exception as e:
        print(f"Error: {e}")  # 에러 발생 시 에러 메시지를 출력합니다.

    db.close()  # 데이터베이스 연결을 종료합니다.

# 시스템에 등록된 모든 식당을 보여주는 함수입니다.
def view_restaurants():
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    try:
        print("\n==================== Restaurants ====================")
        sql = "SELECT * FROM Restaurant"  # Restaurant 테이블에서 모든 식당 정보를 조회하는 SQL 쿼리문입니다.
        cursor.execute(sql)  # 쿼리를 실행합니다.
        restaurants = cursor.fetchall()  # 조회 결과를 모두 가져옵니다.

        if restaurants:
            print("\n🍴 Restaurant List:")
            # 조회된 식당 정보가 있는 경우, 각 식당의 정보를 출력합니다.
            for rest in restaurants:
                print(f"ID: {rest[0]} | Name: {rest[1]} | Address: {rest[2]}")
                print(f"Category: {rest[3]} | Rating: {rest[4]}\n")
        else:
            # 조회된 식당 정보가 없는 경우, 메시지를 출력합니다.
            print("\nNo restaurants found in the system. 🤷‍♂️")

        print("=====================================================")

    except Exception as e:
        print(f"\nError: {e}\n")  # 에러 발생 시 에러 메시지를 출력합니다.

    db.close()  # 데이터베이스 연결을 종료합니다.

# 사용자가 조건에 따라 식당을 검색하는 함수입니다.
def search_restaurants(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== Search Restaurants ====================")
    # 검색 조건 입력 받기
    name = input("Enter restaurant name (or leave blank): ")
    location = input("Enter location (or leave blank): ")
    category = input("Enter category (or leave blank): ")
    rating = input("Enter minimum rating (or leave blank): ")

    print("\nChoose Sorting Criteria:")
    print("1. Rating")
    print("2. Number of Reviews")
    sort_choice = input("Enter your choice (1 or 2): ")

    # 검색 쿼리 구성
    sql = "SELECT * FROM Restaurant WHERE "
    conditions = []  # 검색 조건을 저장할 리스트
    params = []  # SQL 쿼리에 사용될 파라미터를 저장할 리스트

    # 각 검색 조건에 따라 쿼리 조건과 파라미터 추가
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

    # 검색 조건이 없는 경우 모든 식당을 표시
    if not conditions:
        print("No search criteria entered. Displaying all restaurants.")
        sql = "SELECT * FROM Restaurant"
    else:
        # 검색 조건이 있는 경우 쿼리에 조건 추가
        sql += " AND ".join(conditions)

    # 정렬 기준에 따라 쿼리 수정
    if sort_choice == '1':
        sql += " ORDER BY Rating DESC"
    elif sort_choice == '2':
        # 리뷰 수에 따라 정렬하기 위한 서브쿼리 사용
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
            print("\n🔍 Search Results:")
            for rest in restaurants:
                print(f"ID: {rest[0]} | Name: {rest[1]} | Address: {rest[2]}")
                print(f"Category: {rest[3]} | Rating: {rest[4]}\n")
        else:
            print("\nNo matching restaurants found. 🤷‍♂️")

    except Exception as e:
        print(f"Error: {e}")

    # 즐겨찾기에 추가하는 옵션
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

    print("============================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.


# 사용자가 새로운 식당을 추가하는 함수입니다.
def add_restaurant(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== Add New Restaurant ====================")
    # 식당 정보 입력 받기
    name = input("Enter restaurant name: ")
    address = input("Enter restaurant address: ")
    category = input("Enter restaurant category: ")
    rating = input("Enter initial rating (1.0 to 5.0): ")

    # 식당 중복 확인
    cursor.execute("SELECT * FROM Restaurant WHERE Name = %s AND Address = %s", (name, address))
    if cursor.fetchone():
        # 중복되는 식당이 있으면 메시지 출력 후 함수 종료
        print("\n❌ Restaurant already exists in the database. ❌")
        db.close()
        return

    # 식당 ID를 UUID를 사용해 자동 생성
    restaurant_id = str(uuid.uuid4())

    try:
        # 식당 정보를 데이터베이스에 추가
        sql = "INSERT INTO Restaurant (RestaurantID, Name, Address, Category, Rating, UserID) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (restaurant_id, name, address, category, rating, user_id))
        db.commit()
        print(f"\n🌟 Restaurant added successfully with ID {restaurant_id}. 🌟")

        # 식당 연락처 추가 옵션
        print("\nAdd Restaurant Contact Numbers:")
        while True:
            contact_number = input("Enter restaurant contact number (or press Enter to finish): ")
            if not contact_number:
                break  # 연락처 입력을 종료하려면 Enter 키를 누릅니다.
            try:
                # 연락처를 데이터베이스에 추가
                sql = "INSERT INTO Rest_Num (ContactNumber, RestaurantID) VALUES (%s, %s)"
                cursor.execute(sql, (contact_number, restaurant_id))
                db.commit()
                print("✅ Contact number added.")
            except Exception as e:
                print(f"❌ Error: {e}")
                db.rollback()  # 에러 발생 시 변경 사항을 롤백합니다.

    except Exception as e:
        print(f"\n❌ Error adding restaurant: {e}")
        db.rollback()  # 에러 발생 시 변경 사항을 롤백합니다.

    print("============================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 사용자가 식당을 삭제하는 함수입니다.
def delete_restaurant(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== Delete Restaurant ====================")
    # 삭제할 식당의 ID를 입력 받습니다.
    restaurant_id = input("Enter the ID of the restaurant you want to delete: ")

    # 사용자가 등록한 식당인지 확인
    cursor.execute("SELECT * FROM Restaurant WHERE RestaurantID = %s AND UserID = %s", (restaurant_id, user_id))
    restaurant = cursor.fetchone()
    if not restaurant:
        # 해당 식당이 없거나 사용자가 삭제 권한이 없으면 메시지 출력 후 함수 종료
        print("\n❌ Restaurant not found or you do not have permission to delete this restaurant. ❌")
        db.close()
        return

    try:
        # 연관된 연락처 정보 먼저 삭제
        cursor.execute("DELETE FROM Rest_Num WHERE RestaurantID = %s", (restaurant_id,))

        # 식당 정보 삭제
        cursor.execute("DELETE FROM Restaurant WHERE RestaurantID = %s", (restaurant_id,))
        db.commit()  # 변경 사항을 데이터베이스에 커밋합니다.
        print("\n🗑️ Restaurant deleted successfully. 🗑️")
    except Exception as e:
        print(f"\n❌ Error: {e} ❌")
        db.rollback()  # 에러 발생 시 변경 사항을 롤백합니다.

    print("============================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 댓글 추가
def add_comment(user_id, review_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 커서를 생성합니다.

    print("\n==================== Add Comment ====================")
    content = input("Enter your comment: ")  # 사용자로부터 댓글 내용을 입력받습니다.

    try:
        comment_id = str(uuid.uuid4())  # 고유한 댓글 ID를 생성합니다.
        # 댓글 정보를 Comment 테이블에 삽입하는 SQL 명령을 작성합니다.
        sql = "INSERT INTO Comment (CommentID, Content, DateOfCreation, ReviewID, UserID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (comment_id, content, datetime.datetime.now(), review_id, user_id))
        db.commit()  # 데이터베이스에 변경 사항을 커밋합니다.
        print("\n💬 Comment added successfully. 💬")
    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 예외 발생 시 오류 메시지를 출력합니다.
        db.rollback()  # 데이터베이스 변경사항을 롤백합니다.

    print("=======================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.


# 좋아요/싫어요
def update_comment_likes(user_id, comment_id, like_dislike):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 커서를 생성합니다.

    print("\n==================== Update Comment Likes/Dislikes ====================")

    try:
        # Comment 테이블의 LikeDislike 칼럼을 업데이트하는 SQL 명령을 작성합니다.
        # like_dislike 변수의 값(양수 또는 음수)에 따라 좋아요 또는 싫어요를 갱신합니다.
        sql = "UPDATE Comment SET LikeDislike = LikeDislike + %s WHERE CommentID = %s"
        cursor.execute(sql, (like_dislike, comment_id))
        db.commit()  # 데이터베이스에 변경 사항을 커밋합니다.

        # 사용자의 입력에 따라 적절한 메시지를 출력합니다.
        if like_dislike > 0:
            print("\n👍 Comment liked successfully. 👍")
        else:
            print("\n👎 Comment disliked successfully. 👎")
    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 예외 발생 시 오류 메시지를 출력합니다.
        db.rollback()  # 데이터베이스 변경사항을 롤백합니다.

    print("=======================================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 사용자가 특정 식당의 리뷰를 보는 함수입니다.
def view_reviews(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 데이터베이스 작업을 위한 커서 객체를 생성합니다.

    print("\n==================== View Reviews ====================")
    # 리뷰를 볼 식당의 ID를 입력받습니다.
    restaurant_id = input("Enter the ID of the restaurant to view reviews: ")

    try:
        # 해당 식당의 모든 리뷰를 조회합니다.
        cursor.execute("SELECT * FROM Review WHERE RestaurantID = %s", (restaurant_id,))
        reviews = cursor.fetchall()

        if not reviews:
            # 리뷰가 없는 경우 메시지를 출력합니다.
            print("\nNo reviews found for this restaurant. 🤷‍♂️")
        else:
            # 리뷰가 있는 경우 각 리뷰의 정보를 출력합니다.
            print("\n📝 Reviews for Restaurant:")
            for review in reviews:
                print(f"\nReview ID: {review[0]} | Title: {review[1]} | Rating: {review[4]}")
                print(f"Date: {review[3]} | Content: {review[2]}")

                # 각 리뷰에 대한 댓글 조회
                cursor.execute("SELECT * FROM Comment WHERE ReviewID = %s", (review[0],))
                comments = cursor.fetchall()

                if comments:
                    # 댓글이 있는 경우 댓글 정보를 출력합니다.
                    print("\nComments:")
                    for comment in comments:
                        print(f"- ID: {comment[0]} | {comment[1]} (Date: {comment[2]}, Likes/Dislikes: {comment[3]})")
                else:
                    # 댓글이 없는 경우 메시지를 출력합니다.
                    print("No comments on this review.")

    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 에러 발생 시 에러 메시지를 출력합니다.

    # 사용자가 리뷰에 댓글을 추가할 수 있는 옵션을 제공합니다.
    add_comment_choice = input("\nWould you like to add a comment to any review? (yes/no): ")
    if add_comment_choice.lower() == 'yes':
        review_id_to_comment = input("Enter the ID of the review you want to comment on: ")
        add_comment(user_id, review_id_to_comment)  # 댓글 추가 함수를 호출합니다.

    # 사용자가 댓글에 좋아요/싫어요를 추가할 수 있는 옵션을 제공합니다.
    update_like_dislike_choice = input("\nWould you like to like/dislike any comment? (yes/no): ")
    if update_like_dislike_choice.lower() == 'yes':
        comment_id_to_update = input("Enter the ID of the comment you want to like/dislike: ")
        like_or_dislike = int(input("Enter 1 for like or -1 for dislike: "))
        update_comment_likes(user_id, comment_id_to_update, like_or_dislike)  # 좋아요/싫어요 업데이트 함수를 호출합니다.

    print("=======================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 리뷰 작성
def write_review(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 커서를 생성합니다.

    print("\n==================== Write Review ====================")
    restaurant_id = input("Enter the ID of the restaurant you are reviewing: ")  # 리뷰할 레스토랑 ID를 입력받습니다.
    title = input("Enter the title of your review: ")  # 리뷰의 제목을 입력받습니다.
    content = input("Enter your review content: ")  # 리뷰 내용을 입력받습니다.
    rating = float(input("Enter your rating for the restaurant (1.0 to 5.0): "))  # 레스토랑에 대한 평점을 입력받습니다.

    review_id = str(uuid.uuid4())  # 고유한 리뷰 ID를 생성합니다.
    now = datetime.datetime.now()  # 현재 날짜와 시간을 기록합니다.

    try:
        # Review 테이블에 리뷰 정보를 삽입하는 SQL 명령을 작성합니다.
        sql = "INSERT INTO Review (ReviewID, Title, Content, DateOfCreation, Rating, UserID, RestaurantID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (review_id, title, content, now, rating, user_id, restaurant_id))
        db.commit()  # 데이터베이스에 변경 사항을 커밋합니다.
        print(f"\n🌟 Review added successfully with ID {review_id}. 🌟")
    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 예외 발생 시 오류 메시지를 출력합니다.
        db.rollback()  # 데이터베이스 변경사항을 롤백합니다.

    print("=======================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 레스토랑 추천
def recommend_restaurants(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 커서를 생성합니다.

    print("\n==================== Recommended Restaurants ====================")

    try:
        # 사용자가 높게 평가한 카테고리를 찾기 위한 SQL 쿼리를 실행합니다.
        cursor.execute("""
            SELECT Category FROM Restaurant 
            JOIN Review ON Restaurant.RestaurantID = Review.RestaurantID 
            WHERE Review.UserID = %s 
            ORDER BY Review.Rating DESC LIMIT 1
        """, (user_id,))
        favorite_category = cursor.fetchone()  # 사용자의 가장 좋아하는 카테고리를 얻습니다.

        if favorite_category:
            # 사용자가 좋아하는 카테고리에 속한 다른 식당을 추천하기 위한 SQL 쿼리를 실행합니다.
            cursor.execute("""
                SELECT * FROM Restaurant 
                WHERE Category = %s AND RestaurantID NOT IN (
                    SELECT RestaurantID FROM Review WHERE UserID = %s
                ) LIMIT 5
            """, (favorite_category[0], user_id))
            recommended_restaurants = cursor.fetchall()  # 추천 식당 목록을 얻습니다.

            if recommended_restaurants:
                print("\n🌟 Based on your interests in " + favorite_category[0] + " category:")
                for restaurant in recommended_restaurants:
                    # 각 추천된 식당의 정보를 출력합니다.
                    print(f"ID: {restaurant[0]} | Name: {restaurant[1]} | Address: {restaurant[2]}")
                    print(f"Category: {restaurant[3]} | Rating: {restaurant[4]}\n")
            else:
                print("\nNo additional restaurants found in your favorite category. 🤷‍♂️")
        else:
            print("\nNo recommendations available based on your reviews. 🤷‍♂️")

    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 예외 발생 시 오류 메시지를 출력합니다.

    print("===============================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 회원탈퇴
def delete_user(user_id):
    db = connect_db()  # 데이터베이스에 연결합니다.
    cursor = db.cursor()  # 커서를 생성합니다.

    print("\n==================== Delete User Account ====================")
    try:
        # 사용자의 즐겨찾기를 삭제합니다.
        cursor.execute("DELETE FROM Favorite WHERE UserID = %s", (user_id,))

        # 사용자가 작성한 리뷰와 사용자가 등록한 식당의 리뷰 ID를 조회합니다.
        cursor.execute("""
            SELECT ReviewID FROM Review 
            WHERE UserID = %s OR RestaurantID IN (
                SELECT RestaurantID FROM Restaurant WHERE UserID = %s
            )
        """, (user_id, user_id))
        review_ids = [review_id for (review_id,) in cursor.fetchall()]

        # 사용자 또는 사용자의 식당에 대한 모든 댓글을 삭제합니다.
        for review_id in review_ids:
            cursor.execute("DELETE FROM Comment WHERE ReviewID = %s", (review_id,))

        # 사용자의 모든 리뷰를 삭제합니다.
        for review_id in review_ids:
            cursor.execute("DELETE FROM Review WHERE ReviewID = %s", (review_id,))

        # 사용자가 등록한 식당의 연락처 정보 및 식당 정보를 삭제합니다.
        cursor.execute("SELECT RestaurantID FROM Restaurant WHERE UserID = %s", (user_id,))
        restaurant_ids = [restaurant_id for (restaurant_id,) in cursor.fetchall()]

        for restaurant_id in restaurant_ids:
            cursor.execute("DELETE FROM Rest_Num WHERE RestaurantID = %s", (restaurant_id,))
            cursor.execute("DELETE FROM Restaurant WHERE RestaurantID = %s", (restaurant_id,))

        # 사용자 계정을 삭제합니다.
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        db.commit()  # 데이터베이스에 변경 사항을 커밋합니다.
        print("\n🗑️ User account and all related data have been deleted successfully. 🗑️")
    except Exception as e:
        print(f"\n❌ Error: {e} ❌")  # 예외 발생 시 오류 메시지를 출력합니다.
        db.rollback()  # 데이터베이스 변경사항을 롤백합니다.

    print("============================================================")

    db.close()  # 데이터베이스 연결을 종료합니다.

# 메인함수
def main():
    is_logged_in = False  # 사용자 로그인 상태를 추적합니다.
    logged_in_user_id = None  # 로그인한 사용자의 ID를 저장합니다.

    while True:
        print("\n==================== RestaurantDB Management System ====================")
        if not is_logged_in:
            # 사용자가 로그인하기 전에 표시되는 메뉴입니다.
            print("\n🌐 Welcome to RestaurantDB 🌐")
            print("1. Login")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("👉 Enter your choice: ")

            if choice == '1':
                is_logged_in, logged_in_user_id = login()  # 로그인 함수를 호출합니다.
            elif choice == '2':
                sign_up()  # 회원가입 함수를 호출합니다.
            elif choice == '3':
                print("\n👋 Exiting the program. Goodbye! 👋")
                break  # 프로그램을 종료합니다.
            else:
                print("\n❌ Invalid choice. Please try again. ❌")  # 잘못된 선택을 처리합니다.

        else:
            # 사용자가 로그인한 후에 표시되는 메뉴입니다.
            print("\n📋 Logged in as: " + logged_in_user_id)
            print("1. View My Page")
            print("2. View Restaurants")
            print("3. Search Restaurants")
            print("4. Add Restaurant")
            print("5. Delete Restaurant")
            print("6. View Reviews")
            print("7. Write Review")
            print("8. Recommend Restaurants")
            print("9. Delete User")
            print("10. Logout")
            choice = input("👉 Enter your choice: ")

            # 사용자가 선택한 옵션에 따라 해당 기능을 수행하는 함수를 호출합니다.
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
                recommend_restaurants(logged_in_user_id)

            elif choice == '9':
                delete_user(logged_in_user_id)
                is_logged_in = False  # 사용자를 로그아웃 시킵니다.

            elif choice == '10':
                is_logged_in = False  # 사용자를 로그아웃 시킵니다.
                print("\n👋 Logged out successfully. See you again! 👋")
            else:
                print("\n❌ Invalid choice. Please try again. ❌")  # 잘못된 선택을 처리합니다.

        print("========================================================================")

if __name__ == "__main__":
    main()
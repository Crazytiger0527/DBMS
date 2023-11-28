import pymysql

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
    # 모든 식당 정보 출력
    pass

def search_restaurants():
    # 식당 검색 및 즐겨찾기 추가 기능
    pass

def add_restaurant():
    # 새로운 식당 정보 추가
    pass

def delete_restaurant():
    # 식당 정보 삭제
    pass

def view_reviews():
    # 특정 식당에 대한 리뷰와 댓글 조회
    pass

def write_review():
    # 리뷰 작성
    pass

def delete_user():
    # 사용자 계정 삭제
    pass

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
                # view_restaurants()
                pass
            elif choice == '3':
                # search_restaurants()
                pass
            elif choice == '4':
                # add_restaurant()
                pass
            elif choice == '5':
                # delete_restaurant()
                pass
            elif choice == '6':
                # view_reviews()
                pass
            elif choice == '7':
                # write_review()
                pass
            elif choice == '8':
                # delete_user()
                pass
            elif choice == '9':
                is_logged_in = False
                print("Logged out successfully.")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

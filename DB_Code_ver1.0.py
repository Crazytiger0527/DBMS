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
        return True
    else:
        print("ID 또는 비밀번호가 잘못되었습니다.")
        return False

    db.close()

def sign_up():
    pass

def view_my_page():
    # 로그인한 사용자의 정보, 식당, 리뷰, 코멘트, 즐겨찾기 정보 출력
    pass

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

    while True:
        if not is_logged_in:
            # 로그인 하기 전 메뉴
            print("\n===== Welcome to RestaurantDB =====")
            print("1. Login")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                is_logged_in = login()
            elif choice == '2':
                # sign_up()
                pass
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
                # view_my_page()
                pass
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


if __name__ == "__main__":
    main()

import java.sql.*;

public class DBMS_HW_1 {

    private static final String JDBC_URL = "jdbc:mysql://192.168.56.101:3308/madang";
    private static final String USER = "root";
    private static final String PASSWORD = "1234";

    public static void main(String[] args) {
        try {
            // 데이터베이스 연결
            Connection connection = DriverManager.getConnection(JDBC_URL, USER, PASSWORD);

            // 데이터 삽입
            insertData(connection);

            // 데이터 검색
            searchData(connection, 11);

            // 데이터 삭제
            deleteData(connection, 11);
            
            // 데이터 검색
            searchData(connection, 11);

            // 연결 종료
            connection.close();
        } catch(Exception e){ System.out.println(e);} 
    }

    private static void insertData(Connection connection) throws SQLException {
        // Book 테이블에 데이터 삽입
        String insertBookQuery = "INSERT INTO Book (bookid, bookname, publisher, price) VALUES (?, ?, ?, ?)";
        try (PreparedStatement preparedStatement = connection.prepareStatement(insertBookQuery)) {
            preparedStatement.setInt(1, 11);
            preparedStatement.setString(2, "Sample Book");
            preparedStatement.setString(3, "esport");
            preparedStatement.setInt(4, 15000);

            int rowsAffected = preparedStatement.executeUpdate();
            System.out.println(rowsAffected + " row(s) inserted into Book table");
        }
    }
    
    private static void searchData(Connection connection, int bookId) throws SQLException {
        // Book 테이블에서 특정 bookid의 데이터 검색
        String searchBookQuery = "SELECT * FROM Book WHERE bookid = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(searchBookQuery)) {
            preparedStatement.setInt(1, bookId);

            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                System.out.println("Book Table:");

                boolean found = false;
                while (resultSet.next()) {
                    int bookid = resultSet.getInt("bookid");
                    String bookname = resultSet.getString("bookname");
                    String publisher = resultSet.getString("publisher");
                    int price = resultSet.getInt("price");

                    System.out.println("bookid: " + bookid + ", bookname: " + bookname + ", publisher: " + publisher + ", price: " + price);
                    found = true;
                }

                if (!found) {
                    System.out.println("No record found with bookid: " + bookId);
                }
            }
        }
    }

    private static void deleteData(Connection connection, int bookId) throws SQLException {
        // Book 테이블에서 데이터 삭제
        String deleteBookQuery = "DELETE FROM Book WHERE bookid =?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(deleteBookQuery)) {
            preparedStatement.setInt(1, bookId);

            int rowsAffected = preparedStatement.executeUpdate();
            System.out.println(rowsAffected + " row(s) deleted from Book table");
        }
    }
}

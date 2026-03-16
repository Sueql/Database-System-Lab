// C937.java
// 导入所需的Java类
import java.sql.*;
import java.io.*;

// 定义名为C937的Java类
public class C937 {
    // 定义JDBC驱动程序和数据库URL
    static final String JDBC_DRIVER = "org.postgresql.Driver";
    static final String DB_URL = "jdbc:postgresql://123.249.44.161:26000/mydb?ApplicationName=app1";
    // 定义数据库用户名和密码
    static final String USER = "xisu";
    static final String PASS = "XXXIsu@123";

    // 主函数
    public static void main(String[] args) {
        // 保存待插入数据的文件名
        String filename = "./C937.txt";
        // 待插入的数据量
        int data_num = 1000;
        // 字段分隔符
        String delimiter = " ";

        try {
            // 加载驱动程序
            Class.forName(JDBC_DRIVER);
            // 连接数据库
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
            // 创建预编译 SQL 语句
            String sql = "INSERT INTO public.C937(CNUMBER, CNAME, PERIOD,CREDIT, TEACHER) VALUES (?, ?, ?, ?, ?)";
            PreparedStatement ps = conn.prepareStatement(sql);
            // 读取数据文件
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            String line = reader.readLine();
            // 记录当前行数
            int lineNumber = 1;

            for (int i = 0; i < data_num && line != null; i++) {
                if( lineNumber > 100 && lineNumber <= 1000){
                    // 获取每条记录中各字段值
                    String[] fields = line.split(delimiter);
                    // 检查课程名称长度是否超过25个字符，如果超过则跳过该条数据
                    //if (fields[1].length() > 10) {
                    // 读取下一行记录
                    //     line = reader.readLine();
                    //     continue;
                    // }//加上这个if语句还是会报错。。。只能修改C937表中CNAME的长度了
                    // 向 SQL 语句中填入各字段值
                    ps.setString(1, fields[0]);
                    ps.setString(2, fields[1]);
                    ps.setInt(3, Integer.parseInt(fields[2]));
                    ps.setFloat(4, Float.parseFloat(fields[3]));
                    ps.setString(5, fields[4]);
                    // 执行插入语句
                    ps.executeUpdate();
                }

                // 读取下一行记录
                line = reader.readLine();
                lineNumber++;
            }
            // 关闭数据文件
            reader.close();
            // 关闭预编译 SQL 语句
            ps.close();
            // 关闭数据库连接
            conn.close();
            // 输出更新成功的消息
            System.out.println("插入数据成功!");
        } catch (Exception e) {
            // 输出异常信息
            e.printStackTrace();
        }
    }
}
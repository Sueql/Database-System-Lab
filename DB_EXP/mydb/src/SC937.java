// SC937.java
import java.sql.*;
import java.io.*;

public class SC937 {
    // JDBC 驱动名称
    static final String JDBC_DRIVER = "org.postgresql.Driver";
    // 数据库 URL
    static final String DB_URL = "jdbc:postgresql://123.249.44.161:26000/mydb?ApplicationName=app1";
    // 数据库用户名和密码
    static final String USER = "xisu";
    static final String PASS = "XXXIsu@123";

    public static void main(String[] args) {

        String filename = "./SC937.txt";
        int insert_data_num = 180180;        // 插入
        // int delete_data_num = 200;         // 删除
        // boolean flag = true;             // 设置为 true，表示要执行删除操作
        try {
            Class.forName(JDBC_DRIVER);
            Connection openGauss = DriverManager.getConnection(DB_URL, USER, PASS);  // 连接到数据库
            // 创建线程
            InsertThread thread1 = new InsertThread(openGauss, filename, insert_data_num);
            // DeleteThread thread2 = new DeleteThread(openGauss, flag, delete_data_num);
            // 启动线程
            thread1.start();
            // thread2.start();
            thread1.join();
            // thread2.join();
            openGauss.close();    // 关闭数据库连接
            System.out.println("更新数据成功！");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 插入数据线程类
    static class InsertThread extends Thread {
        private final Connection openGauss;
        private final String filename;
        private final int data_num;

        public InsertThread(Connection openGauss, String filename, int data_num) {
            this.openGauss = openGauss;
            this.filename = filename;
            this.data_num = data_num;
        }

        public void run() {
            try {
                String sql = "INSERT INTO public.SC937 (SNUMBER, CNUMBER, GRADE) VALUES (?, ?, ?)";
                PreparedStatement ps = this.openGauss.prepareStatement(sql);
                // 读取数据文件
                BufferedReader reader = new BufferedReader(new FileReader(this.filename));
                String line = reader.readLine();
                for (int i = 0; i < this.data_num && line != null; i++) {
                    // 将每条记录按指定分隔符分割成字段
                    String[] fields = line.split(" ");
                    // 向预编译 SQL 语句中填入各字段值
                    ps.setString(1, fields[0]);
                    ps.setString(2, fields[1]);
                    ps.setFloat(3, Float.parseFloat(fields[2]));
                    ps.executeUpdate();
                    line = reader.readLine();  // 读取下一行记录
                }
                reader.close();
                ps.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
/*
    // 删除数据线程类
    static class DeleteThread extends Thread {
        private final Connection openGauss;
        private final boolean flag;
        private final int data_num;

        public DeleteThread(Connection openGauss, boolean flag, int data_num) {
            this.openGauss = openGauss;
            this.flag = flag;
            this.data_num = data_num;
        }
        public void run() {
            try {
                if (this.flag) {
                    Statement stmt = openGauss.createStatement();
                    // 删除 SQL 语句，随机删除 GRADE 小于 60 的记录
                    String sql = "DELETE FROM public.SC937 WHERE GRADE < 60.0 LIMIT 1";
                    int deletedRecords = 0;
                    for (int i = 0; i < this.data_num; i++) {
                        // 执行删除操作
                        if (stmt.execute(sql)) {
                            deletedRecords++;
                        }
                    }
                    // System.out.println("删除成功");
                    // 关闭 Statement 对象
                    stmt.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }*/
}
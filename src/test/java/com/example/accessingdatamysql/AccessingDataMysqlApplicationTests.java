package com.example.accessingdatamysql;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.beans.factory.annotation.Autowired;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

// @SpringBootTest
// class AccessingDataMysqlApplicationTests {

// 	@Test
// 	void contextLoads() {
// 		System.out.println('================================================');
// 	}

// }



@SpringBootTest
class AccessingDataMysqlApplicationTests {
    @Autowired
    DataSource dataSource;
    @Test
    void contextLoads() throws SQLException {

        //获得数据库连接
        Connection connection = dataSource.getConnection();
        System.out.println(connection +"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

        //关闭
        connection.close();
    }

}



package com.example.accessingdatamysql;

import org.springframework.boot.SpringApplication;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@ComponentScan("com.example.accessingdatamysql")
@MapperScan("com.example.accessingdatamysql.dao") // 让springboot知道mapper是这个项目的持久层
public class AccessingDataMysqlApplication {
	public static void main(String[] args) {
		SpringApplication.run(AccessingDataMysqlApplication.class, args);
	}

}
package com.example.accessingdatamysql.dao;

import org.springframework.stereotype.Repository;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import com.example.accessingdatamysql.domain.User;

@Repository
public interface UserDao {
    @Select("select * from mid.user;")
    List<User> findAll();

    // @Select("select * from mid.user;")
    List<User> findUsersByCondition(String user);
}

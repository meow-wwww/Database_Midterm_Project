package com.example.accessingdatamysql.service;
import com.example.accessingdatamysql.domain.User;
import java.util.List;

public interface UserService {
    List<User> listUsers();
    List<User> listUsersByCondition(String user);
}

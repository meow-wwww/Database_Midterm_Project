package com.example.accessingdatamysql.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import com.example.accessingdatamysql.domain.User;
import com.example.accessingdatamysql.service.UserService;
import com.example.accessingdatamysql.dao.UserDao;

import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserDao userDao;

    @Override
    public List<User> listUsers() {
        return userDao.findAll();
    }

    @Override
    public List<User> listUsersByCondition(String user) {
        return userDao.findUsersByCondition(user);
    }
}
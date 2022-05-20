package com.example.accessingdatamysql.controller;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.accessingdatamysql.domain.User;
import com.example.accessingdatamysql.service.UserService;
import java.util.List;


@AllArgsConstructor
@RequestMapping("/user")
@RestController
public class UserController {
    @Autowired
    UserService userService;

    @GetMapping(value="/", produces = {"application/json;charset=UTF-8"})
    public List<User> getAllUsers() {
        System.out.println("===================");
        return userService.listUsers();
    }
    

    @PostMapping(value = "/getUsers", produces = {"application/json;charset=UTF-8"})
    public List<User> getUsersByCondition(@RequestParam String user) {
        System.out.println("=============");
        System.out.println("getUsers");
        // System.out.println(user);
        // System.out.println((userService.listUsersByCondition(user)).getClass().toString());
        return userService.listUsersByCondition(user);
    }

}

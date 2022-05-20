package com.example.accessingdatamysql.domain;
import lombok.Data;

@Data
public class User {
    private int uid;
    private String user_name;
    private String address;
    private String phone_number;
    private String email;
 
}
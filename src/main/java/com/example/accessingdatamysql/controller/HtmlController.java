package com.example.accessingdatamysql.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/front")
public class HtmlController {

    @RequestMapping("/error")
    public String error() {
        return "error";
    }

    @RequestMapping("/test")
    public String test() {
        return "test";
    }

    @RequestMapping("/")
    public String mainPage() {
        return "mainPage";
    }

}

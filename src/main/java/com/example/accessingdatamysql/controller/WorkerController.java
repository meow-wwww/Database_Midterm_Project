package com.example.accessingdatamysql.controller;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;
// import com.example.accessingdatamysql.model.dto.AllWorkerDTO;
// import com.example.accessingdatamysql.model.dto.CommonResult;
// import com.example.accessingdatamysql.model.dto.WorkerDTO;
// import com.example.accessingdatamysql.service.WorkerService;
// import 
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.*;

@RestController
@AllArgsConstructor
@RequestMapping("/worker")
public class WorkerController {
    @RequestMapping("/")
    public String say(){
        // return new CommonResult<>(200, "添加成功", 1);
        return "{'message1': 'SpringBoot你大爷','message2','SpringBoot你大爷2'}";
    }
}

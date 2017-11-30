package org.bearfly.ewords.controller;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HelloController {
    private final Log logger = LogFactory.getLog(HelloController.class); 
    @RequestMapping(value = "/hello", method = RequestMethod.GET)
    public String hello(@RequestParam(value = "name", required = false, defaultValue = "default value") 
            String name, ModelMap model) {
        model.addAttribute("name", name);
        logger.info("do Hello response");
        return "hello";
    }
 
}

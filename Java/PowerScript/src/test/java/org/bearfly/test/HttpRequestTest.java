package org.bearfly.test;

import java.util.HashMap;
import java.util.Map;

import org.bearfly.tools.HttpRequest;
import org.junit.Test;

public class HttpRequestTest {
    @Test
    public void testSendGet(){
        String url = "https://www.baidu.com/s";
        Map<String, String> params = new HashMap<String, String>();
        params.put("wd", "aa");
        HttpRequest.sendGet(url, params);
    }
}

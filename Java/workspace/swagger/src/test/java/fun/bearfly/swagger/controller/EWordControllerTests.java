package fun.bearfly.swagger.controller;

import org.junit.Before;
import org.junit.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;



public class EWordControllerTests {
	private MockMvc mvc;
	@Before
	public void setUp() throws Exception {
	    mvc = MockMvcBuilders.standaloneSetup(new EWordController()).build();
	}
	@Test
	public void testHelloWorld() throws Exception {
	mvc.perform(MockMvcRequestBuilders.get("/helloworld").accept(MediaType.APPLICATION_JSON))
	            .andExpect(MockMvcResultMatchers.status().isOk())
	            .andDo(MockMvcResultHandlers.print())
	            .andReturn();
	}
}



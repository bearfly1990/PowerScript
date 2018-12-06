
package fun.bearfly.javalearn.annotation;

/**
* @Description: TODO
* @author bearfly1990
* @date Dec 6, 2018 9:24:08 PM
*/
public class TestCaseDemo {
    @TestCase(id = 1, description = "test username")
    public boolean testUsername(String username){
        return false;
    }
    
	@TestCase(id = 2, description = "test password")
    public boolean testPassword(String password){
        return false;
    }
	
	@TestCase(id = 3, description = "test username and password")
    @TestCase(id = 4, description = "test login")
    public boolean testLogin(String username, String password){
        return false;
    }
}

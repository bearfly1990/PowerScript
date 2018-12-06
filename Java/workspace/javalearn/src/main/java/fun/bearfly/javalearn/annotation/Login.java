
package fun.bearfly.javalearn.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Target;

/**
* @Description: TODO
* @author bearfly1990
* @date Dec 6, 2018 9:30:30 PM
*/
@Target(ElementType.METHOD)
public @interface Login {
    String username() default "bearfly1990";
    String password() default "123456";
}


package fun.bearfly.javalearn.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
* @Description: TODO
* @author bearfly1990
* @date Dec 6, 2018 9:22:17 PM
*/
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Repeatable(TestCases.class)
public @interface TestCase {
	public int id();
	public String description() default "";
}

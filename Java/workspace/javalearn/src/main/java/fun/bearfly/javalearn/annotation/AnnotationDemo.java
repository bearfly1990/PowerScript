package fun.bearfly.javalearn.annotation;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;

/**
* @Description: TODO
* @author bearfly1990
* @date Dec 6, 2018 9:40:20 PM
*/
public class AnnotationDemo {
	public static void main(String[] args) {
		Method[] methods = TestCaseDemo.class.getMethods();
		for (Method method : methods) {
			Annotation[] annotations = method.getAnnotations();
			for (Annotation annotation : annotations) {
				if (annotation != null && annotation instanceof TestCase) {
					System.out.println(((TestCase) annotation).id() + " " + ((TestCase) annotation).description());
				} else if (annotation != null && annotation instanceof TestCases) {
					TestCase[] repeatTestCases = method.getAnnotationsByType(TestCase.class);
					for (TestCase testCase : repeatTestCases) {
						System.out.println(testCase.id() + " " + testCase.description());
					}
				}
			}
		}
	}
}

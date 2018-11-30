/**
* @Description: Algorithms samples interface.
* @author bearfly1990
* @date Nov 30, 2018 9:24:26 PM
*/
package org.bearfly.fun.javalearn.algorithms;

public interface IAlgorithms {
	/**
	 * <p>This is the definition to check input string could match pattern or not<p>
	 * <p>example:</p>
	 * <p>matched: input = "java hello world", pattern = "ABC"</p>
	 * <p>matched: input = "java hello java hello", pattern = "ABAB"</p>
	 * <p>unmatch: input = "java hello java", pattern = "ABC"</p>
	 * <p>unmatch: input = "java hello", pattern = "ABC"</p>
	 * <p>...</p>
	 * @param input
	 * @param pattern
	 * @return boolean inputStr could match patter or not
	 * 
	 */
	public boolean matchPattern(String input, String pattern);
}

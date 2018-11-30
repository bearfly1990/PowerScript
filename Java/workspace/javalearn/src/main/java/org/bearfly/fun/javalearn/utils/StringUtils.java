/**
* @Description: StringUtils
* @author bearfly1990
* @date Nov 30, 2018 10:16:58 PM
*/
package org.bearfly.fun.javalearn.utils;

public class StringUtils {
	public static String[] arrayCharToStr(char[] charArray) {
		String[] newStrArray = new String[charArray.length];
		for (int i = 0; i < charArray.length; i++) {
			newStrArray[i] = String.valueOf(charArray[i]);
		}
		return newStrArray;
	}
}

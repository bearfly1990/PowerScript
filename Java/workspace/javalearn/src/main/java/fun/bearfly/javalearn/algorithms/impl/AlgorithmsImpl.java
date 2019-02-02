/**
* @Description: Algorithms Implements
* @author bearfly1990
* @date Nov 30, 2018 9:42:29 PM
*/
package fun.bearfly.javalearn.algorithms.impl;

import java.util.HashMap;
import java.util.Map;

import fun.bearfly.javalearn.algorithms.IAlgorithms;
import fun.bearfly.javalearn.utils.StringUtils;

public class AlgorithmsImpl implements IAlgorithms {

    @Override
    public boolean matchPattern(String input, String pattern) {
        // ["hello", "world", "java"]
        String[] wordArray = input.split(" ");
        // ["A","B","C"]
        String[] patternArray = StringUtils.arrayCharToStr(pattern.toCharArray());

        // if pattern and string num is not matched, no compare any more.
        // e.g. hello world java ！= AB
        if (wordArray.length != patternArray.length) {
            return false;
        }

        Map<String, String> matchedMap = new HashMap<>();

        for (int i = 0; i < patternArray.length; i++) {
            String patternEntry = patternArray[i];
            String wordEntry = wordArray[i];

            if (matchedMap.containsKey(patternEntry)) {
                if (!matchedMap.get(patternEntry).equals(wordEntry)) {
                    // it means the patternEntry have maped a word but current word is not expected.
                    return false;
                }
            } else if (matchedMap.containsValue(wordEntry)) {
                // it means the current patternEntry match a word belong to other patternEntry.
                // so that's not ok.
                return false;
            } else {
                // the first time to map it.
                matchedMap.put(patternEntry, wordEntry);
            }
        }
        return true;
    }

    public boolean matchPattern2(String input, String pattern) {
        // ["hello", "world", "java"]
        String[] wordArray = input.split(" ");
        // ["A","B","C"]
        String[] patternArray = StringUtils.arrayCharToStr(pattern.toCharArray());

        // if pattern and string num is not matched, no compare any more.
        // e.g. hello world java ！= AB
        if (wordArray.length != patternArray.length) {
            return false;
        }

        for (int i = 0; i < patternArray.length; i++) {
            String patternEntry = patternArray[i];
            String wordEntry = wordArray[i];
            if (wordEntry.startsWith("**")) {
                if (!wordEntry.equals(patternEntry)) {
                    return false;
                }
            } else if (patternEntry.startsWith("**")) {
                return false;
            }
            
            for (int j = i; j < patternArray.length; j++) {
                if (wordArray[j].equals(wordEntry)) {
                    wordArray[j] = "**" + patternEntry;
                }
                if (patternArray[j].equals(patternEntry)) {
                    patternArray[j] = "**" + patternEntry;
                }
            }
        }
        return true;
    }
}

/**
* @Description: Algorithms Test Class
* @author bearfly1990
* @date Nov 30, 2018 9:42:29 PM
*/
package org.bearfly.fun.javalearn.algorithms;

import static org.junit.Assert.assertEquals;

import org.bearfly.fun.javalearn.algorithms.impl.AlgorithmsImpl;
import org.junit.Test;

public class AlgorithmsTest {
    @Test
    public void testMatchPattern() {
        IAlgorithms as = new AlgorithmsImpl();

        String input = "java hello world";
        String pattern = "ABC";
        assertEquals(true, as.matchPattern(input, pattern));

        input = "hello hello hello";
        pattern = "AAA";
        assertEquals(true, as.matchPattern(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABC";
        assertEquals(true, as.matchPattern(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABD";
        assertEquals(true, as.matchPattern(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABA";
        assertEquals(false, as.matchPattern(input, pattern));

        input = "java hello hello";
        pattern = "ABC";
        assertEquals(false, as.matchPattern(input, pattern));

        input = "java hello hello";
        pattern = "AB";
        assertEquals(false, as.matchPattern(input, pattern));

    }
    @Test
    public void testMatchPattern2() {
        AlgorithmsImpl as = new AlgorithmsImpl();

        String input = "java hello world";
        String pattern = "ABC";
        assertEquals(true, as.matchPattern2(input, pattern));

        input = "hello hello hello";
        pattern = "AAA";
        assertEquals(true, as.matchPattern2(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABC";
        assertEquals(true, as.matchPattern2(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABD";
        assertEquals(true, as.matchPattern2(input, pattern));

        input = "hello java hello java good";
        pattern = "ABABA";
        assertEquals(false, as.matchPattern2(input, pattern));

        input = "java hello hello";
        pattern = "ABC";
        assertEquals(false, as.matchPattern2(input, pattern));

        input = "java hello hello";
        pattern = "AB";
        assertEquals(false, as.matchPattern2(input, pattern));

    }
}

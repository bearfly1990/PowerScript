### Compare tables in different DB
There is a requirment that my partner want to compare values between two tables at different SqlServer DB.

So I find an example code in web and enhance it to fit my situation, and there is a precondition that the table should have the id.
And the result is the unmatched id.

I will update it better if I'm free.

```Java
package com.ssgx.pamreport.test.dbcompare.dao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ComparisonTest {
    public static void main(String[] args) throws SQLException {
        ComparisonTest ct = new ComparisonTest();
        //My own DAO class, just to get the connection.
        SqlServerDAO sd1 = new SqlServerDAO();
        SqlServerDAO2 sd2 = new SqlServerDAO2();

        sd1.getConnection();
        sd2.getConnection();
        
        ct.compareTable(sd1.conn, sd2.conn, "tblBusinessView");
        System.out.println("----------------");
        ct.compareTable(sd1.conn, sd2.conn, "tblMart");
        System.out.println("----------------");
        ct.compareTable(sd1.conn, sd2.conn, "tblMartElement", "physical_name", "display_name", "type");

    }
    /**
     * The main process method to compare two tables with several columns(default is all columns)
     * @param conn1
     * @param conn2
     * @param tableName
     * @param columns
     * @throws SQLException
     */
    public void compareTable(Connection conn1, Connection conn2, String tableName, String... columns) throws SQLException {

        ResultSet sourceResultSet;
        ResultSet targetResultSet;
        sourceResultSet = getResultSet(conn1, tableName, columns);
        targetResultSet = getResultSet(conn2, tableName, columns);

        Map<Long, String> sourceIdHash = new HashMap<Long, String>();
        Map<Long, String> targetIdHash = new HashMap<Long, String>();

        try {
            long rows = 0;
            do {
                // from source to target
                if (sourceResultSet.next()) {
                    if (targetResultSet.next()) {
                        // get the hash value for each record
                        long sourceHash = hash(getRowValues(sourceResultSet, sourceResultSet.getMetaData()));
                        long targetHash = hash(getRowValues(targetResultSet, targetResultSet.getMetaData()));
                        // put the hash as KEY and the id in the source table as VALUE
                        // if there is conflict, increase the hash value (I treat it have 11 conflict at most)
                        if (sourceIdHash.containsKey(sourceHash)) {
                            sourceIdHash.put(sourceHash + 1, sourceResultSet.getString(1));
                        } else {
                            sourceIdHash.put(sourceHash, sourceResultSet.getString(1));
                        }

                        if (targetIdHash.containsKey(targetHash)) {
                            targetIdHash.put(targetHash + 1, targetResultSet.getString(1));
                        } else {
                            targetIdHash.put(targetHash, targetResultSet.getString(1));
                        }

                        // remove the map if there is mapped hash code
                        // remove from the last conflict first, assume 11 at most.
                        // if the table are totally the same, the code below should work any time
                        if (targetIdHash.containsKey(sourceHash)) {
                            for (int i = 10; i >= 0; i--) {
                                if (targetIdHash.containsKey(sourceHash + i)) {
                                    targetIdHash.remove(sourceHash + i);
                                    break;
                                }
                            }

                            for (int i = 10; i >= 0; i--) {
                                if (sourceIdHash.containsKey(sourceHash + i)) {
                                    sourceIdHash.remove(sourceHash + i);
                                    break;
                                }
                            }
                        }

                        if (sourceIdHash.containsKey(targetHash)) {
                            for (int i = 10; i >= 0; i--) {
                                if (targetIdHash.containsKey(targetHash + i)) {
                                    targetIdHash.remove(targetHash + i);
                                    break;
                                }
                            }

                            for (int i = 10; i >= 0; i--) {
                                if (sourceIdHash.containsKey(targetHash + i)) {
                                    sourceIdHash.remove(targetHash + i);
                                    break;
                                }
                            }
                        }

                    } else {
                        // Add the source row
                        // if process go here, it means the target table record size is larger than source
                        long sourceHash = hash(getRowValues(sourceResultSet, sourceResultSet.getMetaData()));
                        if (sourceIdHash.containsKey(sourceHash)) {
                            sourceIdHash.put(sourceHash + 1, sourceResultSet.getString(1));
                        } else {
                            sourceIdHash.put(sourceHash, sourceResultSet.getString(1));
                        }
                    }
                } else {
                    if (targetResultSet.next()) {
                        // Add the target row
                        // if process go here, it means the target table record size is larger than source
                        long targetHash = hash(getRowValues(targetResultSet, targetResultSet.getMetaData()));
                        if (targetIdHash.containsKey(targetHash)) {
                            targetIdHash.put(targetHash + 1, targetResultSet.getString(1));
                        } else {
                            targetIdHash.put(targetHash, targetResultSet.getString(1));
                        }
                    } else {
                        break;
                    }
                }
                if (rows++ % 1000 == 0) {
                    System.out.println("Rows : " + rows);
                }
            } while (true);
        } finally {
            closeAll(sourceResultSet);
            closeAll(targetResultSet);
        }

        List<Long> repeatList = new ArrayList<Long>();
        //remove the same records from target hash map
        //also add the info to repeatList
        //print the unique record id in source table
        for (final Map.Entry<Long, String> mapEntry : sourceIdHash.entrySet()) {
            if (targetIdHash.containsKey(mapEntry.getKey())) {
                targetIdHash.remove(mapEntry.getKey());
                repeatList.add(mapEntry.getKey());
                continue;
            }
            System.out.println("Only in Source : " + mapEntry.getValue());
        }

        // print the unique record id in target table
        for (final Map.Entry<Long, String> mapEntry : targetIdHash.entrySet()) {
           /* if (sourceIdHash.containsKey(mapEntry.getKey())) {
                sourceIdHash.remove(mapEntry.getKey());
                continue;
            }*/

            System.out.println("Only in Target : " + mapEntry.getValue());
        }
        
        // remove the repeated record in the source table
        for(long idKey : repeatList){
            if(sourceIdHash.containsKey(idKey)){
                sourceIdHash.remove(idKey);
            }
        }

        System.out.println("In source and not target : " + sourceIdHash.size());
        System.out.println("In target and not source : " + targetIdHash.size());
    }

    private ResultSet getResultSet(final Connection connection, final String tableName, final String... columns) {
        String columnStr = "";
        if (columns.length == 0) {
            columnStr = "*";
        } else {
            columnStr = "id";
        }
        for (String column : columns) {
            columnStr = columnStr + "," + column;
        }

        String query = String.format("select %s from %s", columnStr, tableName);

        return executeQuery(connection, query);
    }

    private Object[] getRowValues(final ResultSet resultSet, final ResultSetMetaData resultSetMetaData)
            throws SQLException {
        List<Object> rowValues = new ArrayList<Object>();
        for (int i = 2; i < resultSetMetaData.getColumnCount(); i++) {
            rowValues.add(resultSet.getObject(i));
        }
        return rowValues.toArray(new Object[rowValues.size()]);
    }

/*    private final Connection getConnection(final String url, final String user, final String password,
            final Class<? extends Driver> driverClass) {
        try {
            DriverManager.registerDriver(driverClass.newInstance());
            return DriverManager.getConnection(url, user, password);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }*/

    private final ResultSet executeQuery(final Connection connection, final String query) {
        try {
            return connection.createStatement().executeQuery(query);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    private final Long hash(final Object... objects) {
        StringBuilder builder = new StringBuilder();
        for (Object object : objects) {
            builder.append(object);
        }
        return hash(builder.toString());
    }

    public Long hash(final String string) {
        // Must be prime of course
        long seed = 131; // 31 131 1313 13131 131313 etc..
        long hash = 0;
        char[] chars = string.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            hash = (hash * seed) + chars[i];
        }
        return Long.valueOf(Math.abs(hash));
    }

    private void closeAll(final ResultSet resultSet) {
        Statement statement = null;
        Connection connection = null;
        try {
            if (resultSet != null) {
                statement = resultSet.getStatement();
            }
            if (statement != null) {
                connection = statement.getConnection();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        close(resultSet);
        close(statement);
        close(connection);
    }

    private void close(final Statement statement) {
        if (statement == null) {
            return;
        }
        try {
            statement.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void close(final Connection connection) {
        if (connection == null) {
            return;
        }
        try {
            connection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void close(final ResultSet resultSet) {
        if (resultSet == null) {
            return;
        }
        try {
            resultSet.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

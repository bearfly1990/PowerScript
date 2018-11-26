::mvn org.apache.maven.plugins:maven-dependency-plugin:2.5.1:get \
::  -DremoteRepositories=http://download.java.net/maven/2 \
::  -Dartifact=group:artifact:version \
::  -Ddest=c:\temp\*.jar

mvn org.apache.maven.plugins:maven-dependency-plugin:2.5.1:get -DremoteRepositories=https://mvnrepository.com/artifact/org.codehaus.groovy.modules.http-builder/http-builder -Dartifact=org.codehaus.groovy.modules.http-builder:http-builder:0.6 -Ddest=http-builder.0.6.jar
pause

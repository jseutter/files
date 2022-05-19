# Tips for Java development

### Maven and unit tests

Maven can be told to skip tests by passing -DskipUnitTests on the command line.
The tests will be compiled but not executed.

If the tests are failing to compile, -Dmaven.test.skip will remove them from
compilation.

### Properties files

If tests are failing to run because of missing properties, the properties can
be added to src/test/resources and it will be available on the classpath when
executing tests.

### Building with Maven

Maven is built around goals and phases.  Phases are part of a goal.
The default lifecycle has 23 phases.  The last phase is deploy

mvn deploy

will run all previous phases.  The preceding step is mvn install, which
installs it to the local maven repository (~/.m2/repository).

### Running Spring Boot App with Maven

mvnw spring-boot:run

### Building with Gradle

gradlew tasks

gradlew build or gradlew war to build just the war file

### Running SpringBoot project with gradle

gradlew bootRun

### Running Code in Jboss EAP

Download Jboss EAP from access.redhat.com
Unzip.
Run bin/standalone.bat
Access http://127.0.0.1:9990
If needed, run add-user.bat



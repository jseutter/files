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

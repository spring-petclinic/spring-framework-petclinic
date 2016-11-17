# Spring PetClinic Sample Application [![Build Status](https://travis-ci.org/spring-petclinic/spring-framework-petclinic.svg?branch=master)](https://travis-ci.org/spring-petclinic/spring-framework-petclinic/)

Approved by the Spring team, this repo is a fork of the [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic).
It allows the Spring community to maintain the [legacy branch](https://github.com/spring-projects/spring-petclinic/tree/legacy).
By legacy, we are speaking about building an application without Spring Boot (i.e. plain old Spring Framework configuration) 
and with a 3-layer architecture (i.e. presentation --> service --> repository).
The original repo will now focus on the Spring Boot version of Spring Petclinic and has moved to [aggregate-oriented domain]([https://github.com/spring-projects/spring-petclinic/pull/200).


## Understanding the Spring Petclinic application with a few diagrams
<a href="https://speakerdeck.com/michaelisvy/spring-petclinic-sample-application">See the presentation here</a>

## Running petclinic locally
```
	git clone https://github.com/spring-petclinic/spring-framework-petclinic.git
	cd spring-petclinic
	./mvnw tomcat7:run
```

You can then access petclinic here: http://localhost:9966/petclinic/

<img width="1042" alt="petclinic-screenshot" src="https://cloud.githubusercontent.com/assets/838318/19727082/2aee6d6c-9b8e-11e6-81fe-e889a5ddfded.png">

## In case you find a bug/suggested improvement for Spring Petclinic
Our issue tracker is available here: https://github.com/spring-petclinic/spring-framework-petclinic/issues


## Database configuration

In its default configuration, Petclinic uses an in-memory database (HSQLDB) which
gets populated at startup with data.
A similar setups is provided for MySql and PostgreSQL in case a persistent database configuration is needed.
To run petclinic locally using persistent database, it is needed to run with profile defined in main pom.xml file.

For MySQL database, it is needed to run with 'MySQL' profile defined in main pom.xml file.

```
./mvnw tomcat7:run -P MySQL
```

Before do this, would be good to check properties defined in MySQL profile inside pom.xml file.

```
<properties>
    <jpa.database>MYSQL</jpa.database>
    <jdbc.driverClassName>com.mysql.jdbc.Driver</jdbc.driverClassName>
    <jdbc.url>jdbc:mysql://localhost:3306/petclinic?useUnicode=true</jdbc.url>
    <jdbc.username>root</jdbc.username>
    <jdbc.password>petclinic</jdbc.password>
</properties>
```      

You may also start a MySql database with docker:

```
docker run --name mysql-petclinic -e MYSQL_ROOT_PASSWORD=petclinic -e MYSQL_DATABASE=petclinic -p 3306:3306 mysql:5.7.8
```

For PostgreSQL database, it is needed to run with 'PostgreSQL' profile defined in main pom.xml file.

```
./mvnw tomcat7:run -P PostgreSQL
```

Before do this, would be good to check properties defined in PostgreSQL profile inside pom.xml file.

```
<properties>
    <jpa.database>POSTGRESQL</jpa.database>
    <jdbc.driverClassName>org.postgresql.Driver</jdbc.driverClassName>
    <jdbc.url>jdbc:postgresql://localhost:5432/petclinic</jdbc.url>
    <jdbc.username>postgres</jdbc.username>
    <jdbc.password>petclinic</jdbc.password>
</properties>
```
You may also start a Postgres database with docker:

```
docker run --name postgres-petclinic -e POSTGRES_PASSWORD=petclinic -e POSTGRES_DB=petclinic -p 5432:5432 -d postgres:9.6.0
```

## Working with Petclinic in Eclipse/STS

### prerequisites
The following items should be installed in your system:
* Maven 3 (http://www.sonatype.com/books/mvnref-book/reference/installation.html)
* git command line tool (https://help.github.com/articles/set-up-git)
* Eclipse with the m2e plugin (m2e is installed by default when using the STS (http://www.springsource.org/sts) distribution of Eclipse)

Note: when m2e is available, there is an m2 icon in Help -> About dialog.
If m2e is not there, just follow the install process here: http://eclipse.org/m2e/download/


### Steps:

1) In the command line
```
git clone https://github.com/spring-petclinic/spring-framework-petclinic.git
```
2) Inside Eclipse
```
File -> Import -> Maven -> Existing Maven project
```


## Looking for something in particular?

| Java Config |   |
|-------------|---|
| Java config branch | Petclinic uses XML configuration by default. In case you'd like to use Java Config instead, there is a Java Config branch available [here](https://github.com/spring-petclinic/spring-framework-petclinic/tree/javaconfig) |

| Inside the 'Web' layer | Files |
|------------------------|-------|
| Spring MVC - XML integration | [mvc-view-config.xml](src/main/resources/spring/mvc-view-config.xml)  |
| Spring MVC - ContentNegotiatingViewResolver| [mvc-view-config.xml](src/main/resources/spring/mvc-view-config.xml) |
| JSP custom tags | [WEB-INF/tags](src/main/webapp/WEB-INF/tags), [createOrUpdateOwnerForm.jsp](src/main/webapp/WEB-INF/jsp/owners/createOrUpdateOwnerForm.jsp)|
| Bower Maven profile | [The bower-install maven profile is declared into the pom.xml](pom.xml). 
| JavaScript dependencies | [JavaScript libraries are defined by the manifest file bower.json](bower.json) |
| Bower configuration | [Bower configuration using JSON](.bowerrc) |
| Static resources config | [Resource mapping in Spring configuration](/src/main/resources/spring/mvc-core-config.xml#L30) |
| Static resourcs usage | [staticFiles.jsp](src/main/webapp/WEB-INF/jsp/fragments/staticFiles.jsp#L12) |
| Thymeleaf | In the late 2016, the original [Spring Petclinic](https://github.com/spring-projects/spring-petclinic) has moved from JSP to Thymeleaf. |

| 'Service' and 'Repository' layers | Files |
|-----------------------------------|-------|
| Transactions | [business-config.xml](src/main/resources/spring/business-config.xml), [ClinicServiceImpl.java](src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java) |
| Cache | [tools-config.xml](src/main/resources/spring/tools-config.xml), [ClinicServiceImpl.java](src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java) |
| Bean Profiles | [business-config.xml](src/main/resources/spring/business-config.xml), [ClinicServiceJdbcTests.java](src/test/java/org/springframework/samples/petclinic/service/ClinicServiceJdbcTests.java), [PetclinicInitializer.java](src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java) |
| JDBC | [business-config.xml](src/main/resources/spring/business-config.xml), [jdbc folder](src/main/java/org/springframework/samples/petclinic/repository/jdb) |
| JPA | [business-config.xml](src/main/resources/spring/business-config.xml), [jpa folder](src/main/java/org/springframework/samples/petclinic/repository/jpa) |
| Spring Data JPA | [business-config.xml](src/main/resources/spring/business-config.xml), [springdatajpa folder](src/main/java/org/springframework/samples/petclinic/repository/springdatajpa) |


## Interaction with other open source projects

One of the best parts about working on the Spring Petclinic application is that we have the opportunity to work in direct contact with many Open Source projects. We found some bugs/suggested improvements on various topics such as Spring, Spring Data, Bean Validation and even Eclipse! In many cases, they've been fixed/implemented in just a few days.
Here is a list of them:

| Name | Issue |
|------|-------|
| Spring JDBC: simplify usage of NamedParameterJdbcTemplate | [SPR-10256](https://jira.springsource.org/browse/SPR-10256) and [SPR-10257](https://jira.springsource.org/browse/SPR-10257) |
| Bean Validation / Hibernate Validator: simplify Maven dependencies and backward compatibility |[HV-790](https://hibernate.atlassian.net/browse/HV-790) and [HV-792](https://hibernate.atlassian.net/browse/HV-792) |
| Spring Data: provide more flexibility when working with JPQL queries | [DATAJPA-292](https://jira.springsource.org/browse/DATAJPA-292) |
| Dandelion: improves the DandelionFilter for Jetty support | [113](https://github.com/dandelion/dandelion/issues/113) |


# Contributing

The [issue tracker](/issues) is the preferred channel for bug reports, features requests and submitting pull requests.

For pull requests, editor preferences are available in the [editor config](.editorconfig) for easy use in common text editors. Read more and download plugins at <http://editorconfig.org>.





# Build stage: Compile and package the application
FROM maven:3.9.7-eclipse-temurin-17 AS builder
WORKDIR /app
RUN git clone https://github.com/spring-petclinic/spring-framework-petclinic.git
WORKDIR /app/spring-framework-petclinic
RUN mvn clean package -DskipTests

# Runtime stage: Deploy the WAR file to Tomcat
FROM tomcat:10.1
WORKDIR /usr/local/tomcat/webapps/
COPY --from=builder /app/spring-framework-petclinic/target/*.war ./petclinic.war

# Expose the default Tomcat port
EXPOSE 8080

# Start Tomcat server
CMD ["catalina.sh", "run"]
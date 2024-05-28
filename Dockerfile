FROM tomcat:11.0.0-M11-jdk21-openjdk-bookworm
COPY target/petclinic.war /usr/local/tomcat/webapps

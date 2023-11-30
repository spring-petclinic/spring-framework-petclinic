FROM sapmachine:17-jre-ubuntu
WORKDIR /usr/local
RUN apt-get update -y
RUN apt-get install wget -y
RUN wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.1.16/bin/apache-tomcat-10.1.16.tar.gz
RUN tar -xvzf apache-tomcat-10.1.16.tar.gz
RUN mv apache-tomcat-10.1.16 tomcat
RUN rm -rf tomcat/webapps/ROOT*

COPY ROOT.war /usr/local/tomcat/webapps/

WORKDIR /usr/local/tomcat

EXPOSE 8080

ENTRYPOINT ["./bin/catalina.sh", "run"]


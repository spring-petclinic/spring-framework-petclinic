#!/bin/bash

echo "Update dependencies..."
sudo apt update

echo "Install OpenJDK 11..."
sudo apt install -y openjdk-11-jdk

echo "Checking Java version..."
java -version

echo "Create a user for Tomcat"
sudo useradd -m -U -d /opt/tomcat -s /bin/false tomcat

echo "Download tomcat"
VERSION=9.0.53
wget https://dlcdn.apache.org/tomcat/tomcat-9/v${VERSION}/bin/apache-tomcat-${VERSION}.tar.gz -P /tmp

sudo tar -xf /tmp/apache-tomcat-${VERSION}.tar.gz -C /opt/tomcat/
sudo ln -s /opt/tomcat/apache-tomcat-${VERSION} /opt/tomcat/latest
sudo chown -R tomcat: /opt/tomcat
sudo sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh'

echo "Added your user to tomcat group"
usermod -a -G as-is-user tomcat
chmod 775 -R /opt/tomcat/

cat > /etc/systemd/system/tomcat.service <<EOL
[Unit]
Description=Tomcat 9 servlet container
After=network.target

[Service]
Type=forking

User=tomcat
Group=tomcat

Environment="JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom -Djava.awt.headless=true"

Environment="CATALINA_BASE=/opt/tomcat/latest"
Environment="CATALINA_HOME=/opt/tomcat/latest"
Environment="CATALINA_PID=/opt/tomcat/latest/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"

ExecStart=/opt/tomcat/latest/bin/startup.sh
ExecStop=/opt/tomcat/latest/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
EOL

cat /etc/systemd/system/tomcat.service

echo "Reload daemon..."
sudo systemctl daemon-reload

echo "Enable and start Tomcat service"
sudo systemctl enable --now tomcat

echo "Check the service status"
sudo systemctl status tomcat

echo "Configuring firewall"
sudo ufw allow 8080/tcp


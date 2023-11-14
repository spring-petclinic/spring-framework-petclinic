package org.springframework.samples.petclinic;

import org.apache.catalina.startup.Tomcat;
import org.springframework.web.context.support.AnnotationConfigWebApplicationContext;
import org.springframework.web.servlet.DispatcherServlet;

import java.io.File;

public class TomcatServer {

    public static void main(String[] args) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(8081);
        tomcat.getConnector();
        tomcat.setBaseDir(System.getProperty("java.io.tmpdir"));
        tomcat.addWebapp("", new File("src/main/webapp").getAbsolutePath());

        // AnnotationConfigWebApplicationContext spring = new AnnotationConfigWebApplicationContext();
        // tomcat.addServlet("", "dispatcher", new DispatcherServlet(spring)).addMapping("/");

        tomcat.start();
        tomcat.getServer().await();
    }
}

node('JDK-11') {
    stage('vcs') {
        git branch: 'REL_INT_1.0', url: 'https://github.com/satishnamgadda/spring-framework-petclinic.git'
    }
    stage("build") {
        sh '/usr/share/maven/bin/mvn package'
    }
    stage("archive results") {
        junit '**/surefire-reports/*.xml'

    }
}
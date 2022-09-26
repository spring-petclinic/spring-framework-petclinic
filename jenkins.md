scripted pipeline:
----------------------------------------------------------------
pipeline script :
 pipeline{   
    agent {label 't2smalljdk_mvn'}
     stages {
         stage('spring_script') {
         steps{
         git url:'https://github.com/spring-petclinic/spring-framework-petclinic.git',
          branch: 'master'
        }
        }
 stage('bulid'){
 steps{
   sh 'mvn package'  
    }
    }
}
}

pipeline {
    agent any
     environment {
        VERSION = readMavenPom().getVersion()
    }
<<<<<<< HEAD

    stages {
=======
        stages {
>>>>>>> b4fad7477c9013a0bab6362aa0ef375b81091cf1
        stage('checkout') {
            steps {
               checkout scm                 
            }
        }
        stage('build') {
            steps {
                sh 'mvn clean package'
            }
        }
        
        stage('Push to Nexus') { 
           steps {
             nexusArtifactUploader artifacts: [[artifactId: 'spring-framework-petclinic', 
             classifier: '',
             file: 'target/petclinic.war', 
             type: 'war']], credentialsId: '0ce39687-e65a-4039-9d75-66e7db9e279e',
             groupId: 'org.springframework.samples', nexusUrl: 'localhost:8081',
             nexusVersion: 'nexus3', protocol: 'http', 
             repository: 'maven-repo-petclinic', 
             version:VERSION
            } 

        }

        stage('Create deployment package') {
            steps {
             xldCreatePackage artifactsPath: 'target/', darPath: 'petclinic-test.dar', manifestPath: 'deployit-manifest.xml'   
            }
        }
        stage('publish to xldDeploy') {
            steps {
                xldPublishPackage darPath: 'petclinic-test.dar', serverCredentials: 'admin -credentials'
            }
        }
         stage('deploy to xldDeploy') {
            steps {
<<<<<<< HEAD

       xldDeploy environmentId: 'Environments/QA-ENV', packageId: 'Applications/PetClinic-new/'+VERSION, serverCredentials: 'admin -credentials'

                
=======
       xldDeploy environmentId: 'Environments/QA-ENV', packageId: 'Applications/PetClinic-new/'+VERSION, serverCredentials: 'admin -credentials'
>>>>>>> b4fad7477c9013a0bab6362aa0ef375b81091cf1
       } 
         }
            
     }
        
    }
<<<<<<< HEAD
=======

>>>>>>> b4fad7477c9013a0bab6362aa0ef375b81091cf1
}


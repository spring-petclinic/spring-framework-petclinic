pipeline {
    agent any
     environment {
        VERSION = readMavenPom().getVersion()
    }
    stages {
        stages {
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
       xldDeploy environmentId: 'Environments/QA-ENV', packageId: 'Applications/PetClinic-new/'+VERSION, serverCredentials: 'admin -credentials'            

       } 
         }
            
     }
        
    }
}


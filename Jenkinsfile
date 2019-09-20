pipeline {
    agent any
    environment {
        VERSION = readMavenPom().getVersion()
           }
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
        stage('deployment package') {
            steps {
             xldCreatePackage artifactsPath: '/target/', darPath: 'petclinic-test.dar', manifestPath: 'deployit-manifest.xml'   
            }
        }
        stage('publish') {
            steps {
                xldPublishPackage darPath: 'petclinic-test.dar', serverCredentials: 'admin -credentials'
            }
        }
         stage('deploy') {
            steps {
                xldDeploy environmentId: 'Environments/QA-ENV', packageId: echo 'Applications/PetClinic-new/${env.VERSION}', serverCredentials: 'admin -credentials'
       } 
            
     }
        
    }
}

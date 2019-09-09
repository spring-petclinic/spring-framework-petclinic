pipeline {
    agent any
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
             xldCreatePackage artifactsPath: '/target/', darPath: 'petclinic-test2.0.dar', manifestPath: 'deployit-manifest.xml'   
            }
        }
        stage('publish') {
            steps {
                xldPublishPackage darPath: 'petclinic-test2.0.dar', serverCredentials: 'admin -credentials'
            }
        }
         stage('deploy') {
            steps {
        xldDeploy environmentId: 'Environments/QA-ENV', packageId: 'Applications/xld project/PetClinic2.0', serverCredentials: 'admin -credentials'
       } 
            
     }
        
    }
}

pipeline {
    agent  { label 'JDK11' }
      parameters {
        choice(name: 'CHOICE', choices: ['REL_INT_1.0'], description: 'CHOICE')
        string(name: 'MAVEN_GOAL', defaultValue: 'package', description: 'mvn goal') 
        
      }
        
    stages {
        stage('vcs') {
            steps {
                git branch: "${params.CHOICE}", url: 'https://github.com/satishnamgadda/spring-framework-petclinic.git'
            }

        }
        stage('build') {
            steps {
                sh "/usr/share/maven/bin/mvn ${params.MAVEN_GOAL}"
            }
        }
        stage('artifacts') {
            steps {
            archiveArtifacts artifacts: 'target/*.war', followSymlinks: false
            }
        }
        stage('archive results') {
            steps {
                junit '**/surefire-reports/*.xml'
            }
        }
    }
    
}
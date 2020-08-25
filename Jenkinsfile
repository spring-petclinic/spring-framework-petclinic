pipeline {
    agent any

    tools {
        maven "Maven"
    }

    stages {
        stage('verify'){
            steps {
                sh 'mvn -v'
            }
        }
        
        stage('compile'){
            steps{
                sh 'mvn clean compile'
            }
        }
        
        stage('test'){
            steps {
                sh 'mvn test'
            }
            post {
               success {
            		junit '**/target/surefire-reports/TEST-*.xml'
            	}
            }
        }
    }
    post {
        success {
            slackSend channel: 'jenkins-training', teamDomain: 'devinstitut', tokenCredentialId: 'token-slack', message: 'robin-success'
            discordSend description: 'Success - robin', footer: '', image: '', link: '', result: 'SUCCESS', thumbnail: '', title: 'Petclinic', webhookURL: 'https://discordapp.com/api/webhooks/747819422705778738/dHWPHidlNLpiiKftWU84__Ss2LAkws77Swfdk5OWs22qla3hlI1B4zywW8ROg4nAwjRM'
        }
        failure {
            slackSend channel: 'jenkins-training', teamDomain: 'devinstitut', tokenCredentialId: 'token-slack', message: 'robin-fail'
            discordSend description: 'Failure - robin', footer: '', image: '', link: '', result: 'FAILURE', thumbnail: '', title: 'Petclinic', webhookURL: 'https://discordapp.com/api/webhooks/747819422705778738/dHWPHidlNLpiiKftWU84__Ss2LAkws77Swfdk5OWs22qla3hlI1B4zywW8ROg4nAwjRM'
        }
    }
}
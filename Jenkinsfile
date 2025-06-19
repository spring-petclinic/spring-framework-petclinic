
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {Add commentMore actions
                echo "Checking out branch: ${env.BRANCH_NAME}"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                // your build commands here, eg:
                sh './gradlew build'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // your test commands here
                sh './gradlew test'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying application...'
                // deployment steps
                sh './deploy.sh'
            }
        }
    }

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

/*        stage('publish to nexus') {
            steps {
                script {
                    // Read POM xml file using 'readMavenPom' step , this step 'readMavenPom' is included in: https://plugins.jenkins.io/pipeline-utility-steps
                    pom = readMavenPom file: "pom.xml";
                    // Find built artifact under target folder
                    filesByGlob = findFiles(glob: "target/*.${pom.packaging}");
                    // Print some info from the artifact found
                    echo "${filesByGlob[0].name} ${filesByGlob[0].path} ${filesByGlob[0].directory} ${filesByGlob[0].length} ${filesByGlob[0].lastModified}"
                    // Extract the path from the File found
                    artifactPath = filesByGlob[0].path;
                    // Assign to a boolean response verifying If the artifact name exists
                    artifactExists = fileExists artifactPath;
                    if(artifactExists) {
                        echo "*** File: ${artifactPath}, group: ${pom.groupId}, packaging: ${pom.packaging}, version ${pom.version}";
                        nexusArtifactUploader(
                            nexusVersion: NEXUS_VERSION,
                            protocol: NEXUS_PROTOCOL,
                            nexusUrl: NEXUS_URL,
                            groupId: pom.groupId,
                            version: pom.version,
                            repository: NEXUS_REPOSITORY,
                            credentialsId: NEXUS_CREDENTIAL_ID,
                            artifacts: [
                                // Artifact generated such as .jar, .ear and .war files.
                                [artifactId: pom.artifactId,
                                classifier: '',
                                file: artifactPath,
                                type: pom.packaging],
                                // Lets upload the pom.xml file for additional information for Transitive dependencies
                                [artifactId: pom.artifactId,
                                classifier: '',
                                file: "pom.xml",
                                type: "pom"]
                            ]
                        );
                    } else {
                        error "*** File: ${artifactPath}, could not be found";
                    }
                
                }
            }
        }*/

      stage('Push to Nexus') { 
      steps {
             nexusArtifactUploader artifacts: [[artifactId: 'spring-framework-petclinic', classifier: '', file: 'target/petclinic.war', type: 'war']], credentialsId: '0ce39687-e65a-4039-9d75-66e7db9e279e', groupId: 'org.springframework.samples', nexusUrl: 'localhost:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'petclinic-repo', version:'5.1.1'
       } 

      }

        stage('deployment package') {
            steps {
             xldCreatePackage artifactsPath: 'target/', darPath: 'petclinic-test.dar', manifestPath: 'deployit-manifest.xml'   
            }
        }

        stage('publish') {
            steps {
                xldPublishPackage darPath: 'petclinic-test.dar', serverCredentials: 'admin -credentials'
            }
        }
         stage('deploy') {
            steps {
       xldDeploy environmentId: 'Environments/QA-ENV', packageId: 'Applications/PetClinic-new/5.1.1', serverCredentials: 'admin -credentials'
       } 
            
     }
        
    }
}

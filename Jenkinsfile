pipeline {
    agent {label "slave1"}
    
    stages {
        stage('GitSCM') {
            steps {
                checkout([
                $class: 'GitSCM',
//branches - can add more than 1 branch
                branches: [[name: 'main']],
//add the usrl for the branch you want to coonect to, adding the ssh url or https???
                userRemoteConfigs: [[
                    url: 'https://github.com/PokiBal/MyProject_1.git',
                    credentialsId: ''
                ]]
            ])
         }
    }
        stage('Build DockerImage'){
            steps{
                sh 'docker build -t flask_docker .'
                sh 'docker run -p 5000:5000 -d flask_docker'
            }
        }
        stage('Test_Save') {
            steps {
                script {
                    ip = Curl https://checkip.amazonaws.com
                    def response = httpRequest url: f"{ip}:5000"
                    strResult = ''
                    if (response.status == 200) {
                        strResult = "Success" 
                    } 
                    else {
                        error 'Unexpected response status code'
                        strResult = "Failed" 
                    }
                def my_dict = ["message": strResult]
                writeJSON(file: 'result.json', json: my_dict)
                }
            }
        }

        stage('UploadToS3Bucket') {
            steps {
                echo "UploadToS3Bucket"
            }
        }
}
}



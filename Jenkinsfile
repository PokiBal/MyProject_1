pipeline {
    agent {label "slave1"}
    environment {
        TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
    }

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
        stage("build user") {
            steps{
                wrap([$class: 'BuildUser', useGitAuthor: true]) {
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    def strResult = sh(returnStdout: true, script: 'curl -IsS https://checkip.amazonaws.com | grep HTTP || true')
                    if (strResult.trim() == "HTTP/1.1 200 OK") {
                        _testResults = "Success" 
                    } 
                    else {
                        error 'Unexpected response status code - HTTP/1.1 404 Not Found'
                        _testResults = "Failed" 
                    }
                }
            }
        }

        stage('SaveResultsToJson'){
            steps {
                script{
                def data = [:]
                data['time'] = sh 'echo "$TIME"'
                data['username'] = sh 'echo ${BUILD_USER}'
                data['testresult'] = _testResults
                def json = new groovy.json.JsonSlurperClassic().toJson(data)
                sh "echo '${json}' > TestResullt.json"
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

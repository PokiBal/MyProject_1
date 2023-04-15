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
        stage('SaveResultsToJson'){
            steps {
                script{
                import groovy.json.JsonBuilder
                //writeJSON(file: 'testResults.json', json: testResults)
                
                def data = [:]
                data['time'] = sh 'echo "$TIME"'
                data['username'] = sh 'echo ${BUILD_USER}'
                data['date'] = sh(script: 'date "+%Y-%m-%d"', returnStdout: true).trim()
                def json = new JsonBuilder(data)
                sh "echo '${json.toPrettyString()}' > TestResullt.json"
                }
            }
        }

        stage('SaveResultsToJson'){
            steps {
                script{
                import groovy.json.JsonBuilder
                //writeJSON(file: 'testResults.json', json: testResults)
                
                def data = [:]
                data['time'] = sh 'echo "$TIME"'
                data['username'] = sh 'echo ${BUILD_USER}'
                data['date'] = sh(script: 'date "+%Y-%m-%d"', returnStdout: true).trim()
                def json = new JsonBuilder(data)
                sh "echo '${json.toPrettyString()}' > TestResullt.json"
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

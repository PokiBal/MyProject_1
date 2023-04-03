pipeline {
    agent {lable "slave1"}
    
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
        stage('Test') {
            steps {
                echo "this is a test"
            }
        }
        stage('Build DockerImage'){
            steps{
                sh 'docker build -t flask_docker .'
                sh 'docker run -p 5000:5000 -d flask_docker'
            }
        }
}
}


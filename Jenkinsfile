pipeline {
    agent {label "slave1"}
    environment {
        TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
    }

    parameters {
        string(name: 'imagename', defaultValue: '', description: 'Name of the Docker image')
        string(name: 'imagetag', defaultValue: '', description: 'Image tag for Docker build')
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
                echo "build image"
                sh "docker build -t ${params.imagenam}:${params.imagetag} ."
                sh "docker run -p 5000:5000 -d --name my-flask-container ${params.imagename}"
            }
        }
        stage('Run Container'){
            steps{
                echo "build image"
            }
        }
        stage("build user") {
            steps{
                wrap([$class: 'BuildUser', useGitAuthor: true]) {
                    sh "export USERNAME=${BUILD_USER}"
                }
            }
        }

        stage('Test') {
            steps {
                echo "test"
            }
        }

        stage('UploadToS3Bucket') {
            steps {
                echo "UploadToS3Bucket"
            }
        }
    }
}

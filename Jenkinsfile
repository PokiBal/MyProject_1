pipeline {
    agent any
    
    stages {
        stage('GitSCM') {
            steps {
                checkout([
                $class: 'GitSCM',
//branches - can add more than 1 branch
                branches: [[name: 'main']],
//add the usrl for the branch you want to coמnect to, adding the ssh url 
                userRemoteConfigs: [[
                    url: 'git@github.com:PokiBal/MyProject_1.git',
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
   }
}

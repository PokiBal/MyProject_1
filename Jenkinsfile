pipeline {
    agent any
    
    stages {
        stage('GitSCM') {
            steps {
                checkout([
                $class: 'GitSCM',
                branchs: [[name: 'main']],
                userRemoteConfit : [[
                    url: 'git@github.com:PokiBal/MyProject_1.git'
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

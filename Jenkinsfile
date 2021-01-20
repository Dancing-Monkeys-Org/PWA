pipeline {
  agent any
  stages {
    stage('SCM') {
      steps {
        git(branch: 'release', credentialsId: 'SSH', poll: true, url: 'git@github.com:Dancing-Monkeys-Org/PWA.git')
      }
    }

    dir("${env.WORKSPACE}/src"){
      sh "pwd"

      stage('Build') {
        steps {
          sh 'docker-compose build'
        }
      }

      stage('Deploy') {
        steps {
            sh '''docker stop frontend
                  docker stop backend
                  docker-compose up -d'''
        }
      }
    }
  }
}
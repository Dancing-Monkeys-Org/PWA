pipeline {
  agent any
  stages {
    
    stage('SCM') {
      steps {
        git(branch: 'release', credentialsId: 'SSH', poll: true, url: 'git@github.com:Dancing-Monkeys-Org/PWA.git')
      }
    }

    stage('Build') {
      steps {
        dir("${env.WORKSPACE}/src"){
          sh 'docker-compose build'
        }
      }
    }

    stage('Deploy') {
      steps {
        dir("${env.WORKSPACE}/src"){
          sh '''docker stop frontend
                docker stop backend
                docker-compose up -d'''
        }
      }
    }

  }
}
pipeline {
  agent any
  stages {
    stage('SCM') {
      steps {
        git(branch: 'release', credentialsId: 'jenkins-generated-ssh-key', poll: true, url: 'git@github.com:Dancing-Monkeys-Org/PWA.git')
      }
    }

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
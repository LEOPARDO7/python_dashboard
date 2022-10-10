pipeline {
    
    agent any
    
      
    environment {
        WORKSPACE        =  pwd()
    }


     options { 
            buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
            skipDefaultCheckout()
            disableConcurrentBuilds()
    } 
     stages {
       stage('Cleanup Workspace'){
          steps {
               println "${env.BRANCH_NAME}"
               cleanWs()
               //clean up temp directory
               dir("${env.WORKSPACE}@tmp") {
                     deleteDir()
               }
               //clean up script directory
               dir("${env.WORKSPACE}@script") {
                     deleteDir()
               }
               dir("${env.WORKSPACE}@script@tmp") {
                     deleteDir()
               }
               step([$class: 'WsCleanup']) 
               }
               }
       stage('checkout code'){
          steps {
               
               git credentialsId: 'git_1', url: 'https://github.com/LEOPARDO7/python_dashboard.git'
               sh "ls"
               sh "pwd"
               }
               }  
       stage('push image'){
          steps {
              script{
               try {
               sh '''
                sudo docker build -t demo1:latest . 
               '''
              } catch(def exception){
                echo"Cathch error ${exception}"
                slackSend channel: "#indiatechteam", message: "Docker stage failed: ${env.JOB_NAME} ${env.BUILD_NUMBER} ${exception}"
                }
             }
           }
        }
    }
 }

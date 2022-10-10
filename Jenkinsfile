def COMMIT_MSGS = ''
def LIST = ''
def CONT_INST = ''
pipeline {
    
    agent any
    
    environment {
        WORKSPACE        =  pwd()
        NEXUS_SCRT      = credentials('nexus_Scrt')
        NEXUS_DOCRED    = credentials('nexusdocred')
        DOCKER_TKN   = credentials('Docker_lst_Tkn')
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



       
        
    }
 }

def COMMIT_MSGS = ''
def LIST = ''
def CONT_INST = ''
pipeline {
    
    agent any
    
    environment {
        GIT_BRANCH       = 'main'
        WORKSPACE        =  pwd()
        couchDB_URL		= 'https://couchdb.cloudzenix.online/'
		couch_api_svc	= 'cloudzenix'
        sonar_url       = 'https://sonar.cloudzenix.online/dashboard?id=com.mt%3Aspring-boot-mongo'
		couchDB_env		= 'czdevelopment'
        NEXUS_SCRT      = credentials('nexus_Scrt')
        IMAGE_NAME      = "ec2-18-208-6-67.compute-1.amazonaws.com:8084/python-application"
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
         stage('checkout code'){
            steps {
               
               git credentialsId: 'python_dashboard_app', url: 'https://vijaynimbalkar@bitbucket.org/cloudzenix/ec2-dashboard-python-app.git'
               }
               }   
         
         stage('sonarcodescan'){
            steps {
            withSonarQubeEnv('Sonar') {
              sh "/opt/sonar-scanner/bin/sonar-scanner -Dsonar.projectKey=CZ-dashbord"
              }
            } 
         }
 
         stage("Auto-increment TAG") {
			steps {
				script {
              withCredentials([string(credentialsId: 'Couchdb_Sert', variable: 'Couchdb_Sert')]) {
   				sh '''
					ID=$(curl -k -s -u cloudzenix:${Couchdb_Sert} -X GET ${couchDB_URL}/${couch_api_svc}/${couchDB_env} | jq -r ._id)
					REV=$(curl -k -s -u cloudzenix:${Couchdb_Sert} -X GET ${couchDB_URL}/${couch_api_svc}/${couchDB_env} | jq -r ._rev)
					TAG_Major=$(curl -k -s -u cloudzenix:${Couchdb_Sert} -X GET ${couchDB_URL}/${couch_api_svc}/${couchDB_env} | jq -r .Tag_Major)
					TAG_Minor=$(curl -k -s -u cloudzenix:${Couchdb_Sert} -X GET ${couchDB_URL}/${couch_api_svc}/${couchDB_env} | jq -r .Tag_Minor)
					current_tag="$TAG_Major.$TAG_Minor"
					echo "current_tag: $current_tag"
					if [[ $TAG_Minor -le "98" ]]
					then
						echo "incrementing Minor value."
						TAG_Minor=$(($TAG_Minor+1))
						TAG="$TAG_Major.$TAG_Minor"
						echo "TAG after increment: $TAG"
					else
						echo "Minor tag exceeded 99. So, Incrementing Major value."
						TAG_Major=$(($TAG_Major+1))
						TAG_Minor="0"
						TAG="$TAG_Major.$TAG_Minor"
						echo "TAG after increment: $TAG"
					fi
					curl -k -s -u cloudzenix:${Couchdb_Sert} -X PUT "${couchDB_URL}/${couch_api_svc}/${couchDB_env}" -d "{\\"_id\\":\\"$ID\\",\\"_rev\\":\\"$REV\\",\\"Tag_Major\\":\\"$TAG_Major\\",\\"Tag_Minor\\":\\"$TAG_Minor\\",\\"TAG\\":\\"$TAG\\"}"
					'''
					env.TAG = sh(script: 'curl -k -s -u cloudzenix:${Couchdb_Sert} -X GET ${couchDB_URL}/${couch_api_svc}/${couchDB_env} | jq -r .TAG', returnStdout: true)
					env.TAG = "${couchDB_env}"+"-"+"${TAG}"
					echo "TAG Value: ${TAG}"
                    }
				}
			}
		}

		 stage('push image'){
          steps {
              script{
               try {
               sh '''
                docker build -t ${IMAGE_NAME}:${TAG} . --build-arg CONT_INST="${CONT_INST}"
                docker tag ${IMAGE_NAME}:${TAG} cloudzenix/python_dashboard_app
                docker login -u cloudzenix -p ${DOCKER_TKN}
                docker push cloudzenix/python_dashboard_app 
                docker login ec2-18-208-6-67.compute-1.amazonaws.com:8084 -u admin -p CloudZenix
                docker push ${IMAGE_NAME}:${TAG}
                echo ${IMAGE_NAME}
                echo ${TAG}
                echo cloudzenix/sample-spring-app > sysdig_secure_images
               '''
              } catch(def exception){
                echo"Cathch error ${exception}"
                slackSend channel: "#indiatechteam", message: "Docker stage failed: ${env.JOB_NAME} ${env.BUILD_NUMBER} ${exception}"
                }
             }
           }
        }


        stage("Deploy to EKS ") {
			steps {
                sh "kubectl delete -f sa.yaml -n default"
                sh "kubectl delete -f pod.yaml -n default"
                sh "kubectl delete -f service.yaml -n default"
                sh "kubectl apply -f sa.yaml -n default"
   			    sh "kubectl apply -f pod.yaml -n default"
   			    sh "kubectl apply -f service.yaml -n default"
                sleep time: 10000, unit: 'MILLISECONDS'
			 	sh "kubectl get svc"
				
             }
        }
        
    }
 }

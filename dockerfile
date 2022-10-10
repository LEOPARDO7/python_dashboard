FROM centos
RUN cd /etc/yum.repos.d/ && sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&  sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && yum -y install java
COPY ./myproject  /root/myproject
RUN yum install unzip -y
RUN yum install curl -y && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && yum install unzip -y && unzip awscliv2.zip && ./aws/install
RUN yum install python3 -y
RUN yum install epel-release -y
RUN yum install python3-pip
RUN pip3 --version
RUN pip3 install flask
RUN pip3 install boto3
RUN pip3 install requests
RUN pip3 install flask_session
RUN pip3 install --upgrade pip
RUN pip3 install setuptools_rust
ENTRYPOINT ["python3", "/root/myproject/myproject.py"]


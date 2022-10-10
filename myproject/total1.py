import boto3

def fun(a, f, t):
  if a == "Opssbx":
    accountid = "602011150591"
  elif a == "Main":
    accountid = "978322299160"
  elif a == "Devsbx":
    accountid = "459602490943"
  arn = "arn:aws:iam::"+accountid+":role/cz_devsbx_role"
  session_name = "example-role1"
  client = boto3.client("sts")
  response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
  temp_credentials = response["Credentials"]

  client = boto3.client('ce',
    aws_access_key_id=temp_credentials["AccessKeyId"],
    aws_secret_access_key=temp_credentials["SecretAccessKey"],
    aws_session_token=temp_credentials["SessionToken"],
    region_name="us-east-1")
  response = client.get_cost_and_usage(
    TimePeriod={
        'Start': f,
        'End': t
    },
    Granularity='MONTHLY',

    Metrics=[
        'AmortizedCost',
    ],

    GroupBy=[
        {
            'Type':'DIMENSION',
            'Key': 'SERVICE'
        },
    ]
)
  tr = " "
  for i in (response['ResultsByTime'][0]['Groups']):
    a = (i['Keys'])
    b = (i['Metrics']['AmortizedCost']['Amount'])
    if b!="0":
      tr += "<tr><td valign='top'>{}</td><td valign='top'>{}</td></tr>".format( a, b)



  #a = response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']
  body = '<body style="background-color:Chili Pepper">'
  header = '<h1 align="center">AWS EC2 Billing </h1>'
  back ='<center><input type="button" value="Go back!" onclick="history.back()"></center>'
  table = '<table border=1 align="center"><tr><th>Services</th><th>Amount in "$"</th></tr>'
  end = "</table>"
  end1 = '</body>'
  Fun1 = open("/root/myproject/templates/billing1.html","w")
  Fun1.write(header+body+table+tr+end+back+end1)
  Fun1.close()


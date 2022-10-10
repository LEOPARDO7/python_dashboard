import boto3

def fun(a, f, t):
  client = boto3.client('ce', region_name='us-east-1')
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
            'Key': 'INSTANCE_TYPE'
        },
    ],
    Filter={
        'Dimensions':{
            'Key': 'SERVICE',
            'Values': ['Amazon Elastic Compute Cloud - Compute'],
            'MatchOptions': ['EQUALS']
            }
        }

)
  tr = " "
  for i in (response['ResultsByTime'][0]['Groups']):
    a = i['Keys']
    b = i['Metrics']['AmortizedCost']['Amount']
    tr += "<tr><td valign='top'>{}</td><td valign='top'>{}</td></tr>".format( a, b)



  #a = response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']
  body = '<body style="background-color:Chili Pepper">'
  header = '<h1 align="center">AWS EC2 Billing </h1>'
  back ='<center><input type="button" value="Go back!" onclick="history.back()"></center>'
  table = '<table border=1 align="center"><tr><th>InstanceType</th><th>Amount in "$"</th></tr>'
  end = "</table>"
  end1 = '</body>'
  Fun1 = open("/root/myproject/templates/billing.html","w")
  Fun1.write(header+body+table+tr+end+back+end1)
  Fun1.close()

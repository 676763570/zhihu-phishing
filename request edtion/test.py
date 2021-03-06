from defs import *
from send_email import *
import json
import time

def Save_data(User_data,Completed,Wait_q):
    with open('User_data.json','w') as F:
        F.write(json.dumps(User_data))
    with open('Completed.txt','w') as F:
        F.write(json.dumps(Completed))
    with open('Wait_q.txt','w') as F:
        F.write(json.dumps(Wait_q))
    print('Saved sucess')
    send_email('Data Saved sucess')
def Load_data():
    with open('User_data.json','r') as F:
        User_data = json.loads(F.read())
    with open('Completed.txt','r') as F:
        Completed = json.loads(F.read())
    with open('Wait_q.txt','r') as F:
        Wait_q = json.loads(F.read())
    return User_data,Completed,Wait_q

try:
	User_data,Completed,Wait_q = Load_data()
	print('load data')
except:
	Fir_token = 'TechMonster'
	User_data = {}
	Completed = []
	Wait_q = []
	wait_q.append(Fir_token)

#parameters
test_time = True
viaual = False
act_limit = 1000


while True:
	start_t = time.time()
	try:
		success = True
		token = Wait_q[0]
		print(token,'Completed',len(Completed),'Wait_q',len(Wait_q))
		url = 'https://www.zhihu.com/people/'+token

		#判断用户合法
		exist = True
		r = Get_r(url)
		if len(re.findall(token,r.text)) == 0:
			exist = False
			success = False
			del Wait_q[0]

		if exist:
			user,res = Parse_user(url,test_time=test_time,visual=viaual,act_limit=act_limit)

			User_data[user] = res
			for u in User_data[user]['following']:
				if u['url_token'] not in Wait_q and u['url_token'] not in Completed:
					Wait_q.append(u['url_token'])
			del Wait_q[0]
			Completed.append(user)

	except Exception as e:
		print(e,'\n'*2)
		#send_email('demo stopped\n'+'Exception'+str(e))
		del Wait_q[0]
		success = False
		pass

	if success:
		end_t = time.time()
		print('\n',len(Completed),'th user cost',round((end_t-start_t)/60,2),'min','\n'*2)
		if(len(Completed)>200):
			break
Save_data(User_data,Completed,Wait_q)
#Python 3.7.4
#Make by: Lonely Dark

#Import modules:
import requests
from time import sleep, strftime
from random import randint
import threading

#Your token:
token='Token here:'

def post(token,fr_list_id):
	#Post in your wall
	message='This is auto message. Cleared friends: \n '+ str(fr_list_id[::]) + '\n \n Script finished at ' + strftime('%H:%M:%S') + ' ' + strftime('%x')
	requests.get('https://api.vk.com/method/wall.post', params={'access_token': token, 'v': '5.101','message': message}).json()
	with open('log.txt', 'a') as file:
		file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Request vk_api wall.post'+'\n')


def clear(token): 
	#Get friends
	fr_get_del=requests.get('https://api.vk.com/method/friends.get', params={'access_token': token, 'v': '5.101', 'fields': 'deactivated'}).json()
	with open('log.txt', 'a') as file:
		file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Request vk_api friends.get'+'\n')
	fr_get_del=fr_get_del['response']
	fr_list_id=[]
	#Get friend deleted or banned
	for i in fr_get_del['items']:
		if 'deactivated' in i:
			fr_list_id=[i['id']]
	#If in fr_list_id nothing:
	if len(fr_list_id)==0:
		print('Not found deactivated.')
		message='This is auto message. \n Not found friends deactivated, goodbye! \n \n Script finished at ' + strftime('%H:%M:%S') + ' ' + strftime('%x')
		requests.get('https://api.vk.com/method/wall.post', params={'access_token': token, 'v': '5.101', 'message': message}).json()
		with open('log.txt', 'a') as file:
			file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Nothing in fr_list_id, exit.'+'\n')

		return False
	else:
		#Else:
		for i in fr_list_id:
			#Delete friends banned or deleted
			requests.get('https://api.vk.com/method/friends.delete', params={'access_token': token, 'v': '5.101', 'user_id': i}).json()
			with open('log.txt', 'a') as file:
				file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Delete friend: @id' + str(i)+'\n')
			#Sleep random range 0,3 sec
			sleep(randint(0,3))
		#Add to fr_list_id @id	
		for i in range(len(fr_list_id)):
			fr_list_id[i]='@id'+str(fr_list_id[i])
		print('Delete: \n'+ str(fr_list_id[::]))
		#Run post()
		th=threading.Thread(target=post, args=(token,fr_list_id))
		with open('log.txt', 'a') as file:
				file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Run Thread post'+'\n')
		th.start()


main=threading.Thread(target=clear, args=(token,))
with open('log.txt', 'a') as file:
	file.write('[log]:'+'['+strftime('%H:%M:%S')+' '+strftime('%x')+']'+': '+'Run Thread main'+'\n')
main.start()
main.join()
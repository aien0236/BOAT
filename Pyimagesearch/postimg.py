import requests
def photo_send(imagename):   # send photo to website server
	url = 'https://71d2b2f7.ngrok.io/api/paint'
	datas = {'UserId': 1, 'ImageName' : imagename}
	files = {'Image': open(imagename, 'rb')}
	response = requests.post(url, datas, files = files)
	print(response.text)

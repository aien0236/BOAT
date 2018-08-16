def photo_send(imagename):   # send photo to website server
	url = 'https://cf44ab4a.ngrok.io/api/album/'
	datas = {'UserId': 1, 'ImageName' : imagename}
	files = {'Image': open('images/' + imagename + '.jpg', 'rb')}
	response = requests.post(url, datas, files = files)
	print(response.text)

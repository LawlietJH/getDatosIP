# -*- coding: utf-8 -*-

# By: LawlietJH
# Version: 1.0.0


import sys
import requests
from bs4 import BeautifulSoup


def getIPData(IP=''):
	
	def strToDict(string):
		dictionary = {}
		lista = string.split(',')
		for x in lista:
			x = x.strip()
			x, y = x.split(':')
			if x.startswith("'"): x = x[1:-1]
			if y.startswith("'"): y = y[1:-1]
			dictionary[x] = y
		return dictionary
	
	page = 'https://www.localizaip.com/localizar-ip.php/'
	params = {'ip': IP}
	
	try:
		req = requests.get(page, params=params)
	except requests.exceptions.ConnectionError:
		return {'Conexion':'Sin Conexion'}
	
	if req.status_code == 200:
		
		data = {}
		soup = BeautifulSoup(req.text, 'html.parser')
		datos = soup.find_all('span')[1]
		
		for x in datos:
			if 'array' in x:
				
				x = x.replace('countryCode', 'codigo')
				x = x.replace('countryName', 'pais')
				x = x.replace('city', 'ciudad')
				x = x.replace('latitude', 'latitud')
				x = x.replace('longitude', 'longitud')
				
				data = x.split('array(')[1]
				data = data.replace(' => ', ':')
				data = data.replace('\n','')
				data = data.split(',)')[0]
				data = strToDict(data)
				
				break
		
		datos = soup.find('input', {'name':'ip'})
		data['ip'] = unicode(datos).split('value="')[1].split('"')[0]
		
		return data


if len(sys.argv) == 2:
	
	IP = sys.argv[1]
	temp = IP.split('.')
	
	if len(temp) == 4:
		
		for x in temp:
			if not x.isdigit():
				print('\n\n\t IP No Valida.\n')
				sys.exit()
		
		data = getIPData(IP)

		print('\n\n')
		for x in data: print(x + ': ' + data[x])
	
	else: print('\n\n\t IP No Valida.\n')

elif len(sys.argv) == 1:
	
	data = getIPData()
	
	print('\n\n')
	for x in data: print(x + ': ' + data[x])
	
else:
	
	print('\n\n\t Modo de Uso: python getDatosIP.py 255.255.255.255\n')


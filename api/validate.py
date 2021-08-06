import requests
from geopy.geocoders import Nominatim


class Coordenadas:

	def __init__(self, cep: "É esperado um STRING"):
		self._cep = cep
		self._resultado = "error"

	@property
	def resultado(self):
		return self._resultado

	def valido(self):
		#Trata CEP's sem nada
		if (self._cep == "00000000"):
			return False
		else:
			#Consulta o CEP informado pelo usuário
			api = requests.get(f'https://viacep.com.br/ws/{self._cep}/json/')
			
			#Verifica se o CEP é válido
			if (api.status_code == 200) and (not 'erro' in api.json()):
				#Transforma os dados em Json
				endereco = api.json()
				#rua = endereco['logradouro']
				#bairro = endereco['bairro']
				#cidade = endereco['localidade']

				#Se o endereço não tiver bairro
				if (endereco['bairro'] == ""):
					geolocator = Nominatim(user_agent="geo_cep")
					location = geolocator.geocode(endereco['localidade'])
					if (location != None):
						self._resultado = {"latitude": location.latitude, "longitude": location.longitude, "Nivel": "Cidade"}
						return True
					else:
						self._resultado = {"error": "Não consegui identificar as coordenadas da região informada"}
						return False
				elif (endereco['logradouro'] != ""):
					geolocator = Nominatim(user_agent="geo_cep")
					location = geolocator.geocode(endereco['logradouro'] + ", " + endereco['localidade'] + " - " + endereco['bairro'])
					if (location != None):
						self._resultado = {"latitude": location.latitude, "longitude": location.longitude, "Nivel": "Rua"}
						return True
					else:
						location = geolocator.geocode(endereco['localidade'] + " - " + endereco['bairro'])
						if (location != None):
							self._resultado = {"latitude": location.latitude, "longitude": location.longitude, "Nivel": "Bairro"}
							return True
						else:
							self._resultado = {"error": "Não consegui identificar as coordenadas da região informada"}
							return False
				#Se tiver bairro e cidade
				else:
					geolocator = Nominatim(user_agent="geo_cep")
					location = geolocator.geocode(endereco['bairro'] + ", " + endereco['localidade'])
					try:
						geolocator = Nominatim(user_agent="geo_cep")
						location = geolocator.geocode(endereco['localidade'])
						self._resultado = {"Cidade": endereco['localidade'], "Bairro": endereco['bairro'], "Rua": endereco['logradouro'], "latitude": location.latitude, "longitude": location.longitude}
						return True
					except:
						self._resultado = {"error": "Não consegui identificar as coordenadas da região informada"}
						return False
			else:
				return False
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
				geolocator = Nominatim(user_agent="geoloc")
				location = geolocator.geocode(endereco['localidade'] + ", " + endereco['bairro'])
				#Se encontrar o bairro
				if (location != None):
					self._resultado = {"latitude": location.latitude, "longitude": location.longitude}
					return True
				#Se tiver apenas cidade
				else:
					geolocator = Nominatim(user_agent="test_app")
					location = geolocator.geocode(endereco['localidade'])
					self._resultado = {"latitude": location.latitude, "longitude": location.longitude}
					return True
			else:
				return False
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .validate import Coordenadas

# Create your views here.
def visualiza(request, cep):
	#Verifica o CEP inserido pelo o usuário
	objeto_cep = Coordenadas(cep)
	if (objeto_cep.valido()):
		return JsonResponse(objeto_cep.resultado, status=200)
	else:
		return JsonResponse({"error": "O CEP inserido contem erros!"}, status=400)

def erro(request):
	return redirect('/api/')

def semDados(request):
	return JsonResponse({"error": "Insira um CEP! Exemplo: ...api/06454000/ ou ...api/06454-000/"}, status=400)

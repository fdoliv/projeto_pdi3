#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import cv2
from random import randint
from math import sqrt
import numpy as np

# o segundo parâmetro da função indicará o modo de cor da imagem
# 0 = modo escala de cinza (1 canal de intensidade)
# 1 = modo imagem colorida (3 canais de intensidade)
# default = 1

def gerar_centroides(k=8):
	centroides = []
	for i in xrange(k):
		centroides.append([randint(0, 256)])
	return centroides


# Método que calcula a distancia euclidiana entre os indivíduos
def distancia_euclides(p1, p2, y=2):
    soma = pow(p1 - p2, y)
    return sqrt(soma)

# verifica qual o centroid mais proximo
def centroide_proximo(centroides, ponto):
	menor = 10000000
	centroide = None
	for c in centroides:
		distancia = distancia_euclides(c, ponto)		
		if menor > distancia:
			menor = distancia
			centroide = c
	#print centroide
	return centroide
def set_vetor_g(centroides, img):
	g = []
	for i in xrange(img.shape[0]):
		g.append([])
		for j in xrange(img.shape[1]):
			d = []
			g[i].append(centroide_proximo(centroides, img[i][j]))
	return g

def calcular_centroides(g, centroides, img):
	c_retorno = []	
	for centroide in centroides: 	
		soma = [0, 0]
		p = 0.0
		for i in xrange(len(g)):
			for j in xrange(len(g[i])):
				if g[i][j] == centroide:
					soma[0] += img[i][j]				
					p +=1
		if(soma[0] == 0):
			c_retorno.append([0])
		else:	
			c_retorno.append([round(soma[0]/p)])
	#print c_retorno
	return c_retorno
			
def kmeans(img, k=8, L=100):
	centroides = gerar_centroides(k=k)
	g = []
	g_ant = []
	trocou = True;
	cont = 0
	while trocou:
		# faz uma copia de g
		g_ant = g[:]
		g = set_vetor_g(centroides, img)
		# verifica se g teve algum valor alterado
		if (g == g_ant ):
			trocou = False
		# recalcula os centroides
		centroides = calcular_centroides(g, centroides, img)
		
		cont += 1
	
	return g, centroides

def calcular_valor_pixel(pixel, max_centroide):
	if(pixel[0] == max_centroide): 
		#print 1
		return 0
	return 1 *255

def binarizar(img, shape_0, shape_1, max_centroide):
	img_r = img[:]
	for i in xrange(shape_0):
		for j in xrange(shape_1):
			img_r[i][j] = calcular_valor_pixel(img[i][j], max_centroide)
	return img_r

# Acessando Atributos da Imagem
#print "Altura (height): %d pixels" % (img.shape[0])
#print "Largura (width): %d pixels" % (img.shape[1])
#print "Canais (channels): %d"      % (img.shape[2])

for i in xrange(10, 11):
	# carrega a imagem em escala de cinza
	img = cv2.imread (str(i)+'.png', 0)
	# executa o kmeans na imagem
	g, c = kmeans(img, k=2, L=1000000000000000)
	img_binarizada = np.array(g)
	img_kmeans = img_binarizada.copy() 
	# obtem o valor do pixel de maior intensidade
	max_centroide = max(c)
	# binariza a imagem
	binarizar(img_binarizada,img.shape[0],img.shape[1], max_centroide)
	# Mostra a porcentagem de cobertura vegetal da imagem 
	print "A cobertura vegetal da imagem "+str(i)+".png é de %.2f porcento." % (100*(img_binarizada.sum()/255.0)/img_binarizada.size)

	# grava as imagens 
	cv2.imwrite(str(i)+'_kmeans.png', img_kmeans)
	cv2.imwrite(str(i)+'_binarizada.png', img_binarizada)




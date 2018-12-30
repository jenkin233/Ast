# -*- coding: utf-8 -*-

# 画出余弦相似度和编辑距离图
# 
import matplotlib.pyplot as plt

def read_file(file_name):
	y = []
	f = open(file_name,"r")
	lines = f.readlines()
	for line in lines:
		y_t = line.strip()
		y.append(float(y_t))
	return y

def plot_cos(file_name):

	y = read_file(file_name)
	x = range(1,len(y)+1)

	plt.plot(x,y)

	plt.ylabel('cos similarity')

	plt.xlabel('release')

	plt.show()

def plot_distance(file_name):

	y = read_file(file_name)
	x = range(1,len(y)+1)

	plt.plot(x,y)

	plt.ylabel('distance')

	plt.xlabel('release')

	plt.show()

if __name__ == "__main__":
	# plot_cos("record_simi.txt")
	# plot_distance("record_dist.txt")
	plot_cos("rele_record_simi.txt")
	plot_distance("rele_record_dist.txt")

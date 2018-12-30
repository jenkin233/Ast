# -*- coding: utf-8 -*-
# 项目的主体
# 
import os
import numpy as np
import Levenshtein
from build import get_asts
from sklearn.feature_extraction.text import CountVectorizer


### 寻找当前项目中所有的.py文件
def search_file(all_files, filepath):
	files = os.listdir(filepath)
	for fi in files:
		fi_d = os.path.join(filepath,fi)            
		if os.path.isdir(fi_d):
			search_file(all_files, fi_d)                  
		else:
			tmp_l = fi.split(".")
			if len(tmp_l) > 1 and tmp_l[1] == "py":
				#print >> fp, fi_d
				#fp.write(fi_d+"\n")
				all_files.append(fi_d)

def get_all_pyfile():
	filepath = os.getcwd() + "\\flask-sqlalchemy"
	all_files = []
	search_file(all_files, filepath)
	return all_files

### 获得所有commit
def get_commits(file_name):
	file = open(file_name)
	commits = file.readlines()
	file.close()
	return commits

### 获得所有release
def get_releases():
	file = open("releases.txt")
	releases = file.readlines()
	file.close()
	return releases

### 切换版本
def switch_version(commit):
	cwd = os.getcwd()
	file_dir = os.getcwd() + "\\flask-sqlalchemy"
	os.chdir(file_dir)
	os.system('git checkout '+commit)
	os.chdir(cwd)

### 计算两个commit之间的余弦相似度和编辑距离
def calc_project_similarity(old_files,old_asts,new_files,new_asts):

	similarity = 0.0
	distance = 0.0

	# 找到所有新增、删除和不变的文件
	same_file = [file for file in old_files if file in new_files]
	delete_file = [file for file in old_files if file not in new_files]
	add_file = [file for file in new_files if file not in old_files]

	# 删除的文件和新增的文件,相似度为0
	# 故不用计算相似度

	# 删除的文件和新增的文件，dist记为ast长度
	for file in delete_file:
		ind = old_files.index(file)
		distance += len(old_asts[ind])

	for file in add_file:
		ind = new_files.index(file)
		distance += len(new_asts[ind])

	# 计算修改文件的相似度和距离
	for file in same_file:
		old_ind = old_files.index(file)
		new_ind = new_files.index(file)
		similarity += calc_ast_similarity_cos(old_asts[old_ind],new_asts[new_ind])
		distance += calc_edit_distance(old_asts[old_ind],new_asts[new_ind])

	# 平均相似度
	similarity /= (len(delete_file)+len(add_file)+len(same_file))

	return similarity,distance

def cos_sim(vector_a, vector_b):
	"""
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a 
    :param vector_b: 向量 b
    :return: sim
    """
	vector_a = np.mat(vector_a)
	vector_b = np.mat(vector_b)
	num = float(vector_a * vector_b.T)
	denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
	cos = num / denom
	sim = 0.5 + 0.5 * cos
	return sim

### 计算两个ast树之间的余弦相似度
def calc_ast_similarity_cos(ast1,ast2):
	corpus = [ast1,ast2]
	cntVector = CountVectorizer()
	cntTf = cntVector.fit_transform(corpus)
	codes_vec = cntTf.toarray()
	return cos_sim(codes_vec[0],codes_vec[1])

### 计算编辑距离
def calc_edit_distance(ast1,ast2):
	return Levenshtein.distance(ast1,ast2)

def calc_commits(file,similaritys,distance):
	commits = get_commits(file)
	
	for id,commit in enumerate(commits):
		print (id)
		#切换到下一版本
		switch_version(commit)
		#获得所有.py文件
		new_files = get_all_pyfile()
		#对所有.py文件生成ast树
		new_asts = get_asts(new_files)
		# 计算两个commit之间的相似度
		if id > 0:
			simi,dist = calc_project_similarity(old_files,old_asts,new_files,new_asts)
			similaritys.append(simi)
			distance.append(dist)
			
		old_files = new_files
		old_asts = new_asts

if __name__ == "__main__":

	commits_file ="commits.txt"
	release_file ="release_commits.txt"

	similaritys = []
	distance = []
	# 计算连续commit
	calc_commits(commits_file,similaritys,distance)
	# 存储结果
	f = open("record_simi.txt","w")
	for simi in similaritys:
		f.write(str(simi)+"\n")
	f.close()
	f = open("record_dist.txt","w")
	for dist in distance:
		f.write(str(dist)+"\n")
	f.close()
	
	
	rele_similaritys = []
	rele_distance = []
	# 计算连续release
	calc_commits(release_file,rele_similaritys,rele_distance)
	# 存储结果
	f = open("rele_record_simi.txt","w")
	for simi in rele_similaritys:
		f.write(str(simi)+"\n")
	f.close()
	f = open("rele_record_dist.txt","w")
	for dist in rele_distance:
		f.write(str(dist)+"\n")
	f.close()
	




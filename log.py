# -*- coding: utf-8 -*-
# 根据git log 产生的日志文件，获得所有的commit
fp = open("log.txt", "r",encoding='UTF-8')
fc = open("commit.txt", "w")
commit_list = []
for line in fp.readlines():
	if line.startswith("commit") and len(line.split(" "))==2:
		commit_num = line.split(" ")[1]
		commit_list.append(commit_num)
print (len(commit_list))

commit_list.reverse()

for i in commit_list:
	fc.write(i)
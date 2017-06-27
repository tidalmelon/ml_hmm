import os
import sys
import random
import math


def get_word_ch(word):
    ch_lst=[]
    i=0
    word_len=len(word)
    while i<word_len:
        if ord(word[i])>127:
            ch_lst.append(word[i:i+2])
            i+=2
        else:
            ch_lst.append(word[i])
            i+=1
    return ch_lst

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print>>sys.stderr, "usage:", sys.argv[0], "<txt_file>", "<model_file>"
        sys.exit(1)

    f_txt=open(sys.argv[1])

    STATUS_NUM=4
    #B, M, E, S

    A=[[0.0 for col in range(STATUS_NUM)] for row in range(STATUS_NUM)]
    A_sum=[0.0 for col in range(STATUS_NUM)]

    pi=[0.0 for col in range(STATUS_NUM)]
    pi_sum=0.0

    B=[{} for col in range(STATUS_NUM)]
    B_sum=[0.0 for col in range(STATUS_NUM)]

    while True:
        line=f_txt.readline()
        if not line:break
        line = line.decode('gbk')
        line=line.strip()
        if len(line)<1: continue
        
        words=line.split()

        ch_lst=[]
        status_lst=[]
        for word in words:
            cur_ch_lst=get_word_ch(word)
            cur_ch_num=len(cur_ch_lst)
            cur_status_lst=[0 for ch in range(cur_ch_num)]

            if cur_ch_num==1:
                cur_status_lst[0]=3
            else:
                cur_status_lst[0]=0
                cur_status_lst[-1]=2
                for i in range(1,cur_ch_num-1):
                    cur_status_lst[i]=1

            ch_lst.extend(cur_ch_lst)
            status_lst.extend(cur_status_lst)

        
        for i in range(len(ch_lst)):
            cur_status=status_lst[i]
            cur_ch=ch_lst[i]
            if i==0: 
                pi[cur_status]+=1.0
                pi_sum+=1.0

            if cur_ch in B[cur_status]: B[cur_status][cur_ch]+=1.0
            else: B[cur_status][cur_ch]=1.0
            B_sum[cur_status]+=1.0

            if i+1<len(ch_lst): 
                A[cur_status][status_lst[i+1]]+=1.0
                A_sum[cur_status]+=1.0

            #sys.stderr.write(ch_lst[i]+":"+str(status_lst[i])+" ")
        #sys.stderr.write("\n")

    f_txt.close()

    for i in range(STATUS_NUM):
        pi[i]/=pi_sum

        for j in range(STATUS_NUM): A[i][j]/=A_sum[i]
        
        for ch in B[i]: B[i][ch]/=B_sum[i] 


    f_mod=open(sys.argv[2], "wb")
    for i in range(STATUS_NUM):
        if pi[i]!=0.0: log_p=math.log(pi[i])
        else: log_p=0.0
        f_mod.write(str(log_p)+" ")
    f_mod.write("\n")


    for i in range(STATUS_NUM):
        for j in range(STATUS_NUM):
            if A[i][j]!=0.0: log_p=math.log(A[i][j])
            else: log_p=A[i][j]
            f_mod.write(str(log_p)+" ")
        f_mod.write("\n")

    for i in range(STATUS_NUM):
        for ch in B[i]:
            if B[i][ch]!=0.0: log_p=math.log(B[i][ch])
            else: log_p=0.0
            line = ch+" "+str(log_p)+" "
            line = line.encode('utf-8')
            f_mod.write(line)
        f_mod.write("\n")

    f_mod.close()


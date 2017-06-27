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

def print_status_matrix(status_matrix, obj_file):
    STATUS_NUM=4
    o_len=len(status_matrix[0])
    for row in range(STATUS_NUM):
        for col in range(o_len):
            print>>obj_file, "%.2f:%d "%(status_matrix[row][col][0], status_matrix[row][col][1]),
        print>>obj_file

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print>>sys.stderr, "usage:", sys.argv[0], "<model_file>"
        sys.exit(1)

    #load mod
    STATUS_NUM=4

    pi=[0.0 for col in range(STATUS_NUM)]
    A=[[0.0 for col in range(STATUS_NUM)] for row in range(STATUS_NUM)]
    B=[{} for col in range(STATUS_NUM)]

    f_mod=open(sys.argv[1])

    pi_tokens=f_mod.readline().split()
    for i in range(STATUS_NUM):
        pi[i]=float(pi_tokens[i])

    for i in range(STATUS_NUM):
        A_i_tokens=f_mod.readline().split()
        for j in range(STATUS_NUM):
            A[i][j]=float(A_i_tokens[j])

    print>>sys.stderr, pi
    print>>sys.stderr, A

    for i in range(STATUS_NUM):
        B_i_tokens=f_mod.readline().split()
        token_num=len(B_i_tokens)
        j=0
        print>>sys.stderr, i,">>>",token_num
        while j+1<token_num:
            B[i][B_i_tokens[j]]=float(B_i_tokens[j+1])
            if j<=10:
                print>>sys.stderr, B_i_tokens[j]+":"+B_i_tokens[j+1], 
            j+=2
        print>>sys.stderr
    
    f_mod.close()


    #seg
    while True:
        line=sys.stdin.readline()
        if not line: break
        line=line.strip().decode('utf-8')

        ch_lst=get_word_ch(line)
        ch_num=len(ch_lst)
        if ch_num<1:
            print
            continue

        status_matrix=[[[0.0,0] for col in range(ch_num)] \
        for st in range(STATUS_NUM)]

        #init
        for i in range(STATUS_NUM):
            if ch_lst[0] in B[i]: cur_B=B[i][ch_lst[0]]
            else: cur_B=-1000000.0
            if pi[i]==0.0: cur_pi=-100000.0
            else: cur_pi=pi[i]
            status_matrix[i][0][0]=cur_pi+cur_B
            status_matrix[i][0][1]=i #init status
        #print_status_matrix(status_matrix, sys.stderr) 

        #viterbi
        for i in range(1,ch_num):
            for j in range(STATUS_NUM):
                max_p=None
                max_status=None
                for k in  range(STATUS_NUM):
                    cur_A=A[k][j]
                    if cur_A==0.0: cur_A=-1000000.0
                    cur_p=status_matrix[k][i-1][0]+cur_A
                    if max_p is None or max_p < cur_p:
                        max_p=cur_p
                        max_status=k

                if ch_lst[i] in B[j]: cur_B=B[j][ch_lst[i]]
                else: cur_B=-1000000.0
                status_matrix[j][i][0]=max_p+cur_B
                status_matrix[j][i][1]=max_status
        print_status_matrix(status_matrix, sys.stderr) 

        #get max path
        max_end_p=None
        max_end_status=None
        for i in range(STATUS_NUM):
            if max_end_p is None or  status_matrix[i][ch_num-1][0]>max_end_p:
                max_end_p=status_matrix[i][ch_num-1][0]
                max_end_status=i
        best_status_lst=[0 for ch in range(ch_num)]
        best_status_lst[ch_num-1]=max_end_status

        i=ch_num-1
        cur_best_status=max_end_status
        while i>0:
            pre_best_status=status_matrix[cur_best_status][i][1]
            best_status_lst[i-1]=pre_best_status
            cur_best_status=pre_best_status
            i-=1

        #output
        print>>sys.stderr,best_status_lst
        sys.stdout.write(ch_lst[0])
        for i in range(1,ch_num):
            if best_status_lst[i-1] in {2,3} or best_status_lst[i] in {0,3}:
                sys.stdout.write(" ")
            print type(ch_lst[i])
            sys.stdout.write(ch_lst[i])
        sys.stdout.write("\n")
        sys.stdout.flush()



/*
 * @Description:
 * hash����Ϊȡģ����
 * @Author: Fishermanykx
 * @LastEditors: Fishermanykx
 * @LastEditTime: 2020-03-29 21:08:10
 */
///////////////////////////////////////////////////////////////////////
////  Copyright 2020 by mars.                                        //
///////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common.h"

#define HIST_LEN 24  // ȫ����ʷ�Ĵ������ȣ�ȡ24λ
#define N 16777216   // the number of perceptrons����ģȡ2^24(10^7����)
#define THERSHOLD 2147483647  // ��ֵ��y_out�������ֵ��ֹͣѵ��������
#define TAKEN 'T'
#define NOT_TAKEN 'N'

// ��֧Ԥ������״̬��Ϣ
int perceptron_table[N][HIST_LEN];  // perception table   ��������
int numPhtEntries;  // entries in perception table     ���������е�����
int ghr[HIST_LEN];  // global history register         ȫ����ʷ�Ĵ���
int historyLength;  // history length                  ��ʷ����
int y_out;          // ÿһ�ε�Ԥ��ֵ

void PREDICTOR_init(void) {
  historyLength = HIST_LEN;
  numPhtEntries = N;  // ������������2^24�ÿ����18λ

  // ��ʼ����������
  memset(perceptron_table, 0, sizeof(int) * N * (HIST_LEN));
  // ��ʼ��ȫ����ʷ�Ĵ���
  memset(ghr, 0, (HIST_LEN) * sizeof(int));
  ghr[0] = 1;
}

// �ӵ�ַ��index�Ĺ�ϣ����
int ComputePTIndex(UINT64 PC) {
  int ptIndex = 0;

  // ��-1�滻Ϊ0������ghr��ֵ
  int ghr_num = 0;
  int pow_2 = 1;
  int bit_val = 0;
  for (int i = 0; i < HIST_LEN; ++i) {
    bit_val = (ghr[i] < 0) ? 0 : 1;
    ghr_num += bit_val * pow_2;
    pow_2 <<= 1;
  }
  // hash
  ptIndex = (PC ^ ghr_num) % numPhtEntries;

  return ptIndex;
}

// Ԥ��ģ��
// ����ַ�ĵ�24λȡ����ģN��õ�index
// ����index����perceptronȡ�����˼�ΪȨ����������ghr�����
// ����ֵ��Ϊ״̬y
// �����״̬��ֵ�Ǹ�����Ԥ����ת
// �����״̬��ֵΪ������Ԥ�ⲻ��ת
char GetPrediction(UINT64 PC) {
  int ptIndex = ComputePTIndex(PC);
  int *perception = perceptron_table[ptIndex];  // Ȩ������
  // ������õ�y_out
  y_out = perception[0];
  for (int i = 1; i < HIST_LEN; ++i) {
    y_out += (perception[i] * ghr[i]);
  }
  // Ԥ��
  if (y_out < 0) {
    return NOT_TAKEN;
  } else {
    return TAKEN;
  }
}

// ��֧Ԥ����
// ���ݷ�ָ֧��ʵ��ִ�н���������¶�Ӧ�ı��ͼ�����
// ������Ϊ��ת�����Ӧ�ı��ͼ�����+1
// ������Ϊ����ת�����Ӧ�ı��ͼ�����-1
// ����ȫ����ʷ�Ĵ�����
// ���Ϊ��ת����1��λ��GHR�����λ
// ���Ϊ����ת����0��λ��GHR�����λ
void UpdatePredictor(UINT64 PC, OpType opType, char resolveDir, char predDir,
                     UINT64 branchTarget) {
  opType = opType;
  predDir = predDir;
  branchTarget = branchTarget;

  int phtIndex = ComputePTIndex(PC);
  //	printf("PC=%016llx resolveDir=%c predDir=%c branchTarget=%016llx\n", PC,
  // resolveDir, predDir, branchTarget);

  // ѵ��������
  int taken = (resolveDir == TAKEN) ? 1 : -1;
  int sign_y_out = (y_out >= 0) ? 1 : -1;
  int abs_y_out = (y_out >= 0) ? y_out : (-1 * y_out);

  if (sign_y_out != taken || abs_y_out <= THERSHOLD) {
    for (int i = 0; i < HIST_LEN; ++i) {
      perceptron_table[phtIndex][i] += (taken * ghr[i]);
    }
  }

  // update the GHR
  for (int rev_i = HIST_LEN - 1; rev_i > 1; --rev_i) {
    ghr[rev_i] = ghr[rev_i - 1];
  }
  if (resolveDir == TAKEN) {
    ghr[1] = 1;  // ������Ϊ��ת����1�������
  } else {
    ghr[1] = -1;  // ������Ϊ����ת����-1�������
  }
}

void PREDICTOR_free(void) { ; }

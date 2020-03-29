/*
 * @Description:
 * hash函数为取模运算
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

#define HIST_LEN 24  // 全局历史寄存器长度，取24位
#define N 16777216   // the number of perceptrons，规模取2^24(10^7量级)
#define THERSHOLD 2147483647  // 阈值，y_out超过这个值即停止训练传感器
#define TAKEN 'T'
#define NOT_TAKEN 'N'

// 分支预测器的状态信息
int perceptron_table[N][HIST_LEN];  // perception table   感受器表
int numPhtEntries;  // entries in perception table     感受器表中的项数
int ghr[HIST_LEN];  // global history register         全局历史寄存器
int historyLength;  // history length                  历史长度
int y_out;          // 每一次的预测值

void PREDICTOR_init(void) {
  historyLength = HIST_LEN;
  numPhtEntries = N;  // 感受器表，共有2^24项，每项有18位

  // 初始化感受器表
  memset(perceptron_table, 0, sizeof(int) * N * (HIST_LEN));
  // 初始化全局历史寄存器
  memset(ghr, 0, (HIST_LEN) * sizeof(int));
  ghr[0] = 1;
}

// 从地址到index的哈希函数
int ComputePTIndex(UINT64 PC) {
  int ptIndex = 0;

  // 将-1替换为0，计算ghr的值
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

// 预测模块
// 将地址的低24位取出，模N后得到index
// 而后将index处的perceptron取出（此即为权重向量）与ghr作点积
// 所得值即为状态y
// 如果该状态的值非负，则预测跳转
// 如果该状态的值为负，则预测不跳转
char GetPrediction(UINT64 PC) {
  int ptIndex = ComputePTIndex(PC);
  int *perception = perceptron_table[ptIndex];  // 权重向量
  // 作点积得到y_out
  y_out = perception[0];
  for (int i = 1; i < HIST_LEN; ++i) {
    y_out += (perception[i] * ghr[i]);
  }
  // 预测
  if (y_out < 0) {
    return NOT_TAKEN;
  } else {
    return TAKEN;
  }
}

// 分支预测器
// 根据分支指令实际执行结果，来更新对应的饱和计数器
// 如果结果为跳转，则对应的饱和计数器+1
// 如果结果为不跳转，则对应的饱和计数器-1
// 更新全局历史寄存器：
// 结果为跳转，将1移位到GHR的最低位
// 结果为不跳转，将0移位到GHR的最低位
void UpdatePredictor(UINT64 PC, OpType opType, char resolveDir, char predDir,
                     UINT64 branchTarget) {
  opType = opType;
  predDir = predDir;
  branchTarget = branchTarget;

  int phtIndex = ComputePTIndex(PC);
  //	printf("PC=%016llx resolveDir=%c predDir=%c branchTarget=%016llx\n", PC,
  // resolveDir, predDir, branchTarget);

  // 训练传感器
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
    ghr[1] = 1;  // 如果结果为跳转，则将1放入队列
  } else {
    ghr[1] = -1;  // 如果结果为不跳转，则将-1放入队列
  }
}

void PREDICTOR_free(void) { ; }

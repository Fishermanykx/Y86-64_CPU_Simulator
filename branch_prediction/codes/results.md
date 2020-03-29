# 分支预测器

以trace文件`SHORT_MOBILE-30.bt9.trace.gz`为测试用例

运行命令位于`run.sh`中，文件内容如下：

```bash
make
./predictor traces/SHORT_MOBILE-30.bt9.trace.gz
```

若使用原来的GShare算法，结果为：

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    4620079
  MISPRED_PER_1K_INST         	 :     7.0143
```



## 目标一：1位的分支预测器

结果：

```bash
  NUM_INSTRUCTIONS               :  658661227
  NUM_BR                         :  123358312
  NUM_UNCOND_BR                  :   11682421
  NUM_CONDITIONAL_BR             :  111675892
  NUM_MISPREDICTIONS             :    6139116
  MISPRED_PER_1K_INST            :     9.3206
```



## 目标二：扩展全局分支历史长度

### 长度为17位时的结果

```bash
  NUM_INSTRUCTIONS               :  658661227
  NUM_BR                         :  123358312
  NUM_UNCOND_BR                  :   11682421
  NUM_CONDITIONAL_BR             :  111675892
  NUM_MISPREDICTIONS             :    4620079
  MISPRED_PER_1K_INST            :     7.0143
```

### 长度为19位时的结果

```bash
  NUM_INSTRUCTIONS               :  658661227
  NUM_BR                         :  123358312
  NUM_UNCOND_BR                  :   11682421
  NUM_CONDITIONAL_BR             :  111675892
  NUM_MISPREDICTIONS             :    4103720
  MISPRED_PER_1K_INST            :     6.2304
```

### 长度为21位时的结果

```bash
  NUM_INSTRUCTIONS               :  658661227
  NUM_BR                         :  123358312
  NUM_UNCOND_BR                  :   11682421
  NUM_CONDITIONAL_BR             :  111675892
  NUM_MISPREDICTIONS             :    3734536
  MISPRED_PER_1K_INST            :     5.6699
```

### 长度为23位时的结果

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    2551739
  MISPRED_PER_1K_INST         	 :     3.8741
```

### 长度为25位时的结果

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    2267255
  MISPRED_PER_1K_INST         	 :     3.4422
```

### 长度为27位时的结果

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    1952124
  MISPRED_PER_1K_INST         	 :     2.9638
```



## 目标三：为每个分支指令分配完全独立的状态机

状态机为2位时

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    6982248
  MISPRED_PER_1K_INST         	 :    10.6007
```

状态机为3位时

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    7192542
  MISPRED_PER_1K_INST         	 :    10.9199
```



## 目标四：实现局部历史信息

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    6982278
  MISPRED_PER_1K_INST         	 :    10.6007
```



## 目标五：实现局部+全局历史信息

实现思路：在目标四的基础上增加了一个全局寄存器，查找全局历史信息表计算Index的方式：

```python
UINT32 phtIndex = ((PC << (HIST_LEN - LOCAL_HIST_LEN)) + lhr) % (numPhtEntries);
```

结果如下：

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    4601983
  MISPRED_PER_1K_INST         	 :     6.9869
```



## 目标六：使用其他hash函数

### 使用移位(左移)

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :   41649151
  MISPRED_PER_1K_INST         	 :    63.2330
```

### 使用移位(右移)

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :   41863589
  MISPRED_PER_1K_INST         	 :    63.5586
```

### 使用加法

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    4601493
  MISPRED_PER_1K_INST         	 :     6.9861
```

### 使用逐位与

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :   11763753
  MISPRED_PER_1K_INST         	 :    17.8601
```

### 使用逐位或

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    6778606
  MISPRED_PER_1K_INST         	 :    10.2915
```



## 目标七：进一步优化

### 每条指令分配2位独立状态机+全局历史信息

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    1628198
  MISPRED_PER_1K_INST         	 :     2.4720
```



### Dynamic Branch Prediction with Perceptrons

```bash
  NUM_INSTRUCTIONS            	 :  658661227
  NUM_BR                      	 :  123358312
  NUM_UNCOND_BR               	 :   11682421
  NUM_CONDITIONAL_BR          	 :  111675892
  NUM_MISPREDICTIONS          	 :    2477065
  MISPRED_PER_1K_INST         	 :     3.7608
```

参考文献：

[1] Jiménez, D. A., & Lin, C. (2001, January). Dynamic branch prediction with perceptrons. In *Proceedings HPCA Seventh International Symposium on High-Performance Computer Architecture* (pp. 197-206). IEEE.
---
id: 3
logic_id: 100
name: 2选1MUX
level: 1
tags:
points: 1
---

# 2选1MUX

## 题目描述
二路选择器的逻辑特点是：

- 当选择器`sel`为`0`输出`a`的值
- 当选择器sel为`1`时，输出为`b`的值

## 输入格式
输入`a`,`b`,`sel` 都为`1`bit信号

## 输出格式
输出`out` 为`1`bit信号
你需要通过`sel`来控制`out`的结果

## 代码
```verilog
module Mux(
    input sel,
    input a,
    input b,
    output out
);
    // 在这里输入你的代码 请不要修改模块和信号名称
endmodule
```

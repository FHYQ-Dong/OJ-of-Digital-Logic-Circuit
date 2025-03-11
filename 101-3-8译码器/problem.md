---
id: 11
logic_id: 101
name: 3-8译码器
level: 1
tags:
points: 1
---

# 3-8译码器

## 题目描述
3-8译码器
该模块将3bit输入转为8bit输出
输入000对应输出为0000_0001
输入011对应输出为0000_1000
输入111对应输出为1000_0000

## 输入格式
- `x`: 3bit

## 输出格式
- `y`: 8bit

## 代码
```verilog
module decoder(
    input [2:0] x,
    output reg [7:0] y
);
    // 在这里输入你的代码 请不要修改模块和信号名称
endmodule
```

---
id: 25
logic_id: 202
name: 4位2进制计数器
level: 1
tags:
points: 1
---

# 4位2进制计数器

## 题目描述
生成一个4位二进制计数器，其计数范围为0到15（包括 0 和 15），周期为 16。
同步的复位信号将计数器复位为0。（当reset信号为active的时候，寄存器在下一个时钟沿到来之后被复位。）

## 输入格式
- `clk`: 1bit
- `reset`: 1bit

## 输出格式
- `q`: 4bit

## 代码
```verilog
module four_bit_counter(
    input clk,
    input reset,     
    output [3:0] q
);
    // 在这里输入你的代码 请不要修改模块和信号名称
endmodule
```

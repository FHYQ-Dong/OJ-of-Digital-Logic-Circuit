---
id: 28
logic_id: 200
name: D触发器
level: 1
tags:
points: 1
---

# D触发器

## 题目描述
D触发器是一种电路，它存储一个位并定期更新，通常在时钟信号的上升沿更新。
本题中你需要创建一个D触发器，实现在每个时钟的上升沿将d的值赋予q。

## 输入格式
- `clk`: 1bit
- `d`: 1bit

## 输出格式
- `q`: 1bit

## 代码
```verilog
module D_flip_flop(
    input clk,
    input d,
    output reg q
);
    // 在这里输入你的代码 请不要修改模块和信号名称
endmodule
```

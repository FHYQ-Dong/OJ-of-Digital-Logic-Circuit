---
id: 69
logic_id: 206
name: 滑动平均滤波器
level: 1
tags:
points: 1
---

# 滑动平均滤波器

## 题目描述
![滑动平均滤波器.png](assets/滑动平均滤波器.png)

## 输入格式
- `clk`: 1bit
- `reset`: 1bit
- `din[4:0]`: 5bit

## 输出格式
- `dout[7:0]`: 8bit

## 代码
```verilog
module maf(
    input clk,
    input reset,
    input [4:0] din,
    output [7:0] dout
    );
        // 在这里输入你的代码 请不要修改模块和信号名称
		// 补充说明，数学上可以证明，如果内部累加器的位宽大于等于8bit，则累加器溢出不影响结果的正确性
    endmodule
```

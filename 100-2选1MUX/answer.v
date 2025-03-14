/*
 * id: 3
 * logic_id: 100
 * name: 2选1MUX
 * level: 1
 * tags: 
 * points: 1
 */

module Mux(
    input sel,
    input a,
    input b,
    output out
);
    // 在这里输入你的代码 请不要修改模块和信号名称
    assign out = (sel == 1'b0) ? a : b;
endmodule
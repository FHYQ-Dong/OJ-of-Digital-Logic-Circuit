/*
 * id: 2
 * logic_id: 2
 * name: XNOR 门
 * level: 1
 * tags: 
 * points: 1
 */

module Xnor( 
    input a, 
    input b, 
    output out
);
    // 在这里输入你的代码 请不要修改模块和信号名称
    assign out = !(a ^ b);
endmodule
/*
 * id: 9
 * logic_id: 3
 * name: “1”的数目
 * level: 1
 * tags: 
 * points: 1
 */

module population_count( 
    input [2:0] in, 
    output [1:0] out  );
    assign out[0] = in[2] ^ in[1] ^in[0];
    assign out[1] = (in[2] & in[1]) | (in[1] & in[0]) | (in[2] & in[0]);
    // 在这里输入你的代码 请不要修改模块和信号名称
endmodule
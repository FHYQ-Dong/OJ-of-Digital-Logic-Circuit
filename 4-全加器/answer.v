/*
 * id: 1
 * logic_id: 4
 * name: 全加器
 * level: 1
 * tags: 
 * points: 1
 */

module full_adder(
    input a, b, cin,
    output cout, sum
);
    // 在这里输入你的代码 请不要修改模块和信号名称
    assign cout = (a & b) | (a & cin) | (b & cin);
    assign sum = a ^ b ^ cin;
endmodule
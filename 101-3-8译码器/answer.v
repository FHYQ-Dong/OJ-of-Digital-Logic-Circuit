/*
 * id: 11
 * logic_id: 101
 * name: 3-8译码器
 * level: 1
 * tags: 
 * points: 1
 */

module decoder(
    input [2:0] x,
    output reg [7:0] y
);
    // 在这里输入你的代码 请不要修改模块和信号名称
    always @(*) begin
        y = 
            (x == 3'b000) ? 8'b00000001 :
            (x == 3'b001) ? 8'b00000010 :
            (x == 3'b010) ? 8'b00000100 :
            (x == 3'b011) ? 8'b00001000 :
            (x == 3'b100) ? 8'b00010000 :
            (x == 3'b101) ? 8'b00100000 :
            (x == 3'b110) ? 8'b01000000 :
        	8'b10000000 ;
    end
endmodule
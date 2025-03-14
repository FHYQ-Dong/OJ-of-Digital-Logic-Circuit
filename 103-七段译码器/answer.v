/*
 * id: 45
 * logic_id: 103
 * name: 七段译码器
 * level: 1
 * tags: 
 * points: 1
 */

module BCD7( 
    input [3:0] din, 
    output reg [6:0] dout
);
    // 在这里输入你的代码 请不要修改模块和信号名称
    always @(*) begin
        case (din)
            4'd0: dout = 7'b0111111;
            4'd1: dout = 7'b0000110;
            4'd2: dout = 7'b1011011;
            4'd3: dout = 7'b1001111;
            4'd4: dout = 7'b1100110;
            4'd5: dout = 7'b1101101;
            4'd6: dout = 7'b1111101;
            4'd7: dout = 7'b0000111;
            4'd8: dout = 7'b1111111;
            4'd9: dout = 7'b1101111;
            default: dout = 7'b0111111;
        endcase
    end
endmodule
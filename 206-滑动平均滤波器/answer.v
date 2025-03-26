/*
 * id: 69
 * logic_id: 206
 * name: 滑动平均滤波器
 * level: 1
 * tags: 
 * points: 1
 */

module maf(
    input clk,
    input reset,
    input [4:0] din,
    output [7:0] dout
    );

    reg [7:0] sum;
    reg [47:0] history;
    assign dout = sum;

    always @(posedge clk) begin
        if (reset) begin
            sum <= 7'b0;
            history <= 48'b0;
        end else begin
            sum <= sum - history[47:40] + history[7:0];
            history <= {history[39:0], 3'b0, din};
        end
    end

endmodule

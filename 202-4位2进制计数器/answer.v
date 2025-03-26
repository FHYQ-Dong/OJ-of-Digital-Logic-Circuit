/*
 * id: 25
 * logic_id: 202
 * name: 4位2进制计数器
 * level: 1
 * tags: 
 * points: 1
 */

module four_bit_counter(
    input clk,
    input reset,     
    output [3:0] q
);
    reg [3:0] q;

    always @(posedge clk) begin
        if (reset) begin
            q <= 4'b0000;
        end else begin
            q <= q + 1;
        end
    end

endmodule

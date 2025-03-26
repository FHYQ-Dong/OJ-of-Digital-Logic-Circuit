/*
 * id: 30
 * logic_id: 203
 * name: 十进制计数器
 * level: 1
 * tags: 
 * points: 1
 */

module decade_counter(
    input clk,
    input reset,
    output [3:0] q
);
    reg [3:0] q;

    always @(posedge clk) begin
        if (reset) begin
            q <= 4'b0000;
        end else begin
            if (q == 4'b1001) begin
                q <= 4'b0000;
            end else begin
                q <= q + 1;
            end
        end
    end

endmodule

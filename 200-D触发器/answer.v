/*
 * id: 28
 * logic_id: 200
 * name: D触发器
 * level: 1
 * tags: 
 * points: 1
 */

module D_flip_flop(
    input clk,
    input d,
    output reg q
);
    always @(posedge clk) begin
        q <= d;
    end

endmodule

/*
 * id: 70
 * logic_id: 204
 * name: M序列
 * level: 1
 * tags: 
 * points: 1
 */

module lfsr (
    input clk,
    input preset,     
    output out
);
    reg [4:0] state;
    assign out = state[0];

    always @(posedge clk) begin
        if (!preset) begin
            state <= 5'b11111;
        end else begin
            state <= {state[3] ^ state[0], state[4:1]};
        end
    end

endmodule

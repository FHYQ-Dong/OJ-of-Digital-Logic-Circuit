/*
 * id: 29
 * logic_id: 201
 * name: D锁存器
 * level: 1
 * tags: 
 * points: 1
 */

module D_latch(
    input d, 
    input ena,
    output q
);
    reg q;
    always @(*) begin
        if (ena) begin
            q <= d;
        end
    end

endmodule

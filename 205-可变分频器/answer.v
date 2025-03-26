/*
 * id: 66
 * logic_id: 205
 * name: 可变分频器
 * level: 1
 * tags: 
 * points: 1
 */

module divider (
    input clk,
    input reset,     
    input [4:0] div,
    output out
);
    reg out;
    reg [4:0] count;

    always @(posedge clk) begin
        if (reset) begin
            count <= 5'b00000;
            out <= 1'b0;
        end else begin
            // div+1 even
            if (div[0] == 1'b1) begin
                if (count == ((div + 1) >> 1) - 1) begin
                    count <= 5'b00000;
                    out <= ~out;
                end else begin
                    count <= count + 1;
                end
            end
            // div+1 odd
            else begin
                if ((count == ((div + 2) >> 1) - 1) && (!out)) begin
                    count <= 5'b00000;
                    out <= ~out;
                end else if ((count == (div >> 1) - 1) && out) begin
                    count <= 5'b00000;
                    out <= ~out;
                end else begin
                    count <= count + 1;
                end
            end
        end
    end

endmodule

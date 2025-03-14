/*
 * id: 38
 * logic_id: 102
 * name: 将二进制码转换为格雷码
 * level: 1
 * tags: 
 * points: 1
 */

module B2G( 
    input  [7:0] in, 
    output reg [7:0] binary2gray
);
    integer i;
    always @(*) begin
        binary2gray[7] = in[7];
        for (i = 6; i >= 0; i = i - 1) begin
            binary2gray[i] = in[i+1] ^ in[i];
        end
    end
endmodule
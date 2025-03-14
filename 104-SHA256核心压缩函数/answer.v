/*
 * id: 55
 * logic_id: 104
 * name: SHA256核心压缩函数
 * level: 2
 * tags: 
 * points: 1
 */

// round compression function
module sha256_round (
    input [31:0] Kt, Wt,
    input [31:0] a_in, b_in, c_in, d_in, e_in, f_in, g_in, h_in,
    output [31:0] a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out
    );
// 请在此补充完整
    wire [31:0] t1_res, t2_res, S0_res, S1_res, Ch_res, Maj_res;
    sha256_S0 u_S0 (
        .x(a_in),
        .S0(S0_res)
    );
    sha256_S1 u_S1 (
        .x(e_in),
        .S1(S1_res)
    );
    Ch u_Ch (
        .x(e_in),
        .y(f_in),
        .z(g_in),
        .Ch(Ch_res)
    );
    Maj u_Maj (
        .x(a_in),
        .y(b_in),
        .z(c_in),
        .Maj(Maj_res)
    );
    // t1 = H + S1 + ch + Kt + Wt
    assign t1_res = h_in + S1_res + Ch_res + Kt + Wt;
    // t2 = S0 + Maj(A,B,C)
    assign t2_res = S0_res + Maj_res;
    // (A, B, C, D, E, F, G, H) = (t1+t2, A, B, C, D+t1, E, F, G)
    assign a_out = t1_res + t2_res;
    assign b_out = a_in;
    assign c_out = b_in;
    assign d_out = c_in;
    assign e_out = d_in + t1_res;
    assign f_out = e_in;
    assign g_out = f_in;
    assign h_out = g_in;
endmodule

// S0(x)
// S0 = (A rr 2) xor (A rr 13) xor (A rr 22)
module sha256_S0 (
    input wire [31:0] x,
    output wire [31:0] S0
    );
assign S0 = ({x[1:0], x[31:2]} ^ {x[12:0], x[31:13]} ^ {x[21:0], x[31:22]});
endmodule

// S1(x)
// (E rr 6) xor (E rr 11) xor (E rr 25)
module sha256_S1 (
    input wire [31:0] x,
    output wire [31:0] S1
    );
// 请在此补充完整
    assign S1 = ({x[5:0], x[31:6]} ^ {x[10:0], x[31:11]} ^ {x[24:0], x[31:25]});
endmodule

// Ch(x,y,z)
module Ch (
    input wire [31:0] x, y, z,
    output wire [31:0] Ch
    );
assign Ch = ((x & y) ^ (~x & z));
endmodule

// Maj(x,y,z)
module Maj (
    input wire [31:0] x, y, z,
    output wire [31:0] Maj
    );
// 请在此补充完整
    assign Maj = (x & y) | (y & z) | (z & x);
endmodule
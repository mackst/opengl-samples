#version 330

uniform mat4 View;
uniform mat4 Projection;

layout(points) in;
layout(triangle_strip, max_vertices = 4) out;

out vec2 txcoord;

void main()
{
    vec4 pos = View * gl_in[0].gl_Position;
    txcoord = vec2(-1, -1);
    gl_Position = Projection * (pos + vec4(txcoord, 0, 0));
    EmitVertex();

    txcoord = vec2(1, -1);
    gl_Position = Projection * (pos + vec4(txcoord, 0, 0));
    EmitVertex();

    txcoord = vec2(-1, 1);
    gl_Position = Projection * (pos + vec4(txcoord, 0, 0));
    EmitVertex();

    txcoord = vec2(1, 1);
    gl_Position = Projection * (pos + vec4(txcoord, 0, 0));
    EmitVertex();
}

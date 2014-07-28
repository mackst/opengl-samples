#version 330

uniform mat4 ViewProjection;
layout(location=0) in vec4 vposition;
layout(location=1) in vec4 vcolor;
layout(location=2) in vec3 voffset; // the per instance offset
out vec4 fcolor;

void main()
{
    fcolor = vcolor;
    gl_Position = ViewProjection * (vposition + vec4(voffset, 0));
}

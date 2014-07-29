#version 330

layout(std140) uniform Matrices
{
    mat4 ViewProjection;
    mat4 Model[8];
}

layout(location=0) in vec4 vposition;
layout(location=1) in vec4 vcolor;
layout(location=2) in vec3 voffset; // the per instance offset
out vec4 fcolor;

void main()
{
    fcolor = vcolor;
    gl_Position = ViewProjection * Model[gl_InstanceID] * vposition;
}

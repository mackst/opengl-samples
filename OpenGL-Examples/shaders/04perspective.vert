#version 330

uniform mat4 ViewProjection;
layout(location=0) in vec4 vposition;
layout(location=1) in vec4 vcolor;
out vec4 fcolor;

void main()
{
    fcolor = vcolor;
    gl_Position = ViewProjection * vposition;
}

#version 330

layout(location = 0) in vec4 vposition;

void main()
{
    gl_Position = vposition;
}

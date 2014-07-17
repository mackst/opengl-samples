#version 330

in vec4 vposition;
in vec4 vcolor;

out vec4 fcolor;

void main()
{
    fcolor = vcolor;
    gl_Position = vposition;
}

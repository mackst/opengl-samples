#version 430

layout(location=0) in vec3 pos;

uniform mat4 MVP;
uniform float time;

void main()
{
    gl_Position = MVP * vec4(pos, 1.);
}
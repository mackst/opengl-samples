#version 430

// using http://adrianboeing.blogspot.com/2011/02/ripple-effect-in-webgl.html
// to make ripple effect

layout(location=0) in vec3 pos;

uniform mat4 MVP;
uniform float time;

const float amplitude = 0.125;
const float frequency = 4;
const float PI = 3.14159;

void main()
{
    float r = length(pos);
    float y = amplitude * sin(-PI * r * frequency+time);
    gl_Position = MVP * vec4(pos.x, y, pos.z, 1.);
}
#version 430 core

layout(location=0) in vec3 pos;
layout(location=1) in vec3 normal;

uniform vec4 lightPos; // light position
uniform vec3 Kd; // diffuse reflectivity
uniform vec3 Ld; // diffuse intensity

uniform mat3 NormalMatrix;
uniform mat4 MVP; // modle view projection matrix
uniform mat4 MV; // modle view matrix

out vec3 color;

void main()
{
    vec3 norm = normalize(NormalMatrix * normal);
    vec4 eye = MV * vec4(pos, 1.);
    vec3 dir = normalize(vec3(lightPos - eye));
    
    color = Ld * Kd * max(dot(dir, norm), 0.);
    
    gl_Position = MVP * vec4(pos, 1.);
}
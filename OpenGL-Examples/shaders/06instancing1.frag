#version 330

in vec4 fcolor;
layout(location = 0) out vec4 FragColor;

void main()
{
    FragColor = fcolor;
    // the following line is required for fxaa (will not work with blending)
    FragColor.a = dot(fcolor.rgb, vec3(0.299, 0.587, 0.114));
}

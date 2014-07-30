#version 330

in vec2 txcoord;

layout(location = 0) out vec4 FragColor;

void main()
{
    float s = 0.2 * (1 / (1 + 15. * dot(txcoord, txcoord)) - 1 / 16.);
    FragColor = s * vec4(.3, 0.3, 1.0, 1);
}

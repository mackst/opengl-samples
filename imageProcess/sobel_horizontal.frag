#version 430

in vec2 uv;

uniform sampler2D textureMap;

out vec4 outColor;

// filter
const float filterWeights[9] = {-1.,  0.,  1.,
                                -2.,  0.,  2.,
                                -1.,  0.,  1.};
const float factor = 1.0;

void main()
{
    ivec2 texSize = textureSize(textureMap, 0);
    float s = float(texSize.s);
    float t = float(texSize.t);
    
    // pixel offset
    vec2 step01 = vec2(1. / s, 0.);
    vec2 step02 = vec2(0., 1. / t);
    vec2 step03 = vec2(1. / s, 1. / t);
    vec2 step04 = vec2(1. / s, -1. / t);
    
    vec3 color = vec3(0., 0., 0.);
    
    color += texture(textureMap, uv).rgb * filterWeights[4];
    color += texture(textureMap, uv - step04).rgb * filterWeights[0];
    color += texture(textureMap, uv + step02).rgb * filterWeights[1];
    color += texture(textureMap, uv + step03).rgb * filterWeights[2];
    color += texture(textureMap, uv - step01).rgb * filterWeights[3];
    color += texture(textureMap, uv + step01).rgb * filterWeights[5];
    color += texture(textureMap, uv - step03).rgb * filterWeights[6];
    color += texture(textureMap, uv - step02).rgb * filterWeights[7];
    color += texture(textureMap, uv + step04).rgb * filterWeights[8];
    
    color /= factor;
    
    outColor = vec4(color, 1.0);
}
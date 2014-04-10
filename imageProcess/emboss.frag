#version 430

in vec2 uv;

uniform sampler2D textureMap;

out vec4 outColor;

// filter
//const float filterWeights[9] = { 0., 0., 1.,
//                                 0., 1., 0.,
//                                 0., 0., 0. };
//const float factor = 1.;

void main()
{
    ivec2 texSize = textureSize(textureMap, 0);
    float s = float(texSize.s);
    float t = float(texSize.t);
    
    // pixel offset
    //vec2 step01 = vec2(1. / s, 0.);
    //vec2 step02 = vec2(0., 1. / t);
    vec2 step03 = vec2(1. / s, 1. / t);
    //vec2 step04 = vec2(1. / s, -1. / t);
    
    vec3 color = vec3(0., 0., 0.);
    
    vec3 color0 = texture(textureMap, uv).rgb;
    vec3 color3 = texture(textureMap, uv + step03).rgb;
    
    vec3 diffs = color0 - color3;
    float maxValue = diffs.r;
    if(abs(diffs.g) > abs(maxValue))
        maxValue = diffs.g;
    if(abs(diffs.b) > abs(maxValue))
        maxValue = diffs.b;
    
    float gray = clamp(maxValue + .5, 0., 1.);
    outColor = vec4(gray, gray, gray, 1.0);
}

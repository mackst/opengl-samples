#version 430

smooth in vec2 uv;

uniform sampler2D textureMap;
uniform bool useFilter; // turn filter on or off

out vec4 outColor;

// filter
const float filterWeights[9] = { 1.0f, 2.0f, 1.0f,
                               2.0f, 4.0f, 2.0f,
                               1.0f, 2.0f, 1.0f };


void main()
{
    vec4 color = texture(textureMap, uv);
    
    if(useFilter)
    {
        ivec2 texSize = textureSize(textureMap, 0);
        float s = float(texSize.s);
        float t = float(texSize.t);
        
        vec2 step01 = vec2(1. / s, 0.);
        vec2 step02 = vec2(0., 1. / t);
        vec2 step03 = vec2(1. / s, 1. / t);
        vec2 step04 = vec2(1. / s, -1. / t);
        
        vec3 tempColor = vec3(0., 0., 0.);
        
        tempColor += color.rgb * filterWeights[4];
        tempColor += texture(textureMap, uv - step04).rgb * filterWeights[0];
        tempColor += texture(textureMap, uv + step02).rgb * filterWeights[1];
        tempColor += texture(textureMap, uv + step03).rgb * filterWeights[2];
        tempColor += texture(textureMap, uv - step01).rgb * filterWeights[3];
        tempColor += texture(textureMap, uv + step01).rgb * filterWeights[5];
        tempColor += texture(textureMap, uv - step03).rgb * filterWeights[6];
        tempColor += texture(textureMap, uv - step02).rgb * filterWeights[7];
        tempColor += texture(textureMap, uv + step04).rgb * filterWeights[8];
        
        tempColor /= (filterWeights[0] + filterWeights[1] + filterWeights[2] + filterWeights[3] + filterWeights[4] + filterWeights[5] + filterWeights[6] + filterWeights[7] + filterWeights[8]);
        
        outColor = vec4(tempColor, 1.0);
    } else {
        outColor = color;
    }
}
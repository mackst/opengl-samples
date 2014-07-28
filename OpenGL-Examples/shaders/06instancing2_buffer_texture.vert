#version 330

uniform mat4 ViewProjection;
uniform samplerBuffer offset_texture; // the buffer_texture sampler
layout(location=0) in vec4 vposition;
layout(location=1) in vec4 vcolor;

out vec4 fcolor;

void main()
{
    // access the buffer texture with the InstanceID (tbo[InstanceID])
    vec4 offset = texelFetch(offset_texture, gl_InstanceID);
    fcolor = vcolor;
    gl_Position = ViewProjection * (vposition + offset);
}

#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_position;

out vec2 uv_0;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_model;

void main() {
    uv_0 = in_texcoord_0;
    gl_Position = matrix_projection * matrix_view * matrix_model * vec4(in_position, 1.0);
}

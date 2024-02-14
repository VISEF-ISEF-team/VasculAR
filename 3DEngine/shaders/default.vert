#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec2 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_model;

void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(matrix_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(matrix_model))) * vec3(in_normal, 0.0);
    gl_Position = matrix_projection * matrix_view * matrix_model * vec4(in_position, 1.0);
}

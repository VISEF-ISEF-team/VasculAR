#version 330 core

layout (location = 2) in vec3 in_position;

uniform mat4 matrix_projection;
uniform mat4 matrix_view_light;
uniform mat4 matrix_model;

void main() {
    mat4 mvp = matrix_projection * matrix_view_light * matrix_model;
    gl_Position = mvp * vec4(in_position, 1.0);
}
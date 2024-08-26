@echo off
gcc c_testing/glfw.c -I./include/GLFW -I./include/GL -L./libs/GLFW -lglfw3 -lopengl32 -lgdi32 -lglew32 -lm

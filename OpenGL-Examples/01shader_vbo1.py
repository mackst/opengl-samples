# -*- coding: utf-8 -*-

# OpenGL example code - Shader and VBO
# This example shows the setup and usage of shaders and a vbo+vao

import ctypes

import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders

from glfw import *


class Window(object):

    def __init__(self, width=640, height=480, title='GLFW opengl window'):
        self.width = width
        self.height = height
        self.title = title
        self.window = None

        self.__vertexShader = './shaders/01shader_vbo1.vert'
        self.__fragmentShader = './shaders/01shader_vbo1.frag'
        self.__shaderProgram = None
        self.__vao = None

    def shaderFromFile(self, shaderType, shaderFile):
        """read shader from file and compile it"""
        shaderSrc = ''
        with open(shaderFile) as sf:
            shaderSrc = sf.read()

        return shaders.compileShader(shaderSrc, shaderType)

    def initGL(self):
        """opengl initialization"""
        # load shaders
        vertexShader = self.shaderFromFile(GL_VERTEX_SHADER, self.__vertexShader)
        fragmentShader = self.shaderFromFile(GL_FRAGMENT_SHADER, self.__fragmentShader)
        self.__shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
        if not self.__shaderProgram:
            self.close()

        # generate and bind the vao
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)

        # generate and bind the buffer object
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        # data for a fullscreen quad
        vertexData = np.array([
                               # x   y    z      R    G    B
                                1.0, 1.0, 0.0,  1.0, 0.0, 0.0, # vertex 0
                               -1.0, 1.0, 0.0,  0.0, 1.0, 0.0, # vertex 1
                                1.0, -1.0, 0.0, 0.0, 0.0, 1.0, # vertex 2
                                1.0, -1.0, 0.0, 0.0, 0.0, 1.0, # vertex 3
                               -1.0, 1.0, 0.0,  0.0, 1.0, 0.0, # vertex 4
                               -1.0, -1.0, 0.0, 1.0, 0.0, 0.0, # vertex 5
                               ], dtype=np.float32)

        # fill with data
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

        # set up generic attrib pointers
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))

        glBindVertexArray(0)

    def renderGL(self):
        """opengl render method"""
        # clear first
        glClear(GL_COLOR_BUFFER_BIT)

        # use the shader program
        glUseProgram(self.__shaderProgram)

        # bind the vao
        glBindVertexArray(self.__vao)

        # draw
        glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindVertexArray(0)
        glUseProgram(0)

    def initWindow(self):
        """setup window options. etc, opengl version"""
        # select opengl version
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)

    def show(self):
        """create the window and show it"""
        self.initWindow()

        self.window = glfwCreateWindow(self.width, self.height, self.title, 0, 0)
        if self.window == 0:
            glfwTerminate()
            raise Exception('failed to open window')

        glfwMakeContextCurrent(self.window)

        # initialize opengl
        self.initGL()

        while not glfwWindowShouldClose(self.window):
            glfwPollEvents()

            self.renderGL()

            # check for errors
            error = glGetError()
            if error != GL_NO_ERROR:
                raise Exception(error)

            # finally swap buffers
            glfwSwapBuffers(self.window)

        self.close()

    def close(self):
        glfwDestroyWindow(self.window)
        glfwTerminate()



if __name__ == '__main__':
    import os.path

    if glfwInit() == GL_FALSE:
        raise Exception('failed to init GLFW')

    title = os.path.basename(__file__)
    win = Window(title=title[:-3])
    win.show()

# -*- coding: utf-8 -*-

# OpenGL example code - Geometry Shader and Blending
# Uses a geometry shader to expand points to billboard quads.
# The billboards are then blended while drawing to create a galaxy
# made of particles.

import ctypes

import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders

from glfw import *
import glm


class Window(object):

    def __init__(self, width=640, height=480, title='GLFW opengl window'):
        self.width = width
        self.height = height
        self.title = title
        self.window = None

        self.__vertexShader = './shaders/%s.vert' % self.title
        self.__fragmentShader = './shaders/%s.frag' % self.title
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
        vertexData = np.array([0,], dtype=np.float32)

        # fill with data
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

        # set up generic attrib pointers
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)

        glBindVertexArray(0)

        # we are drawing 3d objects so we want depth testing
        glEnable(GL_DEPTH_TEST)


    def renderGL(self):
        """opengl render method"""
        # get the time in seconds
        t = glfwGetTime()

        # clear first
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # use the shader program
        glUseProgram(self.__shaderProgram)

        # calculate ViewProjection matrix
        projection = glm.perspective(90.0, 4.0 / 3.0, .1, 100.0)

        # translate the world/view position
        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -5.0))

        # make the camera rotate around the origin
        view = glm.rotate(view, 90.0 * t, glm.vec3(1.0, 1.0, 1.0))

        viewProjection = np.array(projection * view, dtype=np.float32)

        # set the uniform
        glUniformMatrix4fv(self.__vpLocation, 1, GL_FALSE, viewProjection)

        # bind the vao
        glBindVertexArray(self.__vao)

        # draw
        glDrawElements(GL_TRIANGLES, 6*6, GL_UNSIGNED_INT, None)

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


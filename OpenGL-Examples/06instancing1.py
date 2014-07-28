# -*- coding: utf-8 -*-

# OpenGL example code - Instancing
# create 8 instances of the cube from the perspective example
# with an additional offset buffer and AttribDivisor

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
        self.__pevShader = './shaders/05post_effect.vert'
        self.__pefShader = './shaders/05post_effect.frag'
        self.__shaderProgram = None
        self.__pesProgram = None
        self.__vao = None
        self.__pevao = None
        self.__fbo = None
        self.__vpLocation = None
        self.__peTexLocation = None
        self.__texture = None

        self.__fxaa = True
        self.__space_dow = False

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

        self.__vpLocation = glGetUniformLocation(self.__shaderProgram, 'ViewProjection')

        # generate and bind the vao
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)

        # generate and bind the buffer object
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        # data for a fullscreen quad
        vertexData = np.array([
                               # x   y    z      U    V
                               # face 0:
                                1.0, 1.0, 1.0,       1.0, 0.0, 0.0, # vertex 0
                               -1.0, 1.0, 1.0,       1.0, 0.0, 0.0, # vertex 1
                                1.0,-1.0, 1.0,       1.0, 0.0, 0.0, # vertex 2
                               -1.0,-1.0, 1.0,       1.0, 0.0, 0.0, # vertex 3

                               # face 1:
                                1.0, 1.0, 1.0,       0.0, 1.0, 0.0, # vertex 0
                                1.0,-1.0, 1.0,       0.0, 1.0, 0.0, # vertex 1
                                1.0, 1.0,-1.0,       0.0, 1.0, 0.0, # vertex 2
                                1.0,-1.0,-1.0,       0.0, 1.0, 0.0, # vertex 3

                               # face 2:
                                1.0, 1.0, 1.0,       0.0, 0.0, 1.0, # vertex 0
                                1.0, 1.0,-1.0,       0.0, 0.0, 1.0, # vertex 1
                               -1.0, 1.0, 1.0,       0.0, 0.0, 1.0, # vertex 2
                               -1.0, 1.0,-1.0,       0.0, 0.0, 1.0, # vertex 3

                               # face 3:
                                1.0, 1.0,-1.0,       1.0, 1.0, 0.0, # vertex 0
                                1.0,-1.0,-1.0,       1.0, 1.0, 0.0, # vertex 1
                               -1.0, 1.0,-1.0,       1.0, 1.0, 0.0, # vertex 2
                               -1.0,-1.0,-1.0,       1.0, 1.0, 0.0, # vertex 3

                               # face 4:
                               -1.0, 1.0, 1.0,       0.0, 1.0, 1.0, # vertex 0
                               -1.0, 1.0,-1.0,       0.0, 1.0, 1.0, # vertex 1
                               -1.0,-1.0, 1.0,       0.0, 1.0, 1.0, # vertex 2
                               -1.0,-1.0,-1.0,       0.0, 1.0, 1.0, # vertex 3

                               # face 5:
                                1.0,-1.0, 1.0,       1.0, 0.0, 1.0, # vertex 0
                               -1.0,-1.0, 1.0,       1.0, 0.0, 1.0, # vertex 1
                                1.0,-1.0,-1.0,       1.0, 0.0, 1.0, # vertex 2
                               -1.0,-1.0,-1.0,       1.0, 0.0, 1.0, # vertex 3
                               ], dtype=np.float32)

        # fill with data
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

        # set up generic attrib pointers
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))

        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)

        indexData = np.array([
                              # face 0:
                              0, 1, 2, # first triangle
                              2, 1, 3, # second triangle
                              # face 1:
                              4, 5, 6, # first triangle
                              6, 5, 7, # second triangle
                              # face 2:
                              8, 9, 10, # first triangle
                              10, 9, 11, # second triangle
                              # face 3:
                              12, 13, 14, # first triangle
                              14, 13, 15, # second triangle
                              # face 4:
                              16, 17, 18, # first triangle
                              18, 17, 19, # second triangle
                              # face 5:
                              20, 21, 22, # first triangle
                              22, 21, 23, # second triangle
                              ], dtype=np.uint)

        # fill with data
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexData.nbytes, indexData, GL_STATIC_DRAW)

        glBindVertexArray(0)

        # create and compiler post effect shader
        pevShader = self.shaderFromFile(GL_VERTEX_SHADER, self.__pevShader)
        pefShader = self.shaderFromFile(GL_FRAGMENT_SHADER, self.__pefShader)
        self.__pesProgram = shaders.compileProgram(pevShader, pefShader)

        # get texture uniform location
        self.__peTexLocation = glGetUniformLocation(self.__pesProgram, 'intexture')

        # generate and bind the vao
        self.__pevao = glGenVertexArrays(1)
        glBindVertexArray(self.__pevao)

        # generate and bind the vertex buffer object
        pevbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, pevbo)

        # data for a fullscreen quad (this time with texture coords)
        peVertexData = np.array([
                                 # x    y    z      u    v
                                  1.0, 1.0, 0.0,   1.0, 1.0,  # vertex 0
                                 -1.0, 1.0, 0.0,   0.0, 1.0,  # vertex 1
                                  1.0, -1.0, 0.0,   1.0, 0.0,  # vertex 2
                                 -1.0, -1.0, 0.0,   0.0, 0.0,  # vertex 3
                                 ], dtype=np.float32)

        # fill with data
        glBufferData(GL_ARRAY_BUFFER, peVertexData.nbytes, peVertexData, GL_STATIC_DRAW)

        # set up generic attrib pointers
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, None)

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))

        # generate and bind the index buffer object
        peibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, peibo)

        peIndexData = np.array([0, 1, 2, # first triangle
                                2, 1, 3, # second triangle
                                ], dtype=np.uint)

        # fill with data
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, peIndexData.nbytes, peIndexData, GL_STATIC_DRAW)

        # "unbind" vao
        glBindVertexArray(0)

        # generate texture
        self.__texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__texture)

        # set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # set texture content
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width, self.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))

        # generate renderbuffers
        rbf = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbf)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, self.width, self.height)

        # generate framebuffer
        self.__fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__fbo)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.__texture, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbf)

    def renderGL(self):
        """opengl render method"""
        # get the time in seconds
        t = glfwGetTime()

        # toggle fxaa on/off with space
        if glfwGetKey(self.window, GLFW_KEY_SPACE) and not self.__space_dow:
            self.__fxaa = not self.__fxaa
        self.__space_dow = glfwGetKey(self.window, GLFW_KEY_SPACE)

        # we are drawing 3d objects so we want depth testing
        glEnable(GL_DEPTH_TEST)

        # bind target framebuffer
        if self.__fxaa:
            glBindFramebuffer(GL_FRAMEBUFFER, self.__fbo)
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)

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

        # apply post processing only when fxaa is on
        if self.__fxaa:
            # bind the "screen frambuffer"
            glBindFramebuffer(GL_FRAMEBUFFER, 0)

            # we are not 3d rendering so no depth test
            glDisable(GL_DEPTH_TEST)

            # use the shader program
            glUseProgram(self.__pesProgram)

            # bind texture to texture unit 0
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.__texture)

            # set uniform
            glUniform1i(self.__peTexLocation, 0)

            # bind the vao
            glBindVertexArray(self.__pevao)

            # draw
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

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


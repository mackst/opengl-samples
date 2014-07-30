# -*- coding: utf-8 -*-

# OpenGL example code - transform feedback
# This example simulates the same particle system as the buffer mapping
# example. Instead of updating particles on the cpu and uploading
# the update is done on the gpu with transform feedback.

import math
import ctypes
from random import randint
from random import random as rand

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
        self.__geomShader = './shaders/%s.geom' % self.title
        self.__fragmentShader = './shaders/%s.frag' % self.title
        self.__shaderProgram = None
        self.__vao = None
        self.__vbo = None

        self.__viewLocation = None
        self.__projLocation = None

        self.__particles = 128 * 1024
        self.__tfShader = './shaders/09tfshader.vert'
        self.__tshaderProgram = None
        self.__centerLocation = None
        self.__radiusLocation = None
        self.__gLocation = None
        self.__dtLocation = None
        self.__bounceLocation = None
        self.__seedLocation = None

        self.__center = []
        self.__radius = []
        # physical parameters
        self.__dt = 1.0 / 60.0
        self.__g = glm.vec3(0.0, -9.81, 0.0)
        self.__bounce = 1.2  # inelastic: 1.0, elastic: 2.0

        self.__currentBuffer = 0
        self.__bufferCount = 2

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
        geomShader = self.shaderFromFile(GL_GEOMETRY_SHADER, self.__geomShader)
        fragmentShader = self.shaderFromFile(GL_FRAGMENT_SHADER, self.__fragmentShader)
        self.__shaderProgram = shaders.compileProgram(vertexShader, geomShader, fragmentShader)
        if not self.__shaderProgram:
            self.close()

        # obtain location of projection uniform
        self.__viewLocation = glGetUniformLocation(self.__shaderProgram, 'View')
        self.__projLocation = glGetUniformLocation(self.__shaderProgram, 'Projection')

        # transform feedback shader and program
        tfShader = self.shaderFromFile(GL_VERTEX_SHADER, self.__tfShader)
        self.__tshaderProgram = glCreateProgram()
        glAttachShader(self.__tshaderProgram, tfShader)

        # specify transform feedback output
        varyings = (ctypes.c_char_p * 2)("outposition", "outvelocity")
        c_array = ctypes.cast(varyings, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        glTransformFeedbackVaryings(self.__tshaderProgram, len(varyings), c_array, GL_INTERLEAVED_ATTRIBS)

        glLinkProgram(self.__tshaderProgram)

        self.__centerLocation = glGetUniformLocation(self.__tshaderProgram, 'center')
        self.__radiusLocation = glGetUniformLocation(self.__tshaderProgram, 'radius')
        self.__gLocation = glGetUniformLocation(self.__tshaderProgram, 'g')
        self.__dtLocation = glGetUniformLocation(self.__tshaderProgram, 'dt')
        self.__bounceLocation = glGetUniformLocation(self.__tshaderProgram, 'bounce')
        self.__seedLocation = glGetUniformLocation(self.__tshaderProgram, 'seed')

        # randomly place particles in a cube
        vertexData = []
        for i in xrange(self.__particles):
            # initial position
            pos = glm.vec3(.5 - rand(),
                           .5 - rand(),
                           .5 - rand())
            vertexData.append(glm.vec3(0.0, 20.0, 0.0) + 5.0 * pos)

            # initial velocity
            vertexData.append(glm.vec3(0.0, 0.0, 0.0))

        # generate vbos and vaos
        self.__vao = glGenVertexArrays(self.__bufferCount)
        self.__vbo = glGenBuffers(self.__bufferCount)

        vertexData = np.array(vertexData, dtype=np.float32)
        for i in range(self.__bufferCount):
            glBindVertexArray(self.__vao[i])

            glBindBuffer(GL_ARRAY_BUFFER, self.__vbo[i])

            # fill with initial data
            glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

            # set up generic attrib pointers
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)
            # set up generic attrib pointers
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))

        glBindVertexArray(0)

        # we are blending so no depth testing
        glDisable(GL_DEPTH_TEST)

        # enable blending
        glEnable(GL_BLEND)
        # and set the blend function to result = 1 * source + 1 * destination
        glBlendFunc(GL_ONE, GL_ONE)

        # define sphere for the particles to bounce off
        center = []
        radius = []
        center.append((0.0, 12.0, 1.0))
        radius.append(3)
        center.append((-3.0, 0.0, 0.0))
        radius.append(7)
        center.append((5.0, -10.0, 0.0))
        radius.append(12)
        self.__center = np.array(center, dtype=np.float32)
        self.__radius = np.array(radius, dtype=np.float32)

        # physical parameters
        self.__dt = 1.0 / 60.0
        self.__g = np.array((0.0, -9.81, 0.0), dtype=np.float32)
        self.__bounce = 1.2

        self.__currentBuffer = 0

    def renderGL(self):
        """opengl render method"""
        # get the time in seconds
        t = glfwGetTime()

        # use the transform shader program
        glUseProgram(self.__tshaderProgram)

        # set the uniforms
        glUniform3fv(self.__centerLocation, 3, self.__center)
        glUniform1fv(self.__radiusLocation, 3, self.__radius)
        glUniform3fv(self.__gLocation, 1, self.__g)
        glUniform1f(self.__dtLocation, self.__dt)
        glUniform1f(self.__bounceLocation, self.__bounce)
        glUniform1i(self.__seedLocation, randint(0, 0x7fff))

        # bind the current vao
        glBindVertexArray(self.__vao[(self.__currentBuffer + 1) % self.__bufferCount])

        # bind transform feedback target
        glBindBufferBase(GL_TRANSFORM_FEEDBACK_BUFFER, 0, self.__vbo[self.__currentBuffer])

        glEnable(GL_RASTERIZER_DISCARD)

        # perform transform feedback
        glBeginTransformFeedback(GL_POINTS)
        glDrawArrays(GL_POINTS, 0, self.__particles)
        glEndTransformFeedback()

        glDisable(GL_RASTERIZER_DISCARD)

        # clear first
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # use the shader program
        glUseProgram(self.__shaderProgram)

        # calculate ViewProjection matrix
        projection = glm.perspective(90.0, 4.0 / 3.0, .1, 100.0)
        projection = np.array(projection, dtype=np.float32)

        # translate the world/view position
        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -30.0))

        # make the camera rotate around the origin
        view = glm.rotate(view, 30.0, glm.vec3(1.0, 0.0, 0.0))
        view = glm.rotate(view, -22.5 * t, glm.vec3(0.0, 1.0, 0.0))
        view = np.array(view, dtype=np.float32)

        # set the uniform
        glUniformMatrix4fv(self.__viewLocation, 1, GL_FALSE, view)
        glUniformMatrix4fv(self.__projLocation, 1, GL_FALSE, projection)

        # bind the vao
        glBindVertexArray(self.__vao[self.__currentBuffer])

        # draw
        glDrawArrays(GL_POINTS, 0, self.__particles)

        glBindVertexArray(0)
        glUseProgram(0)

        # advance buffer index
        self.__currentBuffer = (self.__currentBuffer + 1) % self.__bufferCount

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


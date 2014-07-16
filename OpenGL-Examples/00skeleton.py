# -*- coding: utf-8 -*-

# OpenGL example code - Skeleton
# Skeleton code that all the other examples are based on


from OpenGL.GL import *

from pyglfw.glfw import *


class Window(object):

    def __init__(self, width=640, height=480, title='GLFW opengl window'):
        self.width = width
        self.height = height
        self.title = title

    def initGL(self):
        """opengl initialization"""
        pass

    def renderGL(self):
        """opengl render method"""
        pass

    def initWindow(self):
        """setup window options. etc, opengl version"""
        # select opengl version
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)

    def show(self):
        """create the window and show it"""
        self.initWindow()

        window = glfwCreateWindow(self.width, self.height, self.title, 0, 0)
        if window == 0:
            glfwTerminate()
            raise Exception('failed to open window')

        glfwMakeContextCurrent(window)

        # initialize opengl
        self.initGL()

        while not glfwWindowShouldClose(window):
            glfwPollEvents()

            self.renderGL()

            # check for errors
            error = glGetError()
            if error != GL_NO_ERROR:
                raise Exception(error)

            # finally swap buffers
            glfwSwapBuffers(window)

        glfwDestroyWindow(window)
        glfwTerminate()



if __name__ == '__main__':
    if glfwInit() == GL_FALSE:
        raise Exception('failed to init GLFW')

    win = Window()
    win.show()

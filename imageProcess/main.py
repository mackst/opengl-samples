#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''display an image using opengl'''


import sys

import PySide
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtOpenGL import *

from OpenGL.GL import *
from OpenGL.GL import shaders

import numpy as np
from PIL import Image

def shaderFromFile(shaderType, shaderFile):
    '''create shader from file'''
    shaderSrc = ''
    with open(shaderFile) as sf:
        shaderSrc = sf.read()
    return shaders.compileShader(shaderSrc, shaderType)

class MyGLWidget(QGLWidget):
    
    def __init__(self, gformat, parent=None):
        super(MyGLWidget, self).__init__(gformat, parent)
        
        # filter shaders
        self.filters = ('shader.frag', 'gaussian.frag', )
        self.activeFilter = 'shader.frag'
        
        # buffer object ids
        self.vaoID = None
        self.vboVerticesID = None
        self.vboIndicesID = None
        self.textureID = None
        self.sprogram = {}
        
        self.vertices = None
        self.indices = None
        
        # chang this to load your image file
        self.loadImage('Lenna.png')
        
    def loadImage(self, imageFile):
        # load the image using Pillow
        self.im = Image.open(imageFile)
        
        # set window size to the images size
        self.setGeometry(40, 40, self.im.size[0], self.im.size[1])
        # set window title
        self.setWindowTitle('Dispaly with filter[%s]' % self.activeFilter)
    
    def initializeGL(self):
        glClearColor(0, 0, 0, 0)
        
        # load shaders
        for shader in self.filters:
            # create shader from file
            vshader = shaderFromFile(GL_VERTEX_SHADER, 'shader.vert')
            fshader = shaderFromFile(GL_FRAGMENT_SHADER, shader)
            # compile shaders
            self.sprogram[shader] = shaders.compileProgram(vshader, fshader)
        
            # get attribute and set uniform for shaders
            glUseProgram(self.sprogram[shader])
            self.vertexAL = glGetAttribLocation(self.sprogram[shader], 'pos')
            self.tmUL = glGetUniformLocation(self.sprogram[shader], 'textureMap')
            glUniform1i(self.tmUL, 0)
            glUseProgram(0)
        
        # two triangle to make a quad
        self.vertices = np.array((0.0, 0.0, 
                                  1.0, 0.0, 
                                  1.0, 1.0, 
                                  0.0, 1.0), dtype=np.float32)
        self.indices = np.array((0, 1, 2, 
                                 0, 2, 3), dtype=np.ushort)
        
        # set up vertex array
        self.vaoID = glGenVertexArrays(1)
        self.vboVerticesID = glGenBuffers(1)
        self.vboIndicesID = glGenBuffers(1)
        
        glBindVertexArray(self.vaoID)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboVerticesID)
        # copy vertices data from memery to gpu memery
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # tell opengl how to procces the vertices data
        glEnableVertexAttribArray(self.vertexAL)
        glVertexAttribPointer(self.vertexAL, 2, GL_FLOAT, GL_FALSE, 0, None)
        # send the indice data too
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vboIndicesID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
        # flip the image in the Y axis
        im = self.im.transpose(Image.FLIP_TOP_BOTTOM)
        
        # set up texture
        self.textureID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        # set filters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # set uv coords mode
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        # send the image data to gpu memery
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.im.size[0], self.im.size[1], 
                     0, GL_RGB, GL_UNSIGNED_BYTE, im.tostring())
        
        print("Initialization successfull")
        
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        
    def paintGL(self, *args, **kwargs):
        # clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # active shader
        glUseProgram(self.sprogram[self.activeFilter])
        # draw triangles
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_SHORT, None)
        glUseProgram(0)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            index = self.filters.index(self.activeFilter)
            if index == len(self.filters) - 1:
                index = 0
            else:
                index += 1
            self.activeFilter = self.filters[index]
            self.setWindowTitle('Dispaly with filter[%s]' % self.activeFilter)
        self.updateGL()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gformat = QGLFormat()
    gformat.setVersion(4, 3)
    gformat.setProfile(QGLFormat.CoreProfile)
    mywidget = MyGLWidget(gformat)
    mywidget.show()
    
    # print information on screen
    sys.stdout.write("\tUsing PySide " + PySide.__version__)
    sys.stdout.write("\n\tVendor: " + glGetString(GL_VENDOR))
    sys.stdout.write("\n\tRenderer: " + glGetString(GL_RENDERER))
    sys.stdout.write("\n\tVersion: " + glGetString(GL_VERSION))
    sys.stdout.write("\n\tGLSL: " + glGetString(GL_SHADING_LANGUAGE_VERSION))
    
    sys.exit(app.exec_())


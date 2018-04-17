'''An opengl demo for PyQt5
test on Windows with Python3.6
'''

import array

from PySide2 import QtGui


GL_FLOAT = 0x1406
GL_COLOR_BUFFER_BIT = 0x00004000
GL_TRIANGLES = 0x0004
GL_VERSION = 0x1F02

vertexShaderCode = '''#version 410  
  
layout(location=0) in vec4 position;  
layout(location=1) in vec4 color;  
  
out vec4 theColor;  
  
void main()  
{  
    gl_Position = position;  
    theColor = color;  
} 
'''

fragmentShaderCode = '''#version 410  
  
in vec4 theColor;  
  
out vec4 outColor;  
  
void main()  
{  
    outColor = theColor;  
}
'''

class Triangle(QtGui.QOpenGLWindow, QtGui.QOpenGLFunctions):

    def __init__(self, parent=None):
        # super(Triangle, self).__init__(QtGui.QOpenGLWindow.NoPartialUpdate, parent)
        QtGui.QOpenGLWindow.__init__(self, QtGui.QOpenGLWindow.NoPartialUpdate, parent)
        QtGui.QOpenGLFunctions.__init__(self)

        format_ = QtGui.QSurfaceFormat()
        format_.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        format_.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        format_.setVersion(4, 6)
        self.setFormat(format_)

        self.program = QtGui.QOpenGLShaderProgram()
        self.vao = QtGui.QOpenGLVertexArrayObject()

    def __del__(self):
        self.program.deleteLater()
        self.vao.destroy()

    def initializeGL(self):
        # self.gl = self.context().versionFunctions()
        # self.gl = self.context().functions()
        #
        self.initializeOpenGLFunctions()
        self.printContextInformation()
        #

        self.program.create()
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex, vertexShaderCode)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment, fragmentShaderCode)
        self.program.link()
        assert self.program.isLinked()

        vertexData = array.array('f', [
            # position
            0.0, 0.5, 0.0, 1.0,
            0.5, -0.366, 0.0, 1.0,
            -0.5, -0.366, 0.0, 1.0,
            # colors
            1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0
        ])

        vertexMem = memoryview(vertexData)

        vbo = QtGui.QOpenGLBuffer()
        vbo.create()
        vbo.setUsagePattern(vbo.StaticDraw)
        vbo.bind()
        # vbo.allocate(vertexData, vertexData.buffer_info()[1]*vertexData.itemsize)
        vbo.allocate(vertexData, vertexMem.nbytes)

        self.vao.create()
        self.vao.bind()
        vbo.bind()
        self.program.bind()

        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 4, 0)

        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, GL_FLOAT, 12*vertexMem.itemsize, 4, 0)

        self.vao.release()
        self.program.release()
        vbo.destroy()

    # def resizeGL(self, w, h):
    #     super(Triangle, self).resizeGL(w, h)

    def paintGL(self):
        self.glClear(GL_COLOR_BUFFER_BIT)
        self.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.program.bind()
        self.vao.bind()

        self.glDrawArrays(GL_TRIANGLES, 0, 3)

        self.program.release()
        self.vao.release()

    def printContextInformation(self):
        glType = 'OpenGL ES' if self.context().isOpenGLES() else "OpenGL"
        # glVersion = self.gl.glGetString(GL_VERSION)
        glVersion = self.glGetString(GL_VERSION)

        print('{} : {}'.format(glType, glVersion))


if __name__ == '__main__':
    import sys

    app = QtGui.QGuiApplication(sys.argv)

    window = Triangle()
    window.setTitle('PySide2 Opengl demo')
    window.resize(1280, 720)
    window.show()


    def cleanup():
        global window
        del window

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec_())

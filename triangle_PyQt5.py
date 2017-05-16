'''An opengl demo for PyQt5
test on Windows with Python3.6
'''

import array

from PyQt5 import QtGui


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

class Triangle(QtGui.QOpenGLWindow):

    def __init__(self, parent=None):
        super(Triangle, self).__init__(QtGui.QOpenGLWindow.NoPartialUpdate, parent)

        format_ = QtGui.QSurfaceFormat()
        format_.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        format_.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        # PyQt5 5.8.2 only has 4.1.0 opengl binding
        format_.setVersion(4, 1)
        self.setFormat(format_)

        self.gl = None
        self.program = QtGui.QOpenGLShaderProgram()
        self.vao = QtGui.QOpenGLVertexArrayObject()

    def __del__(self):
        self.program.deleteLater()
        self.vao.destroy()

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()
        #
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
        self.program.setAttributeBuffer(0, self.gl.GL_FLOAT, 0, 4, 0)

        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, self.gl.GL_FLOAT, 12*vertexMem.itemsize, 4, 0)

        self.vao.release()
        self.program.release()
        vbo.destroy()

    # def resizeGL(self, w, h):
    #     super(Triangle, self).resizeGL(w, h)

    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        self.gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.program.bind()
        self.vao.bind()

        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

        self.program.release()
        self.vao.release()

    def printContextInformation(self):
        glType = 'OpenGL ES' if self.context().isOpenGLES() else "OpenGL"
        glVersion = self.gl.glGetString(self.gl.GL_VERSION)

        print('{} : {}'.format(glType, glVersion))


if __name__ == '__main__':
    import sys

    app = QtGui.QGuiApplication(sys.argv)

    window = Triangle()
    window.setTitle('PyQt5 Opengl demo')
    window.resize(1280, 720)
    window.show()

    sys.exit(app.exec_())

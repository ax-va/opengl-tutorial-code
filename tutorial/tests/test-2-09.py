import OpenGL.GL as GL
import math
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from tutorial.core.base import Base
from tutorial.core.utils import Utils
from tutorial.core.attribute import Attribute
from tutorial.core.uniform import Uniform


class Test(Base):
    """ Animate triangle changing its color """
    def initialize(self):
        print("Initializing program...")
        # initialize program #
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self._program_ref = Utils.initialize_program(vs_code, fs_code)
        # render settings (optional) #
        # specify color used when clearly
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        # set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # set up vertex attribute #
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self._vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self._program_ref, 'position')
        # set up uniforms #
        self._translation = Uniform('vec3', [-0.5, 0.0, 0.0])
        self._translation.locate_variable(self._program_ref, 'translation')
        self._base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self._base_color.locate_variable(self._program_ref, 'baseColor')

    def update(self):
        """ Update data """
        # self._base_color.data[0] = (math.sin(3 * self._time) + 1) / 2
        self._base_color.data[0] = (math.sin(self._time) + 1) / 2
        self._base_color.data[1] = (math.sin(self._time + 2.1) + 1) / 2
        self._base_color.data[2] = (math.sin(self._time + 4.2) + 1) / 2
        # reset color buffer with specified color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self._program_ref)
        self._translation.upload_data()
        self._base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)


# instantiate this class and run the program
Test().run()
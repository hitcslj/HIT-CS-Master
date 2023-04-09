import glfw
from OpenGL.GL import *

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(640, 480, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Clear the screen to black
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw a triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(-0.5, -0.5, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0.5, -0.5, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0.5, 0)
        glEnd()

        # Swap buffers
        glfw.swap_buffers(window)

        # Poll for events
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()

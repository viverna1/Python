from manim import *  # type: ignore

# config.media_dir = "Librares/.mainm/media"
config.frame_rate = 60

class Math(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # place the circle two units left from the origin
        circle.move_to(LEFT * 2)
        # place the square to the left of the circle
        square.next_to(circle, LEFT)
        # align the left border of the triangle to the left border of the circle
        triangle.align_to(circle, LEFT)

        self.play(Create(circle), Create(square), Create(triangle))
        self.wait(1)

if __name__ == "__main__":
    scene = Math()
    scene.render()

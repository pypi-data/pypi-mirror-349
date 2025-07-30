import pygame

class SpriteAnimation:
    def __init__(self, image_path, frame_size, frame_duration, loop=True, final_size=None, flipped=False):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_size = frame_size  # (width, height)
        self.frame_duration = frame_duration  # Time per frame in milliseconds
        self.loop = loop
        self.final_size = final_size  # (width, height) to scale each frame
        self.default_flipped = flipped  # Used if draw() doesn't specify

        self.frames = self._load_frames()
        self.current_frame = 0
        self.time_accumulator = 0
        self.finished = False

    def _load_frames(self):
        frames = []
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        frame_width, frame_height = self.frame_size

        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                rect = pygame.Rect(x, y, frame_width, frame_height)
                frame = self.sprite_sheet.subsurface(rect).copy()

                # Scale if needed
                if self.final_size:
                    frame = pygame.transform.scale(frame, self.final_size)

                frames.append(frame)

        return frames

    def update(self, dt):
        if self.finished:
            return

        self.time_accumulator += dt
        if self.time_accumulator >= self.frame_duration:
            self.time_accumulator = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def draw(self, surface, position, flipped=None):
        if not self.frames:
            return

        frame = self.frames[self.current_frame]

        # Use default flipped if not specified
        if flipped is None:
            flipped = self.default_flipped

        if flipped:
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, position)

    def reset(self):
        self.current_frame = 0
        self.time_accumulator = 0
        self.finished = False

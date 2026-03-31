def load_image(filepath):
    """Load an image from the specified filepath."""
    return pygame.image.load(filepath)

def handle_input():
    """Handle user input and return the state of keys."""
    return pygame.key.get_pressed()

def draw_text(surface, text, position, font, color):
    """Draw text on the given surface at the specified position."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def reset_game_settings():
    """Reset game settings to default values."""
    return {
        'gravity': 0.5,
        'jump_power': 10,
        'player_speed': 5,
    }
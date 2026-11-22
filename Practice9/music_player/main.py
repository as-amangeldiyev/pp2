from pathlib import Path

import pygame


music_folder = Path(__file__).parent / "music"
tracks = sorted(
    [file for file in music_folder.iterdir() if file.suffix.lower() in (".mp3", ".wav", ".ogg")],
    key=lambda file: file.name.lower(),
)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((760, 420))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
next_track = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(next_track)
index = 0
paused = False
playing = False
running = True


def play_track():
    global paused, playing
    if tracks:
        pygame.mixer.music.load(str(tracks[index]))
        pygame.mixer.music.play()
        paused = False
        playing = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == next_track and tracks and playing:
            index = (index + 1) % len(tracks)
            play_track()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                if pygame.mixer.music.get_busy() and not paused:
                    pygame.mixer.music.pause()
                    paused = True
                elif paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    play_track()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                paused = False
                playing = False
                pygame.event.clear(next_track)
            elif event.key in (pygame.K_n, pygame.K_b) and tracks:
                change = 1 if event.key == pygame.K_n else -1
                index = (index + change) % len(tracks)
                play_track()

    screen.fill((28, 32, 44))
    if tracks:
        title = tracks[index].name
        seconds = max(0, pygame.mixer.music.get_pos()) // 1000
        position = f"{seconds // 60:02}:{seconds % 60:02}"
    else:
        title = "Add music files to the music folder"
        position = "00:00"

    screen.blit(font.render("Music Player", True, "white"), (35, 40))
    screen.blit(font.render(title, True, "white"), (35, 125))
    screen.blit(font.render("Position: " + position, True, "white"), (35, 180))
    screen.blit(font.render("P Play/Pause   S Stop   N Next   B Previous   Q Quit", True, "white"), (35, 300))
    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()

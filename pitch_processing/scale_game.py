freqs = [
    32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74,
    65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 
    130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 
    261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 
    523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 
    1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53,
    2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07, 
    4186.01 # C1 to C8
]

major_steps = [0, 2, 2, 1, 2, 2, 2, 1]

root_note = 0
cur_note = 0  # Means we need to hit root note, then it increments
major_index = 0
good_streak = 0  # To determine when we have succeeded in "hitting" a note 
score = 0
time_intervals = [] # To measure how long it takes to hit each note

pitch_values = [0]  # Example pitch value in Hz

def check_note_success(pitch):
    global cur_note
    global major_index
    global good_streak
    global score
    global prev_time
    target = freqs[cur_note]
    if pitch > target - 3 and pitch < target + 3:
        good_streak += 1
        if good_streak >= 10: # FPS = 20
            h = target - freqs[root_note] + 25
            y = height - h * scaling 
            pygame.draw.rect(fixed_surface, white_trans, (0, y, width, height - y))
            major_index += 1
            if major_index < len(major_steps):
                cur_note = cur_note + major_steps[major_index]
            score += 1
            good_streak = 0
            time_intervals.append(int(round(time.time() - prev_time, 0)))
            prev_time = time.time()
    else:
        good_streak = 0


running = True
menu_phase = True
results_phase = False
prev_time = 0

key_set = 'cdefgab'
key_index = 0
key_number = 4

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            stream.stop_stream()
            stream.close()
            p.terminate()
            pygame.quit()
            sys.exit()
        elif menu_phase and event.type == pygame.KEYDOWN:
            button = event.unicode
            if button in key_set:
                key_index = key_set.index(button)
            elif button in '1234567':
                root_note = 0
                cur_note = 0 
                major_index = 0
                good_streak = 0
                score = 0
                time_intervals = []
                pitch_values = [0] 

                key_number = int(button)
                relative_C = (key_number-1) * 12
                root_note = relative_C + sum(major_steps[:key_index+1])
                cur_note = root_note
                major_index = 0
                freq_range = [freqs[root_note + sum(major_steps[:i+1])] for i in range(len(major_steps))]
                fixed_surface.fill(black)
                draw_bg(freq_range)
                menu_phase = False 
                prev_time = time.time()
        elif results_phase and event.type == pygame.KEYDOWN: 
            button = event.unicode
            if button == 'r':
                results_phase = False
                menu_phase = True
                text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    if menu_phase or results_phase:
        screen.fill(black)
        for i, text_surface in enumerate(text_surfaces):
            y_position = i * text_surface.get_height()
            screen.blit(text_surface, ((width - text_surface.get_width()) // 2, y_position))
        pygame.display.flip()
        continue
    
    # Clear the screen
    screen.fill(black)

    screen.blit(fixed_surface, (0, 0))

    # Draw the bar based on the pitch value
    pitch = np.mean(np.array(pitch_values[-7:]))
    draw_bar(pitch)
    check_note_success(pitch)
    if score == 8:
        text_surfaces = [font.render("Note " + str(8 - i) + ": " + str(t) + " seconds", True, (255, 255, 255)) for i, t in enumerate(time_intervals[::-1])]
        results_phase = True
        
    # Update the display
    pygame.display.flip()

    # Set the frame rate (adjust as needed)
    pygame.time.Clock().tick(20)


#define SDL_MAIN_HANDLED
#include <SDL2/SDL.h>
#include <stdlib.h>
#include <stdio.h>

#define GRID_SIZE 20
#define CELL_SIZE 25
#define SCREEN_WIDTH (GRID_SIZE * CELL_SIZE)
#define SCREEN_HEIGHT (GRID_SIZE * CELL_SIZE)

typedef struct {
    int x, y;
} Point;

typedef struct {
    Point* segments;
    int length;
    int direction; // 0=right, 1=down, 2=left, 3=up
} Snake;

Point food;
Snake snake;

void initGame(void) {
    // Initialize snake in the middle
    snake.length = 1;
    snake.segments = malloc(sizeof(Point) * GRID_SIZE * GRID_SIZE);
    snake.segments[0].x = GRID_SIZE / 2;
    snake.segments[0].y = GRID_SIZE / 2;
    snake.direction = 0;

    // Place initial food
    food.x = rand() % GRID_SIZE;
    food.y = rand() % GRID_SIZE;
}

void drawGame(SDL_Surface* surface) {
    // Clear screen (black)
    SDL_FillRect(surface, NULL, SDL_MapRGB(surface->format, 0, 0, 0));

    // Draw snake (green)
    SDL_Rect rect;
    rect.w = CELL_SIZE - 2;
    rect.h = CELL_SIZE - 2;
    for(int i = 0; i < snake.length; i++) {
        rect.x = snake.segments[i].x * CELL_SIZE + 1;
        rect.y = snake.segments[i].y * CELL_SIZE + 1;
        SDL_FillRect(surface, &rect, SDL_MapRGB(surface->format, 0, 255, 0));
    }

    // Draw food (red)
    rect.x = food.x * CELL_SIZE + 1;
    rect.y = food.y * CELL_SIZE + 1;
    SDL_FillRect(surface, &rect, SDL_MapRGB(surface->format, 255, 0, 0));
}

int main(int argc, char* argv[]) {
    SDL_Window* window = NULL;
    SDL_Surface* screenSurface = NULL;
    
    if(SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    window = SDL_CreateWindow("Snake Game", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        fprintf(stderr, "Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    screenSurface = SDL_GetWindowSurface(window);
    initGame();

    SDL_Event e;
    int quit = 0;
    Uint32 lastMove = 0;
    const int moveDelay = 150; // Snake speed (lower = faster)

    while (!quit) {
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) {
                quit = 1;
            }
            else if (e.type == SDL_KEYDOWN) {
                switch (e.key.keysym.sym) {
                    case SDLK_d:
                    case SDLK_RIGHT:
                        if (snake.direction != 2) snake.direction = 0; break;
                    case SDLK_s:
                    case SDLK_DOWN:
                        if (snake.direction != 3) snake.direction = 1; break;
                    case SDLK_a:
                    case SDLK_LEFT:
                        if (snake.direction != 0) snake.direction = 2; break;
                    case SDLK_w:
                    case SDLK_UP:
                        if (snake.direction != 1) snake.direction = 3; break;
                }
            }
        }

        Uint32 currentTime = SDL_GetTicks();
        if (currentTime - lastMove > moveDelay) {
            // Move snake body
            for (int i = snake.length - 1; i > 0; i--) {
                snake.segments[i] = snake.segments[i-1];
            }

            // Move snake head
            switch (snake.direction) {
                case 0: snake.segments[0].x++; break;
                case 1: snake.segments[0].y++; break;
                case 2: snake.segments[0].x--; break;
                case 3: snake.segments[0].y--; break;
            }

            // Check food collision
            if (snake.segments[0].x == food.x && snake.segments[0].y == food.y) {
                snake.length++;
                food.x = rand() % GRID_SIZE;
                food.y = rand() % GRID_SIZE;
            }

            lastMove = currentTime;
        }

        drawGame(screenSurface);
        SDL_UpdateWindowSurface(window);
        SDL_Delay(16);
    }

    free(snake.segments);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

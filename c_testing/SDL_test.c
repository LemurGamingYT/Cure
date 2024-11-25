#define SDL_MAIN_HANDLED
#include <SDL2/SDL.h>
#include <stdio.h>


#define BOARD_SIZE 8
#define CELL_SIZE 80
#define SCREEN_SIZE (BOARD_SIZE * CELL_SIZE)

#define true 1
#define false 0
#define bool int


typedef enum {
    WHITE, BLACK
} PieceColor;

typedef enum {
    EMPTY, PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING
} PieceType;

typedef struct {
    PieceType type;
    PieceColor color;
} Piece;


Piece board[BOARD_SIZE][BOARD_SIZE];

void initBoard(void) {
    for (int file = 0; file < BOARD_SIZE; file++) {
        for (int rank = 0; rank < BOARD_SIZE; rank++) {
            board[file][rank].type = EMPTY;
        }
    }

    for (int i = 0; i < BOARD_SIZE; i++) {
        board[1][i].type = PAWN;
        board[1][i].color = BLACK;
        board[6][i].type = PAWN;
        board[6][i].color = WHITE;
    }

    int backrow[] = {2, 3, 4, 5, 6, 4, 3, 2};
    for (int i = 0; i < BOARD_SIZE; i++) {
        board[0][i].type = backrow[i];
        board[0][i].color = BLACK;
        board[7][i].type = backrow[i];
        board[7][i].color = WHITE;
    }
}

void drawBoard(SDL_Surface* surface) {
    SDL_Rect rect;
    rect.w = CELL_SIZE;
    rect.h = CELL_SIZE;

    for (int file = 0; file < BOARD_SIZE; file++) {
        for (int rank = 0; rank < BOARD_SIZE; rank++) {
            rect.x = rank * CELL_SIZE;
            rect.y = file * CELL_SIZE;

            if ((file + rank) % 2 == 0) {
                SDL_FillRect(surface, &rect, SDL_MapRGB(surface->format, 240, 217, 181));
            } else {
                SDL_FillRect(surface, &rect, SDL_MapRGB(surface->format, 181, 136, 99));
            }
        }
    }
}


int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Could not initialise SDL\n");
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Chess", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        SCREEN_SIZE, SCREEN_SIZE, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        fprintf(stderr, "Window could not be created\n");
        return 1;
    }

    SDL_Surface* surface = SDL_GetWindowSurface(window);
    initBoard();

    SDL_Event e;
    bool running = true;
    while (running) {
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT)
                running = false;
        }

        drawBoard(surface);
        SDL_UpdateWindowSurface(window);
        SDL_Delay(16);
    }

    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

#Puzzle Assignemt 1 - Phase 1

##How to build program
*Use Python 2.7* 

##Puzzle Details
The game is Color Connect. Given a square playing board (n x n), connect the matching colors with an unbroken line. All colors must be connected and no two lines may cross. When referencing a point in the grid, the upper left corner is 0x0 and the colom should be listed first. Ex: 1,2 = column 1, row 2

##Example Input
4 2      <- 4x4 grid with 2 colors
0 e e e  <- first row, color 0 starts at position 0,0
e e 1 e  <- color 1 starts at 2,1
e e e e
1 e e 0	<- colors 1 and 0 end on row 4

##Example Output
100      <- program too 100 microseconds
10       <- there were 10 moves made
1 2 2,0 1 0,0 2 0,0 3 0,1 2 3,0 3 1,0 3 2,1 1 3,0 3 3,1 0 3 <- these are the moves
0 0 0 0  <- resulting grid with colors connected
e e 1 0  <- notice that no lines cross
e e 1 0
1 1 1 0
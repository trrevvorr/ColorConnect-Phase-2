# Color Connect - Iterative Deepening, Depth-First Tree Search

## How to Build the Script
#### Compiling*
* *Use Python 2.7*  
* Type `python solve_color_connect.py input_p1.txt`
* Tested and working on OS X, Unix, and Windows

#### Output
`180088` <- solution took 180088 **_microseconds_**   
`10`     <- there were 10 moves made  
`0 1 0, 0 2 0, 0 3 0, 0 3 1, 0 3 2, 1 1 1, 1 1 2, 1 0 2, 0 3 3, 1 0 3` <- these are the moves  
`0  0  0  0` <- resulting grid with colors connected  
`e  1  1  0`  
`1  1  e  0`  
`1  e  e  0`  

#### Output 2
If you instead compile with `python solve_color_connect.py input_p1.txt pretty`, the output will look something like this:  
![Pretty Output](http://snappyimages.nextwavesrl.netdna-cdn.com/img/b7def6c1b375dbd2fa78d9af5fd8fc8a.png)

#### Runtime
It's all relative but here are the average times I got for solving puzzles 1, 2, and 3 with SMART_FINAL_DETECT set to False.
1. 1.1 seconds
2. 115 seconds
3. 350 seconds

Here are the average times I got with SMART_FINAL_DETECT set to True.
1. 0.35 seconds
2. 12 seconds
3. 5.7 seconds

## Puzzle Details
The game is Color Connect. Given a square playing board (n x n), connect the matching colors with an unbroken line. All colors must be connected and no two lines may cross. When referencing a point in the grid, the upper left corner is 0x0 and the column should be listed first. Ex: 1,2 = column 1, row 2

#### Example Input
`4 2`      <- 4x4 grid with 2 colors  
`0 e e e`  <- first row, color 0 starts at position 0,0  
`e e 1 e`  <- color 1 starts at 2,1  
`e e e e`  
`1 e e 0`	<- colors 1 and 0 end on row 4



_* I know python isn't technically compiled, it's interpreted, but whatever_

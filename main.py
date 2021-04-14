from display import *
from draw import *
from matrix import *
from parse import *

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
transform = new_matrix()

##matrix = new_matrix()
##print("initial test matrix, returns to this after every test")
##matrix = [[0, 1, 2, 1],[3, 4, 5, 1],[6, 7, 8, 1],[9, 10, 11, 1]]
##print_matrix(matrix)
##print()
##
###translate test translate by (1,2,3)
##print("translate test, translate by (1,2,3)")
##transform = make_translate(1, 2, 3)
##matrix_mult(transform, matrix)
##print_matrix(matrix)
##print()
##
###scale test dilate everything by 2
##print("dilation test, dilate by (2,2,2)")
##matrix = [[0, 1, 2, 1],[3, 4, 5, 1],[6, 7, 8, 1],[9, 10, 11, 1]]
##transform = make_scale(2,2,2)
##matrix_mult(transform, matrix)
##print_matrix(matrix)
##print()

matrix = new_matrix()

parse_file( 'script.txt', matrix, transform, screen, [0, 0, 0] )


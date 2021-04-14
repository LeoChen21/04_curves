from display import *
from matrix import *
from draw import *
from math import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
	 circle: add a circle to the edge matrix - 
	         takes 4 arguments (cx, cy, cz, r)
	 hermite: add a hermite curve to the edge matrix -
	          takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	         takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
               then multiply the transform matrix by the translation matrix -
               takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'hermite', 'bezier'  ]

def parse_file( fname, edges, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    c = 0
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:
            c+= 1
            args = lines[c].strip().split(' ')

        if line == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, transform)

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, transform)

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(t, transform)

        elif line == 'circle':
            #cx, cy, cz, r
            t = 0.0
            r = float(args[3])
            while t < 1:
                add_point(edges, r * math.cos(2.0 * math.pi * t) + float(args[0]),
                                 r * math.sin(2.0 * math.pi * t) + float(args[1]),
                                 args[2])
                t += 0.002
##       hermite: add a hermite curve to the edge matrix -
##	          takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)

        elif line == 'hermite':
            iH = new_matrix()
            xG = new_matrix()
            yG = new_matrix()
                
            x0 = float(args[0])
            y0 = float(args[1])
            x1 = float(args[2])
            y1 = float(args[3])
            rx0 = float(args[4])
            ry0 = float(args[5])
            rx1 = float(args[6])
            ry1 = float(args[7])

            iH = [[2, -3, 0, 1], [-2, 3, 0, 0], [1, -2, 1, 0], [1, -1, 0, 0]]

            xG = [[x0, x1, rx0, rx1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
            matrix_mult(iH, xG)

            yG = [[y0, y1, ry0, ry1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
            matrix_mult(iH, yG)
                

            t = 0.0

            while t < 1:
                
                x = generate_curve_coefs(xG[0][0], xG[0][1], xG[0][2], xG[0][3], t)
                y = generate_curve_coefs(yG[0][0], yG[0][1], yG[0][2], yG[0][3], t)
                a = generate_curve_coefs(xG[0][0], xG[0][1], xG[0][2], xG[0][3], t + 0.001)
                b = generate_curve_coefs(yG[0][0], yG[0][1], yG[0][2], yG[0][3], t + 0.001)
                
                add_edge(edges, x, y, 1, a, b, 1)
                t += 0.002

            
                
##bezier: add a bezier curve to the edge matrix -
##takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
        
        elif line == 'bezier':
            B = new_matrix()
            xG = new_matrix()
            yG = new_matrix()
            
            x0 = float(args[0])
            y0 = float(args[1])
            x1 = float(args[2])
            y1 = float(args[3])
            x2 = float(args[4])
            y2 = float(args[5])
            x3 = float(args[6])
            y3 = float(args[7])

            B = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]

            xG = [[x0, x1, x2, x3], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
            matrix_mult(B, xG)

            yG = [[y0, y1, y2, y3], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
            matrix_mult(B, yG)

            t = 0.0

            while t < 1:
                
                x = generate_curve_coefs(xG[0][0], xG[0][1], xG[0][2], xG[0][3], t)
                y = generate_curve_coefs(yG[0][0], yG[0][1], yG[0][2], yG[0][3], t)
                a = generate_curve_coefs(xG[0][0], xG[0][1], xG[0][2], xG[0][3], t + 0.001)
                b = generate_curve_coefs(yG[0][0], yG[0][1], yG[0][2], yG[0][3], t + 0.001)
                
                add_edge(edges, x, y, 1, a, b, 1)
                t += 0.002
                
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )

        elif line == 'display' or line == 'save':
            clear_screen(screen)
            draw_lines(edges, screen, color)

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1

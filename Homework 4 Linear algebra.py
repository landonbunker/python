import math
import numpy as np

#Landon Bunker
#CS2300
#Program Assignment 4
#Part1: perform culling to identify whether the input traingle is back facing or front facing
#Part2: perform parallel projection for each point and project it along the projection direction, then implement persepective projection
#Part3: compute the distance between the normal and the plane, secondly see if the line intersects with the triangle

def main():
    part1_return  = []
    part2_return  = []
    part3_return  = []
    
    input_files = ["input_1.txt", "input_2.txt", "input_3.txt", "input_4.txt"]

    #part 1
    for i in input_files:
        with open(i) as f:
            file_name = "lbunker_output_A_" + i
            file = open(file_name, "w")
            first_line = f.readline()
            ints=first_line.split(" ")

            #eye location point
            num1_1=float(ints[0])
            num1_2=float(ints[1])
            num1_3=float(ints[2])

            #light direction
            ld1=float(ints[3])
            ld2=float(ints[4])
            ld3=float(ints[5])

            #for loop to iterate over the lines in the file
            for line in f:
                triangle = line
                point_array = triangle.split(" ")
                p1=float(point_array[0])
                p2=float(point_array[1])
                p3=float(point_array[2])
                q1=float(point_array[3])
                q2=float(point_array[4])
                q3=float(point_array[5])
                r1=float(point_array[6])
                r2=float(point_array[7])
                r3=float(point_array[8])

                #append the results to a list
                part1_return.append(culling(num1_1, num1_2, num1_3, p1, p2, p3, q1, q2, q3, r1, r2, r3))
                part2_return.append(intensity(ld1, ld2, ld3, p1, p2, p3, q1, q2, q3, r1, r2, r3))
                part3_return.append(culling_intensity(num1_1, num1_2, num1_3, ld1, ld2, ld3, p1, p2, p3, q1, q2, q3, r1, r2, r3))

                point_array = []

            f.close()
        
        #print the answers to the file.
        print("Culling: " , end= "")
        file.write("Cullling:")

        for num in part1_return:
            string = str(num)
            string += " "
            file.write(string)
            print(num , ", ", end = "")

        print("\nIntensity: ")
        file.write("\nIntensity: ")
        for num in part2_return:
            string = str(num)
            string += " "
            file.write(string)
            print(num , ", ", end = "")

        print("\nBoth: ")
        file.write("\nBoth: ")
        for num in part3_return:
            string = str(num)
            string += " "
            file.write(string)
            print(num , ", ", end = "")
        
        #reset the lists
        part1_return = []
        part2_return = []
        part3_return = []

    #part 2 sub part 1
    for i in input_files:
        with open(i) as f:
            
            #create and read in data from the file
            file_name = "lbunker_output_B1_" + i
            file = open(file_name, "w")
            first_line = f.readline()
            ints=first_line.split(" ")

            #plane
            plane1=float(ints[0])
            plane2=float(ints[1])
            plane3=float(ints[2])

            #normal to plane
            normal1=float(ints[3])
            normal2=float(ints[4])
            normal3=float(ints[5])

            #parallel projection
            proj1=float(ints[6])
            proj2=float(ints[7])
            proj3=float(ints[8])

            #for loop to iterate over lines
            for line in f:

                points = line
                point_array = points.split(" ")
                
                #first point
                p1=float(point_array[0])
                p2=float(point_array[1])
                p3=float(point_array[2])

                #call function and add return string to final string
                print_string = parallel_projection(plane1, plane2, plane3, normal1, normal2, normal3, proj1, proj2, proj3, p1, p2, p3)

                q1=float(point_array[3])
                q2=float(point_array[4])
                q3=float(point_array[5])

                print_string += parallel_projection(plane1, plane2, plane3, normal1, normal2, normal3, proj1, proj2, proj3, q1, q2, q3)

                r1=float(point_array[6])
                r2=float(point_array[7])
                r3=float(point_array[8])

                print_string += parallel_projection(plane1, plane2, plane3, normal1, normal2, normal3, proj1, proj2, proj3, r1, r2, r3)
                
                print_string += "\n"
                
                #write the final string to the file
                file.write(print_string)
        
        #close file so that you can open the next one
        f.close()

    #part 2 sub part 2
    for i in input_files:
        with open(i) as f:
            
            #create and read in data from the file
            file_name = "lbunker_output_B2_" + i
            file = open(file_name, "w")
            first_line = f.readline()
            ints=first_line.split(" ")

            #plane
            plane1=float(ints[0])
            plane2=float(ints[1])
            plane3=float(ints[2])

            #normal to plane
            normal1=float(ints[3])
            normal2=float(ints[4])
            normal3=float(ints[5])

            
            #for loop to iterate over lines
            for line in f:

                points = line
                point_array = points.split(" ")
                
                #first point
                p1=float(point_array[0])
                p2=float(point_array[1])
                p3=float(point_array[2])

                #call function and add return string to final string
                print_string = perspective_projection(plane1, plane2, plane3, normal1, normal2, normal3, p1, p2, p3)

                q1=float(point_array[3])
                q2=float(point_array[4])
                q3=float(point_array[5])

                print_string += perspective_projection(plane1, plane2, plane3, normal1, normal2, normal3, q1, q2, q3)

                r1=float(point_array[6])
                r2=float(point_array[7])
                r3=float(point_array[8])

                print_string += perspective_projection(plane1, plane2, plane3, normal1, normal2, normal3, r1, r2, r3)

                print_string += "\n"
                
                #write the final string to the file
                file.write(print_string)
        
        #close file so that you can open the next one
        f.close()

    #part 3 sub part 1
    for i in input_files:
        with open(i) as f:
            
            #create and read in data from the file
            file_name = "lbunker_output_C1_" + i
            file = open(file_name, "w")

            print_string = ""
            #for loop to iterate over lines
            for line in f:

                points = line
                point_array = points.split(" ")
                
                #plane
                p1=float(point_array[0])
                p2=float(point_array[1])
                p3=float(point_array[2])

                #normal
                n1=float(point_array[3])
                n2=float(point_array[4])
                n3=float(point_array[5])

                #point
                pt1=float(point_array[6])
                pt2=float(point_array[7])
                pt3=float(point_array[8])

                print_string = str(distance_point_plane(p1, p2, p3, n1, n2, n3, pt1, pt2, pt3))
                
                print_string += "\n"
                
                #write the final string to the file
                file.write(print_string)
        
        #close file so that you can open the next one
        f.close()

    #part 3 sub part 2
    for i in input_files:
        with open(i) as f:
            
            #create and read in data from the file
            file_name = "lbunker_output_C2_" + i
            file = open(file_name, "w")
            first_line = f.readline()
            ints=first_line.split(" ")

            #point1
            p1=float(ints[0])
            p2=float(ints[1])
            p3=float(ints[2])

            #point coordinate
            ptc1=float(ints[3])
            ptc2=float(ints[4])
            ptc3=float(ints[5])

            
            #for loop to iterate over lines
            for line in f:

                points = line
                point_array = points.split(" ")
                
                #first point
                ptr1=float(point_array[0])
                ptr2=float(point_array[1])
                ptr3=float(point_array[2])

                #second point
                qtr1=float(point_array[3])
                qtr2=float(point_array[4])
                qtr3=float(point_array[5])

                #third point
                rtr1=float(point_array[6])
                rtr2=float(point_array[7])
                rtr3=float(point_array[8])

                print_string = str(intersection_line_triangle(p1, p2, p3, ptc1, ptc2, ptc3, ptr1, ptr2, ptr3, qtr1, qtr2, qtr3, rtr1, rtr2 ,rtr3))

                print_string += "\n"
                
                #write the final string to the file
                file.write(print_string)
        
        #close file so that you can open the next one
        f.close()


def culling(eyelocation1, eyelocation2, eyelocation3, p1, p2, p3, q1, q2, q3, r1, r2, r3):
     #finding the centroid point 
    centroid1 = ((p1 + p2 + p3)/3)
    centroid2 = ((q1 + q2 + q3)/3)
    centroid3 = ((r1 + r2 + r3)/3)

    #calculating bottom of equation v = (e-c)/||e-c||
    v1length = eyelocation1 - centroid1 
    v2length = eyelocation2 - centroid2
    v3length = eyelocation3 - centroid3

    vlength = math.sqrt(v1length**2 + v2length**2 + v3length**2)

    #vector v from the equation
    v1 = (eyelocation1 - centroid1) / vlength
    v2 = (eyelocation2 - centroid2) / vlength
    v3 = (eyelocation3 - centroid3) / vlength

    #find vector normal
    u1 = q1 - p1
    u2 = q2 - p2
    u3 = q3 - p3

    w1 = r1 - p1
    w2 = r2 - p2
    w3 = r3 - p3
    
    cross1 = u2*w3 - w2*u3
    cross2 = u3*w1 - w3*u1
    cross3 = u1*w2 - w1*u2

    nlength = math.sqrt(cross1**2 + cross2**2 + cross3**2)

    #vector n from equation (u ^ w) / ||u ^ w||
    n1 = cross1 / nlength
    n2 = cross2 / nlength
    n3 = cross3 / nlength

    dot_product_result_part1 = (n1*v1) + (n2*v2) + (n3*v3)

    if (dot_product_result_part1 < 0):
        #back facing
        return 0 
    else:
        #front facing
        return 1

def intensity(light_direction1, light_direction2, light_direction3, p1, p2, p3, q1, q2, q3, r1, r2, r3):
    #find vector normal
    u1 = q1 - p1
    u2 = q2 - p2
    u3 = q3 - p3

    w1 = r1 - p1
    w2 = r2 - p2
    w3 = r3 - p3
    
    cross1 = u2*w3 - w2*u3
    cross2 = u3*w1 - w3*u1
    cross3 = u1*w2 - w1*u2

    nlength = math.sqrt(cross1**2 + cross2**2 + cross3**2)

    #vector n from equation (u ^ w) / ||u ^ w||
    n1 = cross1 / nlength
    n2 = cross2 / nlength
    n3 = cross3 / nlength

    #subpart2 (-d * n) / (||n|| ||d||)

    dot_product_result_part2 = (n1*-light_direction1) + (n2*-light_direction2) + (n3*-light_direction3)
    dlength = math.sqrt(light_direction1**2 + light_direction2**2 + light_direction3**2)

    cos_theta = dot_product_result_part2 / (dlength * nlength)

    if (cos_theta < 0):
        return 0
    else:
        return 1

def culling_intensity(eyelocation1, eyelocation2, eyelocation3, light_direction1, light_direction2, light_direction3, p1, p2, p3, q1, q2, q3, r1, r2, r3):
    #finding the centroid point 
    centroid1 = ((p1 + p2 + p3)/3)
    centroid2 = ((q1 + q2 + q3)/3)
    centroid3 = ((r1 + r2 + r3)/3)

    #calculating bottom of equation v = (e-c)/||e-c||
    v1length = eyelocation1 - centroid1 
    v2length = eyelocation2 - centroid2
    v3length = eyelocation3 - centroid3

    vlength = math.sqrt(v1length**2 + v2length**2 + v3length**2)

    #vector v from the equation
    v1 = (eyelocation1 - centroid1) / vlength
    v2 = (eyelocation2 - centroid2) / vlength
    v3 = (eyelocation3 - centroid3) / vlength

    #find vector normal
    u1 = q1 - p1
    u2 = q2 - p2
    u3 = q3 - p3

    w1 = r1 - p1
    w2 = r2 - p2
    w3 = r3 - p3
    
    cross1 = u2*w3 - w2*u3
    cross2 = u3*w1 - w3*u1
    cross3 = u1*w2 - w1*u2

    nlength = math.sqrt(cross1**2 + cross2**2 + cross3**2)

    #vector n from equation (u ^ w) / ||u ^ w||
    n1 = cross1 / nlength
    n2 = cross2 / nlength
    n3 = cross3 / nlength

    dot_product_result_part1 = (n1*v1) + (n2*v2) + (n3*v3)

    if (dot_product_result_part1 < 0):
        #back facing
        facingvalue = 0
        return 0
        
    else:
        #front facing
        facingvalue = 1

    #subpart2 (-d * n) / (||n|| ||d||)
    if (facingvalue == 1) :

        dot_product_result_part2 = (n1*-light_direction1) + (n2*-light_direction2) + (n3*-light_direction3)
        dlength = math.sqrt(light_direction1**2 + light_direction2**2 + light_direction3**2)

        cos_theta = dot_product_result_part2 / (dlength * nlength)

        cos_theta = round(cos_theta,4)
        return cos_theta

def parallel_projection(plane1, plane2, plane3, normal1, normal2, normal3, proj1, proj2, proj3, x1, x2, x3):
    #equation  x' = x + [([q-x] . n) / v.n]v
    #middle portion of bracket
    bracket1 = plane1 - x1
    bracket2 = plane2 - x2
    bracket3 = plane3 - x3

    #both dot products
    dot_product_bracket_n = (bracket1*normal1) + (bracket2*normal2) + (bracket3*normal3)
    dot_product_v_n = (proj1*normal1) + (proj2*normal2) + (proj3*normal3)

    #everything within the brackets
    mid = dot_product_bracket_n / dot_product_v_n

    #final point as projection
    xprime1 = x1 + (mid * normal1)
    xprime2 = x2 + (mid * normal2)
    xprime3 = x3 + (mid * normal3)

    #rounding to 4 decimal places
    xprime1 = round(xprime1, 4)
    xprime2 = round(xprime2, 4)
    xprime3 = round(xprime3, 4)

    #putting values into a final string to return
    return_string = (str(xprime1) + " " +  str(xprime2) +  " " + str(xprime3) +  " ")

    return return_string
    
def perspective_projection(plane1, plane2, plane3, normal1, normal2, normal3, x1, x2, x3):
    dot_product_p_n = (plane1*normal1) + (plane2*normal2) + (plane3*normal3)
    dot_product_x_n = (x1*normal1) + (x2*normal2) + (x3*normal3)

    xprime1 = (dot_product_p_n/dot_product_x_n) * x1
    xprime2 = (dot_product_p_n/dot_product_x_n) * x2
    xprime3 = (dot_product_p_n/dot_product_x_n) * x3

    #rounding to 4 decimal places
    xprime1 = round(xprime1, 4)
    xprime2 = round(xprime2, 4)
    xprime3 = round(xprime3, 4)

    #putting values into a final string to return
    return_string = (str(xprime1) + " " +  str(xprime2) +  " " + str(xprime3) +  " ")

    return return_string

def distance_point_plane(p1, p2, p3, n1, n2, n3, pt1, pt2, pt3):
    #equation d = ((-n . q + n . x) / n . n) ||n||
    #length of vector n
    nlength = math.sqrt(n1**2 + n2**2 + n3**2)

    #dot products 
    dot_product_pt_n = (pt1*n1) + (pt2*n2) + (pt3*n3)
    dot_product_n_n = (n1*n1) + (n2*n2) + (n3*n3)
    dot_product_plane_negativeN = (p1*-n1) + (p2*-n2) + (p3*-n3)

    # solving for t
    t = (dot_product_plane_negativeN + dot_product_pt_n) / dot_product_n_n

    #calculating total distance
    distance = t * nlength

    #round to 4 decimal places

    distance = round(distance, 4)
    return distance
    
def intersection_line_triangle(x1, x2, x3, ptc1, ptc2, ptc3, ptr1, ptr2, ptr3, qtr1, qtr2, qtr3, rtr1, rtr2, rtr3):
    #equation x + tv = p1 + u1(p2 -p1) + u2(p3 -p1)
    #vector v defined by y - x
    v1 = ptc1 - x1
    v2 = ptc2 - x2
    v3 = ptc3 - x3
    
    # w = p2 - p1, z = p3 - p1
    w1 = qtr1 - ptr1
    w2 = qtr2 - ptr2
    w3 = qtr3 - ptr3

    z1 = rtr1 - ptr1
    z2 = rtr2 - ptr2
    z3 = rtr3 - ptr3
    
    #a b and c = x_n - p1
    a = x1 - ptr1
    b = x2 - ptr2
    c = x3 - ptr3

    #3x3 matrix of w, z, and -v
    A = np.array([[w1, z1, -v1], [w2, z2, -v2], [w3, z3, -v3]])
    # a, b, c in a 3x1 matrix
    B = np.array([a, b, c])
    
    #solving for the linear system
    answers = np.linalg.pinv(A).dot(B)

    #checking to see if u1 and u2 are both between 1 and 0 as well as check if u1 +u2 is less then 1
    if (answers[0] < 1 and answers[0] > 0 and answers[1] < 1 and answers[1] > 0 and answers[0] + answers[1] < 1):
        answers[0] = round(answers[0], 4)
        answers[1] = round(answers[1], 4)
        answers[2] = round(answers[2], 4)

        return_string = str(answers[0]) + " "
        return_string += str(answers[1]) + " "
        return_string += str(answers[2])
    else:
        return_string = "Does not intersect."
    
    return return_string
   
   
    
if __name__ == "__main__":
    main()
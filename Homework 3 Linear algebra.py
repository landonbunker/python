import math
import numpy

#Landon Bunker
#CS2300
#Program Assignment 3 
#Part1: Take a 2x2 matrix and 2x1 vector and try to find the vector in the equtaion Ax=b
#Part2: Given the matrix A (2x2 matrix taking the first two column vectors from the input file), compute the eigenvalues, eigenvectors, and multiplication of the three
#Part3: given the points determine whether it is 2d or 3d and then calculate the area of the triangle and then the distance from the third point to the line


def main():

    threeDFlag = True

    output_files = ["test_input_1.txt", "test_input_2.txt", "test_input_3.txt", "test_input_4.txt"]
    output_files_part3 = ["test_input_1.txt", "test_input_2.txt", "test_input_3.txt", "test_input_4.txt", "3D_test_input_1.txt" , "3D_test_input_2.txt"]

    #Read the file and trap the input into 6 different variables so that you can perform calculations on the variables for the first two parts
    for i in output_files:
        with open(i) as f:
            ints_first_line = f.readline()
            ints=ints_first_line.split(" ")
            matrix1_1=int(ints[0])
            matrix1_2=int(ints[1])
            vector_1=int(ints[2])

            ints_second_line = f.readline()
            ints+=ints_second_line.split(" ")
            matrix2_1=int(ints[3])
            matrix2_2=int(ints[4])
            vector_2=int(ints[5])

        #call the calculations for the first part
        calculationsPart1(matrix1_1, matrix1_2, matrix2_1, matrix2_2, vector_1, vector_2, i)

        #call the calculations for the second part
        calculationsPart2(matrix1_1, matrix1_2, matrix2_1, matrix2_2, vector_1, vector_2, i)

    #part 3 calculations
    for i in output_files_part3:
        with open(i) as f:
            
            #reading in the first line
            pt_first_line = f.readline()
            pt=pt_first_line.split(" ")
            pt1_1=(pt[0])
            pt2_1=(pt[1])
            pt3_1=(pt[2])

            #reading in the second line
            pt_second_line = f.readline()
            pt=pt_second_line.split(" ")
            pt1_2=(pt[0])
            pt2_2=(pt[1])
            pt3_2=(pt[2])

            #reading in the third line and determining whether it is a 3d or a 2d triangle
            pt_third_line = f.readline()
            if not pt_third_line:
                threeDFlag = False

            else:
                pt=pt_third_line.split(" ")
                pt1_3=int(pt[0])
                pt2_3=int(pt[1])
                pt3_3=int(pt[2])



            #casting the inputs to ints
            pt1_1=int(pt1_1)
            pt2_1=int(pt2_1)
            pt3_1=int(pt3_1)
            pt1_2=int(pt1_2)
            pt2_2=int(pt2_2)
            pt3_2=int(pt3_2)
            

            if(threeDFlag == False):
                calculationsPart3_2d(pt1_1, pt1_2, pt2_1, pt2_2, pt3_1, pt3_2, i)
            else:
                calculationsPart3_3d(pt1_1, pt1_2, pt1_3, pt2_1, pt2_2, pt2_3, pt3_1, pt3_2, pt3_3, i)
            


# part 1
def calculationsPart1(matrix1_1:int, matrix1_2:int, matrix2_1:int, matrix2_2:int, vector_1:int, vector_2:int, file_name):
    file_name += "_Output_Part1"
    file = open(file_name, "w")
    determinate = getDeterminate2x2(matrix1_1, matrix2_1, matrix1_2,matrix2_2)
    #Testing to see if the determinate is equal to 0
    if ( determinate == 0) :

        #determining whether the system is inconsistent or underdetermined
        if (matrix2_1 != 0 ):
            x1=1
            x2=((vector_1-matrix1_1)/matrix1_2)

            if (matrix2_1*x1 + matrix2_2*x2 != vector_2):
                file.write("System is inconsistent")
                print("System is inconsistent")
            
            else:
                file.write("System is undetermined")
                print("System is undetermined")

        elif(matrix1_2 == 0 and matrix1_1 != 0):
            x2 = 1
            x1=(vector_1/matrix1_1)

            if (matrix2_1*x1 + matrix2_2*x2 != vector_2):
                file.write("System is inconsistent")
                print("System is inconsistent")
            
            else:
                file.write("System is undertermined")
                print("System is undetermined")

        elif (matrix1_1 == 0 and matrix2_1 == 0 and vector_1 != 0):
            file.write("System is inconsistent")
            print("System is inconsistent")

        elif (matrix1_1 == 0 and matrix2_1 == 0 and vector_1 == 0):
            file.write("System is inconsistent")
            print("System is underdetermined")
        
    #the system was not inconsistent or undetermined    
    else:
        #calculate the inverse of the first matrix
        e=matrix2_2/determinate
        f=(-matrix1_2)/determinate
        g=(-matrix2_1)/determinate
        h=matrix1_1/determinate

        #calculate the new vector that we are to find
        x1 = (e*vector_1) + (f*vector_2)
        x2 = (g*vector_1) + (h*vector_2)

        #print the vector that we needed to find
        final_string = printVector2x1(x1,x2)
        file.write(final_string)

# part 2
def calculationsPart2(matrix1_1:float, matrix1_2:float, matrix2_1:float, matrix2_2:float, vector_1:float, vector_2:float, file_name):
    file_name += "_Output_Part2"
    file = open(file_name, "w")
    a=matrix1_1
    b=matrix1_2
    c=matrix2_1
    d=matrix2_2

    original_matrix = numpy.array([[matrix1_1, matrix1_2] , [matrix2_1, matrix2_2]])

    #getting delta so that we can solve for the eigenvalues
    discriminant=(a+d)**2 - 4*(a*d - b*c)
    
    discriminant = abs(discriminant)

    delta1=((a + d + math.sqrt(discriminant))/2)
    delta2=((a + d - math.sqrt(discriminant))/2)

    #printing the eigen values
    print()
    print("^: ", end="")
    final_string = printMatrix2x2(delta1, 0, 0, delta2)
    file.write(final_string)


    #simplyfying variables using delta 1 so that we can solve for r1
    A=a-delta1
    D=d-delta1

    #testing to see if there are any real eigenvectors that exist 
    if (a == 0 and b == 0 and c == 0):
        file.write("no non-trivial eigenvector exists for the matrix")
        print("no non-trivial eigenvector exists for the matrix")

    elif (A==0 and c !=0):
        #row pivot
        matrix1_1=c
        martix1_2=D
        matrix2_1=A
        matrix2_2=b

    elif (A == 0 and c == 0 and b != 0):
        #column pivot
        matrix1_1=b
        matrix1_2=A
        matrix2_1=D
        matrix2_2=c

        #swapping the two numbers from the vector
        swap=vector_1
        vector_1=vector_2
        vector_2=swap

        #if there are no need for any pivots then set the first calculations to a new matrix
    else:
        matrix1_1=A
        matrix1_2=b
        matrix2_1=c
        matrix2_2=D


    #matrix multiplication 
    matrixM1 = matrix1_1
    matrixM2 = matrix1_2
    matrixM3 = 0
    matrixM4 = -(matrix1_2*matrix2_1/matrix1_1) + matrix2_2
    
    #if -bc/A + D = 0 then set r2 to 1 and solve for r1
    r_normalized = math.sqrt((matrix1_2/matrix1_1)**2 + 1) 

    #calculating components for r1
    vectorR1_1=-matrix1_2/(matrix1_1 * r_normalized)
    vectorR1_2=1/r_normalized

    #printing R1 and R2
    print()
    print("R1: ", end="")
    vector_string = printVector2x1(vectorR1_1, vectorR1_2)
    file.write(vector_string)


    #simplyfying variables for delta 2 so that we can solve for r2
    A=a-delta2
    D=d-delta2

    #testing to see if there are any real eigenvectors that exist 
    if (a == 0 and b == 0 and c == 0):
        file.write("no non-trivial eigenvector exists for the matrix")
        print("no non-trivial eigenvector exists for the matrix")

    elif (A==0 and c !=0):
        #row pivot
        matrix1_1=c
        martix1_2=D
        matrix2_1=A
        matrix2_2=b

    elif (A == 0 and c == 0 and b != 0):
        #column pivot
        cs1_1=b
        cs1_2=A
        cs2_1=D
        cs2_2=c

        #row pivot
        matrix1_1 = cs2_1
        matrix1_2 = cs2_2
        matrix2_1 = cs1_1
        matrix2_2 = cs1_2

        #swapping the two numbers from the vector
        swap=vector_1
        vector_1=vector_2
        vector_2=swap

        #if there are no need for any pivots then set the first calculations to a new matrix
    else:
        matrix1_1=A
        matrix1_2=b
        matrix2_1=c
        matrix2_2=D


    #matrix multiplication 
    matrixM1 = matrix1_1
    matrixM2 = matrix1_2
    matrixM3 = 0
    matrixM4 = -(matrix1_2*matrix2_1/matrix1_1) + matrix2_2
    
    #if -bc/A + D = 0 then set r2 to 1 and solve for r1
    r_normalized = math.sqrt((matrix1_2/matrix1_1)**2 + 1) 

    #calculating components for r2
    vectorR2_1=-matrix1_2/(matrix1_1 * r_normalized)
    vectorR2_2=1/r_normalized

    print("R2: ", end="")
    vector_string = printVector2x1(vectorR2_1, vectorR2_2)
    file.write(vector_string)

    #creating matrices so that you can multiply them together
    R = numpy.array([[vectorR1_1, vectorR1_2], [vectorR2_1, vectorR2_2]])
    R_transpose = numpy.array([[vectorR1_1, vectorR2_1], [vectorR1_2, vectorR2_2]])
    eigenVectors=numpy.array([[delta1, 0], [0, delta2]])

    #multiplying matrices
    R_Rtranspose_eigen= R @ R_transpose @ eigenVectors
    

    #printing the result of the multiplication
    print("R * Rtranspose * eigenvalues: ")
    
    numpy.savetxt(file, R_Rtranspose_eigen, fmt='%.4f')

    
    #printing 1 or 0 depending on if the result is equal to the original matrix
    if (numpy.allclose(R_Rtranspose_eigen, original_matrix, rtol=1e-04)):
        file.write("1")
        print("1: they are equal")
    else:
        file.write("0")
        print("0: not equal")

    file.close()

# part 3 for a 2d triangle
def calculationsPart3_2d(p1_1, p1_2, p2_1, p2_2, p3_1, p3_2, file_name):
    file_name += "_Output_Part3"
    file = open(file_name, "w")

    #calculating the first two vectors from the three points that were given
    a1_1 = p2_1 - p1_1
    a1_2 = p2_2 - p1_2
    a2_1 = p3_1 - p1_1
    a2_2 = p3_2 - p1_2

    #calculate the area
    T = abs(1/2 * ((a1_1 * a2_2) - (a1_2 * a2_1)))

    print()
    print("the area of the triangle is: ", T)
    file.write(format(T, ".4f"))
    file.write("\n")

    #get vector for distance
    v1_1 = p2_1 - p1_1
    v1_2 = p2_2 - p1_2

    w1_1 = p3_1 - p1_1
    w1_2 = p3_2 - p1_2

    #calculate the vectors length
    w_length = math.sqrt((w1_1 ** 2) + (w1_2 ** 2))
    v_length = math.sqrt((v1_1 ** 2) + (v1_2 ** 2))

    #calculate the dot product of the two vectors
    dot_product_v_w = ((v1_1*w1_1) + (v1_2 * w1_2))

    #cos(theta) by dot product and the length
    cos_theta = dot_product_v_w/(w_length * v_length)

    #calculate the distance
    distance = w_length * (math.sqrt(1 - (cos_theta **2)))

    print("the distance from point to the line is: ", end="")
    print(format(distance, ".4f"))

    file.write(format(distance, ".4f"))

# part 3 for a 3d triangle
def calculationsPart3_3d(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, file_name):
    file_name += "_Output_Part3"
    file = open(file_name, "w")

    #calculating the cross product of the points
    cross1 = ((p1_2*p2_3) - (p2_2*p1_3))
    cross2 = ((p1_3*p2_1) - (p2_3*p1_1))
    cross3 = ((p1_1*p2_2) - (p2_1*p1_2))

    #length of the cross product
    length_of_cross = math.sqrt((cross1 **2) + (cross2 ** 2) + (cross3 ** 3))
    
    #area of the triangle
    T = abs(1/2 * length_of_cross)
    
    print()
    print("The area of the triangle is: " , end = "")
    print(format(T, ".4f"))
    file.write(format(T, ".4f"))
    file.write("\n")

    #calculating the midpoint 
    m1_1 = (p1_1 + p2_1)/2
    m1_2 = (p1_2 + p2_2)/2
    m1_3 = (p1_3 + p2_3)/2

    #calculate the normal vector
    n_length = math.sqrt(((p2_1 - p1_1) ** 2) + ((p2_2 - p1_2) ** 2) + ((p2_3 - p1_3) ** 2))
    n1_1 = (p2_1 - p1_1)/n_length
    n1_2 = (p2_2 - p1_2)/n_length
    n1_3 = (p2_3 - p1_3)/n_length

    distance = ((n1_1 * p3_1) + (n1_2 * p3_2) + (n1_3 * p3_3) - ((n1_1 * m1_1) + (n1_2 * m1_2) + (n1_3 * m1_3)))
    
    print("the distance from the point to the plane: ", end = "")
    print(format(distance, ".4f"))
    file.write(format(distance, ".4f"))

# print method for 2x1 vectors
def printVector2x1(x1, x2):
    final_string = ""
    print("Vector: [", end="")
    print(format(x1, ".4f"),end="")
    print(" ", end="")
    print(format(x2, ".4f"), end="")
    print("]")

    #creating a final string so that it can be written to a file
    final_string+="Vector: ["
    final_string+= format(x1, ".4f")
    final_string+=" "
    final_string+= format(x2, ".4f")
    final_string+="]\n"

    return final_string


# method to find the determinate for a 2x2 matrix
def getDeterminate2x2(matrix1_1, matrix2_1, matrix1_2, matrix2_2):
    determinate = ((matrix1_1*matrix2_2) - (matrix1_2*matrix2_1))
    return determinate

# method to print a 2x2 matrix
def printMatrix2x2(matrix1_1, matrix1_2, matrix2_1, matrix2_2):
    final_string = ""
    print("Matrix (2x2):   [", end="")
    print(format(matrix1_1, ".4f"),end="")
    print(" ", end="")
    print(format(matrix1_2, ".4f"), end="")
    print("]")
    print("                   [", end="")
    print(format(matrix2_1, ".4f"),end="")
    print(" ", end="")
    print(format(matrix2_2, ".4f"), end="")
    print("]")

    #creating a final string so that it can be written to a file
    final_string += "["
    final_string += format(matrix1_1, ".4f")
    final_string += " "
    final_string += format(matrix1_2, ".4f")
    final_string +=  "] \n"
    final_string += "["
    final_string += format(matrix2_1, ".4f")
    final_string += " "
    final_string += format(matrix2_2, ".4f")
    final_string +=  "] \n"

    return final_string


if __name__ == "__main__":
    main()
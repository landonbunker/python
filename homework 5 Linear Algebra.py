import math
import numpy as np
import random

#Landon Bunker
#CS2300
#Program Assignment 5
#Part1: perform the simple page rank algorithm and output the eigenvector for the web pages and the rank order of the web pages
#Part2: perform linear binary classification so that you can determine whether or not the features should be implemented or not.

def main ():
    #initializing variables for each part and setting the input files
    input_filesA = ["input_A.txt", "inputA2.txt", "inputA3.txt"]
    input_filesB = ["test_input_B.txt", "test_input_B2.txt"]

    #variables for Part A
    input_it = 1
    sum = 0
    max_iterations = 1000
    current_guess = []
    initial_guess = []
    eigenvector = []
    ranks = []
    found_answer_flag = False
    invalid_input_flag = False

    # Variables for part B
    initial_weight = 1
    f_array = []
    weight_array = []
    classification_array = []


    #for loop to test each input file for part A
    for i in input_filesA:
        with open(i) as f:
            #creating the output file name
            file_name = "lbunker_output_A" 
            file_name += str(input_it) + ".txt"
            file = open(file_name, "w")

            #putting the data into a 2d array
            data = np.genfromtxt(i)

            #creating the transpose of the array so that we can see if the columns add up to 1
            transpose = np.ndarray.transpose(data)
            
            #testing to see if the columns add up to 1 and none of the numbers are non negative
            for columns in transpose:
                for index in columns:
                    sum += index
                    if (index < 0):
                        invalid_input_flag = True
                
                #testing to see if the sum of the column is not in the bounds of 1
                if (sum < .999 or sum > 1.001):
                    invalid_input_flag = True

                #resetting the sum for next loop
                sum = 0

            #testing to see if the invalid input flag has been set
            if (invalid_input_flag == False):   

                #creating the current guess and putting the original matrix into a matrix
                current_guess = np.array(current_guess) 
                data = np.array(data)

                #setting the tolerance
                tolerance = .03    

                #for loop to set the initial guess 
                for rows in data:
                    found_answer_flag = False
                    initial_guess = []
                    for index in rows:
                        if(index == 0):
                            initial_guess.append(0)
                        else:
                            initial_guess.append(1/index)

                    #setting the last guess as the first guess
                    last_guess = np.array(initial_guess) 
                    
                    #running the iterations for a set amount of iterations
                    for i in range(max_iterations):
                        last_guess = np.round(last_guess,3)
                        initial_guess = np.round(initial_guess, 3)
                        current_guess = np.matmul(data, last_guess)

                        #getting the length of the last and current guess to compare 
                        last_guess_length = np.linalg.norm(last_guess)
                        current_guess_length = np.linalg.norm(current_guess)

                        #testing to see if the guesses converged 
                        if (current_guess_length - last_guess_length < tolerance and current_guess_length - last_guess_length > 0):
                            answer = current_guess
                            
                            answer_length = np.linalg.norm(answer)
                            answer_length = np.round(answer_length, 3)
                            eigenvector.append(answer_length)

                            ranks.append(np.linalg.matrix_rank(data))
                            found_answer_flag = True

                        #resetting so that the current guess can be changed
                        last_guess = current_guess
                        
                        if (found_answer_flag == True):
                            break

                    if (found_answer_flag == False):
                        eigenvector.append( "max number of iterations reached")

                #print eigenvector to a file
                print(eigenvector)
                print(ranks)
                string = ', '.join(map(str, eigenvector))
                file.write(string)
                string = ', '.join(map(str, ranks))
                file.write("\n")
                file.write(string)

                #restting the string for the next output file
                string = " "

            else:

                #if the invalid input flag was set then print invalid input
                file.write("invalid input")
        
        #output file name counter incremented 
        input_it += 1
        
    input_it = 1

    
    #for loop to test each input file for part B
    for i in input_filesB:
        with open(i) as f:
            with open("training_input_B.txt"):
                
                #setting up the output file name
                file_name = "lbunker_output_B"
                file_name += str(input_it) + ".txt"
                file = open(file_name, "w")

                #putting the data into a 2d array
                data = np.genfromtxt(i)
                
                #indexing into the 2d array so that we can train the program
                for row in data:
                    for i in row:
                        f_sub = initial_weight * i

                        #calculating error e  - Y1 -f(W,x1)
                        y1 = random.randint(0,1)
                        error_e = y1 - f_sub

                        #update weights array 
                        weight_array.append(initial_weight + (error_e * i))
                        if (f_sub >= 0):
                            f_array.append(1)
                        else:
                            f_array.append(0)
                
                #doing test with W*F to determine if the test is recommended or not
                for i in range(len(weight_array)):
                    test = weight_array[i] * f_array[i]

                    if (test >= 0 ):
                        classification_array.append(1)
                    else:
                        classification_array.append(0)
                
                #classification array
                print(classification_array)    
                #print the weight vector
                print(weight_array)

                #write to the output file with the classification array and the weight array
                string = ', '.join(map(str, classification_array))
                file.write(string)
                string = ', '.join(map(str, weight_array))
                file.write("\n")
                file.write(string)

                #resetting the string for the next output file
                string = " "

                #resetting the weight vector
                weight_array = []

            #incrementing file name
            input_it += 1

        


                
if __name__ == "__main__":
    main()
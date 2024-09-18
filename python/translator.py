import sys
#Pass in args, determine if english or braille
#Read string and translate using dictionary
#Output answer, ensure test file passes

#When having to convert to and from two different values I chose a dictionary as it creates key value pairs that are easily accessible
#Since there is a finite number of possible letters/numbers a dictionary takes a bit more intial setup but covers all possibilities for the given task
braille_eng_dict = {
    #Letters
    'a' : 'O.....',
    'b' : 'O.O...',
    'c' : 'OO....',
    'd' : 'OO.O..',
    'e' : 'O..O..',
    'f' : 'OOO...',
    'g' : 'OOOO..',
    'h' : 'O.OO..',
    'i' : '.OO...',
    'j' : '.OOO..',
    'k' : 'O...O.',
    'l' : 'O.O.O.',
    'm' : 'OO..O.',
    'n' : 'OO.OO.',
    'o' : 'O..OO.',
    'p' : 'OOO.O.',
    'q' : 'OOOOO.',
    'r' : 'O.OOO.',
    's' : '.OO.O.',
    't' : '.OOOO.',
    'u' : 'O...OO',
    'v' : 'O.O.OO',
    'w' : '.OOO.O',
    'x' : 'OO..OO',
    'y' : 'OO.OOO',
    'z' : 'O..OOO',
    #Numbers
    '1' : 'O.....',
    '2' : 'O.O...',
    '3' : 'OO....',
    '4' : 'OO.O..',
    '5' : 'O..O..',
    '6' : 'OOO...',
    '7' : 'OOOO..',
    '8' : 'O.OO..',
    '9' : '.OO...',
    '0' : '.OOO..',
    #Symbols and follow
    'capitalFollows' : '.....O',
    'decimalFollows' : '.O...O',
    'numberFollows' : '.O.OOO',
    '.' : '..OO.O',
    ',' : '..O...',
    '?' : '..O.OO',
    '!' : '..OOO.',
    ':' : '..OO..',
    ';' : '..O.O.',
    '-' : '....OO',
    '/' : '.O..O.',
    '<' : '.OO..O',
    '>' : 'O..OO.',
    '(' : 'O.O..O',
    ')' : '.O.OO.',
    'space' : '......',
}

#Braille will always have a length of a multiple of 6
#There is a chance an english string can be a multiple of six so add a second check to see if it contains ONLY braille characters 'O' and '.'
def CheckLang(arg):
    #Remove any whitespace that might cause the program to assume english
    arg = arg.replace(' ', '')

    #Check if the input is a multiple of 6
    check_length = len(arg) % 6 == 0

    #Iterate through the arg message to see if all of the characters are in braille
    check_chars = all(char in 'O.' for char in arg)

    #Check if the message is in braille, if not it is safe to assume it is english
    if check_length and check_chars:
        return 'Braille'
    else:
        return 'English'


#After deciding if the message is in english or braille, translate it
def TranslateMessage(arg):

    #Translate from Braille to English
    if CheckLang(arg) == 'Braille':

        message = []

        split = [arg[i:i+6] for i in range(0, len(arg), 6)]

        #Set flags for capitals and for numbers
        capital = False
        number = False

        for entry in split:
            if entry == braille_eng_dict['capitalFollows']:
                #If the capital entry is found, set the flag to true
                capital = True
                continue
            elif entry == braille_eng_dict['numberFollows']:
                #If the number entry is found, set the flag to true
                number = True
                continue
            elif entry == braille_eng_dict['space']:
                #If the space flag is found, create a whitespace character in its place
                message.append(' ')
                #Reset the flags to ensure the next word is treated as its own entity
                number = False
                capital = False
                continue

            #If the number flag is found print numbers dictionary values 
            if number:
                for key, value in braille_eng_dict.items():
                    if value == entry and key.isdigit():
                        message.append(key)
                        break
            else:
                #If there are no numbers print the alphabetical dictionary values
                for key, value in braille_eng_dict.items():
                    if value == entry and key.isalpha():
                        #If the capital flag is found, capitalize the next letter
                        if capital:
                            message.append(key.upper())
                            capital = False  
                        else:
                            message.append(key)
                        break



        message = ''.join(message)

        return message
    


    #Translate from English to Braille
    else:
        #Initialize an empty list to hold the result
        result = []
        
        #Flag to track when the first number is seen to add numberFollows
        first_number = False

        #Iterate through the message and handle each character and add a '||' flag to distinguish between parts
        for char in arg:
            if char.isupper():
                #Check for capitals, if there is a capital add capitalFollows in front of the capital, turn the capital into lower for dictionary
                result.append('capitalFollows')
                result.append(char.lower())
            elif char.isnumeric() and not first_number:
                #Check for numbers, if there is a number add numberFollows in front of the first one only
                result.append('numberFollows')
                result.append(char)
                first_number = True
            elif char.isnumeric():
                #Append numbers normally after the first one
                result.append(char)
            elif char == ' ':
                #Append the space key to replace whitespace
                result.append('space')
            else:
                #Append all the lowercase letters as individual parts to be translated
                result.append(char)
        
        #Add '||' flag around each item in the list
        final_string = '||'.join(result)

        #Add leading and trailing '||' so it is read properly
        final_string = '||' + final_string + '||'

        #Split the different parts to be translated from the dictionary
        split = final_string.split('||')

        #Create a list to store the translated items
        message = []

        #Iterate through the message and translate all parts to braille
        for entry in split:
            if entry in braille_eng_dict:
                message.append(braille_eng_dict[entry])
        
        #Join the message parts into a final Braille output
        message = ''.join(message)
        
        return message



if __name__ == '__main__':
    #Get the args from the command line
    args = sys.argv[1:]
    
    #Join all the args so they can be translated 
    input_string = ' '.join(args)
    
    #Translate the message using the created function
    output = TranslateMessage(input_string)
    
    #Output the translated message
    print(output)
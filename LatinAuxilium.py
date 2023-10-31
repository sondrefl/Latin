import random
from colorama import Fore, Style

def odst():

    infile = open('latinordliste.txt','r')
    
    latin = [] # list of latin words
    norsk = [] # list of norwegian words
    category = [] # list of categorys and there indexes

    r = 0

    for line in infile:
        """
        Loop that runs through the file latinordliste.txt and sort it in to different lists
        """
        words = line.split("        ")

        if len(words) == 1:
            """
            if len(words) is 1 that means a new category is starting, so we append the name of the 
            category and the index r to the list category
            """
            #print(f"name: {words[0][:-1], r}")
            cateogry_name = words[0][:-1]
            cat = (cateogry_name, r)
            category.append(cat)
        else:
            latin.append(words[0])
            norsk.append(words[-1][:-1])

            r += 1

    infile.close()

    for i in range(len(norsk)):
        """
        sins there are different amount of spaces between the latin word and the norwegian words in the text file
        there will in mosted cases be some spaces at the start of the norwegian word that we need to remove, so
        that is what this loop does
        """
        for j in range(len(norsk[i])):
            if norsk[i][0] == " ":
                norsk[i] = norsk[i][1:]
            else:
                break

    d = dict(zip(latin, norsk)) # dictonery from latin to norwegian, eks d["cor"] = "hjerte"
    d_nor = dict(zip(norsk, latin)) # dictonery from norwegian to latin, eks d_nor["hjerte"] = "cor"

    for i in range(len(category)):
        """
        when we read the file above we get the name and the index of there the categoryes starts, and sins we know where
        each caegory starts we also knowes where the previus category endes, so in this loop we add the index of there the
        categoryes end. 
        """

        if i == len(category)-1:
            category[i] = (category[i][0], category[i][1], len(latin))
        else:
            category[i] = (category[i][0], category[i][1], category[i+1][1])


    category += [("All", 0, len(latin))]

    """
    for i in range(len(latin)):
        print(f"{i}, {latin[i]}")

    print(category)

    """

    return latin, norsk, d, d_nor, category


def quiz_med_alternativ(latin, norsk, d, d_nor):
    """
    Under maintenance

    latin, liste med utrykk på latin
    norsk, liste med norsk oversetelse av ordene i latin listen
    d,  dic latin til norsk
    d_nor, dic norsk til latin

    """

    rep = 0
    correct = 0
    wrong = 0

    used = []
    list_correct = []
    list_wrong = []

    for _ in range(1001):

        if len(used) == len(latin):

            if len(list_wrong) == 0:
                print(f"\n{Fore.GREEN}Gratulerer du klarte alle ordene!!!{Style.RESET_ALL}")
                return 0
            else:
                print("\nDu fikk følgene ord riktig")

                for i in list_correct:
                    print(f"{Fore.GREEN}{i} = {d[i]}{Style.RESET_ALL}")

                print("\nDu fikk følgene ord feil")

                for i in list_wrong:
                    print(f"{Fore.RED}{i} = {d[i]}{Style.RESET_ALL}")

                return 0

        word = random.choice(latin)
        nor_word = d[word]

        if word not in used:
            used.append(word)
        else:
            continue


        odst = []
        odst.append(nor_word)

        for _ in range(20):
            """
            Making a list of alternativ answers
            """
            halo = random.choice(norsk)

            if halo in odst:
                continue
            else:
                odst.append(halo)
                if len(odst) == 5:
                    break
                continue

        print(f"\nHva Betyr {word}\n")
        for i in range(1,6):
            halo = random.choice(odst)

            if halo == nor_word:
                numrik = i

            print(f"{i}. {halo}")
            odst.remove(halo)

        print("")
        print(f"{Fore.GREEN}Correct: {correct}{Style.RESET_ALL} {Fore.RED}Wrong: {wrong}{Style.RESET_ALL} number of words: {len(latin)}")
        
        for _ in range(5):

            forslag = input("svar: ")

            try:
                forslag = int(forslag)

                if forslag > 0 and forslag < 6:
                    forslag = str(forslag)
                    break
                else:
                    print("\nAnswer is out of range, please try again\n")
            except ValueError:
                if len(forslag) < 1:
                    print("no answer provierd, please try again")
                    continue

                break

        if forslag.lower() == nor_word.lower() or forslag == str(numrik):
            rep += 1
            correct += 1
            list_correct.append(word)
            #print("Riktig!!!")
            print(f"{Fore.GREEN}Riktig!!!{Style.RESET_ALL}")

            if len(used) == len(latin):
                master = input("That was all the questions, q to quit, enter to see the result: ")
                if master == "q":
                    exit()
                else:
                    continue   
            else:              
                master = input("q to quit, enter to continue: ")
                if master == "q":
                    exit()
                else:
                    continue
        else:

            print(f"\n{Fore.RED}***Desverre feil***{Style.RESET_ALL}\nRiktig svar: {nor_word}\n")
            rep += 1
            wrong += 1
            master = input("q to quit, enter to continue: ")
            list_wrong.append(word)

            if len(used) == len(latin):
                master = input("That was all the questions, q to quit, enter to see the result: ")
                if master == "q":
                    exit()
                else:
                    continue   

            else:           

                if master == "q":
                    exit()
                else:
                    continue      

    return rep

if __name__ == "__main__":

    latin, norsk, d, d_nor, category = odst()

    for _ in range(100):

        print("")
        print("*"*25)
        print("\nWelcome to Latin Auxilium\n")
        print("*"*25)
        print("\nwhat category do you want to practice?\n")

        for i in range(len(category)):
            print(f"{i+1}. {category[i][0]}")

        for _ in range(10):
            print("")
            answer = input("Answer: ")
            try:
                answer = int(answer)
                if answer <= len(category) and answer > 0:

                    sel_latin = latin[category[answer-1][1]:category[answer-1][2]]
                    sel_norsk = norsk[category[answer-1][1]:category[answer-1][2]]

                    rep = quiz_med_alternativ(sel_latin, sel_norsk, d, d_nor)
                    break
                else:
                    sec_answer = input("Input not valid please, press enter to try again, or q to Quit: ")
                    if sec_answer.lower() != "q":
                        continue
                    else:
                        exit()
            except ValueError:
                sec_answer = input("Input not valid please, press enter to try again, or q to Quit: ")
                if sec_answer.lower() != "q":
                    continue
                else:
                    exit()                

        print("")
        again = input("Do you want to try another round? type [YES] for new round: ")

        if again == "YES" or again == "yes":
            continue
        else: 
            break


import random

def ssp(choise, diffculty = "нормально"):

    weapon_reverse = {
     1: "камень",
     2: "ножницы", 
     3: "бумага"
    }

    weapon = {
     "камень": 1,
     "ножницы": 2, #абузим словарь для удобства (1 -> 2 -> 3 -> 1...)
     "бумага": 3
    }

    if diffculty == "нормально":
        computerweapon = weapon_reverse[random.randint(1,3)]
        win_string = "Компьютер выбрал "+f"{computerweapon}"

        if (computerweapon == "камень" and choise == "ножницы"): #за это говно я не ручаюсь
            win_string = win_string + "\nВы проиграли!" 
        elif (computerweapon == "камень" and choise == "камень"):
            win_string = win_string + "\nНичья!"
        elif (computerweapon == "камень" and choise == "бумага"):
            win_string = win_string + "\nВы выиграли!"
        
        if (computerweapon == "ножницы" and choise == "ножницы"):
            win_string = win_string + "\nНичья!" 
        elif (computerweapon == "ножницы" and choise == "камень"):
            win_string = win_string + "\nВы выиграли!"
        elif (computerweapon == "ножницы" and choise == "бумага"):
            win_string = win_string + "\nВы проиграли!"

        if (computerweapon == "бумага" and choise == "ножницы"):
            win_string = win_string + "\nВы выиграли!" 
        elif (computerweapon == "бумага" and choise == "камень"):
            win_string = win_string + "\nВы проиграли!"
        elif (computerweapon == "бумага" and choise == "бумага"):
            win_string = win_string + "\nНичья!"

    if diffculty == "невозможно": #по сравнению с кодом выше это просто гений чистой красоты 
        computerimba = weapon[choise] - 1
        if computerimba == 0: computerimba = 3
        win_string = "Компьютер выбрал "+f"{weapon_reverse[computerimba]}"+"\nВы проиграли! =)"
    
    
    return win_string
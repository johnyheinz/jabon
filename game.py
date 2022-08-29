import random

def ssp(choise, diffculty = "нормально"):

    weapon = {
     "камень": 1,
     "ножницы": 2, #абузим словарь для удобства (1 -> 2 -> 3 -> 1...)
     "бумага": 3
    }

    weapon_reverse = {
     1: "камень",
     2: "ножницы", 
     3: "бумага"
    }

    if diffculty == "нормально":
        computerweapon = weapon_reverse[random.randint(1,3)]
        win_string = "Компьютер выбрал "+f"{computerweapon}"
         
        if (computerweapon == choise): #это ЧУТЬ лучше чем было раньше
            win_string += "\nНичья!"
            return win_string

        if (computerweapon == "камень" and choise == "ножницы"): win_string += "\nВы проиграли!" 
        else: win_string += "\nВы выиграли!"
            
        if (computerweapon == "ножницы" and choise == "камень"): win_string += "\nВы выиграли!"
        else: win_string += "\nВы проиграли!"

        if (computerweapon == "бумага" and choise == "ножницы"): win_string += "\nВы выиграли!"  
        else: win_string += "\nВы проиграли!"
            

    if diffculty == "невозможно": #по сравнению с кодом выше это просто гений чистой красоты 
        computerimba = weapon[choise] - 1
        if computerimba == 0: computerimba = 3
        win_string = "Компьютер выбрал "+f"{weapon_reverse[computerimba]}"+"\nВы проиграли! =)"
    
    return win_string
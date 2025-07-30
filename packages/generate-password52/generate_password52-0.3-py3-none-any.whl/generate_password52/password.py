import random as rm

def pass_hard(num):
    str1 = '1234567890'
    str2 = 'qwertyuiopasdfghjklzxcvbnm'
    str3 = str2.upper()
    str4 = str1+str2+str3
    ls = list(str4)
    rm.shuffle(ls)
    psw = ''.join([rm.choice(ls) for x in range(num)])
    print(f'Password: {psw}')

def pass_lite(eat_num, num_num):
    eat = ['Apple', 'Orange', 'Pineapple', 'Watermelon', 'Tomato', 'Onions', 'Cucumber', 'Lemon', '']
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    num_rm = rm.sample(num, k = num_num)
    eat_rm = rm.sample(eat, k = eat_num)
    print('Password: '+''.join(map(str, eat_rm + num_rm)))

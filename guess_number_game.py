
import random

def guess_number_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    print("��ӭ������������Ϸ��")
    print("���Ѿ������һ��1��100֮������֡��������ܷ�µ����ɣ�")

    while True:
        guess = input("��������Ĳ²⣺")
        try:
            guess = int(guess)
            attempts += 1
            if guess < number_to_guess:
                print("̫С�ˣ�����һ�Ρ�")
            elif guess > number_to_guess:
                print("̫���ˣ�����һ�Ρ�")
            else:
                print(f"��ϲ�㣡��¶��ˣ������� {number_to_guess}��")
                print(f"���ܹ������� {attempts} �Ρ�")
                break
        except ValueError:
            print("������һ����Ч��������")

# ������Ϸ
guess_number_game()

import random
import time
from colorama import init, Fore
init(autoreset=True)
words = ["python", "code", "hacker", "terminal", "matrix", "script", "debug", "compile", "variable", "function"]
def game():
    print(Fore.GREEN + "=== ハッカー風タイピングゲーム ===")
    print("30秒でできるだけ多くの単語をタイプしよう！")
    input("Enterキーでスタート...")
    score = 0
    start_time = time.time()
    time_limit = 30
    while time.time() - start_time < time_limit:
        word = random.choice(words)
        print(Fore.CYAN + f"\n>> {word}")
        typed = input(">>> ")
        if typed == word:
            print(Fore.GREEN + ":チェックマーク大: 正解！")
            score += 1
        else:
            print(Fore.RED + "✘ 間違い！")
    print(Fore.YELLOW + f"\n:3時: タイムアップ！スコア: {score}点")
if __name__ == "__main__":
    game()
time_limit = 60
print(Fore.YELLOW + f"\n:3時: タイムアップ！スコア: {score}点")
if score >= 10:
    print(Fore.MAGENTA + r"""
     /\_/\
    ( o.o ) ＜ やったね！10点以上！
     > ^ <
    """)

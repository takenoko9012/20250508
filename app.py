import tkinter as tk
from tkinter import messagebox
import random

# カードの定義
suits = ['♠', '♥', '♦', '♣']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# カードをシャッフルしてデッキを作成
def create_deck():
    deck = [(value, suit) for suit in suits for value in values]
    random.shuffle(deck)
    return deck

# 手札の合計を計算
def calculate_hand(hand):
    total = 0
    ace_count = 0
    for card in hand:
        value, _ = card
        if value in ['J', 'Q', 'K']:
            total += 10
        elif value == 'A':
            ace_count += 1
            total += 11
        else:
            total += int(value)
    
    # エースを1としてカウントする場合
    while total > 21 and ace_count:
        total -= 10
        ace_count -= 1
    
    return total

# ゲームの状態を更新
def update_game():
    player_total.set(f"プレイヤー: {calculate_hand(player_hand)}")
    dealer_total.set(f"ディーラー: {calculate_hand(dealer_hand)}")
    player_hand_label.config(text="プレイヤーの手札: " + ' '.join([f"{v}{s}" for v, s in player_hand]))
    dealer_hand_label.config(text="ディーラーの手札: " + ' '.join([f"{v}{s}" for v, s in dealer_hand]))

# プレイヤーがカードを引く
def hit():
    player_hand.append(deck.pop())
    update_game()
    if calculate_hand(player_hand) > 21:
        messagebox.showinfo("結果", "バスト！ディーラーの勝ち！")
        reset_game()

# プレイヤーがカードを引かない
def stand():
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        update_game()
    if calculate_hand(dealer_hand) > 21:
        messagebox.showinfo("結果", "ディーラーのバスト！プレイヤーの勝ち！")
    elif calculate_hand(dealer_hand) > calculate_hand(player_hand):
        messagebox.showinfo("結果", "ディーラーの勝ち！")
    elif calculate_hand(dealer_hand) < calculate_hand(player_hand):
        messagebox.showinfo("結果", "プレイヤーの勝ち！")
    else:
        messagebox.showinfo("結果", "引き分け！")
    reset_game()

# ゲームをリセット
def reset_game():
    global deck, player_hand, dealer_hand
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    update_game()

# メインウィンドウ
root = tk.Tk()
root.title("ブラックジャック")

# ゲーム初期化
deck = create_deck()
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]

# プレイヤーとディーラーの合計
player_total = tk.StringVar()
dealer_total = tk.StringVar()

# UIコンポーネント
player_hand_label = tk.Label(root, text="プレイヤーの手札: " + ' '.join([f"{v}{s}" for v, s in player_hand]))
player_hand_label.pack()

dealer_hand_label = tk.Label(root, text="ディーラーの手札: " + ' '.join([f"{v}{s}" for v, s in dealer_hand]) + " ?")
dealer_hand_label.pack()

player_total_label = tk.Label(root, textvariable=player_total)
player_total_label.pack()

dealer_total_label = tk.Label(root, textvariable=dealer_total)
dealer_total_label.pack()

hit_button = tk.Button(root, text="ヒット", command=hit)
hit_button.pack()

stand_button = tk.Button(root, text="スタンド", command=stand)
stand_button.pack()

reset_button = tk.Button(root, text="リセット", command=reset_game)
reset_button.pack()

# ゲームの状態更新
update_game()

# メインループ
root.mainloop()

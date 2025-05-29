import tkinter as tk
import random

deck = []
dealer_hand = []
hands = []
game_over = True
chips = 100
bet = 0
message = ""
initial_bet = 0


suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def update_double_down_button():
    global initial_bet, chips
    bet = int(bet_entry.get())
    if bet <= 0 or bet * 2 > chips or bet != initial_bet:
        double_button.config(state=tk.DISABLED)
    else:
        double_button.config(state=tk.NORMAL)


def init_deck():
    deck = [rank + suit for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def card_value(card):
    rank = card[:-1]
    if rank in ["J", "Q", "K"]:
        return 10
    elif rank == "A":
        return 11
    else:
        return int(rank)


def total(hand):
    val = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[:-1] == "A")
    while val > 21 and aces:
        val -= 10
        aces -= 1
    return val


def update_display():
    if not hands:
        player_hand_str.set("プレイヤー: （未配布）")
        dealer_hand_str.set("ディーラー: （未配布）")
        chips_str.set(f"チップ: {chips}")
        result_str.set(message)
        return

    current = hands[0]
    player_hand_str.set(f"プレイヤー: {' '.join(current)}（合計: {total(current)}）")
    if game_over:
        dealer_hand_str.set(f"ディーラー: {' '.join(dealer_hand)}（合計: {total(dealer_hand)}）")
    else:
        dealer_hand_str.set(f"ディーラー: {dealer_hand[0]} ?")
    chips_str.set(f"チップ: {chips} | ベット額: {bet}")
    result_str.set(message)


def hit():
    global message, game_over
    if not game_over:
        hands[0].append(deck.pop())
        update_display()

        if total(hands[0]) > 21:
            message = "バーストしました！"
            game_over = True
            update_display()
            finish_round()


def stand():
    global message
    message = "スタンドしました。ディーラーのターン..."
    update_display()
    set_buttons_state(False)

    root.after(500, delayed_finish_round)


def delayed_finish_round():
    root.after(500, finish_round)


def double_down():
    global bet, chips, message, game_over
    if len(hands[0]) == 2 and chips >= bet:
        chips -= bet
        bet *= 2
        hands[0].append(deck.pop())

        if total(hands[0]) > 21:
            message = "ダブルダウン！バーストしました！"
            game_over = True
            update_display()
            finish_round()
        else:
            message = "ダブルダウン！1枚引いてスタンドします..."
            update_display()
            set_buttons_state(False)
            root.after(2000, delayed_finish_round)
    else:
        message = "ダブルダウンできません"
        update_display()


def set_buttons_state(enabled):
    state = tk.NORMAL if enabled else tk.DISABLED
    hit_button.config(state=state)
    stand_button.config(state=state)
    double_button.config(state=state)


def finish_round():
    global game_over, message, chips
    game_over = True

    while total(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    player_score = total(hands[0])
    dealer_score = total(dealer_hand)

    if player_score > 21:
        message += " 負けました。"
    elif dealer_score > 21 or player_score > dealer_score:
        chips += bet * 2
        message += " 勝ちました！"
    elif player_score == dealer_score:
        chips += bet
        message += " 引き分けです。"
    else:
        message += " 負けました。"

    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)
    double_button.config(state=tk.DISABLED)
    restart_button.config(state=tk.NORMAL)
    bet_entry.config(state=tk.NORMAL)

    if chips <= 0:
        message += "\nチップが無くなりました。ゲームオーバー！"
        hit_button.config(state=tk.DISABLED)
        stand_button.config(state=tk.DISABLED)
        double_button.config(state=tk.DISABLED)
        restart_button.config(state=tk.DISABLED)
        bet_entry.config(state=tk.DISABLED)

    update_display()


def restart():
    global deck, dealer_hand, hands, game_over, chips, bet, message, initial_bet
    try:
        bet_input = int(bet_entry.get())
        if bet_input <= 0 or bet_input > chips:
            result_str.set("無効なベット額")
            return
    except ValueError:
        result_str.set("数字を入力してください")
        return

    bet = bet_input
    initial_bet = bet
    chips -= bet

    deck = init_deck()
    dealer_hand = [deck.pop(), deck.pop()]
    hands.clear()
    hands.append([deck.pop(), deck.pop()])
    game_over = False
    message = ""

    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)
    double_button.config(state=tk.NORMAL)
    restart_button.config(state=tk.DISABLED)
    bet_entry.config(state=tk.DISABLED)
    update_display()


root = tk.Tk()
root.title("ブラックジャック")

player_hand_str = tk.StringVar()
dealer_hand_str = tk.StringVar()
result_str = tk.StringVar()
chips_str = tk.StringVar()

tk.Label(root, textvariable=player_hand_str, font=("Arial", 16)).pack()
tk.Label(root, textvariable=dealer_hand_str, font=("Arial", 16)).pack()
tk.Label(root, textvariable=result_str, font=("Arial", 20)).pack()
tk.Label(root, textvariable=chips_str, font=("Arial", 20)).pack()

tk.Label(root, text="ベット額:").pack()
bet_entry = tk.Entry(root)
bet_entry.insert(0, "10")
bet_entry.pack()

hit_button = tk.Button(
    root, text="ヒット", command=hit, state=tk.DISABLED, font=("Arial", 14), width=10, height=2
)
hit_button.pack(side=tk.LEFT, padx=5)

stand_button = tk.Button(
    root, text="スタンド", command=stand, state=tk.DISABLED, font=("Arial", 14), width=10, height=2
)
stand_button.pack(side=tk.LEFT, padx=5)

double_button = tk.Button(
    root, text="ダブルダウン", command=double_down, state=tk.DISABLED, font=("Arial", 14), width=12, height=2
)
double_button.pack(side=tk.LEFT, padx=5)

restart_button = tk.Button(root, text="ゲーム開始", command=restart, font=("Arial", 14), width=12, height=2)
restart_button.pack(side=tk.LEFT, padx=5)


update_display()
root.mainloop()

import os
import random
import sys
import time

# Constants
CARD_WIDTH = 7
CARD_HEIGHT = 5
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# Terminal thingies
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.015, enabled=True):
    if not enabled:
        print(text)
        return
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def dramatic_pause(seconds=1.0, enabled=True):
    if enabled:
        time.sleep(seconds)

# Card And Deck stuff muehehehehehehheheheheheheheh
def create_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append({"rank": rank, "suit": suit})
        random.shuffle(deck)
        return deck

def get_card_value(hand):
    total = 0
    aces = 0
    for card in hand:
        rank = card["rank"]
        if rank in ["J", "Q", "K"]:
            total += 10
        elif rank == "A":
            aces += 1
            total += 11
        else:
            total += int(rank)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def is_natural_blackjack(hand):
    if len(hand) == 2 and get_card_value(hand) == 21:
        return True
    return False

# Art stuff or smth (ps dont mind my comments ik im being 
# cringe and this has literally no use but here we are yeahhhhhhh 
# i js luv art and spmammminnggggggggggg heehehhehehehhehe 
# im going insane i have so much work to do 
# but im doing this instead of my school work oh fuck me
# no one asks how im doing but im doing this so i can be happy and not
# be sad and depressed and lonely and sad and depressed and lonely and sad and depressed and lonely and sad and its gonna keep going on
# an on and on and on and on and on and woohoooo alr back to working i got a bit distracted)

def render_card_row(hand, hidden_second=False):
    lines = ["", "", "", "", ""]
    for i, card in enumerate(hand):
        if i == 1 and hidden_second:
            lines[0] += "+-----+ "
            lines[1] += "|  ?  | "
            lines[2] += "| ? ? | "
            lines[3] += "|  ?  | "
            lines[4] += "+-----+ "
        else:
            r = card["rank"]
            s = card["suit"]
            r_str = f"{r:<2}"
            lines[0] += "+-----+ "
            lines[1] += f"|{r_str}   | "
            lines[2] += f"|  {s}  | "
            lines[3] += f"|   {r_str}| "
            lines[4] += "+-----+ "
    return lines

def display_table(
    dealer_hand, player_hand, dealer_hidden, chips, bet, stats, dealer_msg
):
    clear_screen()
    print("-" * 76)
    print(
        "                        THE DEVIL'S CASINO                        ".center(
            76
        )
    )
    print("-" * 76)
    print(
        f" CHIPS: {chips} | CURRENT BET: {bet} | W/L/P: {stats['wins']}/{stats['losses']}/{stats['pushes']} | BJ: {stats['blackjacks']}"
    )
    print("-" * 76)

    print("\n [DEALER'S HAND]")
    d_lines = render_card_row(dealer_hand, hidden_second=dealer_hidden)
    for line in d_lines:
        print("  " + line)

    if not dealer_hidden:
        d_val = get_card_value(dealer_hand)
        print(f"  Value: {d_val}")
    else:
        print(" Value: ?")

    print("\n" + "-" * 76)

    print("\n [YOUR HAND]")
    p_lines = render_card_row(player_hand, hidden_second=False)
    for line in p_lines:
        print("  " + line)
    p_val = get_card_value(player_hand)
    print(f"Value: {p_val}")

    print("\n" + "-" * 76)
    print(f' DEALER: "{dealer_msg}"')
    print("-" * 76)

# Dialgoues hell yeahhhhhhhhh (btw i used a bit of AI in this cuz yeah idk how to write a devils dialogue, im being fr)

DEALER_LINES = {
    "welcome": [
        "Welcome, to the table, mortal. Mortal step up if your soul can afford the stakes.",
        "Ah another lamb arrives. Lamb, let us see if you have any luck stealing.",
        "Sit. Cards have been waiting for you. Cards always do.",
    ],
    "wager": [
        "A small sacrifice. Let's see what it gets you.", 
        "Chips down. The wheel of fate begins to turn.", 
        "Courageous or foolish? Time will tell.",
    ],
    "hit": [
        "Another card, please.",
        "Greed is a heavy burden.", 
        "Drawing into the abyss. Be careful you do not fall.", 
        "A card for the desperate. Let us see.",
    ],
    "stand": [
        "Holding steady in the storm. Interesting.", 
        "Trapped. No going back.", 
        "You trust your hand? How cute.",
    ],
    "double": [
        "Doubling down! Fortune favors the bold, or destroys them.", 
        "Raising the stakes. Music to my ears.", 
        "Double or nothing. A classic error.",
    ],
    "low_val": [
        "A pitiful sum. Shall I put you out of your misery?", 
        "Crawling in the dirt, are we?", 
        "That hand looks suspiciously weak.",
    ],
    "high_val": [
        "Inching nearer to the edge. Are you able to keep your balance?",
        "Walking the razor's edge, aren't we?",
        "Twenty-one ways. Or doom.",
    ],
    "bust": [
        "Bust. The house claims its pay.",
        "Overextended. Your greed will be your downfall.",
        "Collapsed from the weight of your own figures. Pitiful.",
    ],
    "dealer_bust": [
        "The house makes mistakes as well; take what you can.",
        "My hand falls, consider this a charitable act.",
        "A rare error on my part."
    ],
    "player_win": [
        "You survive for another deal. Do not confuse surviving with winning",
        "Take your money. It will be back with me soon enough",
        "A short-lived win. Savour it.",
    ],
    "player_loss": [
        "The house will always win. In the end.",
        "Your luck is beginning to bore me.",
        "Another soul added to the ledger.",
    ],
    "blackjack": [
        "Natural Blackjack, what an annoyance!",
        "Blackjack, beginners or devils—hard to distinguish!",
        "Pristine conditions. Don't let it get into your head!",
    ],
    "push": [
        "A stalemate. Neither life nor death. How dull.",
        "A push. We return to where we started.",
        "Nothing gained, nothing lost. A waste of breath.",
    ],
    "streak_win": [
        "Winning streak? The Universe is merely testing your hubris.",
        "You defy probability. Suspiciously so.",
    ],
    "streak_loss": [
        "Bleeding out, chip by chip. Shall I fetch a bandage?",
        "Your chips vanish like smoke. As expected.",
    ],
    "broke": [
        "Penniless. The game ends when the purse is empty.",
        "Not a single chip left. Come back when you've mortaged something worthwhile.",
    ],
    "cashout": [
        "Leaving already? The night was just beginning.",
        "Fleeing with your spoils. Wise, but cowardly.",
    ],
    "secret": [
        "Ah, you found the hidden word. The devil appreciates curiosity.",
        "You faze behind the curtain. Be careful what looks back.",
    ],        
}

def get_dialogue(category, state=None):
    if category == "streak" and state:
        if state > 2:
            return random.choice(DEALER_LINES["streak_win"])
        elif state < -2:
            return random.choice(DEALER_LINES["streak_loss"])
        return ""
    if category in DEALER_LINES:
        return random.choice(DEALER_LINES[category])
    return "..."

# screens shi wenviuewynvyewiurnvyeiuwnyvru (omg im back to sppaming again im sorry)
def boot_sequence(anim_enabled):
    clear_screen()
    if anim_enabled:
        lines = [
            "You walk out of the house, with a goal in mind....",
            "Money in your hand, the wind bitingly chill....",
            "The door glows in the distance of the cursed place....",
            "You enter ready for the fight against the devil himself....",
        ]
        for line in lines:
            slow_print(line, delay=0.02, enabled=True)
            time.sleep(0.3)
        time.sleep(1.0)
    clear_screen()

def show_title_screen(anim_enabled):
    clear_screen()
    title_art = r"""
    ___________                   ____  .__               /\          _________                  .__                  
    \__    ___/_____     ____    / ___\ |__|  ____ _______\(______    \_   ___ \ _____     ______|__|  ____    ____   
      |    |   \__  \   /    \  / /_/  >|  |_/ __ \\_  __ \/  ___/    /    \  \/ \__  \   /  ___/|  | /    \  /  _ \  
      |    |    / __ \_|   |  \ \___  / |  |\  ___/ |  | \/\___ \     \     \____ / __ \_ \___ \ |  ||   |  \(  <_> ) 
      |____|   (____  /|___|  //_____/  |__| \___  >|__|  /____  >     \______  /(____  //____  >|__||___|  / \____/  
                    \/      \/                   \/            \/             \/      \/      \/          \/          
                                                                                                                  
                                                                ♠  ♥  THE DEVIL'S CASINO  ♦  ♣                                     
    """
    print(title_art)
    print("-" * 76)
    print(
        "            YOUR LUCK AWAITS YOU           ".center(
            76
        )
    )
    print("-" * 76)
    print("\n")
    print(" [1] Enter the Casino")
    print(" [2] Toggle Animations (Current: " + ("ON" if anim_enabled else "OFF") + ")")
    print(" [3] Exit")
    print("\n" + "-" * 76)

def end_game_screen(stats, starting_chips):
    clear_screen()
    ending_art = r"""
     __ __   ___   __ __  _____   ___       ____  __ __  ___    ____  ______ 
    |  |  | /   \ |  |  |/ ___/  /  _]     /    ||  |  ||   \  |    ||      |
    |  |  ||     ||  |  (   \_  /  [_     |  o  ||  |  ||    \  |  | |      |
    |  _  ||  O  ||  |  |\__  ||    _]    |     ||  |  ||  D  | |  | |_|  |_|
    |  |  ||     ||  :  |/  \ ||   [_     |  _  ||  :  ||     | |  |   |  |  
    |  |  ||     ||     |\    ||     |    |  |  ||     ||     | |  |   |  |  
    |__|__| \___/  \__,_| \___||_____|    |__|__| \__,_||_____||____|  |__|  
                                                                         
    """
    print(ending_art)
    print("-" * 95)
    print("                     THE FINAL REPORT                  ".center(95))
    print("-" * 95)
    net_profit = stats["chips"] - starting_chips
    print(f" Starting Balance : {starting_chips} chips")
    print(f" Ending Balance   : {stats['chips']} chips")
    net_str = (
        f"+{net_profit}"
        if net_profit >= 0
        else f"{net_profit}"
    )
    print(f" Net Profit/Loss  : {net_str} chips")
    print(f" Total Rounds     : {stats['rounds']}")
    print(f" Wins / Losses    : {stats['wins']} / {stats['losses']}")
    print(f" Pushes           : {stats['pushes']}")
    print(f" Blackjacks       : {stats['blackjacks']}")
    print("-" * 76) 
    print(
        "        'Take your winnings. They were never going to last.'       ".center(
            76
        )
    )
    print("-" * 76)
    input("\n Press Enter to exit the terminal...")

# Gameplay Loop (btw did you get it that the name of the casino is 
# inspired by Sam 'Ace' Rothstein from the movie Casino?? if you did, 
# then sure as hell you are a ball knower) 

def main():
    anim_enabled = True
    boot_sequence(anim_enabled)

    chips = 500
    starting_chips = 500
    stats = {"wins": 0, "losses": 0, "pushes": 0, "blackjacks": 0, "rounds": 0, "chips": 500}
    streak = 0

    while True:
        show_title_screen(anim_enabled)
        choice = input("\n Select an option (1-3)").strip()

        if choice == "2":
            anim_enabled = not anim_enabled
            continue
        elif choice == "3":
            print("\n Leaving already? The night was just getting started!")
            sys.exit(0)
        elif choice != "1":
            continue

        #main loop
        dealer_msg = get_dialogue("welcome")
        dramatic_pause(1.0, anim_enabled)

        while chips > 0:
            display_table([], [], True, chips, 0, stats, dealer_msg)
            print(f"\n Your current chip balance: {chips}")
            bet_input = input(" Enter your wager (Min 10, 'cashout to leave, or secret word)").strip().lower()

            if bet_input == "cashout" or bet_input == "exit":
                dealer_msg = get_dialogue("cashout")
                display_table([], [], True, chips, 0, stats, dealer_msg)
                dramatic_pause(1.5, anim_enabled)
                stats["chips"] = chips
                end_game_screen(stats, starting_chips)
                return

            if bet_input == "devil" or bet_input == "lucifer" or bet_input == "tangiers":
                dealer_msg = get_dialogue("secret")
                display_table([], [], True, chips, 0, stats, dealer_msg)
                dramatic_pause(2.0, anim_enabled)
                continue

            try:
                bet = int(bet_input)
            except ValueError:
                dealer_msg = "Speak clearly, mortal. Numbers or 'cashout'."
                continue

            if bet < 10:
                dealer_msg = "Minimum wage is 10 chips. Do not insult the house."
                continue
            if bet > chips:
                dealer_msg = "You cannot bet what you do not posses."
                continue

            # Round Start
            stats["rounds"] += 1
            deck = create_deck()
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            dealer_msg = get_dialogue("wager")
            display_table(dealer_hand, player_hand, True, chips, bet, stats, dealer_msg)
            dramatic_pause(0.8, anim_enabled)

            # blackjack check
            p_bj = is_natural_blackjack(player_hand)
            d_bj = is_natural_blackjack(dealer_hand)

            if p_bj or d_bj:
                dealer_msg = get_dialogue("blackjack") if p_bj else "Dealer reveals a natural blackajck."
                display_table(dealer_hand, player_hand, False, chips, bet, stats, dealer_msg)
                dramatic_pause(1.5, anim_enabled)

                if p_bj and d_bj:
                    dealer_msg = get_dialogue("push")
                    stats["pushes"] += 1
                    streak = 0
                elif p_bj:
                    dealer_msg = get_dialogue("blackjack")
                    winnings = int(bet * 1.5)
                    chips += winnings
                    stats["wins"] += 1
                    stats["blackjacks"] += 1
                    streak += 1
                else:
                    dealer_msg = get_dialogue("player_loss")
                    chips -= bet
                    stats["losses"] += 1
                    streak -= 1

                stats["chips"] = chips
                dramatic_pause(1.5, anim_enabled)
                continue
            # Player Turn
            player_busted = False
            double_down_used = False
            while True:
                p_val = get_card_value(player_hand)
                if p_val < 10:
                    dealer_msg = get_dialogue("low_val")
                elif p_val >= 18:
                    dealer_msg = get_dialogue("high_val")
                else:
                    dealer_msg = get_dialogue("hit")

                display_table(dealer_hand, player_hand, True, chips, bet, stats, dealer_msg)

                can_double = (len(player_hand) == 2) and (chips >= bet *2)
                actions = "[H]it, [S]tand" + (", [D]ouble Down" if can_double else "")
                action = input(f" Choose action ({actions}): ").strip().lower()

                if action == "h":
                    player_hand.append(deck.pop())
                    if get_card_value(player_hand) > 21:
                        player_busted = True
                        break

                elif action == "s":
                    dealer_msg = get_dialogue("stand")
                    break
                elif action == "d" and can_double:
                    dealer_msg = get_dialogue("double")
                    chips -= bet
                    bet *= 2
                    player_hand.append(deck.pop())
                    double_down_used = True
                    if get_card_value(player_hand) > 21:
                        player_busted = True
                    break
                else:
                    delaer_msg = "Invalid action. Choose wisely."

                if player_busted:
                    break

            #  Resolve Player Bust
            if player_busted:
                dealer_msg = get_dialogue("bust")
                display_table(dealer_hand, player_hand, False, chips, bet, stats, dealer_msg)
                chips -= bet
                stats["losses"] += 1
                streak -= 1
                stats["chips"] = chips
                dramatic_pause(2.0, anim_enabled)

            else: 
                # Dealer Turn
                display_table(dealer_hand, player_hand, False, chips, bet, stats, "Dealer reveals hidden card....")
                dramatic_pause(1.0, anim_enabled)

                while get_card_value(dealer_hand) < 17:
                    dealer_hand. append(deck.pop())
                    display_table(dealer_hand, player_hand, False, chips, bet, stats, "Dealer draws another card...")
                    dramatic_pause(1.0, anim_enabled)

                p_val = get_card_value(player_hand)
                d_val = get_card_value(dealer_hand)

                if d_val > 21:
                    dealer_msg = get_dialogue("dealer_bust")
                    chips += bet
                    stats["wins"] += 1
                    streak += 1
                elif d_val > p_val:
                    dealer_msg = get_dialogue("player_loss")
                    chips -= bet
                    stats["losses"] += 1
                    streak -= 1
                elif d_val < p_val:
                    dealer_msg = get_dialogue("player_win")
                    chips += bet
                    stats["wins"] += 1
                    streak += 1
                else:
                    dealer_msg = get_dialogue("push")
                    stats["pushes"] += 1
                    streak = 0

                stats["chips"] = chips
                display_table(dealer_hand, player_hand, False, chips, bet, stats, dealer_msg)
                dramatic_pause(2.0, anim_enabled)

            # Streak Dialogue
            streak_msg = get_dialogue("streak", streak)
            if streak_msg:
                dealer_msg = streak_msg 
                display_table(dealer_hand, player_hand, False, chips,  bet, stats, dealer_msg)
                dramatic_pause(1.5, anim_enabled)

            # if Broke (brokie brokie wooooo {i swear im not a capitalist i js 
            # like gambling [not really i dont condone gambling guys please]})
            if chips <= 0:
                dealer_msg = get_dialogue("broke")
                display_table(dealer_hand, player_hand, False, chips, bet, stats, dealer_msg)
                dramatic_pause(2.5, anim_enabled)
                break

        # Game Over (Broke)
        stats["chips"] = chips
        end_game_screen(stats, starting_chips)
        break
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. The devil keeps your chips for now.")
        sys.exit(0)
            



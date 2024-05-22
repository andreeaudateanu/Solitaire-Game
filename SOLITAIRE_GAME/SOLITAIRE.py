"""
Solitaire clone.
"""
"""
Solitaire clone.
"""
import random
from typing import Optional
import arcade


# Titlul ecranului și dimensiunea
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Drag and Drop Cards"

# Definire constante pentru caracteristici buton
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
BUTTON_POSITION_X = SCREEN_WIDTH - BUTTON_WIDTH
BUTTON_POSITION_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10 // 2

RULES_TEXT = [
    "RULES:",
    "1. Drag and drop cards to move them.",
    "2. You can only move cards according to the,",
    "   game rules.",
    "3. The goal is to stack all cards in ascending order,",
    "   following suit, on the top piles.",
    "4. You can flip three cards from the deck at a time.",
    "5. Press 'R' to restart the game.",
]


# Constanta scalare
CARD_SCALE = 0.6

# Dimensiune cărți
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# Dimnsiune mat
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# Spatiere
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# Axa Y a rândului de jos (2 piloane)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Axa X pentru aliniere la stânga
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Vectori pentru cărți
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Axa Y a randului de sus (4 piloane)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Axa Y a randului din mijloc ( 7 piloane)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Spatiere intre mat-uri
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# spatiere intre cărți
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Cconstante pile-uri
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12

# imagine pentru spatele cărții
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_blue2.png"

HINT_BUTTON_SIZE = 50
HINT_BUTTON_POSITION_X = SCREEN_WIDTH - HINT_BUTTON_SIZE
HINT_BUTTON_POSITION_Y = SCREEN_HEIGHT - HINT_BUTTON_SIZE - 90

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # atribute pentru simbol și valoare
        self.suit = suit
        self.value = value

        # imagini pentru partea din față a cărții
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        self.is_face_up = False

        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")



    def face_down(self):

        """ Turn card face-down """

        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)

        self.is_face_up = False



    def face_up(self):

        """ Turn card face-up """

        self.texture = arcade.load_texture(self.image_file_name)

        self.is_face_up = True



    @property
    def is_face_down(self):

        """ Is this card face down? """

        return not self.is_face_up


class HintButton:
    def __init__(self):
        self.is_visible = True  # butonul de Hint este intotdeauna vizibil
        self.is_clicked = False
        self.image = arcade.load_texture(":resources:onscreen_controls/flat_dark/key_square.png")
        self.hint_text = ""
        self.clicked_flag = False
    def draw(self):
        # creare patrat buton
        arcade.draw_texture_rectangle(HINT_BUTTON_POSITION_X, HINT_BUTTON_POSITION_Y, HINT_BUTTON_SIZE,
                                      HINT_BUTTON_SIZE, self.image)

        # creare text buton
        arcade.draw_text("HINT", HINT_BUTTON_POSITION_X, HINT_BUTTON_POSITION_Y - 40,
                         arcade.color.WHITE, font_size=14, anchor_x="center", anchor_y="center")

    def check_click(self, x, y):
        # verificare click - in aria butonului
        if HINT_BUTTON_POSITION_X - HINT_BUTTON_SIZE / 2 <= x <= HINT_BUTTON_POSITION_X + HINT_BUTTON_SIZE / 2 \
                and HINT_BUTTON_POSITION_Y - HINT_BUTTON_SIZE / 2 <= y <= HINT_BUTTON_POSITION_Y + HINT_BUTTON_SIZE / 2:
            self.is_clicked = True

    def reset_click_flag(self):
        self.clicked_flag = False

    def set_hint_text(self, hint_text):
        self.hint_text = hint_text

    def display_hint(self):
        window_width = 400
        window_height = 100
        window_x = (SCREEN_WIDTH - window_width) / 2
        window_y = (SCREEN_HEIGHT - window_height) / 2

        # fundal semi-transparent pe toată suprafața ecranului
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT,
                                     (128, 128, 128, 200))  # Gri cu opacitate semi-transparenta

        # fereastră pentru hint
        arcade.draw_rectangle_filled(window_x + window_width / 2, window_y + window_height / 2,
                                     window_width, window_height,
                                     (124, 149, 149,255))  # Verde cu opacitate completă

        # hint text
        arcade.draw_text(self.hint_text, window_x + window_width / 2, window_y + window_height -  50,
                         arcade.color.BLACK, font_size=14, anchor_x="center", anchor_y="center")

        # buton de inchidere (X)
        close_button_size = 20
        close_button_x = window_x + window_width - close_button_size / 2 - 5
        close_button_y = window_y + window_height - close_button_size / 2 - 5
        arcade.draw_rectangle_filled(close_button_x, close_button_y, close_button_size, close_button_size,
                                     arcade.color.RED)
        arcade.draw_text("X", close_button_x, close_button_y, arcade.color.WHITE, font_size=12,
                         anchor_x="center", anchor_y="center")

    def reset_click_flag(self):
        self.clicked_flag = False


class RuleButton:
    def __init__(self):
        self.is_visible = False
        self.is_clicked = False
        self.image = arcade.load_texture(":resources:onscreen_controls/flat_dark/hamburger.png")


    def draw(self):
        # creare patrat buton
        arcade.draw_texture_rectangle(BUTTON_POSITION_X, BUTTON_POSITION_Y, BUTTON_WIDTH, BUTTON_HEIGHT, self.image)

        # creare text buton
        arcade.draw_text("RULES", BUTTON_POSITION_X, BUTTON_POSITION_Y-40,
                         arcade.color.WHITE, font_size=14, anchor_x="center", anchor_y="center")

    def check_click(self, x, y):
        # verificare click - aria butonului
        if BUTTON_POSITION_X - BUTTON_WIDTH / 2 <= x <= BUTTON_POSITION_X + BUTTON_WIDTH / 2 \
                and BUTTON_POSITION_Y - BUTTON_HEIGHT / 2 <= y <= BUTTON_POSITION_Y + BUTTON_HEIGHT / 2:
            self.is_clicked = True

    def display_rules(self):
        window_width = 400
        window_height = 200
        window_x = (SCREEN_WIDTH - window_width) / 2
        window_y = (SCREEN_HEIGHT - window_height) / 2

        # semi-transparent fundal pe tot ecranul
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT,
                                     (128, 128, 128,200))

        # fereastră reguli
        arcade.draw_rectangle_filled(window_x + window_width / 2, window_y + window_height / 2,
                                     window_width, window_height,
                                     (124, 149, 149,255))  # Verde cu opacitate completă

        # creare text pentru reguli
        for i, line in enumerate(RULES_TEXT):
            arcade.draw_text(line, window_x + window_width / 2, window_y + window_height - 20 - i * 20,
                             arcade.color.BLACK, font_size=12, anchor_x="center", anchor_y="center")

        # buton de inchidere (X)
        close_button_size = 20
        close_button_x = window_x + window_width - close_button_size / 2 - 5
        close_button_y = window_y + window_height - close_button_size / 2 - 5
        arcade.draw_rectangle_filled(close_button_x, close_button_y, close_button_size, close_button_size,
                                     arcade.color.RED)
        arcade.draw_text("X", close_button_x, close_button_y, arcade.color.WHITE, font_size=12,
                         anchor_x="center", anchor_y="center")


class RestartButton:
    def __init__(self):
        self.is_visible = True  # intotdeauna vizibil
        self.is_clicked = False
        self.image = arcade.load_texture(":resources:onscreen_controls/flat_dark/r.png")
        self.position_x = BUTTON_POSITION_X
        self.position_y = BUTTON_POSITION_Y - BUTTON_HEIGHT - 120
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT

    def draw(self):
        # creare buton
        arcade.draw_texture_rectangle( BUTTON_POSITION_X, BUTTON_POSITION_Y - BUTTON_HEIGHT - 120,
                                       BUTTON_WIDTH, BUTTON_HEIGHT, self.image)
        arcade.draw_text("RESTART", BUTTON_POSITION_X, BUTTON_POSITION_Y - BUTTON_HEIGHT - 160,
                         arcade.color.WHITE, font_size=14, anchor_x="center", anchor_y="center")

    def check_click(self, x, y):
        # verificare click - in aria butonului
        if self.position_x - BUTTON_WIDTH / 2 <= x <= self.position_x + BUTTON_WIDTH / 2 \
                and self.position_y - BUTTON_HEIGHT / 2 <= y <= self.position_y + BUTTON_HEIGHT / 2:
            self.is_clicked = True


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.rule_button = RuleButton()

        self.hint_button = HintButton()

        self.displaying_rules = False

        self.displaying_hint = False  # Add a flag for displaying hint
        self.hint_text = ""  # Hint text to be displayed

        self.displaying_hint_window = False  # Flag to control hint window visibility

        self.restart_button = RestartButton()

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.PINE_GREEN)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []



        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.POWDER_BLUE)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.POWDER_BLUE)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.POWDER_BLUE)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.POWDER_BLUE)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            # Deal proper number of cards for that pile
            for j in range(pile_no - PLAY_PILE_1 + 1):
                # Pop the card off the deck we are dealing from
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                self.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                card.position = self.pile_mat_list[pile_no].position
                # Put on top in draw order
                self.pull_to_top(card)

        # Flip up the top cards
        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        self.hint_button.draw()  # Draw the hint button

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()
        self.rule_button.draw()

        self.restart_button.draw()
        self.check_for_win()

        if self.rule_button.is_clicked:
            self.rule_button.display_rules()
            self.displaying_rules = True
            self.rule_button.is_clicked = False

        if self.displaying_rules:
            self.rule_button.display_rules()

        if self.hint_button.is_clicked:
            self.show_hint()  # Call the show_hint method
            self.hint_button.is_clicked = False

        if self.displaying_hint:
            self.hint_button.set_hint_text(self.hint_text)  # Set hint text
            self.hint_button.display_hint()  # Display the hint window


        if self.displaying_hint_window:
            self.hint_button.set_hint_text(self.hint_text)  # Set hint text
            self.hint_button.display_hint()  # Display the hint window

        if self.restart_button.is_clicked:
            self.setup()
            self.restart_button.is_clicked = False

        if self.check_win_condition():
            arcade.draw_text("Congratulations! You won!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")



    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()
        elif symbol == arcade.key.W:
            # Simulate win condition
            self.simulate_win()
            # Update screen instantly
            self.on_draw()
        elif symbol == arcade.key.K:
            # Check for win condition
            self.check_for_win()
        else:
            super().on_key_press(symbol, modifiers)

    def check_win_condition(self):
        """Check if the win condition is met."""
        # Create a set to keep track of the unique kings
        kings = set()
        # Check if there are four different kings at the top of the piles
        for pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
            top_pile = self.piles[pile_index]
            if top_pile and top_pile[-1].value == 'K':
                kings.add(top_pile[-1].suit)

        if len(kings) == 4:
            # Check if all cards are face up under each king
            for pile_index in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
                pile = self.piles[pile_index]
                if pile and pile[-1].value == 'K':
                    for card in pile[:-1]:
                        if not card.face_up:
                            return False  # Not all cards are face up under a king
            return True  # All conditions met for winning
        else:
            return False  # Not all top piles have four different kings

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        self.rule_button.check_click(x, y)
        if self.displaying_rules:
            self.displaying_rules = False
            return

        if self.displaying_hint:
            self.displaying_hint = False  # Close the hint window on any click
            self.hint_button.reset_click_flag()
            return

            # Check for clicks on hint button (existing logic)
        self.hint_button.check_click(x, y)
        if self.hint_button.is_clicked:
            self.show_hint()
            return

        self.restart_button.check_click(x, y)

        # If the restart button is clicked, restart the game
        if self.restart_button.is_clicked:
            self.setup()  # Restart the game
            self.restart_button.is_clicked = False


        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in

            pile_index = self.get_pile_for_card(primary_card)

            # Are we clicking on the bottom deck, to flip three cards?

            if pile_index == BOTTOM_FACE_DOWN_PILE:

                # Flip three cards

                for i in range(3):

                    # If we ran out of cards, stop

                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break

                    # Get top card

                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]

                    # Flip face up

                    card.face_up()

                    # Move card position to bottom-right face up pile

                    card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position

                    # Remove card from face down pile

                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)

                    # Move card to face up list

                    self.piles[BOTTOM_FACE_UP_PILE].append(card)

                    # Put on top draw-order wise
                    self.pull_to_top(card)

            elif primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)


        else:

            # Click on a mat instead of a card?

            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:

                mat = mats[0]

                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?

                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:

                    # Flip the deck back over so we can restart

                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()

                    for card in reversed(temp_list):
                        card.face_down()

                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)

                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def is_card_in_top_pile(self, card):
        """ Check if the card is in any of the top piles """
        for pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
            if card in self.piles[pile_index]:
                return True
        return False

    def close_hint_window(self):
        self.displaying_hint_window = False  # Close the hint window

    def show_hint(self):
        # Iterate through each card in the card list

        for card in self.card_list:
            # Check if the card is face up and not in a top pile
            if card.is_face_up and not self.is_card_in_top_pile(card):
                # Check if the card can be moved to any of the top piles
                for pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
                    if self.is_valid_move_to_top_pile(card, pile_index):
                        # Set the hint text
                        self.hint_text = f"\n\nMove {card.value} of {card.suit} to top pile {pile_index - TOP_PILE_1 + 1
                        }\n\n"
                        self.displaying_hint = True  # Set the flag to display hint
                        return  # Return after suggesting the first valid move found

        # If no valid move to top piles is found, suggest flipping the deck
        self.hint_text = "\n\nConsider flipping the deck to reveal more cards\n\n"
        self.displaying_hint = True  # Set the flag to display hint

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        if self.hint_button.is_clicked:
            self.show_hint()  # Call the show_hint method
            self.hint_button.is_clicked = False

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass
            if pile_index >= TOP_PILE_1 and pile_index <= TOP_PILE_4:
                if self.is_valid_move_to_top_pile(self.held_cards[0], pile_index):
                    # Move the card to the top pile
                    self.move_card_to_top_pile(self.held_cards[0], pile_index)
                    reset_position = False
            # Is it on a middle play pile?
            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Compare with the top card in the pile
                    top_card = self.piles[pile_index][-1]
                    if (CARD_VALUES.index(self.held_cards[0].value) + 1) % len(CARD_VALUES) == CARD_VALUES.index(
                            top_card.value) and \
                            ((self.held_cards[0].suit in ["Diamonds", "Hearts"] and top_card.suit in ["Spades",
                                                                                                      "Clubs"]) or
                             (self.held_cards[0].suit in ["Clubs", "Spades"] and top_card.suit in ["Diamonds",
                                                                                                   "Hearts"])):
                        # Move cards to proper position
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = top_card.center_x, \
                                top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                        for card in self.held_cards:
                            # Cards are in the right position, but we need to move them to the right list
                            self.move_card_to_new_pile(card, pile_index)
                        # Success, don't reset position of cards
                        reset_position = False
                else:
                    # Are there no cards in the middle play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x, \
                            pile.center_y - CARD_VERTICAL_OFFSET * i
                    for card in self.held_cards:
                        # Cards are in the right position, but we need to move them to the right list
                        self.move_card_to_new_pile(card, pile_index)
                    # Success, don't reset position of cards
                    reset_position = False

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def is_valid_move_to_top_pile(self, card, pile_index):
        """ Check if it's a valid move to the top pile """
        top_pile = self.piles[pile_index]
        if len(top_pile) == 0:
            # Dacă pila este goală, doar Asele pot fi plasate acolo
            return card.value == "A"
        else:
            top_card = top_pile[-1]
            # Verificăm dacă cartea corespunde suit-ului și dacă valoarea ei este cu un punct mai mare decât cea a
            # cărții de sus
            return card.suit == top_card.suit and (CARD_VALUES.index(card.value) ==
                                                   CARD_VALUES.index(top_card.value) + 1)

    def move_card_to_top_pile(self, card, pile_index):
        """ Move the card to the top pile """
        # Remove the card from its current pile
        self.remove_card_from_pile(card)
        # Update its position to the top pile
        card.position = self.pile_mat_list[pile_index].position
        # Add the card to the top pile
        self.piles[pile_index].append(card)

    def simulate_win(self):
        """Simulate winning the game by moving all cards to the top piles."""
        for card in self.card_list:
            # Pentru fiecare carte din lista de cărți
            if not self.is_card_in_top_pile(card):
                # Verificăm dacă cartea nu este deja într-una dintre piloanele de sus
                for pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
                    # Încercăm să găsim o poziție validă în pilele de sus pentru această carte
                    if self.is_valid_move_to_top_pile(card, pile_index):
                        # Dacă găsim o poziție validă, mutăm cartea acolo și ieșim din buclă
                        self.move_card_to_top_pile(card, pile_index)
                        break
        # Actualizare ecran instantanee
        self.on_draw()

    def check_for_win(self):
        """ Check if the game is won """
        if self.check_win_condition():
            arcade.draw_text("Congratulations! You won!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")
def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


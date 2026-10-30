create_deck <- function() {
  suits <- c("♠", "♥", "♦", "♣")
  ranks <- c("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
  deck <- expand.grid(rank = ranks, suit = suits, stringsAsFactors = FALSE)
  deck$value <- sapply(deck$rank, function(r) {
    if (r %in% c("J", "Q", "K")) return(10)
    if (r == "A") return(11)
    return(as.numeric(r))
  })
  return(deck[sample(nrow(deck)), ])
}

get_hand_value <- function(hand) {
  total <- sum(hand$value)
  aces <- sum(hand$rank == "A")
  while (total > 21 && aces > 0) {
    total <- total - 10
    aces <- aces - 1
  }
  return(total)
}

play_blackjack <- function() {
  cat("=== SIMPLE BLACKJACK ===\n")
  chips <- 100
  
  while (chips > 0) {
    cat(sprintf("\nYour chips: %d\n", chips))
    bet <- as.integer(readline(prompt = "Enter your bet: "))
    
    if (is.na(bet) || bet <= 0 || bet > chips) {
      cat("Invalid bet. Try again.\n")
      next
    }
    
    deck <- create_deck()
    player_hand <- deck[1:2, ]
    dealer_hand <- deck[3:4, ]
    deck <- deck[-(1:4), ]
    
    cat(sprintf("\nDealer's upcard: %s%s\n", dealer_hand$rank[1], dealer_hand$suit[1]))
    
    while (TRUE) {
      p_val <- get_hand_value(player_hand)
      cat(sprintf("Your hand: %s\n", paste(paste0(player_hand$rank, player_hand$suit), collapse = ", ")))
      cat(sprintf("Your value: %d\n", p_val))
      
      if (p_val > 21) {
        cat("Bust! You lose.\n")
        chips <- chips - bet
        break
      }
      
      action <- tolower(readline(prompt = "Hit [h] or Stand [s]? "))
      if (action == "h") {
        player_hand <- rbind(player_hand, deck[1, ])
        deck <- deck[-1, ]
      } else if (action == "s") {
        break
      }
    }
    
    if (get_hand_value(player_hand) <= 21) {
      while (get_hand_value(dealer_hand) < 17) {
        dealer_hand <- rbind(dealer_hand, deck[1, ])
        deck <- deck[-1, ]
      }
      
      d_val <- get_hand_value(dealer_hand)
      p_val <- get_hand_value(player_hand)
      
      cat(sprintf("Dealer's hand: %s (Value: %d)\n", paste(paste0(dealer_hand$rank, dealer_hand$suit), collapse = ", "), d_val))
      
      if (d_val > 21 || p_val > d_val) {
        cat("You win!\n")
        chips <- chips + bet
      } else if (p_val < d_val) {
        cat("Dealer wins.\n")
        chips <- chips - bet
      } else {
        cat("Push (Tie).\n")
      }
    }
    
    if (chips <= 0) {
      cat("\nYou are out of chips! Game over.\n")
      break
    }
    
    cont <- tolower(readline(prompt = "Play another round? (y/n): "))
    if (cont != "y") break
  }
}
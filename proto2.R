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

play_blackjack2 <- function() {
  cat("=== THE DEVIL'S CASINO (R Edition - Budget Version) ===\n")
  chips <- 500
  
  while (chips > 0) {
    cat("\n--------------------------------------------------\n")
    cat(sprintf(" CHIPS: %d\n", chips))
    cat("--------------------------------------------------\n")
    
    bet_input <- readline(prompt = "Enter your wager (Min 10): ")
    bet <- suppressWarnings(as.integer(bet_input))
    
    if (is.na(bet) || bet < 10 || bet > chips) {
      cat("Dealer: 'Invalid bet, mortal. Try again.'\n")
      next
    }
    
    deck <- create_deck()
    player_hand <- deck[1:2, ]
    dealer_hand <- deck[3:4, ]
    deck <- deck[-(1:4), ]
    
    # Awkward, messy text layout compared to the polished Python version
    cat("\n[DEALER'S HAND]\n")
    cat(sprintf("  [? ?] [%s%s]\n", dealer_hand$rank[2], dealer_hand$suit[2]))
    cat("  Value: ?\n")
    
    cat("\n[YOUR HAND]\n")
    p_cards <- paste0("[", player_hand$rank, player_hand$suit, "]", collapse = " ")
    cat("  ", p_cards, "\n")
    
    p_val <- sum(player_hand$value)
    cat(sprintf("  Value: %d\n", p_val))
    
    player_busted <- FALSE
    
    # Player Turn loop
    while (TRUE) {
      action <- tolower(readline(prompt = "Choose action - [h]it or [s]tand: "))
      
      if (action == "h") {
        player_hand <- rbind(player_hand, deck[1, ])
        deck <- deck[-1, ]
        
        p_cards <- paste0("[", player_hand$rank, player_hand$suit, "]", collapse = " ")
        cat("\n[YOUR HAND]\n  ", p_cards, "\n")
        p_val <- sum(player_hand$value)
        cat(sprintf("  Value: %d\n", p_val))
        
        if (p_val > 21) {
          cat("Dealer: 'Bust. The house takes your chips.'\n")
          chips <- chips - bet
          player_busted <- TRUE
          break
        }
      } else if (action == "s") {
        cat("Dealer: 'Holding steady. Let's see your hand.'\n")
        break
      } else {
        cat("Dealer: 'Speak clearly. Hit or stand.'\n")
      }
    }
    
    if (!player_busted) {
      cat("\n[DEALER REVEALS CARDS]\n")
      d_cards <- paste0("[", dealer_hand$rank, dealer_hand$suit, "]", collapse = " ")
      cat("  ", d_cards, "\n")
      d_val <- sum(dealer_hand$value)
      cat(sprintf("  Value: %d\n", d_val))
      
      while (d_val < 17) {
        cat("Dealer draws another card...\n")
        dealer_hand <- rbind(dealer_hand, deck[1, ])
        deck <- deck[-1, ]
        d_cards <- paste0("[", dealer_hand$rank, dealer_hand$suit, "]", collapse = " ")
        cat("  ", d_cards, "\n")
        d_val <- sum(dealer_hand$value)
        cat(sprintf("  Value: %d\n", d_val))
      }
      
      p_val <- sum(player_hand$value)
      
      if (d_val > 21) {
        cat("Dealer: 'A rare mistake on my part. Take your win.'\n")
        chips <- chips + bet
      } else if (d_val > p_val) {
        cat("Dealer: 'The house always wins in the end.'\n")
        chips <- chips - bet
      } else if (d_val < p_val) {
        cat("Dealer: 'You survive for another deal. Boring.'\n")
        chips <- chips + bet
      } else {
        cat("Dealer: 'A stalemate. Nothing gained.'\n")
      }
    }
    
    if (chips <= 0) {
      cat("\nDealer: 'Penniless. The game ends.'\n")
      cat("=== GAME OVER ===\n")
      break
    }
    
    cont <- tolower(readline(prompt = "Play another round? (y/n): "))
    if (cont != "y") {
      cat("Dealer: 'Fleeing with your spoils. Wise.'\n")
      break
    }
  }
}
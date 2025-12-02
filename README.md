# tic-tac-toe-api
REST API for playing Noughts and Crosses (a.k.a Tic-tac-toe), built for Ethyca’s Technical Challenge

## Instructions on how to run this locally:

Make sure you have Docker installed and running in your system, then do:
```bash
cp .env.example .env
docker compose -f docker-compose.dev.yaml up --build -d
```

You can look at the logs by doing:
```bash
docker compose -f docker-compose.dev.yaml logs api -f
```

## General comments about my thought process when building this

### Architecture Decisions & Tradeoffs
The feature that immediately stood out as a potential challenge was the *"view all games I played in chronological order"* one. The issue here is that, without including authentication (which I imagine would be overkill and not what's expected from this assignment) I'm forced to either store and show all games together as if multiple different players are not possible, or have a way to assign identifiers to different users.
I decided on generating a player id and then the client is instructed to include it as an "X-Player-Id" header. Not including this header will result in each game generating a new player id and each game living in a different game history. I see this as a reasonable tradeoff, the responses can include this and any client can easily store the id so that it can continue to use it. I plan to also build a browser client for this so soon enough I'll be able to demonstrate this.
Again, in a real project I would add authentication but that would require a database like PostgreSQL or MongoDB, encoding/decoding JWT, hashing and storing passwords, signup/login endpoints etc, or using something like AWS Cognito, and I'm pretty sure that's way overkill. I'll stick with a simple Redis container to store game data there (I could've also just stored everything in Python in-memory data structures but I want to at least make it somewhat resemble a real app). I will set a TTL of 24hs for the game data, which should be enough for the purposes of this test, although again, in a real world tic tac toe project (if that was a thing) we would probably want to completely persist the history of our players in a database.

### Gameplay & Behavior
It's not explicitly stated whether the player is always supposed to start the game. I decided to randomize whether the player or the CPU makes the first move. Other than that, I pretty much stuck to the basics. The CPU just makes random moves as suggested in the challenge description.

## Run unit tests
Connect to the running container:
```bash
docker exec -it api /bin/bash
```
Once inside it, run:
```bash
chmod +x tests/run_tests.sh
./tests/run_tests.sh 
```

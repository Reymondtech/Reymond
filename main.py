import matplotlib.pyplot as plt
from unicodedata import normalize


class Voter:
    def __init__(self, name, age, voter_id, origin):
        self.name = name
        self.age = age
        self.voter_id = voter_id
        self.origin = origin
        self.voted = False

    def vote(self):
        if self.age < 18:
            raise ValueError("Voter must be at least 18 years old to vote.")
        self.voted = True

class Election:
    def __init__(self, candidates):
        self.candidates = candidates
        self.votes = {candidate: 0 for candidate in candidates}
        self.voter_registry = {}
        self.votes_by_district = {}

    def register_voter(self, voter):
        self.voter_registry[voter.voter_id] = voter
        if voter.origin not in self.votes_by_district:
            self.votes_by_district[voter.origin] = {candidate: 0 for candidate in self.candidates}

    def cast_vote(self, voter_id, candidate):
        if voter_id not in self.voter_registry:
            raise ValueError("Invalid voter ID.")
        voter = self.voter_registry[voter_id]
        if voter.voted:
            raise ValueError("Voter has already voted.")
        if voter.age < 18:
            raise ValueError("Voter must be at least 18 years old to vote.")
        if candidate.lower() not in self.candidates:
            raise ValueError("Invalid candidate.")

        self.votes[candidate] += 1
        self.votes_by_district[voter.origin][candidate] += 1
        voter.vote()

    def tally_votes(self):
        return self.votes

    def declare_winner(self):
        winner = max(self.votes, key=self.votes.get)
        return winner

    def plot_combined_results(self):
        import numpy as np

        # Sort candidates by total votes
        sorted_candidates = sorted(self.votes.keys(), key=lambda candidate: self.votes[candidate], reverse=True)
        sorted_votes = [self.votes[candidate] for candidate in sorted_candidates]

        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

        # Pie chart for overall election results
        ax1.pie(sorted_votes, labels=sorted_candidates, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Election Results')
        ax1.axis('equal')

        # Bar chart for votes by district
        districts = list(self.votes_by_district.keys())
        bar_width = 0.2
        index = np.arange(len(districts))

        for i, candidate in enumerate(sorted_candidates):
            votes = [self.votes_by_district[district][candidate] for district in districts]
            ax2.bar(index + i * bar_width, votes, bar_width, label=candidate)

        ax2.set_xlabel('District')
        ax2.set_ylabel('Votes')
        ax2.set_title('Votes per District')
        ax2.set_xticks(index + bar_width * len(sorted_candidates) / 2)
        ax2.set_xticklabels(districts)
        ax2.legend()

        # Set y-axis limit to enhance clarity
        ax2.set_ylim(0, max(sorted_votes) + 5) # Adjust 5 to your preferred margin

        # Move y-axis scale (ticks and labels) outside the plot
        ax2.yaxis.set_tick_params(direction='out')

        # Move x-axis scale (ticks and labels) outside the plot
        ax2.xaxis.set_tick_params(direction='out')

        plt.tight_layout()
        plt.show()

    def display_tally(self):
        votes = self.tally_votes()
        print("Current Votes Tally:")
        for candidate, count in votes.items():
            print(f"{candidate}: {count}")

# Define candidates
candidates = ["Obama", "Robert", "Kiiza", "Aliwo"]
normalize_candidate = [x.lower() for x in candidates]

# Create an election
election = Election(normalize_candidate)

# Create voters database
voter1 = Voter("Alicia Maya", 30, "ID001", "District A")
voter2 = Voter("Alina Okla", 25, "ID002", "District B")
voter3 = Voter("Akuna Matata", 16, "ID003", "District C") # This voter is under 18 years old
voter4 = Voter("Roger Ake", 26, "ID004", "District D")
voter5 = Voter("Ali Ako", 29, "ID005", "District C")
voter6 = Voter("Ana Bella", 46, "ID006", "District D")
voter7 = Voter("Ruth Kats", 40, "ID007", "District D")
voter8 = Voter("Ali Kats", 48, "ID008", "District C")
voter9 = Voter("Abaho Patrick", 30, "ID009", "District D")
voter10 = Voter("Ruth Alic", 60, "ID0010", "District B")

election.register_voter(voter1)
election.register_voter(voter2)
election.register_voter(voter3)
election.register_voter(voter4)
election.register_voter(voter5)
election.register_voter(voter6)
election.register_voter(voter7)
election.register_voter(voter8)
election.register_voter(voter9)
election.register_voter(voter10)

# Simulate the voting process
def run_voting_process():
    while True:
         voter_id = input("Enter your voter ID: ")
         candidate = input("Enter the candidate you wish to vote for: ")
         try:
            election.cast_vote(voter_id, candidate)
            print("Vote cast successfully!")
            election.display_tally() # Display the current vote tally after each vote
         except ValueError as e:
            print(e)

         more_votes = input("Are there more voters? (yes/no): ").strip().lower()
         if more_votes != "yes":
            break

run_voting_process()

# Tally votes and declare the winner
votes = election.tally_votes()
print("Votes tally:", votes)
winner = election.declare_winner()
print("The winner is:", winner)

# Plot the combined results
election.plot_combined_results()
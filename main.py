import requests
from bs4 import BeautifulSoup
import re
from datetime import date

# Set today's date
today = date.today().strftime('%Y-%m-%d')

# Set the URL for the Bovada page containing the MLB games and their betting lines
url = f'https://www.bovada.lv/sports/baseball/mlb/{today}'

# Send an HTTP request to the URL and get the response
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the tables on the page
tables = soup.find_all('table')

# Loop through each table
for table in tables:
    # Check if the table contains MLB game information
    if 'MLB' in table.text:
        # Get the name of the teams playing in the game
        teams = re.findall(r'\b[A-Z][a-z]*\b', table.text)
        team1 = teams[0]
        team2 = teams[1]

        # Get the betting lines for the game
        lines = table.find_all('td', class_='bet-price')
        line1 = lines[0].text
        line2 = lines[1].text

        # Get the lineups for each team
        team1_lineup = []
        team2_lineup = []
        lineup_rows = table.find_all('tr')
        for row in lineup_rows:
            if team1 in row.text:
                pitcher = row.find_all('td')[1].text
                team1_lineup.append(pitcher)
                players = row.find_all('a')
                for player in players:
                    team1_lineup.append(player.text)
            elif team2 in row.text:
                pitcher = row.find_all('td')[1].text
                team2_lineup.append(pitcher)
                players = row.find_all('a')
                for player in players:
                    team2_lineup.append(player.text)

        # Print the game information
        print(f'{team1} vs {team2}')
        print(f'Bovada line: {team1} {line1} - {team2} {line2}')
        print(f'{team1} lineup: {team1_lineup}')
        print(f'{team2} lineup: {team2_lineup}')

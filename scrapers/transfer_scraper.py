import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin

class MultiSeasonTransfermarktScraper:
    def __init__(self):
        self.base_url = "https://www.transfermarkt.us"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, url):
        """Fetch a page with proper error handling and rate limiting"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(1)  # Rate limiting to be respectful
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_player_data(self, row):
        """Extract player data from a table row"""
        try:
            cells = row.find_all('td')
            if len(cells) < 18:
                return None
            
            # Extract player name (cell 4)
            player_cell = cells[3]  # 4th cell (0-indexed)
            player_link = player_cell.find('a')
            if not player_link:
                return None
            
            player_name = player_link.get_text(strip=True)
            
            # Extract position (cell 5)
            position_cell = cells[4]
            position_text = position_cell.get_text(strip=True)
            if "Goalkeeper" not in position_text:
                return None
            
            # Extract age (cell 6)
            age = cells[5].get_text(strip=True)
            
            # Extract market value (cell 7)
            market_value = cells[6].get_text(strip=True)
            
            # Extract season (cell 8)
            season = cells[7].get_text(strip=True)
            
            # Extract nationality (cell 9) - look for flag image
            nationality = ""
            nationality_cell = cells[8]
            flag_img = nationality_cell.find('img')
            if flag_img:
                nationality = flag_img.get('title', '')
            
            # Extract team left (cell 12)
            team_left_cell = cells[11]
            team_left = ""
            team_link = team_left_cell.find('a')
            if team_link:
                team_left = team_link.get_text(strip=True)
            
            # Extract team joined (cell 16)
            team_joined_cell = cells[15]
            team_joined = ""
            team_link = team_joined_cell.find('a')
            if team_link:
                team_joined = team_link.get_text(strip=True)
            
            # Extract fee (cell 18)
            fee_cell = cells[17]
            fee_text = fee_cell.get_text(strip=True)
            fee = ""
            # Extract numeric value from fee (e.g., "€31.20m" -> "31.20")
            fee_match = re.search(r'€([\d.]+)m', fee_text)
            if fee_match:
                fee = fee_match.group(1)
            else:
                # Handle other fee formats
                fee = fee_text
            
            return {
                'Player': player_name,
                'Age': age,
                'Season': season,
                'Nationality': nationality,
                'Team Left': team_left,
                'Team Joined': team_joined,
                'Fee': fee
            }
            
        except Exception as e:
            print(f"Error extracting player data: {e}")
            return None
    
    def scrape_transfers(self, url, season_name):
        """Scrape transfer data from the given URL"""
        print(f"Scraping {season_name} transfers from: {url}")
        
        html_content = self.get_page(url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main table with transfer data
        table = soup.find('table', class_='items')
        if not table:
            print("Could not find transfer table")
            return []
        
        transfers = []
        rows = table.find_all('tr', class_=['odd', 'even'])
        
        print(f"Found {len(rows)} transfer rows")
        
        for row in rows:
            player_data = self.extract_player_data(row)
            if player_data:
                transfers.append(player_data)
                print(f"Extracted: {player_data['Player']} - {player_data['Team Left']} -> {player_data['Team Joined']}")
        
        return transfers
    
    def save_to_csv(self, transfers, filename):
        """Save transfer data to CSV file"""
        if not transfers:
            print("No transfers to save")
            return
        
        fieldnames = ['Player', 'Age', 'Season', 'Nationality', 'Team Left', 'Team Joined', 'Fee']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transfers)
        
        print(f"Saved {len(transfers)} transfers to {filename}")

def main():
    # Initialize scraper
    scraper = MultiSeasonTransfermarktScraper()
    
    # Define URLs and season names
    seasons = [
        {
            'url': "https://www.transfermarkt.us/transfers/transferrekorde/statistik/top/plus/1/galerie/0?saison_id=2025&land_id=&ausrichtung=&spielerposition_id=1&altersklasse=&jahrgang=0&leihe=&w_s=",
            'name': '2025-2026',
            'filename': 'goalkeeper_transfers_2025_2026.csv'
        },
        {
            'url': "https://www.transfermarkt.us/transfers/transferrekorde/statistik/top/plus/1/galerie/0?saison_id=2024&land_id=&ausrichtung=&spielerposition_id=1&altersklasse=&jahrgang=0&leihe=&w_s=",
            'name': '2024-2025',
            'filename': 'goalkeeper_transfers_2024_2025.csv'
        },
        {
            'url': "https://www.transfermarkt.us/transfers/transferrekorde/statistik/top/plus/1/galerie/0?saison_id=2023&land_id=&ausrichtung=&spielerposition_id=1&altersklasse=&jahrgang=0&leihe=&w_s=",
            'name': '2023-2024',
            'filename': 'goalkeeper_transfers_2023_2024.csv'
        }
    ]
    
    total_transfers = 0
    
    for season in seasons:
        print(f"\n{'='*50}")
        print(f"Processing {season['name']} season...")
        print(f"{'='*50}")
        
        # Scrape the transfers
        transfers = scraper.scrape_transfers(season['url'], season['name'])
        
        if transfers:
            # Save to CSV
            scraper.save_to_csv(transfers, season['filename'])
            total_transfers += len(transfers)
            
            # Display first few entries as preview
            print(f"\nPreview of {season['name']} data:")
            for i, transfer in enumerate(transfers[:3]):
                print(f"{i+1}. {transfer['Player']}, {transfer['Age']}, {transfer['Season']}, {transfer['Nationality']}, {transfer['Team Left']}, {transfer['Team Joined']}, {transfer['Fee']}")
        else:
            print(f"No transfers were scraped for {season['name']}. Please check the URL and try again.")
    
    print(f"\n{'='*50}")
    print(f"SCRAPING COMPLETE!")
    print(f"Total transfers scraped across all seasons: {total_transfers}")
    print(f"Files created:")
    for season in seasons:
        print(f"  - {season['filename']}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main() 
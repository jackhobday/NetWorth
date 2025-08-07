import requests
from bs4 import BeautifulSoup
import csv
import time
import re

class GoalkeeperMarketValueScraper:
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
            if len(cells) < 9:
                return None
            
            # Extract rank (cell 1)
            rank = cells[0].get_text(strip=True)
            
            # Extract player name (cell 4)
            player_cell = cells[3]  # 4th cell (0-indexed)
            player_link = player_cell.find('a')
            if not player_link:
                return None
            
            player_name = player_link.get_text(strip=True)
            
            # Check if it's a goalkeeper (cell 5)
            position_cell = cells[4]
            position_text = position_cell.get_text(strip=True)
            if "Goalkeeper" not in position_text:
                return None
            
            # Extract age (cell 6)
            age = cells[5].get_text(strip=True)
            
            # Extract nationality (cell 7) - look for flag image
            nationality = ""
            nationality_cell = cells[6]
            flag_img = nationality_cell.find('img')
            if flag_img:
                nationality = flag_img.get('title', '')
            
            # Extract club (cell 8)
            club_cell = cells[7]
            club = ""
            club_link = club_cell.find('a')
            if club_link:
                # Club name is in the title attribute, not text content
                club = club_link.get('title', '')
                if not club:
                    # Fallback to text content if title is not available
                    club = club_link.get_text(strip=True)
            
            # Extract market value (cell 9)
            market_value_cell = cells[8]
            market_value_text = market_value_cell.get_text(strip=True)
            market_value = ""
            # Extract numeric value from market value (e.g., "€40.00m" -> "40.00")
            market_value_match = re.search(r'€([\d.]+)m', market_value_text)
            if market_value_match:
                market_value = market_value_match.group(1)
            else:
                # Handle other market value formats
                market_value = market_value_text
            
            return {
                'Rank': rank,
                'Player': player_name,
                'Age': age,
                'Nationality': nationality,
                'Club': club,
                'Market Value': market_value
            }
            
        except Exception as e:
            print(f"Error extracting player data: {e}")
            return None
    
    def scrape_market_values(self, url):
        """Scrape market value data from the given URL"""
        print(f"Scraping goalkeeper market values from: {url}")
        
        html_content = self.get_page(url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main table with market value data
        table = soup.find('table', class_='items')
        if not table:
            print("Could not find market value table")
            return []
        
        market_values = []
        rows = table.find_all('tr', class_=['odd', 'even'])
        
        print(f"Found {len(rows)} market value rows")
        
        for row in rows:
            player_data = self.extract_player_data(row)
            if player_data:
                market_values.append(player_data)
                print(f"Extracted: {player_data['Player']} - {player_data['Club']} - €{player_data['Market Value']}m")
        
        return market_values
    
    def save_to_csv(self, market_values, filename="goalkeeper_market_values.csv"):
        """Save market value data to CSV file"""
        if not market_values:
            print("No market values to save")
            return
        
        fieldnames = ['Rank', 'Player', 'Age', 'Nationality', 'Club', 'Market Value']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(market_values)
        
        print(f"Saved {len(market_values)} market values to {filename}")

def main():
    # Initialize scraper
    scraper = GoalkeeperMarketValueScraper()
    
    # URL for goalkeeper market values
    url = "https://www.transfermarkt.us/spieler-statistik/wertvollstespieler/marktwertetop/mw/spielerposition_id/1"
    
    # Scrape the market values
    market_values = scraper.scrape_market_values(url)
    
    if market_values:
        # Save to CSV
        scraper.save_to_csv(market_values)
        print(f"\nSuccessfully scraped {len(market_values)} goalkeeper market values")
        
        # Display first few entries as preview
        print("\nPreview of scraped data:")
        for i, player in enumerate(market_values[:5]):
            print(f"{i+1}. {player['Player']}, {player['Age']}, {player['Nationality']}, {player['Club']}, €{player['Market Value']}m")
    else:
        print("No market values were scraped. Please check the URL and try again.")

if __name__ == "__main__":
    main() 
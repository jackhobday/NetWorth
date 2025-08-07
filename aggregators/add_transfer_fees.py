import pandas as pd

def add_recent_fees():
    """
    Add Recent Fee column to goalkeeper_dataset by looking through transfer datasets
    and finding the most recent transfer fee for each goalkeeper.
    """
    
    print("Loading goalkeeper dataset...")
    goalkeeper_data = pd.read_csv('goalkeeper_dataset.csv')
    print(f"Loaded {len(goalkeeper_data)} rows from goalkeeper_dataset.csv")
    
    print("\nLoading transfer datasets...")
    # Load all three transfer datasets
    transfers_2025_2026 = pd.read_csv('goalkeeper_transfers_2025_2026.csv')
    transfers_2024_2025 = pd.read_csv('goalkeeper_transfers_2024_2025.csv')
    transfers_2023_2024 = pd.read_csv('goalkeeper_transfers_2023_2024.csv')
    
    print(f"Loaded {len(transfers_2025_2026)} rows from 2025-2026 transfers")
    print(f"Loaded {len(transfers_2024_2025)} rows from 2024-2025 transfers")
    print(f"Loaded {len(transfers_2023_2024)} rows from 2023-2024 transfers")
    
    # Combine all transfer datasets
    all_transfers = pd.concat([transfers_2025_2026, transfers_2024_2025, transfers_2023_2024], ignore_index=True)
    print(f"Combined transfer dataset has {len(all_transfers)} total rows")
    
    # Create season order for sorting (newest first)
    season_order = {
        '25/26': 1,
        '24/25': 2,
        '23/24': 3
    }
    
    # Add temporary sorting column
    all_transfers['season_order'] = all_transfers['Season'].map(season_order)
    
    # Sort by Player name, then by season order (newest first)
    all_transfers_sorted = all_transfers.sort_values(['Player', 'season_order'])
    
    # Remove the temporary sorting column
    all_transfers_sorted = all_transfers_sorted.drop('season_order', axis=1)
    
    # Get the most recent transfer for each player
    # Group by Player and take the first row (which will be the most recent due to sorting)
    most_recent_transfers = all_transfers_sorted.groupby('Player').first().reset_index()
    
    print(f"Found {len(most_recent_transfers)} unique players with transfers")
    
    # Create a mapping of player name to most recent fee
    player_fee_mapping = dict(zip(most_recent_transfers['Player'], most_recent_transfers['Fee']))
    
    # Add Recent Fee column to goalkeeper dataset
    goalkeeper_data['Recent Fee'] = goalkeeper_data['Player'].map(player_fee_mapping)
    
    # Fill NaN values with empty string (for players without transfers)
    goalkeeper_data['Recent Fee'] = goalkeeper_data['Recent Fee'].fillna('')
    
    # Save the updated dataset
    goalkeeper_data.to_csv('goalkeeper_dataset.csv', index=False)
    
    print(f"\nUpdated goalkeeper_dataset.csv with Recent Fee column")
    print(f"Players with recent transfers: {len(most_recent_transfers)}")
    print(f"Players without transfers: {len(goalkeeper_data) - len(most_recent_transfers)}")
    
    # Show some examples
    print(f"\nExample players with recent transfers:")
    for _, row in most_recent_transfers.head(5).iterrows():
        print(f"  {row['Player']}: €{row['Fee']}m ({row['Season']})")
    
    # Show players in goalkeeper dataset who have recent transfers
    players_with_fees = goalkeeper_data[goalkeeper_data['Recent Fee'] != '']
    print(f"\nPlayers in goalkeeper dataset with recent transfers: {len(players_with_fees['Player'].unique())}")
    
    # Show first few rows as preview
    print(f"\nFirst 5 rows of updated dataset:")
    print(goalkeeper_data[['Player', 'Season', 'Squad', 'Recent Fee']].head().to_string(index=False))
    
    return goalkeeper_data

if __name__ == "__main__":
    add_recent_fees() 
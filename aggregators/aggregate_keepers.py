import pandas as pd

def aggregate_goalkeeper_stats():
    """
    Aggregate all three goalkeeper stats CSV files into one dataset.
    Players will be grouped together with their rows consecutive.
    """
    
    print("Loading goalkeeper stats datasets...")
    
    # Load all three datasets
    stats_2024_2025 = pd.read_csv('keepers_stats_2024_2025.csv')
    stats_2023_2024 = pd.read_csv('keepers_stats_2023_2024.csv')
    stats_2022_2023 = pd.read_csv('keepers_stats_2022_2023.csv')
    
    print(f"Loaded {len(stats_2024_2025)} rows from 2024-2025")
    print(f"Loaded {len(stats_2023_2024)} rows from 2023-2024")
    print(f"Loaded {len(stats_2022_2023)} rows from 2022-2023")
    
    # Combine all datasets
    all_stats = pd.concat([stats_2024_2025, stats_2023_2024, stats_2022_2023], ignore_index=True)
    
    print(f"Combined dataset has {len(all_stats)} total rows")
    
    # Sort by Player name first, then by Season (newest to oldest)
    # Create a season order mapping for proper sorting
    season_order = {
        '2024-2025': 1,
        '2023-2024': 2,
        '2022-2023': 3
    }
    
    # Add a temporary column for sorting
    all_stats['season_order'] = all_stats['Season'].map(season_order)
    
    # Sort by Player name, then by season order
    all_stats_sorted = all_stats.sort_values(['Player', 'season_order'])
    
    # Remove the temporary sorting column
    all_stats_sorted = all_stats_sorted.drop('season_order', axis=1)
    
    # Save the aggregated dataset
    all_stats_sorted.to_csv('goalkeeper_dataset.csv', index=False)
    
    print(f"Saved aggregated dataset with {len(all_stats_sorted)} rows to goalkeeper_dataset.csv")
    
    # Show some statistics
    unique_players = all_stats_sorted['Player'].nunique()
    print(f"Unique players in dataset: {unique_players}")
    
    # Show players who appear in multiple seasons
    player_counts = all_stats_sorted['Player'].value_counts()
    multi_season_players = player_counts[player_counts > 1]
    print(f"Players appearing in multiple seasons: {len(multi_season_players)}")
    
    # Show example of a player with multiple seasons
    if len(multi_season_players) > 0:
        example_player = multi_season_players.index[0]
        example_data = all_stats_sorted[all_stats_sorted['Player'] == example_player]
        print(f"\nExample - {example_player} appears in {len(example_data)} seasons:")
        for _, row in example_data.iterrows():
            print(f"  {row['Player']}, {row['Season']}, {row['Nation']}, {row['Squad']}, {row['Comp']}")
    
    # Show first few rows as preview
    print(f"\nFirst 5 rows of aggregated dataset:")
    print(all_stats_sorted.head().to_string(index=False))
    
    return all_stats_sorted

if __name__ == "__main__":
    aggregate_goalkeeper_stats() 
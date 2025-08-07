import pandas as pd

# European Top 5 Leagues Advanced Goalkeeper Stats 2024-2025
keeper_stats_2024_2025 = pd.read_html('https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats',
                  attrs={"id":"stats_keeper_adv"}, header=None)[0]

# Find the header row (it contains "Rk,Player,Nation,Pos,Squad,Comp,Age,Born,90s,GA,PKA,FK,CK,OG,PSxG,PSxG/SoT,PSxG+/-,/90,Cmp,Att,Cmp%,Att (GK),Thr,Launch%,AvgLen,Att,Launch%,AvgLen,Opp,Stp,Stp%,#OPA,#OPA/90,AvgDist")
header_row = None
for i, row in keeper_stats_2024_2025.iterrows():
    if row.iloc[0] == 'Rk' and row.iloc[1] == 'Player':
        header_row = i
        break

if header_row is not None:
    # Get the header row
    header_data = keeper_stats_2024_2025.iloc[header_row]
    
    # Remove the header row from the dataframe
    keeper_stats_2024_2025 = keeper_stats_2024_2025.drop(header_row)
    
    # Set the column names to the header data
    keeper_stats_2024_2025.columns = header_data
    
    # Now remove any remaining rows that match the header pattern (duplicate headers)
    keeper_stats_2024_2025 = keeper_stats_2024_2025[~((keeper_stats_2024_2025.iloc[:, 0] == 'Rk') & (keeper_stats_2024_2025.iloc[:, 1] == 'Player'))]

# Remove the first column (Rk) and the last column
keeper_stats_2024_2025 = keeper_stats_2024_2025.iloc[:, 1:-1]

# Add Season column after Player column
keeper_stats_2024_2025.insert(1, 'Season', '2024-2025')

keeper_stats_2024_2025.to_csv('keepers_stats_2024_2025.csv', index=False)

# European Top 5 Leagues Advanced Goalkeeper Stats 2023-2024
keeper_stats_2023_2024 = pd.read_html('https://fbref.com/en/comps/Big5/2023-2024/keepersadv/players/2023-2024-Big-5-European-Leagues-Stats',
                  attrs={"id":"stats_keeper_adv"}, header=None)[0]

header_row = None
for i, row in keeper_stats_2023_2024.iterrows():
    if row.iloc[0] == 'Rk' and row.iloc[1] == 'Player':
        header_row = i
        break

if header_row is not None:
    # Get the header row
    header_data = keeper_stats_2023_2024.iloc[header_row]
    
    # Remove the header row from the dataframe
    keeper_stats_2023_2024 = keeper_stats_2023_2024.drop(header_row)
    
    # Set the column names to the header data
    keeper_stats_2023_2024.columns = header_data
    
    # Now remove any remaining rows that match the header pattern (duplicate headers)
    keeper_stats_2023_2024 = keeper_stats_2023_2024[~((keeper_stats_2023_2024.iloc[:, 0] == 'Rk') & (keeper_stats_2023_2024.iloc[:, 1] == 'Player'))]
    
# Remove the first column (Rk) and the last column
keeper_stats_2023_2024 = keeper_stats_2023_2024.iloc[:, 1:-1]

# Add Season column after Player column
keeper_stats_2023_2024.insert(1, 'Season', '2023-2024')

keeper_stats_2023_2024.to_csv('keepers_stats_2023_2024.csv', index=False)

# European Top 5 Leagues Advanced Goalkeeper Stats 2022-2023
keeper_stats_2022_2023 = pd.read_html('https://fbref.com/en/comps/Big5/2022-2023/keepersadv/players/2022-2023-Big-5-European-Leagues-Stats',
                  attrs={"id":"stats_keeper_adv"}, header=None)[0]

header_row = None
for i, row in keeper_stats_2022_2023.iterrows():
    if row.iloc[0] == 'Rk' and row.iloc[1] == 'Player':
        header_row = i
        break

if header_row is not None:
    # Get the header row
    header_data = keeper_stats_2022_2023.iloc[header_row]
    
    # Remove the header row from the dataframe
    keeper_stats_2022_2023 = keeper_stats_2022_2023.drop(header_row)
    
    # Set the column names to the header data               
    keeper_stats_2022_2023.columns = header_data

    # Now remove any remaining rows that match the header pattern (duplicate headers)
    keeper_stats_2022_2023 = keeper_stats_2022_2023[~((keeper_stats_2022_2023.iloc[:, 0] == 'Rk') & (keeper_stats_2022_2023.iloc[:, 1] == 'Player'))]
    
# Remove the first column (Rk) and the last column
keeper_stats_2022_2023 = keeper_stats_2022_2023.iloc[:, 1:-1]

# Add Season column after Player column
keeper_stats_2022_2023.insert(1, 'Season', '2022-2023')

keeper_stats_2022_2023.to_csv('keepers_stats_2022_2023.csv', index=False)












import pandas as pd

# Load the exploded data from the text file
data_exploded = pd.read_csv('output.txt', sep='\t')

# Group by the relevant columns and join the 'Objects' values back together
data_original = data_exploded.groupby(['ID', 'Category', 'Term', 'Count', 'p.adjust'], as_index=False).agg({'Objects': '/'.join})

# Save the re-constructed DataFrame back to a text file
data_original.to_csv('reconstructed_input.txt', sep='\t', index=False)

# Optional: Print confirmation
print("Data has been reconstructed and saved to 'reconstructed_input.txt'.")
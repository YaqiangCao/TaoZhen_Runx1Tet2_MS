import io
from glob import glob
import pandas as pd


def merge_cpg_from_file(input_filepath, output_filepath, proximity_threshold=200, min_sites_per_region=5):
    """
    Reads a BED file, merges proximal CpG sites, and writes the filtered result to a new BED file.

    Args:
        input_filepath (str): Path to the input BED file.
        output_filepath (str): Path to save the output BED file.
        proximity_threshold (int): The maximum distance between sites to be merged.
        min_sites_per_region (int): The minimum number of sites a merged region must have to be kept.
    """
    try:
        df = pd.read_csv(input_filepath, sep='\t', header=None, usecols=[0, 1, 2])
        df.columns = ['chrom', 'start', 'end']
    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    if df.empty:
        print("Input file is empty. No output will be generated.")
        return

    df_sorted = df.sort_values(by=['chrom', 'start']).reset_index(drop=True)

    merged_regions = []
    current_chrom = df_sorted.loc[0, 'chrom']
    current_start = df_sorted.loc[0, 'start']
    current_end = df_sorted.loc[0, 'end']
    site_count = 1

    for i in range(1, len(df_sorted)):
        next_chrom = df_sorted.loc[i, 'chrom']
        next_start = df_sorted.loc[i, 'start']
        next_end = df_sorted.loc[i, 'end']

        if next_chrom == current_chrom and (next_start - current_end) <= proximity_threshold:
            current_end = next_end
            site_count += 1
        else:
            merged_regions.append([current_chrom, current_start, current_end, site_count])
            current_chrom = next_chrom
            current_start = next_start
            current_end = next_end
            site_count = 1

    merged_regions.append([current_chrom, current_start, current_end, site_count])

    merged_df = pd.DataFrame(merged_regions, columns=['chrom', 'start', 'end', 'count'])

    # --- NEW: Filter the results based on the minimum number of sites ---
    filtered_df = merged_df[merged_df['count'] >= min_sites_per_region]

    # Save the filtered DataFrame to the output file
    filtered_df.to_csv(output_filepath, sep='\t', header=False, index=False)
    print(f"Successfully merged and filtered sites. Output saved to: {output_filepath}")


fs = glob("../1.sets/*.bed")
for f in fs:
    fo = f.split("/")[-1]  
    merge_cpg_from_file(f, fo, proximity_threshold=1000)


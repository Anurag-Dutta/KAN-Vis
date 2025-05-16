import numpy as np
import matplotlib.pyplot as plt
import os

file_path = r"..."
data = np.load(file_path)

output_folder = r"..."
os.makedirs(output_folder, exist_ok=True)

num_channels = data.shape[0]

for channel in range(num_channels):
    single_channel_data = data[channel, 0, :, :]
    print(f"Dimensions of channel {channel} of the .npy file: {single_channel_data.shape}")
    
    single_channel_data = np.nan_to_num(single_channel_data, nan=0.0)

    max_value = single_channel_data.max()

    if max_value > 0:
        normalized_data = (single_channel_data / max_value) * 255
    else:
        normalized_data = single_channel_data

    normalized_data = normalized_data.astype(np.uint8)

    masked_data = np.where(normalized_data == 0, 255, normalized_data)

    plt.figure(figsize=(6, 6))
    plt.imshow(masked_data, cmap='gray', vmin=0, vmax=255)

    plt.axis('off')

    output_file = os.path.join(output_folder, f'..._{channel}.png')
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    
    plt.close()
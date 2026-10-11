import numpy as np
from PIL import Image
import argparse
import os
from io import BytesIO

def create_random_color_noise_gif(width, height, num_frames=30, duration=100, max_file_size_kb=None, output_path="random_noise.gif"):
    
    frames = []
    
    print(f"Creating {num_frames} frames of {width}x{height} random color noise...")
    
    for i in range(num_frames):
        random_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        
        frame = Image.fromarray(random_array, 'RGB')
        frames.append(frame)
        
        if (i + 1) % 5 == 0 or i == num_frames - 1:
            print(f"  Frame {i+1}/{num_frames} created")
    
    print("Saving GIF...")
    
    if max_file_size_kb is not None:
        max_file_size_bytes = max_file_size_kb * 1024
        
        optimization_levels = [
            {"optimize": True, "colors": 256},
            {"optimize": True, "colors": 128},
            {"optimize": True, "colors": 64},
            {"optimize": False, "colors": 256},
        ]
        
        best_result = None
        best_size = float('inf')
        
        for params in optimization_levels:
            with BytesIO() as temp_buffer:
                frames[0].save(
                    temp_buffer,
                    format='GIF',
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=params["optimize"],
                    colors=params["colors"],
                    quality=85
                )
                temp_size = temp_buffer.tell()
                
                print(f"  Try: optimize={params['optimize']}, colors={params['colors']} -> {temp_size/1024:.1f}KB")
                
                if temp_size <= max_file_size_bytes and temp_size < best_size:
                    best_size = temp_size
                    best_result = temp_buffer.getvalue()
                
                if best_result is not None and best_size <= max_file_size_bytes * 0.9:
                    break
        
        if best_result is not None:
            with open(output_path, 'wb') as f:
                f.write(best_result)
            final_size = best_size / 1024
            print(f"Saved with size: {final_size:.1f}KB (target: {max_file_size_kb}KB)")
        else:
            print(f"Warning: Could not reduce file size to {max_file_size_kb}KB. Saving with default settings.")
            frames[0].save(
                output_path,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,
                optimize=True
            )
            final_size = os.path.getsize(output_path) / 1024
            print(f"Saved with size: {final_size:.1f}KB (target: {max_file_size_kb}KB)")
    else:
        frames[0].save(
            output_path,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=True
        )
        final_size = os.path.getsize(output_path) / 1024
        print(f"Saved with size: {final_size:.1f}KB")
    
    print(f"Output: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Create random color noise GIF with specified size and file size limits')
    parser.add_argument('-w', '--width', type=int, default=640, help='Image width in pixels (default: 640)')
    parser.add_argument('-ht', '--height', type=int, default=480, help='Image height in pixels (default: 480)')
    parser.add_argument('-f', '--frames', type=int, default=30, help='Number of frames (default: 30)')
    parser.add_argument('-d', '--duration', type=int, default=100, help='Frame duration in ms (default: 100)')
    parser.add_argument('-s', '--max-size', type=int, default=None, help='Maximum file size in KB (default: no limit)')
    parser.add_argument('-o', '--output', type=str, default='random_noise.gif', help='Output file path (default: random_noise.gif)')
    
    args = parser.parse_args()
    
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive integers")
        return
    
    if args.frames <= 0:
        print("Error: Number of frames must be positive")
        return
    
    if args.max_size is not None and args.max_size < 10:
        print("Warning: Very small file size limit. Image quality may be poor.")
    
    create_random_color_noise_gif(
        width=args.width,
        height=args.height,
        num_frames=args.frames,
        duration=args.duration,
        max_file_size_kb=args.max_size,
        output_path=args.output
    )

if __name__ == "__main__":
    main()
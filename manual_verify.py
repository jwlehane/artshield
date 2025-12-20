from backend.processor import ImageProcessor, ProtectionParams, ProtectionType, Intensity
from PIL import Image
import os
import piexif
import numpy as np
import sys

import argparse

# Ensure backend is in path
sys.path.append(os.path.join(os.getcwd(), "backend"))

def main():
    parser = argparse.ArgumentParser(description="Manually verify ArtShield protection on an image.")
    parser.add_argument("input_file", nargs="?", help="Path to the image file to protect.")
    args = parser.parse_args()

    # 1. Prepare input image
    if args.input_file:
        if not os.path.exists(args.input_file):
            print(f"--- ERROR: File not found: {args.input_file}")
            return
        input_path = args.input_file
        print(f"--- Using provided image: {input_path}")
    else:
        # Fallback to creating a sample image if none provided
        input_path = "verify_input_dummy.jpg"
        img = Image.new('RGB', (400, 400), color=(50, 150, 50))
        img.save(input_path)
        print(f"--- No input provided. Created dummy sample image: {input_path}")

    # 2. Setup Protection Parameters
    # We'll use Cloak (Glaze-style) and Metadata Tagging
    params = ProtectionParams(
        image_path=input_path,
        protection_type=ProtectionType.CLOAK_AND_TAG,
        intensity=Intensity.HIGH,
        metadata={
            "author": "ArtShield Artist",
            "copyright": "Copyright 2025 ArtShield",
            "noai": "True"
        }
    )

    # 3. Run the Processor
    print("--- Running Protection Engine...")
    try:
        processor = ImageProcessor(input_path)
        result = processor.process(params)

        if result.success:
            abs_path = os.path.abspath(result.protected_path)
            print(f"--- SUCCESS! Protected image saved to: {abs_path}")
            
            # 4. Verify Results
            with Image.open(result.protected_path) as out_img:
                # Check if pixels changed (Adversarial Noise)
                original_img = Image.open(input_path)
                original_pixels = np.array(original_img)
                protected_pixels = np.array(out_img)
                diff = np.sum(np.abs(original_pixels.astype(int) - protected_pixels.astype(int)))
                print(f"--- Verification: Total pixel difference (Adversarial Noise): {diff}")
                
                # Check Metadata Preservation
                print("--- Verification: Metadata Analysis")
                try:
                    # Load Original EXIF safely
                    if 'exif' in original_img.info:
                        orig_exif = piexif.load(original_img.info['exif'])
                    else:
                        orig_exif = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}

                    # Load Protected EXIF
                    prot_exif = piexif.load(out_img.info['exif'])

                    # Helper to count total tags
                    def count_tags(d):
                        return sum(len(v) for k, v in d.items() if isinstance(v, dict))

                    print(f"    Original Tag Count: {count_tags(orig_exif)}")
                    print(f"    Protected Tag Count: {count_tags(prot_exif)}")

                    # 1. Verify ArtShield Tags
                    artist = prot_exif['0th'].get(piexif.ImageIFD.Artist, b"Not Found").decode()
                    print(f"    [New] ArtShield Artist: {artist}")
                    user_comment = prot_exif['Exif'].get(piexif.ExifIFD.UserComment, b"").decode(errors='ignore')
                    print(f"    [New] NoAI Tag Present: {'NoAI' in user_comment}")

                    # 2. Verify Preservation of Random Original Tag
                    # We check for a tag that isn't one we overwrite (Artist/Copyright/Software)
                    our_tags = [piexif.ImageIFD.Artist, piexif.ImageIFD.Copyright, piexif.ImageIFD.Software]
                    preserved_keys = [k for k in orig_exif['0th'] if k not in our_tags]
                    
                    if preserved_keys:
                        sample_key = preserved_keys[0]
                        orig_val = orig_exif['0th'][sample_key]
                        prot_val = prot_exif['0th'].get(sample_key)
                        
                        is_preserved = (orig_val == prot_val)
                        status = "PASSED" if is_preserved else "FAILED"
                        print(f"    [Preservation] Checking Tag ID {sample_key} (e.g. Model/Make): {status}")
                        if not is_preserved:
                            print(f"      Original: {orig_val}")
                            print(f"      Protected: {prot_val}")
                    elif count_tags(orig_exif) > 0:
                         print("    [Preservation] Original had tags, but all were overwritten by ArtShield defaults (Artist/Copyright).")
                    else:
                        print("    [Preservation] Original image had no EXIF data to preserve.")

                except Exception as e:
                    print(f"    Metadata verification error: {e}")
        else:
            print(f"--- FAILURE: {result.error}")
            
    except Exception as e:
        print(f"--- CRITICAL ERROR: {e}")
    finally:
        # Optional: Clean up input if you want
        # os.remove(input_path)
        pass

if __name__ == "__main__":
    main()

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

# Add the project root to the Python path if needed
sys.path.append('.')

# Try to import from wraipperz
try:
    from wraipperz.api.video_gen import generate_video_from_image, wait_for_video_completion
except ImportError:
    try:
        from src.wraipperz.api.video_gen import generate_video_from_image, wait_for_video_completion
    except ImportError:
        print("ERROR: Could not import the wraipperz library. Make sure it's installed.")
        sys.exit(1)

# Load environment variables
load_dotenv(override=True)

# Function to test video generation with a specific model
def test_model(model_name, image_path, prompt):
    print(f"\n{'='*50}")
    print(f"TESTING MODEL: {model_name}")
    print(f"{'='*50}")
    
    output_filename = f"pixverse_{model_name.split('/')[-1].replace('-', '_')}.mp4"
    
    print(f"Input image: {image_path}")
    print(f"Prompt: {prompt}")
    print(f"Output file: {output_filename}")
    
    try:
        # Convert the image to a video with motion
        result = generate_video_from_image(
            model=model_name,
            image_path=image_path,
            prompt=prompt,
            negative_prompt="low quality, blurry",
            duration=5,
            quality="720p",
            motion_mode="normal",
            wait_for_completion=True,
            output_path=output_filename,
            max_wait_time=300  # Wait up to 5 minutes for completion
        )
        
        print("\nVIDEO GENERATION RESULT:")
        print(f"Video ID: {result.get('video_id', 'unknown')}")
        print(f"Request ID: {result.get('request_id', 'unknown')}")
        
        if 'file_path' in result:
            print(f"SUCCESS! Video downloaded to: {result['file_path']}")
        else:
            print("The video was generated but could not be automatically downloaded.")
            print(f"Video URL (if available): {result.get('url', 'Not available')}")
            print("You can access your videos in the Pixverse dashboard: https://app.pixverse.ai/studio")
        
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    # Check if an image path is provided as a command-line argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Use a default test image if none provided
        image_path = "test_image.png"
    
    # Verify image exists
    if not Path(image_path).exists():
        print(f"ERROR: Image file not found: {image_path}")
        print("Please provide a valid image path as the first argument or create a 'test_image.png' file.")
        sys.exit(1)
    
    # Set up the prompt
    prompt = "Add gentle motion and subtle animation. Maintain the original composition. Good quality, detailed animation."
    
    # Test v4.0 model (will be converted to v4 internally)
    test_model("pixverse/image-to-video-v4.0", image_path, prompt)
    
    # Test v4.5 model
    # test_model("pixverse/image-to-video-v4.5", image_path, prompt)
    
    print("\nAll tests completed. Check the output files if successful.") 
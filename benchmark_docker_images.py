import subprocess
import sys
import os
import time

# Define image build info
dockerfiles = {
    "singlestage": "singlestage.Dockerfile",
    "standalone": "standalone.Dockerfile",
    "multistage": "multistage.Dockerfile",
}

# Tag format for easier reference
image_tags = {key: f"uv-example:{key}" for key in dockerfiles}

def check_prerequisites():
    # Check if Docker is running
    if subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL).returncode != 0:
        print("❌ Docker does not seem to be running.")
        return False
    
    # Check if all Dockerfiles exist
    for name, dockerfile in dockerfiles.items():
        if not os.path.exists(dockerfile):
            print(f"❌ Dockerfile not found: {dockerfile}")
            return False
    return True

def build_image(name, dockerfile):
    print(f"📦 Building '{name}' from {dockerfile}...")
    start_time = time.time()
    result = subprocess.run([
        "docker", "build",
        "-f", dockerfile,
        "-t", image_tags[name],
        "."
    ], capture_output=True, text=True)
    build_time = time.time() - start_time

    if result.returncode != 0:
        print(f"❌ Failed to build {name}:")
        print(result.stderr)
        return None, None
    return image_tags[name], build_time

def get_image_size(image):
    # Get size using docker images command which shows actual disk usage
    result = subprocess.run(
        ["docker", "images", "--format={{.Size}}", image],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️  Failed to inspect image size for {image}")
        return None
    
    # Parse size string (e.g., "123MB" or "1.23GB")
    size_str = result.stdout.strip()
    if 'GB' in size_str:
        size_mb = float(size_str.replace('GB', '')) * 1024
    else:
        size_mb = float(size_str.replace('MB', ''))
    
    return {
        'size': round(size_mb, 2)
    }

def cleanup_images():
    print("\n🧹 Cleaning up images...")
    for image in image_tags.values():
        subprocess.run(["docker", "rmi", image], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = round(seconds % 60, 1)
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"

def main():
    if not check_prerequisites():
        sys.exit(1)

    print("🚀 Starting Docker image size comparison...\n")
    results = {}

    try:
        for name, dockerfile in dockerfiles.items():
            image, build_time = build_image(name, dockerfile)
            if image:
                size = get_image_size(image)
                if size:
                    results[name] = {'size': size['size'], 'time': build_time}
                    print(f"✅ Image '{name}' built:")
                    print(f"   • Size: {size['size']} MB")
                    print(f"   • Build time: {format_time(build_time)}\n")

        if results:
            print("📊 Final Comparison:\n")
            print("Size (including all dependencies):")
            for name, data in sorted(results.items(), key=lambda x: x[1]['size']):
                print(f"• {name.ljust(12)} → {data['size']} MB")
            
            print("\nBuild time:")
            for name, data in sorted(results.items(), key=lambda x: x[1]['time']):
                print(f"• {name.ljust(12)} → {format_time(data['time'])}")
        else:
            print("❌ No images were successfully built and measured")

    finally:
        # Uncomment the next line if you want to automatically cleanup images
        # cleanup_images()
        print("\nDone ✅")

if __name__ == "__main__":
    main()

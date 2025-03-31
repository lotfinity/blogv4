import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.conf import settings
from website.models import InstagramPostSnippet  # Adjust if needed

INSTAGRAM_POSTS_DIR = "/home/lotfikan/blogv3/dentidelil"

class Command(BaseCommand):
    help = "Import Instagram posts as snippets."

    def handle(self, *args, **options):
        files = sorted(
            os.listdir(INSTAGRAM_POSTS_DIR),
            key=lambda f: os.path.getmtime(os.path.join(INSTAGRAM_POSTS_DIR, f)),
            reverse=True
        )
        
        imported_count = 0

        for file in files:
            if file.endswith(".txt"):  # Find a caption file
                base_name = file.replace(".txt", "")
                caption_path = os.path.join(INSTAGRAM_POSTS_DIR, file)
                image_path = os.path.join(INSTAGRAM_POSTS_DIR, base_name + ".jpg")
                video_path = os.path.join(INSTAGRAM_POSTS_DIR, base_name + ".mp4")

                # Read the caption
                with open(caption_path, "r", encoding="utf-8") as f:
                    caption = f.read().strip()

                # Create the snippet
                post = InstagramPostSnippet.objects.create(
                    caption=caption,
                    timestamp=now()
                )

                # Save the image if it exists
                if os.path.exists(image_path):
                    with open(image_path, "rb") as img_file:
                        post.image.save(os.path.basename(image_path), File(img_file))

                # Save the video if it exists
                if os.path.exists(video_path):
                    with open(video_path, "rb") as vid_file:
                        post.video.save(os.path.basename(video_path), File(vid_file))

                post.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully imported: {base_name}"))
                
                imported_count += 1

        if imported_count == 0:
            self.stdout.write(self.style.WARNING("No new Instagram posts were imported."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Total imported: {imported_count}"))
